"""The WALK PORT's reference adapter — Python, in-process, deterministic.

A walk is a ROLE, not a technology: *drive tickets from the rail through the
brigade to a terminal ack* (WALK-SPEC.md). This module is the reference
implementation of that role. It performs every mechanical step of the
contract by calling the sibling canon `rail_adapter` functions IN-PROCESS —
no LLM ever transcribes a pull, a Gate A verdict, or an ack — and invokes an
agent only where the contract is irreducibly agentic: station/expo dispatch.

The walk contract (every adapter, in order — WALK-SPEC.md):

  1. Take the service lock (advisory).                       [deterministic]
  2. Pull-with-lease, scoped to the menu's live types.       [deterministic]
  3. Gate A at pull (must match enqueue-side).               [deterministic]
  4. Resolve context — snapshot eager sources.               [mixed: static
     deterministic via the adapter; live via an injected fetcher]
  5. Dispatch to the expo/stations.                          [AGENT — the
     only irreducibly agentic step]
  6. Ack on the brigade's exit set; terminal tickets file.   [deterministic]
  7. Stop-flag between tickets; release lock on exit.        [deterministic]

CANON LIVES IN ab-skill-factory (adapter/walk.py). Brigades receive a
VENDORED, byte-identical copy stamped via the adapter's `stamp` subcommand
(canon inferred by filename — `CANON_PATHS["walk.py"]`); copies are build
artifacts, never hand-edited. All per-brigade variance arrives through
`WalkConfig` — the file itself never changes.

THE AGENT-RUNNER INTERFACE (pinned here; WALK-SPEC.md "Dispatch"):
a dispatcher is any callable

    dispatch(handle: rail_adapter.TicketHandle, phase: Optional[str]) -> dict

returning at least `{"exit": <brigade-exit-vocab>}` and optionally
`detail`, `terminal` (multi-phase only; default True), `cellar_refs`.
For an in-process brigade the dispatcher IS the station function (no LLM in
it at all). For a discipline brigade the dispatcher wraps an agent runner —
"run an agent with this prompt, optionally force a JSON schema, return the
parsed result":

    run_agent(prompt: str, *, schema: Optional[dict] = None) -> dict

In a Claude Code session that's the Task/Agent tool; in a headless
deployment it's the SDK; in a test it's a stub. `make_expo_dispatcher()`
below adapts any such runner into a dispatcher (the port of the Workflow
driver's serve step). The Workflow script `discipline-rail-walk.run.js`
remains the declared HARNESS-NATIVE adapter of this same port for
deployments that are a Claude Code session and nothing else.

Multi-phase brigades (one ticket spanning N sequential phase stations
behind a `current_phase` field — ab-assessment's shape) declare their
sequence in `WalkConfig.phased_artifacts`; single-dispatch brigades leave it
empty. Phase-chaining is a PARAMETER, not a fork of the walk.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field as dc_field
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

try:  # vendored package context (e.g. brigade/vendor/, skills/service/vendor/)
    from . import rail_adapter  # type: ignore
except ImportError:  # canon home / flat sys.path (adapter/, tests, CLI)
    import rail_adapter  # type: ignore

WALK_VERSION = "1.0.0"
CANON_NAME = "ab-skill-factory/adapter/walk.py"

# Rail dispositions the walk may hand to rail_adapter.ack(). A dispatcher's
# raw exit vocabulary is translated through WalkConfig.exit_map first (e.g.
# the discipline set: answered -> advance, needs-clarification ->
# reroute-to-steward, out-of-scope -> kill). "hold" is NOT an ack — it is the
# brigade-internal wait state (inner-rail merge pending): release the lease,
# leave the ticket queued, no refire increment, no filing.
ACK_EXITS = frozenset({"advance", "kill", "reroute-to-steward", "escalate", "refire-to-author"})
HOLD_EXIT = "hold"

# The discipline-kind exit set's mapping to rail dispositions — the same
# table the Workflow adapter carries (EXIT_TO_ACK), published here so both
# adapters of the port share one source of truth when vendored side by side.
DISCIPLINE_EXIT_MAP = {
    "answered": "advance",
    "partial-with-gaps": "advance",
    "needs-clarification": "reroute-to-steward",
    "out-of-scope": "kill",
}

_SNAPSHOT_ID_RE = re.compile(r"(?m)^- \*\*(?P<id>[^*]+)\*\* \(")


class WalkError(RuntimeError):
    """Walk-mechanics errors: lock contention, bad config, bad dispatch."""


Dispatcher = Callable[..., dict]


@dataclass
class WalkStepResult:
    ticket_id: Optional[str]
    outcome: str
    detail: str = ""
    dispatched_to: Optional[str] = None
    cellar_refs: list[str] = dc_field(default_factory=list)
    path: Optional[str] = None


@dataclass
class WalkConfig:
    """Everything brigade-specific, injected. The walk itself is canon."""

    brigade: str
    rail_dir: Path
    cellar_root: Path
    # Menu scope: the brigade's live artifact types (its MENU's live set).
    # `menu` discovery tickets are automatically in scope (walker_scope_ok
    # subject-scopes them to this brigade).
    allowed_artifacts: frozenset
    # Station-key -> dispatcher. Keys: the artifact type, or
    # "<artifact>:<phase>" for artifacts listed in `phased_artifacts`.
    dispatchers: dict = dc_field(default_factory=dict)
    # artifact -> ordered phase list (multi-phase brigades only).
    phased_artifacts: dict = dc_field(default_factory=dict)
    phase_field: str = "current_phase"
    # Dispatcher exit vocabulary -> rail disposition (identity by default).
    exit_map: dict = dc_field(default_factory=dict)
    # Mechanical Gate-B floor: (handle, phase) -> (ok, reason). Optional.
    gate_b: Optional[Callable[..., tuple]] = None
    # Live-source fetcher for step 4: entry-dict -> str content, or None/raise
    # on miss. When absent, live sources are work-logged as unresolved
    # (best-effort, JS-adapter parity) and the expo judges sufficiency.
    live_fetch: Optional[Callable[[dict], Optional[str]]] = None
    resolver_types: Optional[frozenset] = None
    worker: str = ""
    lease_ttl_min: int = rail_adapter.DEFAULT_LEASE_TTL_MIN
    max_tickets: int = 10
    take_lock: bool = True

    def __post_init__(self) -> None:
        self.rail_dir = Path(self.rail_dir)
        self.cellar_root = Path(self.cellar_root)
        if not self.worker:
            self.worker = f"{self.brigade}-walker"


class Walk:
    def __init__(self, config: WalkConfig):
        self.config = config

    # -- service lock / stop flag (contract steps 1 and 7) ----------------

    @property
    def _service_dir(self) -> Path:
        return self.config.rail_dir / ".service"

    @property
    def lock_path(self) -> Path:
        return self._service_dir / f"{self.config.brigade}.lock"

    @property
    def stop_flag_path(self) -> Path:
        return self._service_dir / f"{self.config.brigade}.stop"

    def _acquire_lock(self) -> None:
        self._service_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.lock_path, "x", encoding="utf-8") as fh:
                fh.write(json.dumps({"worker": self.config.worker, "at": rail_adapter._now_iso(None), "pid": os.getpid()}) + "\n")
        except FileExistsError:
            raise WalkError(
                f"service lock already held at {self.lock_path} — one walker per brigade per rail "
                "(advisory today; `service end` releases it, or remove a stale lock by hand)"
            )

    def _release_lock(self) -> None:
        try:
            self.lock_path.unlink()
        except FileNotFoundError:
            pass

    # -- the loop ----------------------------------------------------------

    def run(self, *, until_dry: bool = False, dry_run: bool = False) -> list[WalkStepResult]:
        if dry_run:
            return self.plan()

        cfg = self.config
        if cfg.take_lock:
            self._acquire_lock()
        results: list[WalkStepResult] = []
        try:
            for _ in range(max(1, cfg.max_tickets)):
                if self.stop_flag_path.exists():
                    results.append(WalkStepResult(None, "stopped", f"stop flag present at {self.stop_flag_path}"))
                    break

                handle = rail_adapter.pull(
                    cfg.rail_dir,
                    cfg.worker,
                    cfg.lease_ttl_min,
                    allowed_artifacts=set(cfg.allowed_artifacts) | {"menu"},
                    brigade=cfg.brigade,
                )
                if handle is None:
                    results.append(WalkStepResult(None, "rail-dry", "rail is dry, nothing to pull"))
                    break

                results.append(self._process_one(handle))

                if not until_dry:
                    break
        finally:
            if cfg.take_lock:
                self._release_lock()
        return results

    def _process_one(self, handle: "rail_adapter.TicketHandle") -> WalkStepResult:
        cfg = self.config

        # Step 3 — Gate A at pull (matches enqueue-side; a mismatch means an
        # adapter mutated the ticket in transit, itself a caught defect).
        rail_files = [p.name for p in cfg.rail_dir.glob("*.ticket.md")]
        lint = rail_adapter.ticket_lint(
            handle.text,
            rail_files,
            allowed_artifacts=set(cfg.allowed_artifacts) | {"menu"},
            resolver_types=cfg.resolver_types,
            cellar_root=cfg.cellar_root,
        )
        if not lint.passed:
            rail_adapter.append(handle.path, f"expo: Gate A re-check FAILED at pull — {lint.summary()}")
            path = rail_adapter.ack(handle.path, "reroute-to-steward", cfg.cellar_root)
            return WalkStepResult(handle.id, "gate-a-fail", lint.summary(), path=str(path))

        # Step 4 — resolve context (replayability; BUNDLE-SPEC).
        self.resolve_context(handle)

        # Step 5 — dispatch (the one agentic step).
        text = handle.path.read_text(encoding="utf-8")
        artifact = (rail_adapter.get_field(text, "artifact") or "").strip()
        phases = cfg.phased_artifacts.get(artifact)
        phase = None
        if phases:
            phase = (rail_adapter.get_field(text, cfg.phase_field) or phases[0]).strip()
        key = f"{artifact}:{phase}" if phase is not None else artifact

        dispatcher = cfg.dispatchers.get(key)
        if dispatcher is None:
            reason = f"no dispatcher registered for {key!r}"
            rail_adapter.append(handle.path, f"expo: {reason} — parking needs-context")
            path = rail_adapter.ack(handle.path, "reroute-to-steward", cfg.cellar_root)
            return WalkStepResult(handle.id, "no-dispatcher", reason, dispatched_to=key, path=str(path))

        if cfg.gate_b is not None:
            ok, reason = cfg.gate_b(handle, phase)
            if not ok:
                rail_adapter.append(handle.path, f"expo: Gate-B floor FAILED — {reason}")
                path = rail_adapter.ack(handle.path, "reroute-to-steward", cfg.cellar_root)
                return WalkStepResult(handle.id, "gate-b-fail", str(reason), dispatched_to=key, path=str(path))

        rail_adapter.append(handle.path, f"expo: dispatch to station {key!r}")
        try:
            raw = dispatcher(handle, phase)
        except Exception as exc:  # a station crash is contention for the steward, not the walk's
            rail_adapter.append(handle.path, f"station {key}: FAILED — {type(exc).__name__}: {exc}")
            path = rail_adapter.ack(handle.path, "reroute-to-steward", cfg.cellar_root)
            return WalkStepResult(handle.id, "station-error", str(exc), dispatched_to=key, path=str(path))

        raw = raw or {}
        raw_exit = str(raw.get("exit", "escalate"))
        exit_ = cfg.exit_map.get(raw_exit, raw_exit)
        detail = str(raw.get("detail", ""))
        terminal = bool(raw.get("terminal", True))
        refs = [str(r) for r in (raw.get("cellar_refs") or [])]

        rail_adapter.append(handle.path, f"station {key}: {raw_exit} — {detail}")

        # Step 6 — ack on the brigade's exit set; terminal files to subject.
        if exit_ == HOLD_EXIT:
            rail_adapter.release(handle.path)
            return WalkStepResult(handle.id, HOLD_EXIT, detail, dispatched_to=key, cellar_refs=refs, path=str(handle.path))

        if exit_ not in ACK_EXITS:
            rail_adapter.append(handle.path, f"expo: unmapped exit {raw_exit!r} (-> {exit_!r}) — escalating")
            path = rail_adapter.ack(handle.path, "escalate", cfg.cellar_root)
            return WalkStepResult(handle.id, "unmapped-exit", f"{raw_exit!r} has no rail disposition", dispatched_to=key, path=str(path))

        path = rail_adapter.ack(
            handle.path,
            exit_,
            cfg.cellar_root,
            terminal=terminal if exit_ == "advance" else True,
            phases=phases,
            phase_field=cfg.phase_field,
            artifact_refs=refs or None,
        )
        return WalkStepResult(handle.id, exit_, detail, dispatched_to=key, cellar_refs=refs, path=str(path))

    # -- step 4: resolution -------------------------------------------------

    def resolve_context(self, handle: "rail_adapter.TicketHandle") -> None:
        resolve_context(handle.path, self.config.cellar_root, live_fetch=self.config.live_fetch)

    # -- dry-run / plan ------------------------------------------------------

    def plan(self) -> list[WalkStepResult]:
        """Show what a run WOULD do — no claims, no writes, no network."""
        cfg = self.config
        results: list[WalkStepResult] = []
        candidates = sorted(cfg.rail_dir.glob("*.ticket.md"), key=lambda p: p.stat().st_mtime)
        now_val = rail_adapter._now_iso(None)
        for p in candidates:
            text = p.read_text(encoding="utf-8")
            if not rail_adapter.walker_scope_ok(text, set(cfg.allowed_artifacts) | {"menu"}, cfg.brigade):
                continue
            status = rail_adapter.get_field(text, "status")
            lease = rail_adapter.get_lease(text)
            workable = (
                status == "queued"
                or (status == "in-build" and lease is None)
                or (status in ("leased", "in-build") and rail_adapter._lease_expired(lease, now_val))
            )
            if not workable:
                continue
            tid = rail_adapter.get_field(text, "ticket") or p.name.removesuffix(".ticket.md")
            artifact = (rail_adapter.get_field(text, "artifact") or "").strip()
            phases = cfg.phased_artifacts.get(artifact)
            phase = (rail_adapter.get_field(text, cfg.phase_field) or phases[0]).strip() if phases else None
            key = f"{artifact}:{phase}" if phase is not None else artifact
            if cfg.dispatchers and key not in cfg.dispatchers:
                results.append(WalkStepResult(tid, "dry-plan", f"WOULD park needs-context — no dispatcher for {key!r}", dispatched_to=key, path=str(p)))
                continue
            results.append(WalkStepResult(tid, "dry-plan", f"WOULD dispatch to station {key!r}", dispatched_to=key, path=str(p)))
        if not results:
            results.append(WalkStepResult(None, "rail-dry", "rail is dry, nothing to pull"))
        return results


# ---------------------------------------------------------------------------
# Step 4 as a standalone primitive — module-level so the Gen-A brigades'
# own walk wrappers (assessment's pass_driver, company-research's and
# sales-collateral's _process_one) call the SAME resolution the reference
# walk runs, closing the resolver's Gen-A gap without forcing those
# brigades onto the Walk class wholesale.
# ---------------------------------------------------------------------------


def resolve_context(
    ticket_path: "str | Path",
    cellar_root: "str | Path",
    *,
    live_fetch: Optional[Callable[[dict], Optional[str]]] = None,
) -> None:
    """Freeze the ticket's eager sources into `## Resolved-context snapshot`
    (append-only; already-snapshotted entry ids are skipped, so a multi-phase
    re-pull or refire doesn't duplicate the section). Static (file/cellar)
    sources record an integrity sha via the adapter; live (url/mcp/qmd)
    sources go through `live_fetch` when wired, else are work-logged as
    unresolved (best-effort — the expo's sufficiency judgment still stands
    between a miss and a bad build)."""
    ticket_path = Path(ticket_path)
    text = ticket_path.read_text(encoding="utf-8")
    plan = rail_adapter.plan_resolution(text, cellar_root)
    done_ids = _snapshotted_ids(text)

    for entry in plan["static"]:
        eid = entry.get("id") or ""
        if not eid or eid in done_ids:
            continue
        if not entry.get("resolved"):
            rail_adapter.append(ticket_path, f"resolution: static source {eid!r} did not resolve ({entry.get('type')}: {entry.get('ref')}) — miss logged, not fatal")
            continue
        rail_adapter.snapshot_source(
            ticket_path,
            entry_id=eid,
            source_type=entry.get("type") or "file",
            ref=entry.get("ref") or "",
            sha256=entry.get("sha256"),
        )

    for entry in plan["live"]:
        eid = entry.get("id") or ""
        if not eid or eid in done_ids:
            continue
        if live_fetch is None:
            rail_adapter.append(ticket_path, f"resolution: live source {eid!r} not resolved (no live fetcher wired) — expo judges sufficiency")
            continue
        try:
            content = live_fetch(entry)
        except Exception as exc:
            content = None
            rail_adapter.append(ticket_path, f"resolution: live fetch FAILED for {eid!r} — {type(exc).__name__}: {exc} — miss logged, not fatal")
        if content is None:
            continue
        rail_adapter.snapshot_source(
            ticket_path,
            entry_id=eid,
            source_type=entry.get("type") or "url",
            ref=entry.get("ref") or "",
            content=str(content),
        )


def _snapshotted_ids(text: str) -> set:
    m = re.search(r"(?ms)^## Resolved-context snapshot\s*$(.*?)(?=^## |\Z)", text)
    if not m:
        return set()
    return {mm.group("id").strip() for mm in _SNAPSHOT_ID_RE.finditer(m.group(1))}


# ---------------------------------------------------------------------------
# Discipline-brigade dispatcher — adapts an agent runner to the port,
# porting the Workflow driver's serve step. This pins the agent-runner
# interface (module docstring): run_agent(prompt, *, schema=None) -> dict.
# ---------------------------------------------------------------------------

SERVE_SCHEMA = {
    "type": "object",
    "properties": {
        "exit": {"type": "string", "enum": ["answered", "partial-with-gaps", "needs-clarification", "out-of-scope"]},
        "summary": {"type": "string"},
        "artifact_path": {"type": "string"},
        "gaps": {"type": "string"},
    },
    "required": ["exit", "summary"],
}


def make_expo_dispatcher(
    run_agent: Callable[..., dict],
    *,
    brigade: str,
    plugin_dir: str | Path,
    cellar_root: str | Path,
    expo_skill: Optional[str | Path] = None,
) -> Dispatcher:
    """Wrap an agent runner as this port's dispatcher for a discipline
    brigade: one agent call serves the ticket end to end per the brigade's
    expo procedure; every rail mutation before/after it stays in-process in
    the walk. Pair with `exit_map=DISCIPLINE_EXIT_MAP` in WalkConfig."""
    plugin_dir = Path(plugin_dir)
    expo = Path(expo_skill) if expo_skill else plugin_dir / "skills" / "expo" / "SKILL.md"

    def dispatch(handle: "rail_adapter.TicketHandle", phase: Optional[str]) -> dict:
        text = handle.path.read_text(encoding="utf-8")
        subject = (rail_adapter.get_field(text, "subject") or "").strip().strip('"').strip("'")
        prompt = (
            f"You are the {brigade} expo, serving ONE rail ticket end to end.\n"
            f"Read the expo procedure at {expo} and follow it exactly — decompose the Order, "
            f"select stations from {plugin_dir}/skills/, compose, finishing touch. "
            "Honest statuses: a held station presents as held.\n"
            f"The ticket is at {handle.path} — its full text:\n---\n{text}\n---\n"
            "Rules of the rail (origin: this ticket rode the queue; gates still apply):\n"
            "- If the Order is ambiguous or the context is thin, do NOT guess: exit needs-clarification "
            "with the itemized questions appended to the work log.\n"
            "- If the Order is outside this brigade's menu, exit out-of-scope and name the right brigade if you can.\n"
            f"- Otherwise produce the composed answer. Write it as a markdown artifact to "
            f"{cellar_root}/{subject or '{subject}'}/artifacts/{handle.id}-answer.md — create dirs as needed, "
            f"and include provenance frontmatter: produced_by brigade {brigade}, the ticket id, and the stations used.\n"
            "- Do NOT edit the ticket file itself — the walk owns every rail mutation, including the work log.\n"
            "- If the answer is complete: exit answered. If real gaps remain that more context would not fix "
            "cheaply, exit partial-with-gaps and state the gaps in both the artifact and the gaps field.\n"
            "Return exit, a one-line summary, artifact_path when you wrote one, gaps when partial."
        )
        result = run_agent(prompt, schema=SERVE_SCHEMA) or {}
        refs: list[str] = []
        ap = result.get("artifact_path")
        if ap:
            ref = str(ap)
            root = str(cellar_root).rstrip("/") + "/"
            if ref.startswith(root):
                ref = ref[len(root):]
            refs.append(ref)
        detail = str(result.get("summary", ""))
        gaps = result.get("gaps")
        if gaps:
            detail += f" — gaps: {gaps}"
        return {"exit": str(result.get("exit", "needs-clarification")), "detail": detail, "cellar_refs": refs}

    return dispatch


# ---------------------------------------------------------------------------
# CLI — plan only. A real run needs Python dispatchers (each brigade's
# service wiring supplies them); the CLI exists so any session can ask
# "what would this brigade's walk do right now" without side effects.
# ---------------------------------------------------------------------------


def _cli(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Canon walk (reference adapter of the walk port) — plan mode")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_plan = sub.add_parser("plan", help="show what a walk run WOULD do (no claims, no writes)")
    p_plan.add_argument("rail_dir")
    p_plan.add_argument("--brigade", required=True)
    p_plan.add_argument("--cellar-root", required=True)
    p_plan.add_argument("--allowed-artifact", action="append", default=[], help="repeat per live menu type")
    p_plan.add_argument("--phased", action="append", default=[], help="artifact=phase1,phase2,... (repeatable)")
    args = parser.parse_args(argv)

    phased = {}
    for spec in args.phased:
        name, _, seq = spec.partition("=")
        phased[name] = [s for s in seq.split(",") if s]
    cfg = WalkConfig(
        brigade=args.brigade,
        rail_dir=Path(args.rail_dir),
        cellar_root=Path(args.cellar_root),
        allowed_artifacts=frozenset(args.allowed_artifact),
        phased_artifacts=phased,
    )
    for r in Walk(cfg).plan():
        print(json.dumps({"ticket_id": r.ticket_id, "outcome": r.outcome, "detail": r.detail, "dispatched_to": r.dispatched_to}))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
