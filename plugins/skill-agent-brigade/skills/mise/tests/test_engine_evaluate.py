"""Tests for evaluate()/classify_status(): severity mapping, agent-executor
handling, and end-to-end evaluation of a small synthetic declaration. All
against tmp_path fixtures.
"""

from __future__ import annotations


def _check(**overrides):
    base = {
        "id": "c",
        "description": "d",
        "executor": "script",
        "type": "path_exists",
        "target": "x",
        "remedy": "r",
        "severity": "FAIL",
    }
    base.update(overrides)
    return base


def test_classify_status_ok_is_pass(mise):
    assert mise.classify_status(_check(), "ok") == "PASS"


def test_classify_status_na_is_na_regardless_of_severity(mise):
    assert mise.classify_status(_check(severity="FAIL"), "na") == "N/A"
    assert mise.classify_status(_check(severity="WARN"), "na") == "N/A"


def test_classify_status_agent_is_unchecked(mise):
    assert mise.classify_status(_check(executor="agent"), "agent") == "UNCHECKED (agent)"


def test_classify_status_broken_maps_to_declared_severity_fail(mise):
    assert mise.classify_status(_check(severity="FAIL"), "broken") == "FAIL"


def test_classify_status_broken_maps_to_declared_severity_warn(mise):
    assert mise.classify_status(_check(severity="WARN"), "broken") == "WARN"


def test_evaluate_mixed_declaration(mise, tmp_path):
    good_dir = tmp_path / "good"
    good_dir.mkdir()
    decl = {
        "roots": {},
        "checks": [
            _check(id="exists-ok", type="path_exists", target=str(good_dir), severity="FAIL"),
            _check(
                id="exists-fail",
                type="path_exists",
                target=str(tmp_path / "missing"),
                severity="FAIL",
            ),
            _check(
                id="exists-warn",
                type="path_exists",
                target=str(tmp_path / "also-missing"),
                severity="WARN",
            ),
            _check(id="agent-check", executor="agent", type="whatever", target="t", severity="FAIL"),
        ],
    }
    results = mise.evaluate(decl, tmp_path)
    by_id = {r["id"]: r["status"] for r in results}
    assert by_id == {
        "exists-ok": "PASS",
        "exists-fail": "FAIL",
        "exists-warn": "WARN",
        "agent-check": "UNCHECKED (agent)",
    }


def test_evaluate_carries_remedy_and_detail_through(mise, tmp_path):
    decl = {
        "roots": {},
        "checks": [
            _check(
                id="c1",
                type="path_exists",
                target=str(tmp_path / "missing"),
                remedy="do the thing",
                severity="FAIL",
            )
        ],
    }
    results = mise.evaluate(decl, tmp_path)
    assert results[0]["remedy"] == "do the thing"
    assert "does not exist" in results[0]["detail"]


def test_evaluate_defaults_mode_to_static(mise, tmp_path):
    decl = {"roots": {}, "checks": [_check(id="c1", target=str(tmp_path))]}
    results = mise.evaluate(decl, tmp_path)
    assert results[0]["mode"] == "static"


def test_evaluate_roots_placeholder_used_by_checks(mise, tmp_path):
    root_dir = tmp_path / "cellar"
    root_dir.mkdir()
    decl = {
        "roots": {"cellar": str(root_dir)},
        "checks": [_check(id="c1", type="path_exists", target="{cellar}/menu.md", severity="FAIL")],
    }
    (root_dir / "menu.md").write_text("hi")
    results = mise.evaluate(decl, tmp_path)
    assert results[0]["status"] == "PASS"
