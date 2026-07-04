"""Unit tests for each check-type implementation: PASS path + negative
controls, called directly against the check_* functions (not through the
CLI). All filesystem activity is confined to pytest's tmp_path.
"""

from __future__ import annotations

import json
import shutil
import stat

import pytest


NODE_AVAILABLE = shutil.which("node") is not None


# --- path_exists ------------------------------------------------------------


def test_path_exists_pass(mise, tmp_path):
    target = tmp_path / "here"
    target.mkdir()
    state, detail = mise.check_path_exists(target)
    assert state == "ok"
    assert "exists" in detail


def test_path_exists_fail_nonexistent(mise, tmp_path):
    target = tmp_path / "does-not-exist"
    state, detail = mise.check_path_exists(target)
    assert state == "broken"
    assert "does not exist" in detail


# --- path_writable -----------------------------------------------------------


def test_path_writable_pass(mise, tmp_path):
    target = tmp_path / "writable-dir"
    target.mkdir()
    state, detail = mise.check_path_writable(target)
    assert state == "ok"
    # the probe file must not survive the check
    assert list(target.iterdir()) == []


def test_path_writable_fail_nonexistent_dir(mise, tmp_path):
    target = tmp_path / "nope"
    state, detail = mise.check_path_writable(target)
    assert state == "broken"
    assert "does not exist" in detail


def test_path_writable_fail_unwritable_dir(mise, tmp_path):
    target = tmp_path / "locked-dir"
    target.mkdir()
    target.chmod(stat.S_IREAD | stat.S_IEXEC)
    try:
        state, detail = mise.check_path_writable(target)
        assert state == "broken"
        assert "not writable" in detail
    finally:
        # restore so pytest's tmp_path cleanup can remove it
        target.chmod(stat.S_IRWXU)


# --- command_on_path ---------------------------------------------------------


def test_command_on_path_pass(mise):
    state, detail = mise.check_command_on_path("ls")
    assert state == "ok"
    assert "found on PATH" in detail


def test_command_on_path_fail_missing_command(mise):
    state, detail = mise.check_command_on_path("definitely-not-a-real-command-xyz123")
    assert state == "broken"
    assert "not found on PATH" in detail


# --- file_parses_json ---------------------------------------------------------


def test_file_parses_json_pass(mise, tmp_path):
    target = tmp_path / "good.json"
    target.write_text('{"a": 1}')
    state, detail = mise.check_file_parses_json(target)
    assert state == "ok"


def test_file_parses_json_fail_bad_json(mise, tmp_path):
    target = tmp_path / "bad.json"
    target.write_text("{not json")
    state, detail = mise.check_file_parses_json(target)
    assert state == "broken"
    assert "invalid JSON" in detail


def test_file_parses_json_fail_missing_file(mise, tmp_path):
    target = tmp_path / "missing.json"
    state, detail = mise.check_file_parses_json(target)
    assert state == "broken"
    assert "does not exist" in detail


# --- file_parses_toml ---------------------------------------------------------


def test_file_parses_toml_pass(mise, tmp_path):
    target = tmp_path / "good.toml"
    target.write_text('a = 1\n[b]\nc = "d"\n')
    state, detail = mise.check_file_parses_toml(target)
    assert state == "ok"


def test_file_parses_toml_fail_bad_toml(mise, tmp_path):
    target = tmp_path / "bad.toml"
    target.write_text("this is not [ valid toml ===")
    state, detail = mise.check_file_parses_toml(target)
    assert state == "broken"
    assert "invalid TOML" in detail


# --- node_syntax ---------------------------------------------------------


@pytest.mark.skipif(not NODE_AVAILABLE, reason="node not on PATH in this environment")
def test_node_syntax_pass(mise, tmp_path):
    target = tmp_path / "good.js"
    target.write_text("const x = 1;\nconsole.log(x);\n")
    state, detail = mise.check_node_syntax(target)
    assert state == "ok"


@pytest.mark.skipif(not NODE_AVAILABLE, reason="node not on PATH in this environment")
def test_node_syntax_fail_bad_syntax(mise, tmp_path):
    target = tmp_path / "bad.js"
    target.write_text("const x = ;;; this is not valid js (((\n")
    state, detail = mise.check_node_syntax(target)
    assert state == "broken"
    assert "syntax error" in detail


def test_node_syntax_fail_missing_target(mise, tmp_path):
    target = tmp_path / "missing.js"
    state, detail = mise.check_node_syntax(target)
    assert state == "broken"
    if NODE_AVAILABLE:
        assert "does not exist" in detail
    else:
        assert "node not on PATH" in detail


def test_node_syntax_node_absent_is_broken_not_ok(mise, tmp_path, monkeypatch):
    """Simulate node being absent regardless of the real environment, by
    making shutil.which return None for this call."""
    target = tmp_path / "whatever.js"
    target.write_text("const x = 1;\n")
    monkeypatch.setattr(mise.shutil, "which", lambda _cmd: None)
    state, detail = mise.check_node_syntax(target)
    assert state == "broken"
    assert "node not on PATH" in detail


# --- python_module ---------------------------------------------------------


def test_python_module_pass_stdlib(mise):
    state, detail = mise.check_python_module("json")
    assert state == "ok"


def test_python_module_fail_missing(mise):
    state, detail = mise.check_python_module("definitely_not_a_real_module_xyz123")
    assert state == "broken"


# --- vendor_stamp ---------------------------------------------------------


def test_vendor_stamp_na_when_no_stamp_file(mise, tmp_path):
    target = tmp_path / "vendored.py"
    target.write_text("print('hi')\n")
    stamp = tmp_path / "vendored.py.stamp.json"  # deliberately absent
    state, detail = mise.check_vendor_stamp(target, stamp)
    assert state == "na"
    assert detail == "N/A (no stamp yet)"


def test_vendor_stamp_pass_when_hash_matches(mise, tmp_path):
    target = tmp_path / "vendored.py"
    target.write_text("print('hi')\n")
    import hashlib

    actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    stamp = tmp_path / "vendored.py.stamp.json"
    stamp.write_text(json.dumps({"sha256": actual_hash, "canon_version": "1.0.0"}))
    state, detail = mise.check_vendor_stamp(target, stamp)
    assert state == "ok"


def test_vendor_stamp_fail_when_hash_mismatches(mise, tmp_path):
    target = tmp_path / "vendored.py"
    target.write_text("print('hi')\n")
    stamp = tmp_path / "vendored.py.stamp.json"
    stamp.write_text(json.dumps({"sha256": "0" * 64, "canon_version": "1.0.0"}))
    state, detail = mise.check_vendor_stamp(target, stamp)
    assert state == "broken"
    assert "drifted from canon" in detail


def test_vendor_stamp_fail_when_target_missing_but_stamp_present(mise, tmp_path):
    target = tmp_path / "vendored.py"  # never created
    stamp = tmp_path / "vendored.py.stamp.json"
    stamp.write_text(json.dumps({"sha256": "0" * 64}))
    state, detail = mise.check_vendor_stamp(target, stamp)
    assert state == "broken"
    assert "does not exist" in detail


# --- menu_freshness -----------------------------------------------------------


def _published(tmp_path, source_hash=None, body="# Menu\n"):
    fm = "---\nmenu_of: x\nversion: 5\n"
    if source_hash is not None:
        fm += f"source_hash: {source_hash}\n"
    fm += "---\n"
    p = tmp_path / "menu-published.md"
    p.write_text(fm + body)
    return p


def test_menu_freshness_pass_when_stamp_matches(mise, tmp_path):
    import hashlib

    packaged = tmp_path / "MENU.md"
    packaged.write_text("# canonical menu v-current\n")
    stamp = hashlib.sha256(packaged.read_bytes()).hexdigest()
    published = _published(tmp_path, source_hash=stamp)
    state, detail = mise.check_menu_freshness(packaged, published)
    assert state == "ok"
    assert "fresh" in detail


def test_menu_freshness_fail_when_source_changed(mise, tmp_path):
    import hashlib

    packaged = tmp_path / "MENU.md"
    packaged.write_text("# canonical menu OLD\n")
    stale_stamp = hashlib.sha256(packaged.read_bytes()).hexdigest()
    published = _published(tmp_path, source_hash=stale_stamp)
    packaged.write_text("# canonical menu NEW — capability changed\n")
    state, detail = mise.check_menu_freshness(packaged, published)
    assert state == "broken"
    assert "changed since last publish" in detail


def test_menu_freshness_fail_when_published_missing(mise, tmp_path):
    packaged = tmp_path / "MENU.md"
    packaged.write_text("# canonical\n")
    state, detail = mise.check_menu_freshness(packaged, tmp_path / "nope.md")
    assert state == "broken"
    assert "not published" in detail


def test_menu_freshness_fail_when_no_stamp(mise, tmp_path):
    packaged = tmp_path / "MENU.md"
    packaged.write_text("# canonical\n")
    published = _published(tmp_path, source_hash=None)
    state, detail = mise.check_menu_freshness(packaged, published)
    assert state == "broken"
    assert "no source_hash stamp" in detail


def test_menu_freshness_fail_when_packaged_missing(mise, tmp_path):
    published = _published(tmp_path, source_hash="0" * 64)
    state, detail = mise.check_menu_freshness(tmp_path / "gone.md", published)
    assert state == "broken"
    assert "packaged" in detail
