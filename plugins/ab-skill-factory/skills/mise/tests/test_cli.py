"""CLI-level tests: exit-code semantics, --json shape, and the negative
controls the build task calls out explicitly:
  - nonexistent path FAILs with the declared remedy in the output
  - unwritable dir -> FAIL
  - missing command -> FAIL or WARN, per declared severity
  - bad TOML -> exit 2
  - vendor_stamp with no stamp file -> N/A, not FAIL (and does not flip exit
    code to 1 even though the check's own severity is FAIL)

Everything runs against tmp_path declarations — never the real cellar/rail.
One true subprocess test exercises the actual `python3 mise.py` entry point
end to end (shebang, argv parsing, process exit code) rather than only the
in-process main().
"""

from __future__ import annotations

import json
import stat
import subprocess
import sys


def write_decl(path, body):
    path.write_text(body)
    return path


# --- exit code semantics ------------------------------------------------------


def test_exit_code_0_when_all_pass(mise, tmp_path, capsys):
    target = tmp_path / "there"
    target.mkdir()
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "ok"
description = "d"
executor = "script"
type = "path_exists"
target = "{target}"
remedy = "r"
severity = "FAIL"
""",
    )
    code = mise.main([str(decl)])
    assert code == 0


def test_exit_code_1_when_any_fail(mise, tmp_path):
    missing = tmp_path / "missing"
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "broken"
description = "d"
executor = "script"
type = "path_exists"
target = "{missing}"
remedy = "r"
severity = "FAIL"
""",
    )
    code = mise.main([str(decl)])
    assert code == 1


def test_exit_code_2_on_engine_error(mise, tmp_path):
    decl = tmp_path / "mise.toml"
    decl.write_text("this [ is === not valid toml")
    code = mise.main([str(decl)])
    assert code == 2


def test_exit_code_2_on_missing_declaration_file(mise, tmp_path):
    code = mise.main([str(tmp_path / "does-not-exist.toml")])
    assert code == 2


def test_warn_does_not_flip_exit_code(mise, tmp_path):
    missing = tmp_path / "missing"
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "warny"
description = "d"
executor = "script"
type = "path_exists"
target = "{missing}"
remedy = "r"
severity = "WARN"
""",
    )
    code = mise.main([str(decl)])
    assert code == 0


# --- negative controls ---------------------------------------------------------


def test_negative_control_nonexistent_path_fails_with_remedy_in_output(mise, tmp_path, capsys):
    missing = tmp_path / "nowhere"
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "rail-root-exists"
description = "rail root exists"
executor = "script"
type = "path_exists"
target = "{missing}"
remedy = "mkdir -p {missing}"
severity = "FAIL"
""",
    )
    code = mise.main([str(decl)])
    out = capsys.readouterr().out
    assert code == 1
    assert "FAIL" in out
    assert f"mkdir -p {missing}" in out


def test_negative_control_unwritable_dir_fails(mise, tmp_path, capsys):
    locked = tmp_path / "locked"
    locked.mkdir()
    locked.chmod(stat.S_IREAD | stat.S_IEXEC)
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "rail-root-writable"
description = "rail root writable"
executor = "script"
type = "path_writable"
target = "{locked}"
remedy = "chmod u+w {locked}"
severity = "FAIL"
""",
    )
    try:
        code = mise.main([str(decl)])
        out = capsys.readouterr().out
        assert code == 1
        assert "FAIL" in out
        assert f"chmod u+w {locked}" in out
    finally:
        locked.chmod(stat.S_IRWXU)


def test_negative_control_missing_command_fail_severity(mise, tmp_path, capsys):
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        """
[[checks]]
id = "some-cli"
description = "d"
executor = "script"
type = "command_on_path"
target = "definitely-not-a-real-command-xyz123"
remedy = "install the thing"
severity = "FAIL"
""",
    )
    code = mise.main([str(decl)])
    out = capsys.readouterr().out
    assert code == 1
    assert "FAIL" in out
    assert "install the thing" in out


def test_negative_control_missing_command_warn_severity(mise, tmp_path, capsys):
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        """
[[checks]]
id = "some-cli"
description = "d"
executor = "script"
type = "command_on_path"
target = "definitely-not-a-real-command-xyz123"
remedy = "install the thing"
severity = "WARN"
""",
    )
    code = mise.main([str(decl)])
    out = capsys.readouterr().out
    assert code == 0  # WARN doesn't fail the run
    assert "WARN" in out
    assert "install the thing" in out


def test_negative_control_bad_toml_exit_code_2(mise, tmp_path, capsys):
    decl = tmp_path / "mise.toml"
    decl.write_text("[[checks]\nid = oops")
    code = mise.main([str(decl)])
    err = capsys.readouterr().err
    assert code == 2
    assert "engine error" in err


def test_negative_control_vendor_stamp_no_stamp_is_na_not_fail(mise, tmp_path, capsys):
    vendored = tmp_path / "rail_adapter.py"
    vendored.write_text("print('vendored')\n")
    stamp = tmp_path / "rail_adapter.py.stamp.json"  # deliberately never created
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "adapter-stamp"
description = "vendor stamp check"
executor = "script"
type = "vendor_stamp"
target = "{vendored}"
stamp_target = "{stamp}"
remedy = "re-stamp via iterate-brigade"
severity = "FAIL"
""",
    )
    code = mise.main([str(decl), "--json"])
    out = capsys.readouterr().out
    payload = json.loads(out)
    # severity is FAIL, but "no stamp yet" must report N/A and must NOT
    # flip the run to a failing exit code.
    assert code == 0
    assert payload["exit_code"] == 0
    assert payload["checks"][0]["status"] == "N/A"
    assert payload["checks"][0]["detail"] == "N/A (no stamp yet)"
    assert payload["summary"]["fail"] == 0
    assert payload["summary"]["na"] == 1


# --- --json shape ---------------------------------------------------------


def test_json_output_shape(mise, tmp_path, capsys):
    ok_dir = tmp_path / "ok"
    ok_dir.mkdir()
    missing = tmp_path / "missing"
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        f"""
[[checks]]
id = "ok-check"
description = "d"
executor = "script"
type = "path_exists"
target = "{ok_dir}"
remedy = "r"
severity = "FAIL"

[[checks]]
id = "fail-check"
description = "d"
executor = "script"
type = "path_exists"
target = "{missing}"
remedy = "r2"
severity = "FAIL"

[[checks]]
id = "agent-check"
description = "d"
executor = "agent"
type = "whatever"
target = "t"
remedy = "r3"
severity = "FAIL"
""",
    )
    code = mise.main([str(decl), "--json"])
    out = capsys.readouterr().out
    payload = json.loads(out)

    assert code == 1
    assert payload["exit_code"] == 1
    assert payload["declaration"] == str(decl)
    assert isinstance(payload["checks"], list) and len(payload["checks"]) == 3
    ids = {c["id"] for c in payload["checks"]}
    assert ids == {"ok-check", "fail-check", "agent-check"}
    assert payload["summary"] == {
        "pass": 1,
        "warn": 0,
        "fail": 1,
        "na": 0,
        "unchecked_agent": 1,
    }
    for c in payload["checks"]:
        assert set(c) >= {
            "id",
            "description",
            "executor",
            "type",
            "target",
            "severity",
            "mode",
            "remedy",
            "status",
            "detail",
        }


def test_live_flag_lists_live_mode_checks(mise, tmp_path, capsys):
    decl = tmp_path / "mise.toml"
    write_decl(
        decl,
        """
[[checks]]
id = "model-access"
description = "model tier responds"
executor = "agent"
type = "model_call"
target = "sonnet"
remedy = "check API key / quota"
severity = "WARN"
mode = "live"
""",
    )
    code = mise.main([str(decl), "--live"])
    out = capsys.readouterr().out
    assert code == 0
    assert "model-access" in out
    assert "checks the calling agent should run itself" in out


# --- real subprocess entry point ---------------------------------------------


def test_subprocess_entry_point_help():
    proc = subprocess.run(
        [sys.executable, str(_mise_py_path()), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert proc.returncode == 0
    assert "mise" in proc.stdout.lower()


def test_subprocess_entry_point_runs_against_tmp_declaration(tmp_path):
    target = tmp_path / "there"
    target.mkdir()
    decl = tmp_path / "mise.toml"
    decl.write_text(
        f"""
[[checks]]
id = "ok"
description = "d"
executor = "script"
type = "path_exists"
target = "{target}"
remedy = "r"
severity = "FAIL"
"""
    )
    proc = subprocess.run(
        [sys.executable, str(_mise_py_path()), str(decl), "--json"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["summary"]["pass"] == 1


def _mise_py_path():
    from pathlib import Path

    return Path(__file__).resolve().parent.parent / "mise.py"
