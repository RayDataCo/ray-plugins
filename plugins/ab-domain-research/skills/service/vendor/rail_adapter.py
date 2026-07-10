#!/usr/bin/env python3
"""rail_adapter — the canonical rail-port implementation for the Agent Brigade house.

Implements the rail interface (RAIL-SPEC.md) + Gate A ticket validity
(TICKET-CONTRACT.md's `ticketLint`, 8 deterministic rules) against the v1
filesystem/vault backend (CELLAR-SPEC.md): a ticket is one markdown file
with YAML frontmatter over four fixed body sections (`## Order` / `##
Resolved-context snapshot` / `## Work log` / `## Artifacts`).

STDLIB ONLY, by design — this file is VENDORED (copied, never imported as
a shared package) into every brigade the factory builds, stamped via
`stamp()` with a version + content hash (same move as
`skills/mise/mise.py`). It must run on a bare `python3` with nothing
installed, which is also why frontmatter is read/written by regex +
string surgery rather than a real YAML parser: only the flat scalar
fields this module needs (`ticket`/`artifact`/`status`/`lease`/`subject`)
are read or rewritten; every other line, including fields this module
doesn't know about, is left byte-for-byte untouched. `context:` (a nested
list) is READ-ONLY via `parse_context_entries()`; `lease` is written as
single-line JSON (a legal YAML flow mapping); long/folded YAML scalars
(quoted `when:` values PyYAML wraps across lines) are read for their
FIRST LINE ONLY — enough for every Gate-A check here, not a full
reconstruction. See ADAPTER-SPEC.md for the full honesty write-up.

Replaces 3+ hand-rolled copies of this shape across the house brigades
(Company Research's `brigade/rail_walk.py`, Sales-Collateral's port of the
same, Assessment's `pass_driver.py` + rail helpers, and this factory's own
JS `rail-walk.run.js` walk's inline `rail` object) — see
BRIGADE-INTERFACE.md "Adapter distribution — vendored from canon" and
IMPLEMENTATION-NOTES-2026-07-03-rail-adapter-canon.md for which reference
won which disputed behavior, including the two drift-bug fixes: the
context-entry scanner now accepts BOTH the 2-space-indent shape
(`context:\\n  - id: ...`) and the 0-indent shape (`context:\\n- id: ...`,
legal YAML block-sequence-at-mapping-indent), and `artifact`/resolver-type
validity are caller-supplied parameters, never a hardcoded enum
(TICKET-CONTRACT's SF-1 amendment).

Public API
----------
    list_tickets(rail_dir, status=None) -> list[Path]
    ticket_lint(text, rail_files, allowed_artifacts=None, resolver_types=None,
                cellar_root=None) -> LintResult
    enqueue(rail_dir, ticket_text, ticket_id, *, allowed_artifacts=None,
            resolver_types=None, cellar_root=None, now=None) -> Path
    pull(rail_dir, worker, ttl_min=DEFAULT_LEASE_TTL_MIN, *, now=None,
         allowed_artifacts=None, brigade=None) -> TicketHandle | None
    walker_scope_ok(text, allowed_artifacts, brigade) -> bool
    append(ticket_path, entry, *, now=None) -> None
    ack(ticket_path, exit, cellar_root, *, now=None) -> Path
    release(ticket_path, *, now=None) -> None
    find_unclosed(cellar_root, since_days=30) -> list[Path]
    stamp(path, *, version=None, stamped_at=None) -> Path
    ADAPTER_VERSION

Claim-by-atomic-rename (v1.2.0, 2026-07-08)
--------------------------------------------
`pull()` no longer leases in place. It CLAIMS the chosen ticket by
`os.rename()`-ing it into `<rail_dir>/.claimed/<worker>/<same filename>` —
POSIX rename(2) is indivisible, so the rename itself is the check-and-claim
in one step; the lease block is written to the file only AFTER this walker
is its sole owner. Two walkers racing for the same ticket can both attempt
the rename; at most one succeeds, the other's rename raises
`FileNotFoundError` (the source vanished under it — the other walker
already won), which `pull()` treats as ordinary contention and moves on to
the next candidate rather than raising. `ack()`/`release()` know how to
find a ticket in its claim dir and move it back (non-terminal exits, and
`release()`) or file it onward to the cellar (terminal exits) exactly as
before. `list_tickets()` now also surfaces claimed (in-flight) tickets —
the holding worker is the claim path's own `.claimed/<worker>/` segment.
See ADAPTER-SPEC.md's "Claim model" section for the full write-up,
including the local-filesystem-only honesty caveat (rename atomicity does
NOT hold across sync-drive-backed rails — Dropbox/iCloud/OneDrive-style
clients reconcile asynchronously against a cloud copy, so two clients can
each perform a locally-atomic rename against their own stale local view).

Frontmatter helpers (public, used throughout): get_field / set_field /
get_lease / parse_context_entries.

CLI: `python3 rail_adapter.py <op> [args]` — an internal script for
workflow agents / vendored programmatic use, NOT a distributed CLI
product with a stable flag surface. Prefer calling the Python functions
directly wherever the caller is already Python.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Optional

ADAPTER_VERSION = "1.2.0"

# Where `pull()` claims a ticket to: `<rail_dir>/.claimed/<worker>/<same filename>`.
# The rename IS the check-and-claim (POSIX rename(2) is indivisible) — see `pull()`'s
# own docstring and ADAPTER-SPEC.md's "Claim model" section for the full honesty
# write-up, including why this guarantee is LOCAL-FILESYSTEM-ONLY.
CLAIM_DIRNAME = ".claimed"
CANON_NAME = "ab-skill-factory/adapter/rail_adapter.py"

DEFAULT_LEASE_TTL_MIN = 60

# This brigade's own live artifact types (MENU.md) — the DEFAULT for
# ticket_lint()/enqueue() when a caller doesn't supply its own menu-derived
# set. Never the universal truth: per TICKET-CONTRACT.md's SF-1 amendment,
# `artifact` validates against the TARGET brigade's own menu, so every
# other brigade must pass its own `allowed_artifacts`.
DEFAULT_ALLOWED_ARTIFACTS = frozenset(
    {"skill", "brigade", "menu", "add-station", "iterate-skill"}
)

# Registered resolver/source types (BUNDLE-SPEC.md / TICKET-CONTRACT rule
# 4). Also a parameter, never hardcoded, for the same reason.
DEFAULT_RESOLVER_TYPES = frozenset({"file", "url", "mcp", "qmd", "cellar"})

# Types this module can deterministically resolve at Gate A rule 5 without
# a live network/MCP round-trip. `url`/`mcp`/`qmd` are steward-side (the
# steward verifies them live at enqueue time per TICKET-CONTRACT's own
# rule-5 note) — this module can't, and always passes them.
_LOCALLY_RESOLVABLE_TYPES = frozenset({"file", "cellar"})

# Rail status enum (TICKET-CONTRACT.md / RAIL-SPEC.md).
STATUS_ENUM = frozenset(
    {"queued", "leased", "in-build", "needs-context", "escalated", "done", "killed"}
)

# The five-exit disposition map (TICKET-CONTRACT's amended exit set,
# RAIL-SPEC's ack() row). `escalate` is a pause on a human's exit call,
# not one of the five exits proper, but ack() still parks it the same way.
STATUS_BY_EXIT: dict[str, str] = {
    "advance": "done",
    "kill": "killed",
    "reroute-to-steward": "needs-context",
    "escalate": "escalated",
}

# Only a TERMINAL disposition (done/killed) files the ticket off the rail
# to its subject. `needs-context` (steward rework) and `escalated` (human
# pause) stay on the rail (RAIL-SPEC + BRIGADE-INTERFACE, 2026-07-03).
FILES_TO_SUBJECT_STATUSES = frozenset({"done", "killed"})

# The four canonical H2 body sections, in required order.
SECTIONS: tuple[str, ...] = (
    "## Order",
    "## Resolved-context snapshot",
    "## Work log",
    "## Artifacts",
)

_TICKET_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_H2_RE = re.compile(r"(?m)^(## .+?)[ \t]*$")
_ENTRY_START_RE = re.compile(r"(?m)^[ \t]*-[ \t]+id:")


class GateAError(ValueError):
    """A Gate-A (ticketLint) failure. Carries the LintResult so callers can
    report the failing rule numbers — the steward-side enqueue check that
    refuses a Gate-A-failing ticket (RAIL-SPEC.md's enqueue row)."""

    def __init__(self, result: "LintResult"):
        self.result = result
        super().__init__(result.summary())


class RailError(RuntimeError):
    """Rail-mechanics errors: unknown exit, unresolvable filing subject,
    already-on-rail id collision, missing frontmatter block."""


# ---------------------------------------------------------------------------
# Frontmatter access — regex + string surgery, no YAML parser.
# ---------------------------------------------------------------------------


def _frontmatter_span(text: str) -> re.Match[str]:
    m = _FM_RE.match(text)
    if not m:
        raise RailError("no parseable '---\\n...\\n---\\n' frontmatter block found")
    return m


def get_field(text: str, key: str) -> Optional[str]:
    """Read a top-level (column-0) scalar frontmatter field's raw string
    value, or None. Anchored to column 0 so a same-named field nested
    inside `context:` (or any indented structure) never shadows it."""
    fm = _frontmatter_span(text).group(1)
    m = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*)$", fm)
    return m.group(1).strip() if m else None


def set_field(text: str, key: str, value: str) -> str:
    """Set/insert a top-level scalar frontmatter field in place; every
    other line is left byte-for-byte untouched. Caller is responsible for
    any quoting/encoding of `value` (e.g. `json.dumps` for lease)."""
    m = _frontmatter_span(text)
    fm = m.group(1)
    pattern = re.compile(rf"(?m)^{re.escape(key)}:[ \t]*.*$")
    new_fm = (
        pattern.sub(lambda _mm: f"{key}: {value}", fm, count=1)
        if pattern.search(fm)
        else fm + f"\n{key}: {value}"
    )
    return text[: m.start()] + f"---\n{new_fm}\n---\n" + text[m.end() :]


def get_lease(text: str) -> Optional[dict[str, Any]]:
    """Decode the `lease` field. This module always WRITES lease as
    single-line JSON, so `json.loads` reads it back; malformed/non-JSON
    values are treated as absent (Gate A rule 3 catches the shape
    mismatch itself for a status that requires a well-formed lease)."""
    raw = get_field(text, "lease")
    if raw is None:
        return None
    raw = raw.strip()
    if raw in ("", "null", "~", "None"):
        return None
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return decoded if isinstance(decoded, dict) else None


def _context_block(fm_text: str) -> str:
    """Extract the raw lines of the `context:` list, indentation-shape
    agnostic. Handles both real-world shapes on the house rail:

      shape A (2-space indent): context:\\n  - id: x\\n    type: file\\n...
      shape B (0-indent, legal YAML block-seq-at-mapping-indent):
                                 context:\\n- id: x\\n  type: cellar\\n...

    Scans forward from `context:` until a line that is neither blank, nor
    indented (an entry's continuation field), nor a 0-indent list dash —
    i.e. until the next top-level key. Drift fix (a): the JS reference
    only ever recognized shape A."""
    lines = fm_text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^context:\s*$", line):
            start = i
            break
    if start is None:
        return ""
    block_lines: list[str] = []
    for line in lines[start + 1 :]:
        if line.strip() == "" or line[:1] in (" ", "\t") or line.lstrip().startswith("-"):
            block_lines.append(line)
            continue
        break  # a genuine top-level key
    return "\n".join(block_lines)


def _entry_field(chunk: str, name: str) -> Optional[str]:
    """Read one field's value from a single context-entry chunk. Only the
    FIRST physical line of the value is captured (see module docstring's
    folded-scalar note) — sufficient for every Gate-A check here. Strips a
    leading/paired quote character."""
    m = re.search(rf"(?m)^[ \t]*-?[ \t]*{name}:[ \t]*(.*)$", chunk)
    if not m:
        return None
    val = m.group(1).strip()
    if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
        val = val[1:-1]
    elif val.startswith('"'):
        val = val[1:]
        if val.endswith("\\"):
            val = val[:-1]
    elif len(val) >= 2 and val[0] == "'" and val[-1] == "'":
        val = val[1:-1]
    return val


def parse_context_entries(text: str) -> list[dict[str, Any]]:
    """Parse `context:` into dicts with `id`/`type`/`ref`/`when`/
    `has_inline_content`. Entry boundaries are found by scanning for
    `- id:` lines regardless of leading whitespace — drift fix (a): the
    JS reference hardcoded a 2-space prefix and silently produced zero
    entries (hence zero eager sources checked) on the 0-indent shape.
    Read-only: this module never writes the context list back."""
    fm = _frontmatter_span(text).group(1)
    block = _context_block(fm)
    if not block.strip():
        return []
    starts = [m.start() for m in _ENTRY_START_RE.finditer(block)]
    entries: list[dict[str, Any]] = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(block)
        chunk = block[s:e]
        entries.append(
            {
                "id": _entry_field(chunk, "id"),
                "type": _entry_field(chunk, "type"),
                "ref": _entry_field(chunk, "ref"),
                "when": _entry_field(chunk, "when"),
                "has_inline_content": bool(re.search(r"(?m)^[ \t]*content:[ \t]*\S", chunk)),
            }
        )
    return entries


def _is_eager(entry: dict[str, Any]) -> bool:
    when = (entry.get("when") or "").strip().lstrip('"').lstrip("'")
    return when.lower().startswith("always")


def _ref_resolves(entry: dict[str, Any], cellar_root: Optional[str | Path]) -> bool:
    """Rule 5's local check: `file`/`cellar` are the only types verifiable
    without a live network/MCP call (`url`/`mcp`/`qmd` always pass here,
    steward-side per TICKET-CONTRACT). Handles `~` expansion, absolute
    paths, and `type: cellar` refs resolved relative to `cellar_root`."""
    t = entry.get("type")
    ref = entry.get("ref") or ""
    if t not in _LOCALLY_RESOLVABLE_TYPES:
        return True
    if not ref:
        return False
    expanded = Path(ref).expanduser()
    if expanded.is_absolute():
        return expanded.exists()
    if t == "cellar":
        if not cellar_root:
            return True  # can't verify without a cellar root — documented limitation
        return (Path(cellar_root) / ref).exists()
    return expanded.exists()  # type == "file", bare relative — best-effort against cwd


# ---------------------------------------------------------------------------
# Gate A — ticketLint (deterministic, 8 rules; TICKET-CONTRACT.md)
# ---------------------------------------------------------------------------


@dataclass
class LintRule:
    n: int
    description: str
    passed: bool
    detail: str = ""


@dataclass
class LintResult:
    rules: list[LintRule] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.rules)

    @property
    def failed_ids(self) -> list[int]:
        return [r.n for r in self.rules if not r.passed]

    def summary(self) -> str:
        ok = sum(1 for r in self.rules if r.passed)
        base = f"Gate A: {ok}/{len(self.rules)} pass"
        return base if self.passed else f"{base} (failed rules: {self.failed_ids})"


def ticket_lint(
    text: str,
    rail_files: Iterable[str | Path],
    allowed_artifacts: Optional[Iterable[str]] = None,
    resolver_types: Optional[Iterable[str]] = None,
    *,
    cellar_root: Optional[str | Path] = None,
) -> LintResult:
    """The 8 deterministic Gate-A rules from TICKET-CONTRACT.md — pure
    pass/fail mechanics, no LLM judgment. Runs at enqueue (steward-side)
    and again at pull (expo-side); pass-at-enqueue/fail-at-pull means an
    adapter mutated the ticket in transit, itself a caught defect.

    `allowed_artifacts` / `resolver_types` are PARAMETERS, never hardcoded
    enums (SF-1 amendment) — default to THIS brigade's own live menu;
    every other brigade must pass its own."""
    artifacts_ok = set(allowed_artifacts) if allowed_artifacts is not None else set(DEFAULT_ALLOWED_ARTIFACTS)
    types_ok = set(resolver_types) if resolver_types is not None else set(DEFAULT_RESOLVER_TYPES)
    rail_file_names = [Path(f).name for f in rail_files]

    try:
        _frontmatter_span(text)
    except RailError as exc:
        detail = str(exc)
        descs = [
            "ticket id present, kebab-case, unique on rail",
            "artifact is a type the target menu offers",
            "status in enum; lease shape matches status",
            "≥1 context source, all well-formed, registered types",
            "eager sources resolve",
            "## Order present and non-empty",
            "four canonical H2 sections, in order",
            "pointers only — no inline content in context",
            "subject is a cellar-contained relative path (no traversal)",
        ]
        return LintResult([LintRule(i + 1, d, False, detail) for i, d in enumerate(descs)])

    rules: list[LintRule] = []

    # Rule 1 — id present, kebab-case, unique on rail.
    ticket_id = get_field(text, "ticket")
    id_shape_ok = bool(ticket_id) and _TICKET_ID_RE.match(ticket_id or "") is not None
    dup_count = sum(1 for f in rail_file_names if f.startswith(f"{ticket_id}.")) if ticket_id else 0
    rules.append(LintRule(1, "ticket id present, kebab-case, unique on rail", id_shape_ok and dup_count <= 1, f"id={ticket_id!r} dup_count={dup_count}"))

    # Rule 2 — artifact ∈ target menu's offered types (menu is universal).
    artifact = get_field(text, "artifact")
    rules.append(LintRule(2, "artifact is a type the target menu offers", artifact in artifacts_ok, f"artifact={artifact!r} allowed={sorted(artifacts_ok)}"))

    # Rule 3 — status ∈ enum; lease null unless leased/in-build, well-formed when set.
    status = get_field(text, "status")
    lease = get_lease(text)
    status_ok = status in STATUS_ENUM
    if status in ("leased", "in-build"):
        lease_ok = isinstance(lease, dict) and all(lease.get(k) not in (None, "") for k in ("worker", "at", "ttl_min"))
    else:
        lease_ok = lease is None
    rules.append(LintRule(3, "status in enum; lease shape matches status", status_ok and lease_ok, f"status={status!r} lease={lease!r}"))

    # Rule 4 — ≥1 context source, all well-formed, registered resolver types.
    entries = parse_context_entries(text)
    well_formed = len(entries) >= 1 and all(
        e.get("id") and e.get("type") and e.get("ref") and e.get("when") and e.get("type") in types_ok for e in entries
    )
    rules.append(LintRule(4, "≥1 context source, all well-formed, registered types", well_formed, f"sources={len(entries)}"))

    # Rule 5 — eager sources resolve (file/cellar checked locally; url/mcp/qmd steward-side).
    eager = [e for e in entries if _is_eager(e)]
    eager_ok = all(_ref_resolves(e, cellar_root) for e in eager)
    rules.append(LintRule(5, "eager sources resolve (file/cellar checked here; url/mcp/qmd are steward-side)", eager_ok, f"eager={len(eager)}"))

    # Rule 6 — ## Order present and non-empty.
    order_m = re.search(r"(?m)^## Order[ \t]*$\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    rules.append(LintRule(6, "## Order present and non-empty", bool(order_m) and order_m.group(1).strip() != ""))

    # Rule 7 — the four canonical H2 sections present, in order.
    positions: list[int] = []
    cursor = -1
    order_correct = True
    for heading in SECTIONS:
        m = re.search(rf"(?m)^{re.escape(heading)}[ \t]*$", text)
        pos = m.start() if m else -1
        if pos == -1 or pos <= cursor:
            order_correct = False
        cursor = pos
        positions.append(pos)
    rules.append(LintRule(7, "four canonical H2 sections, in order", order_correct, f"positions={positions}"))

    # Rule 8 — pointers only, no inline content copies in context.
    rules.append(LintRule(8, "pointers only — no inline content in context", all(not e.get("has_inline_content") for e in entries)))

    # Rule 9 — the resolved subject is cellar-contained (path-traversal guard).
    # `ack()` files a terminal ticket to `<cellar>/<subject>/tickets/`; an
    # unvalidated subject (`../…`, absolute, drive-letter) turns a routine ack
    # into an arbitrary file write OUTSIDE the cellar. Validated here so a
    # malicious ticket never enqueues, and again at the ack write site as
    # defense in depth. Subject may be absent (derived later or unfileable) —
    # that is not a Gate-A failure; only a PRESENT-and-unsafe subject fails.
    resolved_subject = _resolve_subject(text)
    subject_ok = resolved_subject is None or _subject_is_safe(resolved_subject)
    rules.append(LintRule(9, "subject is a cellar-contained relative path (no traversal)", subject_ok, f"subject={resolved_subject!r}"))

    return LintResult(rules)


# ---------------------------------------------------------------------------
# Timestamps + lease expiry
# ---------------------------------------------------------------------------


def _now_iso(now: Optional[str] = None) -> str:
    return now if now is not None else datetime.now().astimezone().isoformat(timespec="seconds")


def _lease_expired(lease: Optional[dict[str, Any]], now_val: str) -> bool:
    if not lease:
        return False
    at, ttl_min = lease.get("at"), lease.get("ttl_min")
    if not at or ttl_min is None:
        return False
    try:
        leased_at = datetime.fromisoformat(str(at))
        now_dt = datetime.fromisoformat(str(now_val))
        return now_dt > leased_at + timedelta(minutes=float(ttl_min))
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------------------
# Work-log append — the append-only primitive every other op rides on.
# ---------------------------------------------------------------------------


def _append_to_section(text: str, heading: str, new_line: str) -> str:
    """Append `new_line` as the last line of the named H2 section, never
    rewriting an existing line. Normalizes to exactly one blank line
    between the section's last bullet and the next heading regardless of
    how many times this is called — ported from the Company Research /
    Sales-Collateral brigades' `_append_to_section` (the winning behavior
    over the JS reference's insert-before-`## Artifacts`, which
    accumulates an extra blank line per append — see IMPLEMENTATION-NOTES)."""
    headings = [(m.start(), m.end(), m.group(1)) for m in _H2_RE.finditer(text)]
    start = end = None
    for i, (h_start, h_end, name) in enumerate(headings):
        if name == heading:
            start = h_end + 1 if text[h_end : h_end + 1] == "\n" else h_end
            end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
            break
    if start is None:
        # Unreachable if Gate A rule 7 passed; append defensively at EOF
        # rather than silently dropping the entry.
        sep = "" if text.endswith("\n") else "\n"
        return text + sep + f"\n{heading}\n\n{new_line}\n"

    section_stripped = text[start:end].rstrip("\n")
    rebuilt = (section_stripped + ("\n" if section_stripped else "")) + new_line + "\n\n"
    return text[:start] + rebuilt + text[end:]


def append(ticket_path: str | Path, entry: str, *, now: Optional[str] = None) -> None:
    """Append one timestamped work-log line (`- <ts> · <entry>`) as the
    last line of `## Work log` — immediately before `## Artifacts` in the
    canonical order. Append-only: every existing line is untouched."""
    path = Path(ticket_path)
    text = path.read_text(encoding="utf-8")
    line = f"- {_now_iso(now)} · {entry}"
    path.write_text(_append_to_section(text, "## Work log", line), encoding="utf-8")


# ---------------------------------------------------------------------------
# list_tickets
# ---------------------------------------------------------------------------


def _claimed_ticket_paths(rail_dir: Path) -> list[Path]:
    """Every ticket currently claimed (in-flight under some walker's
    `.claimed/<worker>/`), across ALL workers. The holding worker is
    recoverable from the path itself — the directory segment immediately
    under `.claimed/` — or from the ticket's own `lease.worker` field."""
    claimed_root = rail_dir / CLAIM_DIRNAME
    if not claimed_root.exists():
        return []
    return list(claimed_root.glob("*/*.ticket.md"))


def list_tickets(rail_dir: str | Path, status: Optional[str] = None) -> list[Path]:
    """Enumerate `*.ticket.md` on the rail — both unclaimed (rail-dir-root)
    and claimed (in-flight, `.claimed/<worker>/…`) tickets — optionally
    filtered to one frontmatter `status`. Filed (closed) tickets have moved
    off `rail_dir` entirely per RAIL-SPEC/CELLAR-SPEC and are never
    returned here.

    A claimed ticket's holder is NOT a separate return field — it's the
    `.claimed/<worker>/` segment of the path itself (or the ticket's own
    `lease.worker`), preserving the `list[Path]` return shape every
    existing caller already depends on."""
    rail_dir = Path(rail_dir)
    if not rail_dir.exists():
        return []
    paths = sorted(rail_dir.glob("*.ticket.md")) + sorted(_claimed_ticket_paths(rail_dir))
    if status is None:
        return paths
    return [p for p in paths if get_field(p.read_text(encoding="utf-8"), "status") == status]


# ---------------------------------------------------------------------------
# enqueue
# ---------------------------------------------------------------------------


def enqueue(
    rail_dir: str | Path,
    ticket_text: str,
    ticket_id: str,
    *,
    allowed_artifacts: Optional[Iterable[str]] = None,
    resolver_types: Optional[Iterable[str]] = None,
    cellar_root: Optional[str | Path] = None,
    now: Optional[str] = None,
) -> Path:
    """The steward-side enqueue check: run Gate A first, refuse (raise
    `GateAError`) on failure — a Gate-A-failing ticket never touches the
    rail. On success, write the file and append the opening
    `steward: enqueued — Gate A: N/N pass` work-log line."""
    rail_dir = Path(rail_dir)
    rail_dir.mkdir(parents=True, exist_ok=True)

    fm_ticket_id = get_field(ticket_text, "ticket") if _FM_RE.match(ticket_text) else None
    if fm_ticket_id is not None and fm_ticket_id != ticket_id:
        raise RailError(f"enqueue: ticket_id argument {ticket_id!r} != frontmatter `ticket:` {fm_ticket_id!r}")

    # Duplicate-id detection covers claimed (in-flight) tickets too — a
    # ticket mid-flight under `.claimed/<worker>/` is off rail-dir-root's
    # own glob, but it's still "already has a file on the rail" for the
    # purposes of Gate A rule 1 and the explicit collision guard below.
    existing_files = [p.name for p in rail_dir.glob("*.ticket.md")]
    existing_files += [p.name for p in _claimed_ticket_paths(rail_dir)]
    result = ticket_lint(ticket_text, existing_files, allowed_artifacts=allowed_artifacts, resolver_types=resolver_types, cellar_root=cellar_root)
    if not result.passed:
        raise GateAError(result)

    path = rail_dir / f"{ticket_id}.ticket.md"
    if path.exists() or any(p.name == path.name for p in _claimed_ticket_paths(rail_dir)):
        raise RailError(f"enqueue: {ticket_id!r} already has a file on the rail at {path}")

    path.write_text(ticket_text if ticket_text.endswith("\n") else ticket_text + "\n", encoding="utf-8")
    append(path, f"steward: enqueued — {result.summary()}", now=now)
    return path


# ---------------------------------------------------------------------------
# pull — advisory lease
# ---------------------------------------------------------------------------


@dataclass
class TicketHandle:
    id: str
    path: Path
    text: str

    @property
    def status(self) -> Optional[str]:
        return get_field(self.text, "status")


def walker_scope_ok(
    text: str,
    allowed_artifacts: Optional[Iterable[str]],
    brigade: Optional[str],
) -> bool:
    """Walker-scope filter for `pull()` (shared-rail finding, 2026-07-06,
    demonstrated live: the sales-collateral walker's oldest-mtime scan
    leased a website-fix ticket and its own Gate A then parked ANOTHER
    brigade's perfectly valid ticket as needs-context). A ticket outside
    the calling walker's scope is SKIPPED — never touched, never judged.

    Two independent, both-optional scopes:
      - `allowed_artifacts`: the walker's own live artifact types (its
        menu's live set, same source Gate A uses). A ticket whose
        `artifact:` is not in the set belongs to some other brigade's
        walker.
      - `brigade`: this walker's brigade name. `artifact: menu` is
        universally valid (every brigade answers discovery), so the
        artifact set alone cannot scope a menu ticket — its `subject:`
        (`brigades/<name>`, per MENU-SPEC) names the one brigade that
        should answer it. With `brigade` given, a menu ticket for anyone
        else is skipped too.

    Both None (the default) preserves the historical scan-everything
    behavior for single-brigade rails and existing callers/tests."""
    if allowed_artifacts is None and brigade is None:
        return True
    artifact = (get_field(text, "artifact") or "").strip()
    if allowed_artifacts is not None and artifact not in set(allowed_artifacts):
        return False
    if brigade is not None and artifact == "menu":
        subject = (get_field(text, "subject") or "").strip().strip('"').strip("'")
        if subject and subject != f"brigades/{brigade}":
            return False
    return True


def pull(
    rail_dir: str | Path,
    worker: str,
    ttl_min: int = DEFAULT_LEASE_TTL_MIN,
    *,
    now: Optional[str] = None,
    allowed_artifacts: Optional[Iterable[str]] = None,
    brigade: Optional[str] = None,
) -> Optional[TicketHandle]:
    """Lease the next workable ticket: the oldest-mtime `queued` ticket
    (rail-dir root), or — failing that — the oldest-mtime `leased`/
    `in-build` ticket whose lease has expired, wherever it currently sits
    (rail-dir root, or a stale `.claimed/<worker>/` from an abandoned
    walker) — appends `lease-reclaimed` so the abandonment is visible, per
    RAIL-SPEC's lease-semantics section. Returns None if the rail is dry.
    `needs-context`/`escalated` are never returned.

    `allowed_artifacts`/`brigade` scope the scan to the calling walker's
    own tickets on a SHARED rail — see `walker_scope_ok()`. Every brigade
    walker on a multi-brigade rail should pass them; omitting both keeps
    the historical scan-everything behavior.

    CLAIM-BY-ATOMIC-RENAME (v1.2.0, 2026-07-08 — replaces the prior
    check-then-write advisory lease): the chosen ticket is claimed by
    `os.rename()`-ing it into `<rail_dir>/.claimed/<worker>/<same
    filename>` BEFORE anything is written to it. POSIX rename(2) is
    indivisible — the rename itself is the check-and-claim, atomically, in
    one step. If another walker's rename already moved the same source
    file out from under this one, `os.rename()` raises
    `FileNotFoundError`; that is treated as ordinary contention (someone
    else won this ticket), not an error — this walker moves on to the next
    candidate rather than raising. Only after a successful rename — at
    which point this walker is the file's sole owner — is the lease block
    written. LOCAL FILESYSTEMS ONLY: this guarantee does not extend to
    sync-drive-backed rails (Dropbox/iCloud/OneDrive/etc.), whose clients
    reconcile asynchronously against a remote copy — a "local" rename can
    be atomic on-disk and still race another client's equally "atomic"
    rename against its own stale local view. See ADAPTER-SPEC.md's "Claim
    model" section."""
    rail_dir = Path(rail_dir)
    if not rail_dir.exists():
        return None
    now_val = _now_iso(now)

    root_candidates = list(rail_dir.glob("*.ticket.md"))
    claimed_candidates = _claimed_ticket_paths(rail_dir)
    candidates = sorted(root_candidates + claimed_candidates, key=lambda p: p.stat().st_mtime)

    claim_dir = rail_dir / CLAIM_DIRNAME / worker
    claim_dir.mkdir(parents=True, exist_ok=True)

    for p in candidates:
        try:
            text = p.read_text(encoding="utf-8")
        except FileNotFoundError:
            continue  # vanished between the glob snapshot and the read — already lost
        if not walker_scope_ok(text, allowed_artifacts, brigade):
            continue
        status = get_field(text, "status")
        if status == "queued":
            reclaim = False
        elif status in ("leased", "in-build") and _lease_expired(get_lease(text), now_val):
            reclaim = True
        else:
            continue

        dest = claim_dir / p.name
        try:
            os.rename(p, dest)
        except FileNotFoundError:
            # Lost the race: another walker's rename already claimed this
            # exact ticket between our read above and this rename call.
            # Contention, not a defect — try the next candidate.
            continue

        text = dest.read_text(encoding="utf-8")
        text = set_field(text, "status", "leased")
        text = set_field(text, "lease", json.dumps({"worker": worker, "at": now_val, "ttl_min": ttl_min}))
        dest.write_text(text, encoding="utf-8")

        if reclaim:
            append(dest, f"rail: lease-reclaimed — prior lease expired, worker={worker}", now=now_val)
        append(dest, f"rail: lease — worker={worker}, ttl_min={ttl_min}", now=now_val)

        final_text = dest.read_text(encoding="utf-8")
        return TicketHandle(id=get_field(final_text, "ticket") or dest.stem.removesuffix(".ticket"), path=dest, text=final_text)

    return None


# ---------------------------------------------------------------------------
# claim-path helpers — shared by release()/ack() to find the rail root from
# a ticket that may currently be sitting under `.claimed/<worker>/`.
# ---------------------------------------------------------------------------


def _is_claimed_path(path: Path) -> bool:
    """True when `path` is `<rail>/.claimed/<worker>/<file>` — i.e. its
    grandparent directory is the claim root."""
    return path.parent.parent.name == CLAIM_DIRNAME


def _rail_root_from_ticket_path(path: Path) -> Path:
    """The rail directory a ticket belongs at rest in, derived from its
    CURRENT path. For a claimed ticket (`<rail>/.claimed/<worker>/<file>`)
    that's three levels up. For a ticket already sitting at rail-dir root
    (never claimed — e.g. every ab-assessment ticket, whose own hand-rolled
    pull()/ack() never touch `.claimed/`), this is a no-op: `path.parent`
    IS already the rail root, so callers that unconditionally route
    through this helper stay byte-for-byte compatible with tickets that
    never entered the claim mechanism at all."""
    if _is_claimed_path(path):
        return path.parent.parent.parent
    return path.parent


def _return_to_rail_root(path: Path) -> Path:
    """Move a (possibly claimed) ticket back to its rail-dir root, if it
    isn't already there. Same-filesystem move (both `.claimed/<worker>/`
    and the rail root live under the same `rail_dir`), so `os.rename` is
    safe and atomic here — unlike the cellar-filing move in `ack()`, which
    deliberately stays copy+unlink because `cellar_root` can be a wholly
    different top-level directory/mount."""
    rail_root = _rail_root_from_ticket_path(path)
    if path.parent == rail_root:
        return path
    dest = rail_root / path.name
    os.rename(path, dest)
    return dest


# ---------------------------------------------------------------------------
# release
# ---------------------------------------------------------------------------


def release(ticket_path: str | Path, *, now: Optional[str] = None) -> None:
    """Give a leased ticket back untouched: status -> queued, lease
    cleared (worker died, budget hit, orderly shutdown). If the ticket is
    currently claimed (`.claimed/<worker>/…`), it's moved back to the
    rail-dir root as part of the same call — a released ticket is, by
    definition, no longer anyone's in-flight work."""
    path = Path(ticket_path)
    path = _return_to_rail_root(path)
    text = path.read_text(encoding="utf-8")
    text = set_field(text, "status", "queued")
    text = set_field(text, "lease", "null")
    path.write_text(text, encoding="utf-8")
    append(path, "rail: release — lease cleared, back to queued", now=now)


# ---------------------------------------------------------------------------
# ack — the five-exit disposition map + file-to-subject on terminal exits
# ---------------------------------------------------------------------------


def _subject_is_safe(subject: str) -> bool:
    """A subject is safe iff it is a NON-EMPTY relative POSIX path that stays
    inside the cellar: not absolute, no Windows drive/UNC, no `..` segment, no
    NUL. This is the structural (cellar-root-independent) half of the
    path-traversal guard for `ack()`'s `<cellar>/<subject>/tickets/` filing;
    `_dest_is_contained()` is the resolve-and-verify half at the write site."""
    if not subject or "\x00" in subject:
        return False
    s = subject.strip()
    if not s or s.startswith("/") or s.startswith("\\"):
        return False
    # Windows drive letter (C:) or UNC — reject on every platform for portability.
    if len(s) >= 2 and s[1] == ":":
        return False
    segments = re.split(r"[\\/]+", s)
    if any(seg == ".." for seg in segments):
        return False
    return True


def _dest_is_contained(dest: Path, cellar_root: Path) -> bool:
    """Defense-in-depth: the resolved filing destination must live under the
    resolved cellar root. Catches anything the structural check missed
    (symlinks in the cellar tree, unforeseen encodings)."""
    try:
        dest.resolve().relative_to(cellar_root.resolve())
        return True
    except (ValueError, OSError):
        return False


def _resolve_subject(text: str) -> Optional[str]:
    """Explicit `subject:` field first; else the first `cellar`-typed
    context source's ref, taken as its first TWO path segments
    (`<section>/<key>`, per CELLAR-SPEC's organization: `companies/<id>`,
    `assessments/<subject>`, `brigades/<name>`, ...) — generalizing the
    Company Research reference's `companies/<id>`-only fallback to every
    cellar section, per TICKET-CONTRACT's own subject-field prose."""
    explicit = get_field(text, "subject")
    if explicit:
        explicit = explicit.strip().strip('"').strip("'")
        if explicit:
            return explicit
    for entry in parse_context_entries(text):
        if entry.get("type") == "cellar" and entry.get("ref"):
            parts = [p for p in entry["ref"].split("/") if p]
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
    return None


def ack(
    ticket_path: str | Path,
    exit: str,
    cellar_root: str | Path,
    *,
    now: Optional[str] = None,
) -> Path:
    """Close out a lease with the expo's terminal disposition
    (TICKET-CONTRACT's five-exit set): `advance -> done`, `kill ->
    killed`, `reroute-to-steward -> needs-context`, escalate-pause ->
    `escalated`. Clears the lease and appends an ack line in every case.

    ONLY on a TERMINAL disposition (`done`/`killed`) does this also FILE
    the ticket to `<cellar_root>/<subject>/tickets/<id>.ticket.md` — the
    rail is clear of it from that instant (2026-07-03 scan-only close-out
    design: no pass-shelf pointer dropped here; `find_unclosed()` is the
    steward's discovery mechanism for delivering the outcome later).
    `needs-context`/`escalated` are pauses/rework, not terminal — the
    ticket stays ON THE RAIL, but a non-terminal ack always resolves it
    back to the rail-dir ROOT (v1.2.0): if `ticket_path` currently sits
    under `.claimed/<worker>/`, it's moved back out — a needs-context/
    escalated ticket is no longer anyone's in-flight claim, so it belongs
    wherever every other unclaimed rail ticket lives, workable again by
    the steward/a human, not orphaned inside a specific walker's claim
    dir. A ticket that was never claimed (already at rail-dir root) is
    left in place — `_return_to_rail_root` is a no-op for it.

    Returns the ticket's path after this call: the filed destination on a
    terminal exit, or its (possibly moved-back) rail-root path otherwise."""
    if exit not in STATUS_BY_EXIT:
        raise RailError(f"ack: unknown exit {exit!r}; expected one of {sorted(STATUS_BY_EXIT)}")

    path = Path(ticket_path)
    new_status = STATUS_BY_EXIT[exit]
    now_val = _now_iso(now)

    text = path.read_text(encoding="utf-8")
    text = set_field(text, "status", new_status)
    text = set_field(text, "lease", "null")
    path.write_text(text, encoding="utf-8")
    append(path, f"ack: {exit} → status {new_status}", now=now_val)

    if new_status not in FILES_TO_SUBJECT_STATUSES:
        return _return_to_rail_root(path)

    subject = _resolve_subject(path.read_text(encoding="utf-8"))
    if subject is None:
        raise RailError(f"ack: cannot file {path.name} — no `subject:` field and no `type: cellar` context source to derive one from")

    # Path-traversal guard (defense in depth; Gate A rule 9 catches this at
    # enqueue, but ack must never write outside the cellar even if a ticket
    # reached a terminal state some other way).
    if not _subject_is_safe(subject):
        raise RailError(f"ack: refusing to file {path.name} — unsafe subject {subject!r} (must be a cellar-contained relative path)")
    cellar_root = Path(cellar_root)
    dest_dir = cellar_root / subject / "tickets"
    if not _dest_is_contained(dest_dir, cellar_root):
        raise RailError(f"ack: refusing to file {path.name} — subject {subject!r} resolves outside the cellar")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    dest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.unlink()
    return dest


# ---------------------------------------------------------------------------
# find_unclosed — the steward's close-out sweep's discovery mechanism
# ---------------------------------------------------------------------------


# Matches both a bare signature line (`- close-out: ...`) and one written via
# this module's own append() (`- <timestamp> · close-out: ...`). The un-anchored
# form missed the latter — caught in the first live sweep, 2026-07-03 (v1.0.1).
_CLOSE_OUT_RE = re.compile(r"(?m)^[ \t]*-\s*(?:[^\n·]*·\s*)?close-out:")


def find_unclosed(cellar_root: str | Path, since_days: int = 30) -> list[Path]:
    """The steward's close-out scan (BRIGADE-INTERFACE's scan-only
    close-out contract, 2026-07-03): walk `<cellar_root>/*/…/tickets/*
    .ticket.md` filed within the last `since_days`, return those with a
    TERMINAL status (`done`/`killed`) whose work log has NO line starting
    `- close-out:`. Scan-only by founder decision — no pass-shelf pointer
    to maintain; this scan plus the ticket's own signature line is the
    entire idempotent discovery mechanism."""
    cellar_root = Path(cellar_root)
    if not cellar_root.exists():
        return []
    cutoff = time.time() - since_days * 86400
    results: list[Path] = []
    for p in cellar_root.rglob("tickets/*.ticket.md"):
        try:
            mtime = p.stat().st_mtime
        except OSError:
            continue
        if mtime < cutoff:
            continue
        text = p.read_text(encoding="utf-8")
        if get_field(text, "status") not in FILES_TO_SUBJECT_STATUSES:
            continue
        if _CLOSE_OUT_RE.search(text):
            continue
        results.append(p)
    return sorted(results)


# ---------------------------------------------------------------------------
# stamp — vendoring provenance (BRIGADE-INTERFACE.md "Adapter distribution")
# ---------------------------------------------------------------------------


def stamp(path: str | Path, *, version: Optional[str] = None, stamped_at: Optional[str] = None) -> Path:
    """Write `<path>.stamp.json` recording this file's canon identity,
    version, and content hash — what `mise`'s `vendor_stamp` check type
    compares a vendored copy against to detect drift. `stamped_at` is
    accepted from the caller rather than derived internally wherever
    practical, so a vendoring build's own timestamp is the single source
    of truth (this is a build-time tool, so an internal default is fine
    when the caller doesn't have one)."""
    p = Path(path)
    data = {
        "file": p.name,
        "canon": CANON_NAME,
        "version": version or ADAPTER_VERSION,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "stamped_at": stamped_at or _now_iso(),
    }
    stamp_path = p.with_name(p.name + ".stamp.json")
    stamp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return stamp_path


# ---------------------------------------------------------------------------
# CLI — internal script, not a distributed product (see module docstring)
# ---------------------------------------------------------------------------


def _cli(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rail_adapter.py",
        description="Internal rail-port script for workflow agents / vendored brigades — not a stable distributed CLI.",
    )
    sub = parser.add_subparsers(dest="op", required=True)

    p_list = sub.add_parser("list", help="list *.ticket.md on the rail")
    p_list.add_argument("rail_dir")
    p_list.add_argument("--status", default=None)

    p_lint = sub.add_parser("lint", help="run Gate A against a ticket file")
    p_lint.add_argument("ticket_path")
    p_lint.add_argument("--rail-dir", default=None)
    p_lint.add_argument("--cellar-root", default=None)

    p_enqueue = sub.add_parser("enqueue", help="Gate A + place a ticket file onto the rail")
    p_enqueue.add_argument("rail_dir")
    p_enqueue.add_argument("ticket_file")
    p_enqueue.add_argument("ticket_id")
    p_enqueue.add_argument("--cellar-root", default=None)

    p_pull = sub.add_parser("pull", help="lease the next workable ticket")
    p_pull.add_argument("rail_dir")
    p_pull.add_argument("--worker", default="rail-adapter-cli")
    p_pull.add_argument("--ttl-min", type=int, default=DEFAULT_LEASE_TTL_MIN)
    p_pull.add_argument(
        "--allowed-artifact", action="append", default=None, dest="allowed_artifacts",
        help="walker scope: repeatable; skip tickets whose artifact: is not among these "
             "(a brigade walker on a shared rail passes its own live types + menu)",
    )
    p_pull.add_argument(
        "--brigade", default=None,
        help="walker scope: with artifact: menu being universal, only lease menu tickets "
             "whose subject is brigades/<this name>",
    )

    p_append = sub.add_parser("append", help="append one work-log entry")
    p_append.add_argument("ticket_path")
    p_append.add_argument("entry")

    p_ack = sub.add_parser("ack", help="close out a lease with a terminal disposition")
    p_ack.add_argument("ticket_path")
    p_ack.add_argument("exit", choices=sorted(STATUS_BY_EXIT))
    p_ack.add_argument("cellar_root")

    p_release = sub.add_parser("release", help="release a leased ticket back to queued")
    p_release.add_argument("ticket_path")

    p_find = sub.add_parser("find-unclosed", help="the steward's close-out scan")
    p_find.add_argument("cellar_root")
    p_find.add_argument("--since-days", type=int, default=30)

    p_stamp = sub.add_parser("stamp", help="write a vendoring provenance stamp")
    p_stamp.add_argument("path")

    args = parser.parse_args(argv)

    try:
        if args.op == "list":
            for p in list_tickets(args.rail_dir, status=args.status):
                print(p)
        elif args.op == "lint":
            text = Path(args.ticket_path).read_text(encoding="utf-8")
            rail_files = [f.name for f in Path(args.rail_dir).glob("*.ticket.md")] if args.rail_dir else []
            result = ticket_lint(text, rail_files, cellar_root=args.cellar_root)
            for r in result.rules:
                print(f"rule {r.n}: {'PASS' if r.passed else 'FAIL'} — {r.description} ({r.detail})")
            print(result.summary())
            return 0 if result.passed else 1
        elif args.op == "enqueue":
            ticket_text = Path(args.ticket_file).read_text(encoding="utf-8")
            try:
                path = enqueue(args.rail_dir, ticket_text, args.ticket_id, cellar_root=args.cellar_root)
            except GateAError as exc:
                for r in exc.result.rules:
                    if not r.passed:
                        print(f"  rule {r.n}: {r.description} ({r.detail})", file=sys.stderr)
                print(exc.result.summary(), file=sys.stderr)
                return 1
            print(f"enqueued {args.ticket_id} -> {path}")
        elif args.op == "pull":
            handle = pull(
                args.rail_dir, args.worker, args.ttl_min,
                allowed_artifacts=args.allowed_artifacts, brigade=args.brigade,
            )
            print("rail is dry" if handle is None else f"pulled {handle.id} ({handle.path})")
        elif args.op == "append":
            append(args.ticket_path, args.entry)
        elif args.op == "ack":
            print(f"acked -> {ack(args.ticket_path, args.exit, args.cellar_root)}")
        elif args.op == "release":
            release(args.ticket_path)
        elif args.op == "find-unclosed":
            for p in find_unclosed(args.cellar_root, since_days=args.since_days):
                print(p)
        elif args.op == "stamp":
            print(f"stamped -> {stamp(args.path)}")
    except (RailError, GateAError) as exc:
        print(f"rail_adapter: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
