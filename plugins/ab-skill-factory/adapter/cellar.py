"""cellar — the canonical filesystem cellar adapter for the Agent Brigade house.

Implements the CELLAR-SPEC port (this plugin's `CELLAR-SPEC.md`) against the
local filesystem as the v1 backend. Every brigade output that should become
durable house knowledge lands here with provenance; nothing in this module
talks to the rail or the ticket contract — those are separate ports
(`rail_adapter.py`, this file's sibling canon).

**VENDORED FROM CANON** (canonized 2026-07-06, closing the shared-lib debt the
three hand-maintained copies had flagged since 2026-07-02): this file's home is
`ab-skill-factory/adapter/cellar.py`; each Python brigade carries a verbatim,
stamped copy at `brigade/cellar.py` (vendored IN PLACE — the import path
`brigade.cellar` predates canonization and is not worth churning; the stamp
sidecar `cellar.py.stamp.json` + each brigade's mise `vendor_stamp` check are
what enforce byte-identity, exactly as for `brigade/vendor/rail_adapter.py`).
Never hand-edit a vendored copy — fix canon, re-vendor verbatim, re-stamp.
Unlike `rail_adapter.py` this module is NOT stdlib-only: it needs PyYAML
(every brigade's mise already declares `python-module-yaml`).

The reconciliation union (2026-07-06): the three copies had drifted by
docstrings plus three real deltas, all kept —
  - the strict subject-slug lint (Company Research + Assessment) — the last
    path segment of `subject` must be lowercase alnum+hyphens;
  - `list()` + dotted-path filtering (Sales Collateral's §4.2 disk-truth
    sweep primitive);
  - `canonical_json()` (Assessment's invariant-equality serialization).

Interface:
    land(content, meta, ref=None) -> str        # write, return cellar ref
    upsert(ref, content, meta) -> str            # living-index escape hatch
    resolve(ref) -> str                          # read back the raw content
    list_refs(prefix=None, kind=None) -> list[str]
    list(filter=None) -> list[{ref, meta}]       # dotted-path predicate map
    cellar_lint(meta) -> None                    # raises CellarLintError
    split_frontmatter(text) / now_iso() / canonical_json(value)

Design notes (documented per CELLAR-SPEC's "v1 honesty" convention):
  - Append-only: `land()` refuses to overwrite an existing ref. Date-stamped
    filenames make collisions rare in practice; an exact-ref collision is a
    lint failure, not a silent overwrite.
  - One deliberate exception: *living index* artifacts (CELLAR-SPEC's fixed,
    non-dated paths, e.g. `companies/<id>/identity.md`) use `upsert()`, a
    narrow, explicitly-named escape hatch from append-only. Brigades without
    a living-index artifact type simply never call it.
  - Markdown artifacts (`.md`) carry YAML frontmatter inline, per the
    CELLAR-SPEC example. Non-markdown artifacts (raw `.json` dumps, `.docx`
    deliverables) can't hold YAML frontmatter without corrupting the payload,
    so their meta lands beside them in a `<ref>.meta.json` sidecar. Both
    paths go through the same `cellar_lint()` gate.
  - No `search()` in v1 — search rides qmd/grep externally over the cellar
    root. `list_refs()` covers enumeration by meta (subject/kind prefix);
    `list()` covers meta-predicate sweeps.
  - No locking or atomic land, same as the spec's own filesystem-backend
    honesty note — single-writer-by-convention in v1.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

CELLAR_ADAPTER_VERSION = "1.0.0"
CANON_NAME = "ab-skill-factory/adapter/cellar.py"

REQUIRED_META_KEYS = ("landed", "kind", "subject", "produced_by", "provenance")
REQUIRED_PRODUCED_BY_KEYS = ("brigade", "ticket", "station")


class CellarRootError(RuntimeError):
    """The cellar location is not declared — refuse to guess."""


class CellarLintError(ValueError):
    """A landed artifact's meta failed cellarLint — it bounces to the producer."""


class CellarConflictError(FileExistsError):
    """An attempted land() collided with an existing ref (append-only violation)."""


@dataclass
class CellarClient:
    """Filesystem-backed cellar adapter. One instance per cellar root."""

    root: Path

    def __init__(self, root: Optional[str | Path] = None):
        # Resolution: explicit arg -> $CELLAR_ROOT -> fail loudly. The old
        # default was one machine's absolute path with a silent mkdir — an
        # unset env var produced writes to a path nobody chose. Creating the
        # tree is still fine once the path is explicitly declared.
        resolved = root if root is not None else os.environ.get("CELLAR_ROOT")
        if not resolved:
            raise CellarRootError(
                "CELLAR_ROOT is not set — the house cellar is an explicit, declared "
                "location (see [roots].cellar in the workspace's mise.toml; keep the "
                "env var and the declaration in agreement, e.g. via the workspace "
                ".claude/settings.json env block)."
            )
        self.root = Path(resolved).expanduser()
        self.root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # cellarLint
    # ------------------------------------------------------------------

    def cellar_lint(self, meta: dict[str, Any]) -> None:
        """Deterministic pass/fail check on landing meta. Raises CellarLintError.

        Mirrors ticketLint()/skillLint() — pure mechanics, no LLM judgment.
        """
        missing = [k for k in REQUIRED_META_KEYS if k not in meta or meta[k] in (None, "")]
        if missing:
            raise CellarLintError(f"cellar_lint: missing required meta keys: {missing}")

        produced_by = meta.get("produced_by")
        if not isinstance(produced_by, dict):
            raise CellarLintError("cellar_lint: produced_by must be a dict")
        missing_pb = [k for k in REQUIRED_PRODUCED_BY_KEYS if not produced_by.get(k)]
        if missing_pb:
            raise CellarLintError(f"cellar_lint: produced_by missing keys: {missing_pb}")

        subject = meta["subject"]
        if not isinstance(subject, str) or "/" not in subject:
            raise CellarLintError(
                f"cellar_lint: subject {subject!r} does not look like a canonical key "
                "(expected '<namespace>/<slug>[/...]', e.g. 'companies/acme' or 'assessments/acme')"
            )
        slug = subject.split("/")[-1]
        if not slug or not all(c.isalnum() or c == "-" for c in slug):
            raise CellarLintError(
                f"cellar_lint: subject slug {slug!r} must be lowercase alnum+hyphens"
            )
        if slug != slug.lower():
            raise CellarLintError(f"cellar_lint: subject slug {slug!r} must be lowercase")

        try:
            datetime.fromisoformat(str(meta["landed"]).replace("Z", "+00:00"))
        except ValueError as e:
            raise CellarLintError(f"cellar_lint: landed is not a valid ISO timestamp: {e}") from e

        supersedes = meta.get("supersedes")
        if supersedes:
            if not self._path_for_ref(supersedes).exists():
                raise CellarLintError(
                    f"cellar_lint: supersedes ref {supersedes!r} does not resolve"
                )

    # ------------------------------------------------------------------
    # land / upsert / resolve / list_refs / list
    # ------------------------------------------------------------------

    def land(self, content: str | bytes, meta: dict[str, Any], ref: Optional[str] = None) -> str:
        """Write an artifact with required provenance meta. Append-only.

        Returns the cellar ref (a backend-relative path, stable across
        backend moves). Raises CellarLintError if meta fails cellar_lint,
        or CellarConflictError if `ref` already exists.
        """
        self.cellar_lint(meta)

        if ref is None:
            ref = self._default_ref(meta)

        path = self._path_for_ref(ref)
        if path.exists():
            raise CellarConflictError(
                f"land: ref {ref!r} already exists — append-only, refusing to overwrite "
                "(re-land beside it with a new date-stamped ref and set supersedes)"
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        self._write(path, content, meta)
        return ref

    def upsert(self, ref: str, content: str, meta: dict[str, Any]) -> str:
        """Write-or-replace a *living index* artifact — the one deliberate,
        explicitly-named escape hatch from append-only (module docstring).
        Everything else goes through `land()`."""
        self.cellar_lint(meta)
        path = self._path_for_ref(ref)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._write(path, content, meta)
        return ref

    def resolve(self, ref: str) -> str:
        """Return the artifact's raw content (frontmatter + body, as landed)."""
        path = self._path_for_ref(ref)
        if not path.exists():
            raise FileNotFoundError(f"resolve: no such cellar ref: {ref!r}")
        return path.read_text(encoding="utf-8")

    def list_refs(self, prefix: Optional[str] = None, kind: Optional[str] = None) -> list[str]:
        """Enumerate landed refs, optionally filtered by subject prefix and/or kind."""
        results: list[str] = []
        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix == ".json" and path.name.endswith(".meta.json"):
                continue  # sidecar, not an artifact in its own right
            ref = str(path.relative_to(self.root))
            if prefix and not ref.startswith(prefix):
                continue
            if kind is not None:
                meta = self._read_meta(path)
                if meta.get("kind") != kind:
                    continue
            results.append(ref)
        return results

    def list(self, filter: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Enumerate landed artifacts as {ref, meta} records, optionally
        filtered by a dotted-path predicate map (e.g.
        `{"produced_by.ticket": ["t-1", "t-2"]}` — value may be a scalar or
        a list of acceptable scalars). Added for the Sales Collateral
        brigade's post-batch disk-truth sweep (its spec §4.2), which reads
        `cellar.list(filter={produced_by.ticket: <batch ticket ids>})` and
        NOTHING else — no work-log paths, no station outputs. `list_refs()`
        (kind/prefix only) stays as-is; this is an additive method, not a
        replacement."""
        filter = filter or {}
        out: list[dict[str, Any]] = []
        for ref in self.list_refs():
            path = self._path_for_ref(ref)
            meta = self._read_meta(path)
            if _matches_filter(meta, filter):
                out.append({"ref": ref, "meta": meta})
        return out

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _path_for_ref(self, ref: str) -> Path:
        return self.root / ref

    def _default_ref(self, meta: dict[str, Any]) -> str:
        date = str(meta["landed"])[:10]
        return f"{meta['subject']}/{date}-{meta['kind']}.md"

    def _write(self, path: Path, content: str | bytes, meta: dict[str, Any]) -> None:
        if path.suffix == ".md":
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            frontmatter = yaml.safe_dump(meta, sort_keys=False, default_flow_style=False)
            path.write_text(f"---\n{frontmatter}---\n\n{content}\n", encoding="utf-8")
        else:
            if isinstance(content, str):
                path.write_text(content, encoding="utf-8")
            else:
                path.write_bytes(content)
            meta_path = path.with_name(path.name + ".meta.json")
            meta_path.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")

    def _read_meta(self, path: Path) -> dict[str, Any]:
        if path.suffix == ".md":
            text = path.read_text(encoding="utf-8")
            fm, _ = split_frontmatter(text)
            return fm or {}
        meta_path = path.with_name(path.name + ".meta.json")
        if meta_path.exists():
            return json.loads(meta_path.read_text(encoding="utf-8"))
        return {}


def _matches_filter(meta: dict[str, Any], filter: dict[str, Any]) -> bool:
    for dotted_key, expected in filter.items():
        value: Any = meta
        for part in dotted_key.split("."):
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break
        expected_values = expected if isinstance(expected, (list, tuple, set)) else [expected]
        if value not in expected_values:
            return False
    return True


def split_frontmatter(text: str) -> tuple[Optional[dict[str, Any]], str]:
    """Split a landed markdown file into (meta_dict, body). Shared parsing
    helper for anything that needs to read a landed note back apart from the
    cellar client itself."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    fm_text = text[4:end]
    body = text[end + 5 :].lstrip("\n")
    try:
        meta = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None, text
    return meta, body


def now_iso() -> str:
    """Local-offset ISO timestamp, matching the CELLAR-SPEC frontmatter example."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def canonical_json(value: Any) -> str:
    """Canonical-JSON serialization for invariant-equality comparisons (the
    Assessment brigade's spec §3 Canonicalization rule: "JSON-valued fields...
    compare as canonical JSON — keys sorted, no insignificant whitespace,
    UTF-8"). Not a cellar_lint/land mechanic — lives here because it is
    generic serialization machinery, same neighborhood as the other
    cellar-adjacent helpers (`split_frontmatter`, `now_iso`)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
