"""Walk-port convergence tests: the rail_adapter v1.3.0 extensions
(pull ticket_id scoping, in-build/no-lease workability, multi-phase ack)
and the canon walk.py reference adapter. tmp_path-only, never touches the
real cellar/rail. Run via
`python3 -m pytest plugins/ab-skill-factory/adapter/tests/ -q`.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import pytest

import rail_adapter as ra
import walk as wk

from test_rail_adapter import make_ticket, context_entry  # shared synthetic builder


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _rail(tmp_path: Path) -> Path:
    rail = tmp_path / "cellar" / "rail"
    rail.mkdir(parents=True, exist_ok=True)
    return rail


def _cellar(tmp_path: Path) -> Path:
    c = tmp_path / "cellar"
    c.mkdir(parents=True, exist_ok=True)
    return c


def _place(rail: Path, text: str, ticket_id: str) -> Path:
    p = rail / f"{ticket_id}.ticket.md"
    p.write_text(text, encoding="utf-8")
    return p


def _eager_source(tmp_path: Path, name: str = "src.md") -> Path:
    p = tmp_path / name
    p.write_text("# a real context source\n", encoding="utf-8")
    return p


def _phased_ticket(tmp_path: Path, *, ticket_id: str = "assess-acme-2026-01-01", phase: str = "p0") -> str:
    src = _eager_source(tmp_path)
    text = make_ticket(ticket_id=ticket_id, context_lines=context_entry(str(src)), subject="companies/acme")
    text = ra.set_field(text, "current_phase", phase)
    text = ra.set_field(text, "refire_round", "0")
    return text


# ===========================================================================
# 1. pull() v1.3.0 — ticket_id scoping + in-build/no-lease workability
# ===========================================================================


def test_pull_ticket_id_scopes_past_an_older_ticket(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="older-one", context_lines=context_entry(str(src))), "older-one")
    time.sleep(0.02)
    _place(rail, make_ticket(ticket_id="target-two", context_lines=context_entry(str(src))), "target-two")

    handle = ra.pull(rail, "w1", ticket_id="target-two")
    assert handle is not None and handle.id == "target-two"
    # the older queued ticket is untouched
    assert (rail / "older-one.ticket.md").exists()


def test_pull_ticket_id_skips_walker_scope(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="foreign-art", artifact="company-jobs-snapshot", context_lines=context_entry(str(src))), "foreign-art")

    # scoped pull would skip it; explicit id is a deliberate act
    assert ra.pull(rail, "w1", allowed_artifacts={"skill"}, brigade="factory") is None
    handle = ra.pull(rail, "w1", allowed_artifacts={"skill"}, brigade="factory", ticket_id="foreign-art")
    assert handle is not None and handle.id == "foreign-art"


def test_pull_ticket_id_returns_none_when_not_workable(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    text = make_ticket(ticket_id="parked-one", status="needs-context", context_lines=context_entry(str(src)))
    _place(rail, text, "parked-one")
    assert ra.pull(rail, "w1", ticket_id="parked-one") is None


def test_pull_in_build_no_lease_is_workable_without_reclaim(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    text = make_ticket(ticket_id="mid-phase", status="in-build", context_lines=context_entry(str(src)))
    _place(rail, text, "mid-phase")

    handle = ra.pull(rail, "w1")
    assert handle is not None and handle.id == "mid-phase"
    assert "lease-reclaimed" not in handle.text  # between-phase state, not an abandonment


def test_pull_in_build_live_lease_is_not_workable(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    lease = json.dumps({"worker": "other", "at": ra._now_iso(None), "ttl_min": 60})
    text = make_ticket(ticket_id="claimed-one", status="in-build", lease=lease, context_lines=context_entry(str(src)))
    _place(rail, text, "claimed-one")
    assert ra.pull(rail, "w1") is None


# ===========================================================================
# 2. ack() v1.3.0 — multi-phase advance, refire-to-author, artifact_refs
# ===========================================================================

PHASES = ["p0", "p1", "p2"]


def test_ack_advance_non_terminal_advances_phase_and_returns_to_root(tmp_path):
    rail = _rail(tmp_path)
    cellar = _cellar(tmp_path)
    _place(rail, _phased_ticket(tmp_path), "assess-acme-2026-01-01")

    handle = ra.pull(rail, "w1")
    assert handle.path.parent.parent.name == ".claimed"

    after = ra.ack(handle.path, "advance", cellar, terminal=False, phases=PHASES)
    text = after.read_text()
    assert after.parent == rail  # back at rail root, workable for the next phase
    assert ra.get_field(text, "status") == "in-build"
    assert ra.get_field(text, "current_phase") == "p1"
    assert ra.get_field(text, "refire_round") == "0"
    assert ra.get_lease(text) is None
    assert "ack: advance → status in-build (current_phase p0 -> p1)" in text


def test_ack_advance_non_terminal_requires_phases(tmp_path):
    rail = _rail(tmp_path)
    cellar = _cellar(tmp_path)
    _place(rail, _phased_ticket(tmp_path), "assess-acme-2026-01-01")
    handle = ra.pull(rail, "w1")
    with pytest.raises(ra.RailError, match="requires `phases`"):
        ra.ack(handle.path, "advance", cellar, terminal=False)


def test_ack_refire_to_author_requeues_and_increments(tmp_path):
    rail = _rail(tmp_path)
    cellar = _cellar(tmp_path)
    _place(rail, _phased_ticket(tmp_path), "assess-acme-2026-01-01")
    handle = ra.pull(rail, "w1")

    after = ra.ack(handle.path, "refire-to-author", cellar)
    text = after.read_text()
    assert after.parent == rail
    assert ra.get_field(text, "status") == "queued"
    assert ra.get_field(text, "refire_round") == "1"

    # and again — the budget counter is cumulative
    handle2 = ra.pull(rail, "w1")
    after2 = ra.ack(handle2.path, "refire-to-author", cellar)
    assert ra.get_field(after2.read_text(), "refire_round") == "2"


def test_ack_artifact_refs_land_in_artifacts_section(tmp_path):
    rail = _rail(tmp_path)
    cellar = _cellar(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="ref-test", subject="companies/acme", context_lines=context_entry(str(src))), "ref-test")
    handle = ra.pull(rail, "w1")

    dest = ra.ack(handle.path, "advance", cellar, artifact_refs=["companies/acme/artifacts/x.md"])
    text = dest.read_text()
    assert "- cellar: `companies/acme/artifacts/x.md`" in text
    assert dest == cellar / "companies/acme" / "tickets" / "ref-test.ticket.md"  # terminal default unchanged


def test_ack_full_phase_chain_ends_done_and_filed(tmp_path):
    rail = _rail(tmp_path)
    cellar = _cellar(tmp_path)
    _place(rail, _phased_ticket(tmp_path), "assess-acme-2026-01-01")

    for expected_next in ["p1", "p2"]:
        handle = ra.pull(rail, "w1")
        assert handle is not None, f"chain broke before phase {expected_next}"
        after = ra.ack(handle.path, "advance", cellar, terminal=False, phases=PHASES)
        assert ra.get_field(after.read_text(), "current_phase") == expected_next

    handle = ra.pull(rail, "w1")  # in-build/no-lease re-pull, final phase
    dest = ra.ack(handle.path, "advance", cellar, terminal=True)
    assert ra.get_field(dest.read_text(), "status") == "done"
    assert dest.parent == cellar / "companies/acme" / "tickets"
    assert not (rail / "assess-acme-2026-01-01.ticket.md").exists()


# ===========================================================================
# 3. walk.py — the reference adapter
# ===========================================================================


def _walk_cfg(tmp_path: Path, **over) -> wk.WalkConfig:
    defaults = dict(
        brigade="testbrigade",
        rail_dir=_rail(tmp_path),
        cellar_root=_cellar(tmp_path),
        allowed_artifacts=frozenset({"skill"}),
        max_tickets=10,
    )
    defaults.update(over)
    return wk.WalkConfig(**defaults)


def test_walk_single_dispatch_advance_files_with_refs(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="one-shot", subject="companies/acme", context_lines=context_entry(str(src))), "one-shot")

    def station(handle, phase):
        return {"exit": "advance", "detail": "did the thing", "cellar_refs": ["companies/acme/artifacts/a.md"]}

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": station})
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["advance"]

    filed = cfg.cellar_root / "companies/acme" / "tickets" / "one-shot.ticket.md"
    assert filed.exists()
    text = filed.read_text()
    assert ra.get_field(text, "status") == "done"
    assert "expo: dispatch to station 'skill'" in text
    assert "station skill: advance — did the thing" in text
    assert "- cellar: `companies/acme/artifacts/a.md`" in text


def test_walk_discipline_exit_map_parks_needs_context_on_rail(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="thin-order", subject="companies/acme", context_lines=context_entry(str(src))), "thin-order")

    def expo(handle, phase):
        return {"exit": "needs-clarification", "detail": "which quarter?"}

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": expo}, exit_map=dict(wk.DISCIPLINE_EXIT_MAP))
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["reroute-to-steward"]

    parked = rail / "thin-order.ticket.md"
    assert parked.exists()  # non-terminal: stays on the rail, back at root
    assert ra.get_field(parked.read_text(), "status") == "needs-context"


def test_walk_hold_releases_without_refire_bump(tmp_path):
    rail = _rail(tmp_path)
    _place(rail, _phased_ticket(tmp_path, ticket_id="waiting-merge"), "waiting-merge")

    def station(handle, phase):
        return {"exit": "hold", "detail": "3 micro-tickets still open"}

    cfg = _walk_cfg(
        tmp_path,
        dispatchers={"skill:p0": station},
        phased_artifacts={"skill": PHASES},
    )
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["hold"]
    text = (rail / "waiting-merge.ticket.md").read_text()
    assert ra.get_field(text, "status") == "queued"
    assert ra.get_field(text, "refire_round") == "0"


def test_walk_multi_phase_chain_until_dry(tmp_path):
    rail = _rail(tmp_path)
    _place(rail, _phased_ticket(tmp_path, ticket_id="assess-acme-2026-01-01"), "assess-acme-2026-01-01")
    seen = []

    def phase_station(handle, phase):
        seen.append(phase)
        return {"exit": "advance", "terminal": phase == "p2", "detail": f"phase {phase} ok"}

    cfg = _walk_cfg(
        tmp_path,
        dispatchers={f"skill:{p}": phase_station for p in PHASES},
        phased_artifacts={"skill": PHASES},
    )
    results = wk.Walk(cfg).run(until_dry=True)

    assert seen == ["p0", "p1", "p2"]
    outcomes = [r.outcome for r in results]
    assert outcomes == ["advance", "advance", "advance", "rail-dry"]
    filed = cfg.cellar_root / "companies/acme" / "tickets" / "assess-acme-2026-01-01.ticket.md"
    assert filed.exists()
    assert ra.get_field(filed.read_text(), "status") == "done"


def test_walk_gate_a_fail_parks_needs_context(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    # four canonical sections out of order -> rule 7 fails at pull
    bad_sections = ("## Order", "## Work log", "## Resolved-context snapshot", "## Artifacts")
    _place(rail, make_ticket(ticket_id="bent-ticket", context_lines=context_entry(str(src)), sections=bad_sections), "bent-ticket")

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": lambda h, p: {"exit": "advance"}})
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["gate-a-fail"]
    assert ra.get_field((rail / "bent-ticket.ticket.md").read_text(), "status") == "needs-context"


def test_walk_no_dispatcher_parks(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="orphan-kind", context_lines=context_entry(str(src))), "orphan-kind")

    cfg = _walk_cfg(tmp_path, dispatchers={})
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["no-dispatcher"]


def test_walk_station_crash_parks_needs_context(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="crashy", context_lines=context_entry(str(src))), "crashy")

    def station(handle, phase):
        raise RuntimeError("boom")

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": station})
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["station-error"]
    text = (rail / "crashy.ticket.md").read_text()
    assert "station skill: FAILED — RuntimeError: boom" in text
    assert ra.get_field(text, "status") == "needs-context"


def test_walk_stop_flag_halts_before_pull(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="never-pulled", context_lines=context_entry(str(src))), "never-pulled")

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": lambda h, p: {"exit": "advance"}})
    w = wk.Walk(cfg)
    w.stop_flag_path.parent.mkdir(parents=True, exist_ok=True)
    w.stop_flag_path.write_text("stop\n")

    results = w.run(until_dry=True)
    assert [r.outcome for r in results] == ["stopped"]
    assert ra.get_field((rail / "never-pulled.ticket.md").read_text(), "status") == "queued"


def test_walk_lock_contention_refuses_and_lock_released_after_run(tmp_path):
    cfg = _walk_cfg(tmp_path, dispatchers={})
    w = wk.Walk(cfg)
    w.lock_path.parent.mkdir(parents=True, exist_ok=True)
    w.lock_path.write_text("{}\n")
    with pytest.raises(wk.WalkError, match="service lock already held"):
        w.run()
    w.lock_path.unlink()

    results = w.run()  # dry rail; lock must be gone afterwards
    assert [r.outcome for r in results] == ["rail-dry"]
    assert not w.lock_path.exists()


def test_walk_resolution_snapshots_static_once_across_phases(tmp_path):
    rail = _rail(tmp_path)
    _place(rail, _phased_ticket(tmp_path, ticket_id="snap-once"), "snap-once")

    cfg = _walk_cfg(
        tmp_path,
        dispatchers={f"skill:{p}": (lambda h, ph: {"exit": "advance", "terminal": ph == "p2"}) for p in PHASES},
        phased_artifacts={"skill": PHASES},
    )
    wk.Walk(cfg).run(until_dry=True)

    filed = cfg.cellar_root / "companies/acme" / "tickets" / "snap-once.ticket.md"
    text = filed.read_text()
    assert text.count("- **core** (file:") == 1  # deduped across the 3 phase re-pulls
    assert re.search(r"- \*\*core\*\* \(file: .*\) — resolved .* · sha256 ", text)


def test_walk_resolution_live_fetch_freezes_content(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    ctx = context_entry(str(src)) + context_entry("https://example.com/report", eid="live-report", type_="url")
    _place(rail, make_ticket(ticket_id="live-src", subject="companies/acme", context_lines=ctx), "live-src")

    def fetch(entry):
        assert entry["id"] == "live-report"
        return "frozen body line 1\nline 2"

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": lambda h, p: {"exit": "advance"}}, live_fetch=fetch)
    wk.Walk(cfg).run()

    filed = cfg.cellar_root / "companies/acme" / "tickets" / "live-src.ticket.md"
    text = filed.read_text()
    assert "- **live-report** (url: https://example.com/report) — resolved" in text
    assert "frozen body line 1" in text


def test_walk_resolution_live_miss_is_logged_not_fatal(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    ctx = context_entry(str(src)) + context_entry("https://example.com/x", eid="live-x", type_="url")
    _place(rail, make_ticket(ticket_id="live-miss", subject="companies/acme", context_lines=ctx), "live-miss")

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": lambda h, p: {"exit": "advance"}})  # no live_fetch
    results = wk.Walk(cfg).run()
    assert [r.outcome for r in results] == ["advance"]
    filed = cfg.cellar_root / "companies/acme" / "tickets" / "live-miss.ticket.md"
    assert "resolution: live source 'live-x' not resolved (no live fetcher wired)" in filed.read_text()


def test_walk_plan_makes_no_writes(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    p = _place(rail, make_ticket(ticket_id="plan-only", context_lines=context_entry(str(src))), "plan-only")
    before = p.read_bytes()

    cfg = _walk_cfg(tmp_path, dispatchers={"skill": lambda h, ph: {"exit": "advance"}})
    results = wk.Walk(cfg).run(dry_run=True)
    assert [r.outcome for r in results] == ["dry-plan"]
    assert "WOULD dispatch to station 'skill'" in results[0].detail
    assert p.read_bytes() == before
    assert not wk.Walk(cfg).lock_path.exists()


def test_make_expo_dispatcher_adapts_agent_runner(tmp_path):
    rail = _rail(tmp_path)
    src = _eager_source(tmp_path)
    _place(rail, make_ticket(ticket_id="agent-serve", subject="companies/acme", context_lines=context_entry(str(src))), "agent-serve")
    cellar = _cellar(tmp_path)
    prompts = []

    def run_agent(prompt, *, schema=None):
        prompts.append(prompt)
        assert schema is wk.SERVE_SCHEMA
        return {"exit": "partial-with-gaps", "summary": "answered 3 of 4", "gaps": "no Q3 data", "artifact_path": f"{cellar}/companies/acme/artifacts/agent-serve-answer.md"}

    dispatch = wk.make_expo_dispatcher(run_agent, brigade="testbrigade", plugin_dir=tmp_path / "plug", cellar_root=cellar)
    cfg = _walk_cfg(tmp_path, dispatchers={"skill": dispatch}, exit_map=dict(wk.DISCIPLINE_EXIT_MAP))
    results = wk.Walk(cfg).run()

    assert [r.outcome for r in results] == ["advance"]
    assert results[0].cellar_refs == ["companies/acme/artifacts/agent-serve-answer.md"]
    assert "serving ONE rail ticket end to end" in prompts[0]
    filed = cellar / "companies/acme" / "tickets" / "agent-serve.ticket.md"
    text = filed.read_text()
    assert "station skill: partial-with-gaps — answered 3 of 4 — gaps: no Q3 data" in text
    assert "- cellar: `companies/acme/artifacts/agent-serve-answer.md`" in text
