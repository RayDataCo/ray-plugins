"""Tests for load_declaration() schema validation and resolve_roots() /
resolve_path_target() path templating. All against tmp_path — never the
real cellar/rail.
"""

from __future__ import annotations

import pytest


MINIMAL_OK_CHECK = """
[[checks]]
id = "c1"
description = "d1"
executor = "script"
type = "path_exists"
target = "somewhere"
remedy = "r1"
severity = "FAIL"
"""


def test_load_declaration_missing_file_raises(mise, tmp_path):
    with pytest.raises(mise.MiseEngineError, match="not found"):
        mise.load_declaration(tmp_path / "nope.toml")


def test_load_declaration_bad_toml_raises(mise, tmp_path):
    path = tmp_path / "bad.toml"
    path.write_text("this [ is not === valid toml")
    with pytest.raises(mise.MiseEngineError, match="not valid TOML"):
        mise.load_declaration(path)


def test_load_declaration_no_checks_raises(mise, tmp_path):
    path = tmp_path / "empty.toml"
    path.write_text('[roots]\nrail = "/tmp/x"\n')
    with pytest.raises(mise.MiseEngineError, match="no \\[\\[checks\\]\\]"):
        mise.load_declaration(path)


def test_load_declaration_missing_required_field_raises(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(
        """
[[checks]]
id = "c1"
description = "d1"
executor = "script"
type = "path_exists"
target = "somewhere"
severity = "FAIL"
"""
    )  # missing 'remedy'
    with pytest.raises(mise.MiseEngineError, match="missing required field"):
        mise.load_declaration(path)


def test_load_declaration_bad_executor_raises(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(
        """
[[checks]]
id = "c1"
description = "d1"
executor = "sorcery"
type = "path_exists"
target = "somewhere"
remedy = "r1"
severity = "FAIL"
"""
    )
    with pytest.raises(mise.MiseEngineError, match="invalid executor"):
        mise.load_declaration(path)


def test_load_declaration_bad_severity_raises(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(
        """
[[checks]]
id = "c1"
description = "d1"
executor = "script"
type = "path_exists"
target = "somewhere"
remedy = "r1"
severity = "MEH"
"""
    )
    with pytest.raises(mise.MiseEngineError, match="invalid severity"):
        mise.load_declaration(path)


def test_load_declaration_unknown_script_type_raises(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(
        """
[[checks]]
id = "c1"
description = "d1"
executor = "script"
type = "reads_tea_leaves"
target = "somewhere"
remedy = "r1"
severity = "FAIL"
"""
    )
    with pytest.raises(mise.MiseEngineError, match="unknown script check type"):
        mise.load_declaration(path)


def test_load_declaration_vendor_stamp_requires_stamp_target(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(
        """
[[checks]]
id = "c1"
description = "d1"
executor = "script"
type = "vendor_stamp"
target = "somewhere"
remedy = "r1"
severity = "WARN"
"""
    )
    with pytest.raises(mise.MiseEngineError, match="stamp_target"):
        mise.load_declaration(path)


def test_load_declaration_duplicate_id_raises(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(MINIMAL_OK_CHECK + MINIMAL_OK_CHECK)
    with pytest.raises(mise.MiseEngineError, match="duplicate check id"):
        mise.load_declaration(path)


def test_load_declaration_ok_returns_dict(mise, tmp_path):
    path = tmp_path / "decl.toml"
    path.write_text(MINIMAL_OK_CHECK)
    decl = mise.load_declaration(path)
    assert decl["checks"][0]["id"] == "c1"


# --- roots / path templating -------------------------------------------------


def test_resolve_roots_expands_tilde_and_absolute(mise, tmp_path, monkeypatch):
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    resolved = mise.resolve_roots({"rail": "~/somewhere"}, tmp_path)
    assert resolved["rail"] == str(fake_home / "somewhere")


def test_resolve_roots_resolves_relative_to_toml_dir(mise, tmp_path):
    resolved = mise.resolve_roots({"cellar": "relative-cellar"}, tmp_path)
    assert resolved["cellar"] == str((tmp_path / "relative-cellar").resolve())


def test_resolve_path_target_substitutes_placeholder(mise, tmp_path):
    roots = {"rail": str(tmp_path / "rail-root")}
    resolved = mise.resolve_path_target("{rail}/tickets", roots, tmp_path)
    assert resolved == (tmp_path / "rail-root" / "tickets")


def test_resolve_path_target_relative_to_toml_dir_when_no_placeholder(mise, tmp_path):
    toml_dir = tmp_path / "brigade" / "skills" / "mise"
    toml_dir.mkdir(parents=True)
    resolved = mise.resolve_path_target("../service/rail-walk.run.js", {}, toml_dir)
    assert resolved == (toml_dir / "../service/rail-walk.run.js").resolve()
    assert resolved == (tmp_path / "brigade" / "skills" / "service" / "rail-walk.run.js")


def test_resolve_name_target_leaves_bare_command_alone(mise):
    assert mise.resolve_name_target("node", {"rail": "/whatever"}) == "node"


def test_menu_freshness_requires_published_target(mise, tmp_path):
    toml = tmp_path / "mise.toml"
    toml.write_text(
        '[[checks]]\nid = "m"\ndescription = "d"\nexecutor = "script"\n'
        'type = "menu_freshness"\ntarget = "MENU.md"\nremedy = "r"\nseverity = "WARN"\n'
    )
    import pytest as _pytest

    with _pytest.raises(mise.MiseEngineError, match="published_target"):
        mise.load_declaration(toml)
