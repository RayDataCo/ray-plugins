"""Tests for the canonical rail_adapter — tmp_path-only, never touches the
real cellar/rail. Run via `python3 -m pytest plugins/skill-agent-brigade/adapter/tests/ -q`
from the repo root.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

import rail_adapter as ra
from conftest import FIXTURES_DIR


# ---------------------------------------------------------------------------
# Fixture-ticket helpers — the two REAL ticket shapes that exposed the
# 2-space-vs-0-indent context-entry parser drift, copied structurally.
# ---------------------------------------------------------------------------


def _factory_menu_ticket_text(brigade_home: Path, menu_spec: Path) -> str:
    tmpl = (FIXTURES_DIR / "factory-menu-restamp-2026-07-03.ticket.md.tmpl").read_text()
    return tmpl.replace("__BRIGADE_HOME__", str(brigade_home)).replace(
        "__MENU_SPEC_PATH__", str(menu_spec)
    )


def _lenovo_ticket_text() -> str:
    return (FIXTURES_DIR / "lenovo-collateral-stress-2026-07-02.ticket.md.tmpl").read_text()


def _seed_lenovo_cellar(cellar_root: Path) -> None:
    """Create the files the lenovo fixture's eager `type: cellar` sources
    point at, so rule 5 can genuinely resolve them (not skip via
    cellar_root=None)."""
    manifest_dir = cellar_root / "assessments/lenovo/build-manifest"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "2026-07-02T161235-manifest.json").write_text("{}")

    contract_dir = cellar_root / "assessments/lenovo/contract-4"
    contract_dir.mkdir(parents=True)
    (contract_dir / "2026-07-02-contract-4.json").write_text("{}")

    exemplar_dir = cellar_root / "competencies/sales-collateral"
    exemplar_dir.mkdir(parents=True)
    (exemplar_dir / "quest-diagnostics-INDEX.md").write_text("# index\n")


# ---------------------------------------------------------------------------
# Minimal synthetic ticket builder — for happy-path + negative-control tests
# that don't need the full real-ticket shape.
# ---------------------------------------------------------------------------

DEFAULT_SECTIONS = ("## Order", "## Resolved-context snapshot", "## Work log", "## Artifacts")


def make_ticket(
    *,
    ticket_id: str = "sample-skill-2026-01-01",
    artifact: str = "skill",
    status: str = "queued",
    lease: str = "null",
    subject: str | None = None,
    context_lines: str = "",
    order: str = "Build a small sample thing end to end.",
    sections: tuple[str, ...] = DEFAULT_SECTIONS,
) -> str:
    subject_line = f"subject: {subject}\n" if subject else ""
    fm = (
        "---\n"
        f"ticket: {ticket_id}\n"
        f"artifact: {artifact}\n"
        f"status: {status}\n"
        "requested_by: tester\n"
        f"{subject_line}"
        f"lease: {lease}\n"
        f"context:\n{context_lines}"
        "---\n"
    )
    body = (
        f"\n{sections[0]}\n\n{order}\n\n"
        f"{sections[1]}\n\nnone yet\n\n"
        f"{sections[2]}\n\n"
        f"{sections[3]}\n\nnone yet\n"
    )
    return fm + body


def context_entry(ref: str, *, eid: str = "core", type_: str = "file", when: str = "always — needed") -> str:
    return f"  - id: {eid}\n    type: {type_}\n    ref: {ref}\n    when: {when}\n"


@pytest.fixture
def eager_ref(tmp_path: Path) -> Path:
    p = tmp_path / "context-source.md"
    p.write_text("# a real context source\n")
    return p


@pytest.fixture
def valid_ticket_text(eager_ref: Path) -> str:
    return make_ticket(context_lines=context_entry(str(eager_ref)), subject="companies/acme")


# ===========================================================================
# 1. Both REAL ticket shapes lint 8/8 — the drift-fix regression test.
# ===========================================================================


def test_factory_menu_shape_2space_indent_lints_8_of_8(tmp_path):
    brigade_home = tmp_path / "brigade-home"
    brigade_home.mkdir()
    menu_spec = brigade_home / "MENU-SPEC.md"
    menu_spec.write_text("# menu spec\n")

    text = _factory_menu_ticket_text(brigade_home, menu_spec)
    result = ra.ticket_lint(text, rail_files=[])

    assert len(result.rules) == 8
    assert result.passed, result.summary()
    entries = ra.parse_context_entries(text)
    assert [e["id"] for e in entries] == ["brigade-home", "menu-spec"]


def test_lenovo_shape_0indent_context_lints_8_of_8(tmp_path):
    cellar_root = tmp_path / "cellar"
    _seed_lenovo_cellar(cellar_root)
    text = _lenovo_ticket_text()

    result = ra.ticket_lint(
        text, rail_files=[], allowed_artifacts={"sales-collateral"}, cellar_root=cellar_root
    )

    assert len(result.rules) == 8
    assert result.passed, result.summary()
    entries = ra.parse_context_entries(text)
    assert [e["id"] for e in entries] == [
        "build-manifest",
        "contract-4",
        "dossier",
        "exemplar-anchors",
    ]
    # 3 of the 4 sources are eager ("always ...."); dossier is conditional.
    eager_ids = [e["id"] for e in entries if ra._is_eager(e)]
    assert eager_ids == ["build-manifest", "contract-4", "exemplar-anchors"]


def test_menu_driven_artifact_enum_accepts_and_rejects(tmp_path):
    """SF-1 drift fix: allowed_artifacts is a caller parameter, not a
    hardcoded enum. The lenovo ticket's `artifact: sales-collateral` must
    be ACCEPTED against its own brigade's menu and REJECTED against this
    factory's default menu."""
    cellar_root = tmp_path / "cellar"
    _seed_lenovo_cellar(cellar_root)
    text = _lenovo_ticket_text()

    accepted = ra.ticket_lint(text, [], allowed_artifacts={"sales-collateral"}, cellar_root=cellar_root)
    assert accepted.passed

    rejected = ra.ticket_lint(text, [], cellar_root=cellar_root)  # default factory menu
    assert not rejected.passed
    assert 2 in rejected.failed_ids


# ===========================================================================
# 2. Gate A negative controls — one per rule.
# ===========================================================================


def test_rule1_fails_on_bad_kebab_case(eager_ref):
    text = make_ticket(ticket_id="Not_Kebab_Case", context_lines=context_entry(str(eager_ref)))
    result = ra.ticket_lint(text, [])
    assert 1 in result.failed_ids


def test_rule1_fails_on_duplicate_id_on_rail(valid_ticket_text):
    dup_files = ["sample-skill-2026-01-01.ticket.md", "sample-skill-2026-01-01.ticket.md"]
    result = ra.ticket_lint(valid_ticket_text, dup_files)
    assert 1 in result.failed_ids


def test_rule2_fails_on_unregistered_artifact(eager_ref):
    text = make_ticket(artifact="not-a-real-type", context_lines=context_entry(str(eager_ref)))
    result = ra.ticket_lint(text, [])
    assert 2 in result.failed_ids


@pytest.mark.parametrize(
    "status,lease",
    [
        ("leased", "null"),  # leased but no lease set
        ("queued", '{"worker": "w", "at": "2026-01-01T00:00:00-05:00", "ttl_min": 60}'),  # lease set but not leased
        ("not-a-status", "null"),  # bad enum value
    ],
)
def test_rule3_fails_on_status_lease_mismatch(eager_ref, status, lease):
    text = make_ticket(status=status, lease=lease, context_lines=context_entry(str(eager_ref)))
    result = ra.ticket_lint(text, [])
    assert 3 in result.failed_ids


def test_rule4_fails_on_missing_context(tmp_path):
    text = make_ticket(context_lines="")
    result = ra.ticket_lint(text, [])
    assert 4 in result.failed_ids


def test_rule4_fails_on_unregistered_resolver_type(eager_ref):
    text = make_ticket(context_lines=context_entry(str(eager_ref), type_="carrier-pigeon"))
    result = ra.ticket_lint(text, [])
    assert 4 in result.failed_ids


def test_rule4_fails_on_incomplete_entry(tmp_path):
    text = make_ticket(context_lines="  - id: core\n    type: file\n")  # no ref/when
    result = ra.ticket_lint(text, [])
    assert 4 in result.failed_ids


def test_rule5_fails_on_missing_eager_file(tmp_path):
    missing = tmp_path / "does-not-exist.md"
    text = make_ticket(context_lines=context_entry(str(missing)))
    result = ra.ticket_lint(text, [])
    assert 5 in result.failed_ids


def test_rule5_passes_when_not_eager_even_if_missing(tmp_path):
    missing = tmp_path / "does-not-exist.md"
    text = make_ticket(context_lines=context_entry(str(missing), when="only if the build needs it"))
    result = ra.ticket_lint(text, [])
    assert 5 not in result.failed_ids


def test_rule5_skips_url_mcp_qmd_types(tmp_path):
    text = make_ticket(context_lines=context_entry("https://example.org/x", type_="url"))
    result = ra.ticket_lint(text, [])
    assert 5 not in result.failed_ids


def test_rule5_resolves_tilde_paths(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "f.md").write_text("x")
    text = make_ticket(context_lines=context_entry("~/sub/f.md"))
    result = ra.ticket_lint(text, [])
    assert 5 not in result.failed_ids


def test_rule5_cellar_type_resolves_relative_to_cellar_root(tmp_path):
    cellar_root = tmp_path / "cellar"
    (cellar_root / "assessments/acme").mkdir(parents=True)
    (cellar_root / "assessments/acme/note.md").write_text("x")
    text = make_ticket(context_lines=context_entry("assessments/acme/note.md", type_="cellar"))

    missing_root = ra.ticket_lint(text, [], cellar_root=tmp_path / "cellar-wrong")
    assert 5 in missing_root.failed_ids

    with_root = ra.ticket_lint(text, [], cellar_root=cellar_root)
    assert 5 not in with_root.failed_ids


def test_rule6_fails_on_empty_order(eager_ref):
    text = make_ticket(order="", context_lines=context_entry(str(eager_ref)))
    result = ra.ticket_lint(text, [])
    assert 6 in result.failed_ids


def test_rule6_fails_on_empty_order_with_multiple_blank_lines(eager_ref):
    """Regression: `\\s*` in the rule-6/rule-7 heading regexes used to
    cross newlines (since `\\s` matches `\\n`), so several consecutive
    blank lines after `## Order` got silently absorbed into the heading
    match itself and the empty-Order check never fired. Multiple blank
    lines (not just a single one) exercises that greediness."""
    text = make_ticket(order="", context_lines=context_entry(str(eager_ref)))
    text = text.replace("## Order\n\n\n\n## Resolved", "## Order\n\n\n\n\n\n## Resolved")
    result = ra.ticket_lint(text, [])
    assert 6 in result.failed_ids


def test_rule6_passes_with_multi_paragraph_order(eager_ref):
    order = "Paragraph one.\n\nParagraph two, with more detail.\n\nParagraph three."
    text = make_ticket(order=order, context_lines=context_entry(str(eager_ref)))
    result = ra.ticket_lint(text, [])
    assert 6 not in result.failed_ids


def test_heading_regex_tolerates_trailing_whitespace_on_heading_line(eager_ref):
    """`[ \\t]*$` (same-line only) must still match a heading line with
    trailing spaces, without bleeding into the next line."""
    text = make_ticket(context_lines=context_entry(str(eager_ref)))
    text = text.replace("## Order\n", "## Order   \n")
    result = ra.ticket_lint(text, [])
    assert result.passed, result.summary()


def test_rule7_fails_on_missing_section(eager_ref):
    text = make_ticket(
        context_lines=context_entry(str(eager_ref)),
        sections=("## Order", "## Resolved-context snapshot", "## Work log", "## Wrong Heading"),
    )
    result = ra.ticket_lint(text, [])
    assert 7 in result.failed_ids


def test_rule7_fails_on_wrong_order(eager_ref):
    text = make_ticket(
        context_lines=context_entry(str(eager_ref)),
        sections=("## Order", "## Work log", "## Resolved-context snapshot", "## Artifacts"),
    )
    result = ra.ticket_lint(text, [])
    assert 7 in result.failed_ids


def test_rule8_fails_on_inline_content(eager_ref):
    entry = "  - id: core\n    type: file\n    ref: {}\n    when: always\n    content: pasted text here\n".format(eager_ref)
    text = make_ticket(context_lines=entry)
    result = ra.ticket_lint(text, [])
    assert 8 in result.failed_ids


def test_valid_ticket_passes_all_8(valid_ticket_text):
    result = ra.ticket_lint(valid_ticket_text, [])
    assert result.passed, result.summary()
    assert result.failed_ids == []


def test_lint_on_unparseable_frontmatter_fails_all_8():
    result = ra.ticket_lint("no frontmatter here at all", [])
    assert len(result.rules) == 8
    assert not result.passed
    assert result.failed_ids == [1, 2, 3, 4, 5, 6, 7, 8]


# ===========================================================================
# 3. list_tickets
# ===========================================================================


def test_list_tickets_empty_dir_returns_empty(tmp_path):
    assert ra.list_tickets(tmp_path / "rail") == []


def test_list_tickets_and_status_filter(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    rail_dir.mkdir()
    ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    other = make_ticket(ticket_id="other-ticket-2026-01-02", status="escalated", lease="null")
    (rail_dir / "other-ticket-2026-01-02.ticket.md").write_text(other)

    all_tickets = ra.list_tickets(rail_dir)
    assert len(all_tickets) == 2

    queued_only = ra.list_tickets(rail_dir, status="queued")
    assert [p.name for p in queued_only] == ["sample-skill-2026-01-01.ticket.md"]


# ===========================================================================
# 4. enqueue
# ===========================================================================


def test_enqueue_happy_path(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    assert path.exists()
    text = path.read_text()
    assert "steward: enqueued — Gate A: 8/8 pass" in text


def test_enqueue_refuses_gate_a_failure(tmp_path):
    rail_dir = tmp_path / "rail"
    bad_text = make_ticket(order="")  # rule 6 + rule 4 (no context) fail
    with pytest.raises(ra.GateAError) as excinfo:
        ra.enqueue(rail_dir, bad_text, "sample-skill-2026-01-01")
    assert not excinfo.value.result.passed
    # never wrote the file
    assert not (rail_dir / "sample-skill-2026-01-01.ticket.md").exists()


def test_enqueue_rejects_id_mismatch(tmp_path, valid_ticket_text):
    with pytest.raises(ra.RailError):
        ra.enqueue(tmp_path / "rail", valid_ticket_text, "some-other-id")


def test_enqueue_rejects_existing_file(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    with pytest.raises(ra.RailError):
        ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")


# ===========================================================================
# 5. pull — advisory lease
# ===========================================================================


def test_pull_returns_none_when_rail_dry(tmp_path):
    assert ra.pull(tmp_path / "rail", "worker-1") is None


def test_pull_happy_path(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    handle = ra.pull(rail_dir, "worker-1", ttl_min=30, now="2026-01-01T09:00:00-05:00")
    assert handle is not None
    assert handle.id == "sample-skill-2026-01-01"
    assert handle.status == "leased"
    assert "rail: lease — worker=worker-1, ttl_min=30" in handle.text
    lease = ra.get_lease(path.read_text())
    assert lease == {"worker": "worker-1", "at": "2026-01-01T09:00:00-05:00", "ttl_min": 30}


def test_pull_never_returns_needs_context_or_escalated(tmp_path):
    rail_dir = tmp_path / "rail"
    rail_dir.mkdir()
    for status, tid in [("needs-context", "parked-a-2026-01-01"), ("escalated", "parked-b-2026-01-01")]:
        text = make_ticket(ticket_id=tid, status=status, lease="null")
        (rail_dir / f"{tid}.ticket.md").write_text(text)
    assert ra.pull(rail_dir, "worker-1") is None


def test_pull_reclaims_expired_lease(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    first = ra.pull(rail_dir, "worker-1", ttl_min=10, now="2026-01-01T09:00:00-05:00")
    assert first.status == "leased"

    # 20 minutes later — past the 10-minute TTL — a second pull reclaims it.
    second = ra.pull(rail_dir, "worker-2", ttl_min=10, now="2026-01-01T09:20:00-05:00")
    assert second is not None
    assert second.id == "sample-skill-2026-01-01"
    assert "rail: lease-reclaimed — prior lease expired, worker=worker-2" in second.text
    assert "rail: lease — worker=worker-2, ttl_min=10" in second.text
    lease = ra.get_lease(path.read_text())
    assert lease["worker"] == "worker-2"


def test_pull_does_not_reclaim_live_lease(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    ra.pull(rail_dir, "worker-1", ttl_min=60, now="2026-01-01T09:00:00-05:00")
    # Only 5 minutes later, well within the 60-minute TTL.
    still_leased = ra.pull(rail_dir, "worker-2", ttl_min=60, now="2026-01-01T09:05:00-05:00")
    assert still_leased is None


def test_pull_picks_oldest_mtime_queued_first(tmp_path):
    rail_dir = tmp_path / "rail"
    rail_dir.mkdir()
    older = rail_dir / "older-ticket-2026-01-01.ticket.md"
    newer = rail_dir / "newer-ticket-2026-01-02.ticket.md"
    newer.write_text(make_ticket(ticket_id="newer-ticket-2026-01-02"))
    time.sleep(0.01)
    older.write_text(make_ticket(ticket_id="older-ticket-2026-01-01"))
    # force "older" to actually have an earlier mtime than "newer"
    now = time.time()
    os.utime(newer, (now, now))
    os.utime(older, (now - 100, now - 100))

    handle = ra.pull(rail_dir, "worker-1")
    assert handle.id == "older-ticket-2026-01-01"


# ===========================================================================
# 6. append — never corrupts existing lines
# ===========================================================================


def test_append_never_corrupts_existing_lines(tmp_path, valid_ticket_text):
    path = tmp_path / "t.ticket.md"
    path.write_text(valid_ticket_text)

    ra.append(path, "first entry", now="2026-01-01T00:00:00-05:00")
    ra.append(path, "second entry", now="2026-01-01T00:01:00-05:00")
    ra.append(path, "third entry", now="2026-01-01T00:02:00-05:00")

    text = path.read_text()
    assert "- 2026-01-01T00:00:00-05:00 · first entry" in text
    assert "- 2026-01-01T00:01:00-05:00 · second entry" in text
    assert "- 2026-01-01T00:02:00-05:00 · third entry" in text
    # order preserved
    assert text.index("first entry") < text.index("second entry") < text.index("third entry")
    # exactly one blank line between the last work-log bullet and ## Artifacts
    assert "third entry\n\n## Artifacts" in text
    # no accumulating blank lines from repeated appends
    assert "\n\n\n" not in text
    # original body sections untouched
    assert "## Order" in text and "Build a small sample thing end to end." in text


def test_append_when_heading_missing_falls_back_defensively(tmp_path):
    path = tmp_path / "broken.ticket.md"
    path.write_text("---\nticket: x\nartifact: skill\nstatus: queued\nlease: null\ncontext:\n---\nno sections here\n")
    ra.append(path, "an entry", now="2026-01-01T00:00:00-05:00")
    text = path.read_text()
    assert "## Work log" in text
    assert "an entry" in text


# ===========================================================================
# 7. release — round trips
# ===========================================================================


def test_release_round_trips(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    ra.pull(rail_dir, "worker-1", now="2026-01-01T09:00:00-05:00")
    assert ra.get_field(path.read_text(), "status") == "leased"

    ra.release(path, now="2026-01-01T09:05:00-05:00")
    text = path.read_text()
    assert ra.get_field(text, "status") == "queued"
    assert ra.get_lease(text) is None
    assert "rail: release — lease cleared, back to queued" in text

    # and it's workable again
    handle = ra.pull(rail_dir, "worker-2", now="2026-01-01T09:06:00-05:00")
    assert handle is not None
    assert handle.id == "sample-skill-2026-01-01"


# ===========================================================================
# 8. ack — five-exit disposition + file-to-subject on terminal exits only
# ===========================================================================


def test_ack_advance_files_done_to_subject(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    cellar_root = tmp_path / "cellar"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    ra.pull(rail_dir, "worker-1")

    dest = ra.ack(path, "advance", cellar_root, now="2026-01-01T10:00:00-05:00")

    assert not path.exists()
    assert dest == cellar_root / "companies/acme/tickets/sample-skill-2026-01-01.ticket.md"
    text = dest.read_text()
    assert ra.get_field(text, "status") == "done"
    assert ra.get_lease(text) is None
    assert "ack: advance → status done" in text


def test_ack_kill_files_killed_to_subject(tmp_path, valid_ticket_text):
    rail_dir = tmp_path / "rail"
    cellar_root = tmp_path / "cellar"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    ra.pull(rail_dir, "worker-1")

    dest = ra.ack(path, "kill", cellar_root)
    assert not path.exists()
    assert ra.get_field(dest.read_text(), "status") == "killed"


@pytest.mark.parametrize("exit_,expected_status", [("reroute-to-steward", "needs-context"), ("escalate", "escalated")])
def test_ack_non_terminal_exits_stay_on_rail(tmp_path, valid_ticket_text, exit_, expected_status):
    rail_dir = tmp_path / "rail"
    cellar_root = tmp_path / "cellar"
    path = ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")
    ra.pull(rail_dir, "worker-1")

    dest = ra.ack(path, exit_, cellar_root)

    assert dest == path
    assert path.exists()  # never moved off the rail
    assert not cellar_root.exists()  # ack() never touches cellar_root for a non-terminal exit
    text = path.read_text()
    assert ra.get_field(text, "status") == expected_status
    assert ra.get_lease(text) is None


def test_ack_unknown_exit_raises(tmp_path, valid_ticket_text):
    path = tmp_path / "t.ticket.md"
    path.write_text(valid_ticket_text)
    with pytest.raises(ra.RailError):
        ra.ack(path, "not-a-real-exit", tmp_path / "cellar")


def test_ack_advance_without_subject_raises(tmp_path):
    text = make_ticket(context_lines=context_entry("https://example.org", type_="url", when="always — external"))
    path = tmp_path / "t.ticket.md"
    path.write_text(text)
    with pytest.raises(ra.RailError):
        ra.ack(path, "advance", tmp_path / "cellar")


def test_ack_derives_subject_from_first_cellar_source_when_no_explicit_field(tmp_path):
    text = make_ticket(
        context_lines=context_entry("assessments/acme/note.md", type_="cellar"),
        subject=None,
    )
    path = tmp_path / "t.ticket.md"
    path.write_text(text)
    cellar_root = tmp_path / "cellar"
    dest = ra.ack(path, "advance", cellar_root)
    assert dest == cellar_root / "assessments/acme/tickets/t.ticket.md"


# ===========================================================================
# 9. find_unclosed — the close-out sweep's discovery mechanism
# ===========================================================================


def _write_filed_ticket(cellar_root: Path, subject: str, ticket_id: str, status: str, with_close_out: bool) -> Path:
    tickets_dir = cellar_root / subject / "tickets"
    tickets_dir.mkdir(parents=True, exist_ok=True)
    text = make_ticket(ticket_id=ticket_id, status=status, subject=subject)
    if with_close_out:
        text = ra._append_to_section(text, "## Work log", "- close-out: requester notified via imessage (2026-01-02T00:00:00-05:00)")
    path = tickets_dir / f"{ticket_id}.ticket.md"
    path.write_text(text)
    return path


def test_find_unclosed_finds_unsigned_terminal_ticket(tmp_path):
    cellar_root = tmp_path / "cellar"
    unsigned = _write_filed_ticket(cellar_root, "companies/acme", "closed-a-2026-01-01", "done", with_close_out=False)
    found = ra.find_unclosed(cellar_root)
    assert unsigned in found


def test_find_unclosed_ignores_signed_ticket(tmp_path):
    cellar_root = tmp_path / "cellar"
    signed = _write_filed_ticket(cellar_root, "companies/acme", "closed-b-2026-01-01", "killed", with_close_out=True)
    found = ra.find_unclosed(cellar_root)
    assert signed not in found


def test_find_unclosed_ignores_non_terminal_status(tmp_path):
    cellar_root = tmp_path / "cellar"
    parked = _write_filed_ticket(cellar_root, "companies/acme", "parked-2026-01-01", "escalated", with_close_out=False)
    found = ra.find_unclosed(cellar_root)
    assert parked not in found


def test_find_unclosed_respects_since_days_window(tmp_path):
    cellar_root = tmp_path / "cellar"
    old = _write_filed_ticket(cellar_root, "companies/acme", "old-ticket-2020-01-01", "done", with_close_out=False)
    old_time = time.time() - 90 * 86400
    os.utime(old, (old_time, old_time))

    assert old not in ra.find_unclosed(cellar_root, since_days=30)
    assert old in ra.find_unclosed(cellar_root, since_days=120)


def test_find_unclosed_empty_when_cellar_root_missing(tmp_path):
    assert ra.find_unclosed(tmp_path / "no-such-cellar") == []


# ===========================================================================
# 10. stamp — vendoring provenance round trip
# ===========================================================================


def test_stamp_round_trip(tmp_path):
    target = tmp_path / "rail_adapter_copy.py"
    target.write_text("# a vendored copy\nprint('hi')\n")

    stamp_path = ra.stamp(target, version="1.2.3", stamped_at="2026-01-01T00:00:00-05:00")

    assert stamp_path == target.with_name(target.name + ".stamp.json")
    data = json.loads(stamp_path.read_text())
    assert data["file"] == "rail_adapter_copy.py"
    assert data["canon"] == "skill-agent-brigade/adapter/rail_adapter.py"
    assert data["version"] == "1.2.3"
    assert data["stamped_at"] == "2026-01-01T00:00:00-05:00"

    import hashlib

    assert data["sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()

    # drift detection: change the file, stamp goes stale
    target.write_text("# a vendored copy, MODIFIED\nprint('hi')\n")
    assert hashlib.sha256(target.read_bytes()).hexdigest() != data["sha256"]


def test_stamp_defaults_to_adapter_version(tmp_path):
    target = tmp_path / "x.py"
    target.write_text("x = 1\n")
    stamp_path = ra.stamp(target)
    data = json.loads(stamp_path.read_text())
    assert data["version"] == ra.ADAPTER_VERSION


# ===========================================================================
# 11. frontmatter helpers — get_field/set_field preserve unknown fields
# ===========================================================================


def test_set_field_preserves_unknown_fields(valid_ticket_text):
    updated = ra.set_field(valid_ticket_text, "status", "leased")
    assert ra.get_field(updated, "status") == "leased"
    # every other top-level field byte-for-byte preserved
    assert ra.get_field(updated, "artifact") == ra.get_field(valid_ticket_text, "artifact")
    assert ra.get_field(updated, "requested_by") == "tester"
    assert ra.get_field(updated, "ticket") == "sample-skill-2026-01-01"


def test_set_field_inserts_when_absent():
    text = "---\nticket: x\nartifact: skill\nstatus: queued\nlease: null\ncontext:\n---\nbody\n"
    updated = ra.set_field(text, "subject", "companies/acme")
    assert ra.get_field(updated, "subject") == "companies/acme"


def test_get_lease_handles_null_and_json():
    assert ra.get_lease("---\nlease: null\n---\n") is None
    assert ra.get_lease("---\nlease: ~\n---\n") is None
    text = '---\nlease: {"worker": "w", "at": "t", "ttl_min": 5}\n---\n'
    assert ra.get_lease(text) == {"worker": "w", "at": "t", "ttl_min": 5}


def test_get_lease_malformed_treated_as_absent():
    assert ra.get_lease("---\nlease: { not: json\n---\n") is None


# ===========================================================================
# 12. CLI smoke test — internal script, still needs to run without crashing.
# ===========================================================================


def test_cli_list_and_lint(tmp_path, valid_ticket_text, capsys):
    rail_dir = tmp_path / "rail"
    ra.enqueue(rail_dir, valid_ticket_text, "sample-skill-2026-01-01")

    exit_code = ra._cli(["list", str(rail_dir)])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "sample-skill-2026-01-01.ticket.md" in out

    ticket_path = rail_dir / "sample-skill-2026-01-01.ticket.md"
    exit_code = ra._cli(["lint", str(ticket_path)])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Gate A: 8/8 pass" in out


def test_cli_enqueue_failure_exits_nonzero(tmp_path, capsys):
    bad = tmp_path / "bad.ticket.md"
    bad.write_text(make_ticket(order=""))
    exit_code = ra._cli(["enqueue", str(tmp_path / "rail"), str(bad), "sample-skill-2026-01-01"])
    assert exit_code == 1
