#!/usr/bin/env python3
"""mise — the skill-agent-brigade readiness-check engine.

"mise en place — everything in its place before service." Reads a brigade's
mise.toml declaration (the single source of truth, Decision D1 —
BRIGADE-INTERFACE.md), runs the `executor = "script"` checks locally, and
lists `executor = "agent"` checks as UNCHECKED (agent) for the calling agent
to verify and merge into one report.

STDLIB ONLY. Zero pip dependencies, by design: this file is meant to be
vendored into every brigade this factory builds (the same "vendored from
canon, version+hash stamped" move as rail_adapter.py — see
BRIGADE-INTERFACE.md "Adapter distribution"), and it must run on a bare
python3 with nothing installed. That constraint is also why the declaration
file is TOML, not YAML: YAML has no stdlib parser; TOML does (`tomllib`,
python 3.11+). See IMPLEMENTATION-NOTES-2026-07-03-mise-build.md for the full
yaml -> toml deviation writeup.

Usage:
    python3 mise.py [DECLARATION] [--live] [--json]

    DECLARATION   path to a mise.toml file (default: mise.toml next to this
                  script — i.e. running `python3 mise.py` from inside a
                  brigade's skills/mise/ dir checks that brigade)
    --live        additionally print which declared checks are live/paid
                  probes (mode = "live") that the calling agent should run
                  itself. mise.py never performs live probes (model calls,
                  MCP round-trips) — those are always executor="agent"
                  entries; static script checks still run as normal.
    --json        machine-readable report instead of the human table.

Exit codes: 0 = no FAIL, 1 = at least one FAIL, 2 = engine error (bad
declaration, unreadable file, malformed TOML, unknown check type, ...).

Check types implemented (executor = "script"):
    path_exists      — target path exists (file or dir).
    path_writable     — target dir accepts a create+delete probe temp file.
    command_on_path   — target is resolvable via the PATH (shutil.which).
    file_parses_json  — target file's contents parse as JSON.
    file_parses_toml  — target file's contents parse as TOML (tomllib).
    node_syntax       — `node --check <target>` exits 0. If node itself is
                        not on PATH, the check cannot run; it is reported
                        "broken" and mapped through the check's declared
                        severity same as any other broken check (this is
                        the "skip with WARN if node absent AND severity
                        says so" behavior from the implementation plan: the
                        declared severity is the thing that "says so").
    python_module     — target module name resolves via
                        importlib.util.find_spec() in the current
                        interpreter.
    vendor_stamp      — compares a stamp file's recorded sha256 (of
                        `target`) to the actual file hash. If the stamp
                        file (`stamp_target`) doesn't exist yet, this is
                        reported as N/A ("no stamp yet"), never FAIL —
                        vendored-from-canon stamps don't exist until a
                        brigade has been through the retrofit pass.

`executor = "agent"` entries are never executed here — mise.py always
reports them as UNCHECKED (agent). Only the checking agent (running the
mise SKILL.md procedure) can verify Workflow-tool callability, MCP
connectivity, skill resolution, or model access.

Out of scope, deliberately (per IMPLEMENTATION-PLAN.md "Out of scope"):
auto-fixing failures, live-probing external services a station merely
might call. mise reports and recommends; it never mutates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from typing import Any

# Seed for the future self-referential vendor stamp: once mise.py itself
# starts getting vendored into domain brigades (build sequence step 4 in
# IMPLEMENTATION-PLAN.md), this is the version a stamp file records against.
MISE_ENGINE_VERSION = "1.0.0"

SCRIPT_CHECK_TYPES = {
    "path_exists",
    "path_writable",
    "command_on_path",
    "file_parses_json",
    "file_parses_toml",
    "node_syntax",
    "python_module",
    "vendor_stamp",
}

# Check types whose `target` (and, for vendor_stamp, `stamp_target`) is a
# filesystem path that should be resolved against [roots] placeholders and,
# if still relative, against the mise.toml's own directory. command_on_path
# and python_module targets are names, not paths, and are left untouched
# apart from root-placeholder substitution.
PATH_LIKE_TYPES = {
    "path_exists",
    "path_writable",
    "file_parses_json",
    "file_parses_toml",
    "node_syntax",
    "vendor_stamp",
}

REQUIRED_CHECK_FIELDS = ("id", "description", "executor", "type", "target", "remedy", "severity")
VALID_EXECUTORS = {"script", "agent"}
VALID_SEVERITIES = {"FAIL", "WARN"}
VALID_MODES = {"static", "live"}


class MiseEngineError(Exception):
    """Raised for anything that makes the run itself untrustworthy —
    malformed declaration, unreadable files, unknown check types. Always
    maps to exit code 2."""


# --------------------------------------------------------------------------
# Declaration loading + validation
# --------------------------------------------------------------------------


def load_declaration(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise MiseEngineError(f"declaration file not found: {path}")
    try:
        with path.open("rb") as f:
            decl = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise MiseEngineError(f"declaration is not valid TOML ({path}): {e}") from e
    except OSError as e:
        raise MiseEngineError(f"could not read declaration ({path}): {e}") from e

    checks = decl.get("checks")
    if not isinstance(checks, list) or not checks:
        raise MiseEngineError(f"declaration has no [[checks]] entries: {path}")

    seen_ids: set[str] = set()
    for i, check in enumerate(checks):
        missing = [f for f in REQUIRED_CHECK_FIELDS if f not in check]
        if missing:
            raise MiseEngineError(
                f"check #{i} is missing required field(s) {missing}: {check!r}"
            )
        if check["executor"] not in VALID_EXECUTORS:
            raise MiseEngineError(
                f"check '{check['id']}' has invalid executor '{check['executor']}' "
                f"(must be one of {sorted(VALID_EXECUTORS)})"
            )
        if check["severity"] not in VALID_SEVERITIES:
            raise MiseEngineError(
                f"check '{check['id']}' has invalid severity '{check['severity']}' "
                f"(must be one of {sorted(VALID_SEVERITIES)})"
            )
        if check["executor"] == "script" and check["type"] not in SCRIPT_CHECK_TYPES:
            raise MiseEngineError(
                f"check '{check['id']}' declares unknown script check type "
                f"'{check['type']}' (must be one of {sorted(SCRIPT_CHECK_TYPES)})"
            )
        mode = check.get("mode", "static")
        if mode not in VALID_MODES:
            raise MiseEngineError(
                f"check '{check['id']}' has invalid mode '{mode}' "
                f"(must be one of {sorted(VALID_MODES)})"
            )
        if check["type"] == "vendor_stamp" and "stamp_target" not in check:
            raise MiseEngineError(
                f"check '{check['id']}' is type vendor_stamp but has no 'stamp_target' field"
            )
        if check["id"] in seen_ids:
            raise MiseEngineError(f"duplicate check id '{check['id']}'")
        seen_ids.add(check["id"])

    return decl


# --------------------------------------------------------------------------
# Path resolution — [roots] placeholders + relative-to-declaration-dir
# --------------------------------------------------------------------------


def resolve_roots(raw_roots: dict[str, str], toml_dir: Path) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for key, value in raw_roots.items():
        expanded = os.path.expanduser(str(value))
        p = Path(expanded)
        if not p.is_absolute():
            p = (toml_dir / p).resolve()
        resolved[key] = str(p)
    return resolved


def _substitute_roots(raw: str, roots: dict[str, str]) -> str:
    out = raw
    for key, value in roots.items():
        out = out.replace("{" + key + "}", value)
    return out


def resolve_path_target(raw: str, roots: dict[str, str], toml_dir: Path) -> Path:
    substituted = _substitute_roots(raw, roots)
    expanded = os.path.expanduser(substituted)
    p = Path(expanded)
    if not p.is_absolute():
        p = (toml_dir / p).resolve()
    return p


def resolve_name_target(raw: str, roots: dict[str, str]) -> str:
    """For command_on_path / python_module: substitute roots (rarely used)
    but never treat the result as a path to resolve relative to anything —
    a bare command or module name stays a bare name."""
    return _substitute_roots(raw, roots)


# --------------------------------------------------------------------------
# Check implementations — each returns (state, detail)
# state in {"ok", "broken", "na"}
# --------------------------------------------------------------------------


def check_path_exists(target: Path) -> tuple[str, str]:
    if target.exists():
        return "ok", f"exists: {target}"
    return "broken", f"path does not exist: {target}"


def check_path_writable(target: Path) -> tuple[str, str]:
    if not target.exists():
        return "broken", f"directory does not exist: {target}"
    if not target.is_dir():
        return "broken", f"not a directory, cannot probe writability: {target}"
    try:
        with tempfile.NamedTemporaryFile(dir=target, prefix=".mise-probe-", delete=True):
            pass
    except OSError as e:
        return "broken", f"directory not writable ({e.strerror or e}): {target}"
    return "ok", f"writable (create+delete probe succeeded): {target}"


def check_command_on_path(target: str) -> tuple[str, str]:
    found = shutil.which(target)
    if found:
        return "ok", f"found on PATH: {found}"
    return "broken", f"not found on PATH: {target}"


def check_file_parses_json(target: Path) -> tuple[str, str]:
    if not target.exists():
        return "broken", f"file does not exist: {target}"
    try:
        text = target.read_text()
    except OSError as e:
        return "broken", f"could not read file ({e}): {target}"
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        return "broken", f"invalid JSON ({e}): {target}"
    return "ok", f"parses as JSON: {target}"


def check_file_parses_toml(target: Path) -> tuple[str, str]:
    if not target.exists():
        return "broken", f"file does not exist: {target}"
    try:
        with target.open("rb") as f:
            tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        return "broken", f"invalid TOML ({e}): {target}"
    except OSError as e:
        return "broken", f"could not read file ({e}): {target}"
    return "ok", f"parses as TOML: {target}"


def check_node_syntax(target: Path) -> tuple[str, str]:
    node = shutil.which("node")
    if node is None:
        return "broken", "node not on PATH — cannot verify script syntax (see node-on-path check)"
    if not target.exists():
        return "broken", f"target script does not exist: {target}"
    try:
        proc = subprocess.run(
            [node, "--check", str(target)],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return "broken", f"could not run `node --check`: {e}"
    if proc.returncode == 0:
        return "ok", f"valid JS syntax: {target}"
    stderr = proc.stderr.strip() or f"node --check exited {proc.returncode}"
    return "broken", f"syntax error in {target}: {stderr}"


def check_python_module(target: str) -> tuple[str, str]:
    import importlib.util

    try:
        spec = importlib.util.find_spec(target)
    except (ImportError, ModuleNotFoundError, ValueError) as e:
        return "broken", f"module not importable ({e}): {target}"
    if spec is None:
        return "broken", f"module not importable: {target}"
    return "ok", f"importable: {target}"


def check_vendor_stamp(target: Path, stamp_target: Path) -> tuple[str, str]:
    if not stamp_target.exists():
        return "na", "N/A (no stamp yet)"
    if not target.exists():
        return "broken", f"vendored file does not exist: {target}"
    try:
        stamp_text = stamp_target.read_text()
        stamp_data = json.loads(stamp_text)
    except (OSError, json.JSONDecodeError) as e:
        return "broken", f"could not read/parse stamp file ({e}): {stamp_target}"
    recorded = stamp_data.get("sha256")
    if not recorded:
        return "broken", f"stamp file has no 'sha256' field: {stamp_target}"
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual == recorded:
        return "ok", f"stamp matches canon (sha256 {actual[:12]}...)"
    return (
        "broken",
        f"stamp mismatch — vendored copy has drifted from canon "
        f"(recorded {recorded[:12]}..., actual {actual[:12]}...)",
    )


# --------------------------------------------------------------------------
# Dispatch
# --------------------------------------------------------------------------


def run_check(check: dict[str, Any], roots: dict[str, str], toml_dir: Path) -> tuple[str, str]:
    """Returns (state, detail) where state in {"ok", "broken", "na", "agent"}."""
    if check["executor"] == "agent":
        return "agent", "executor=agent — not evaluated in a static run; the calling agent verifies"

    check_type = check["type"]
    raw_target = check["target"]

    if check_type == "path_exists":
        return check_path_exists(resolve_path_target(raw_target, roots, toml_dir))
    if check_type == "path_writable":
        return check_path_writable(resolve_path_target(raw_target, roots, toml_dir))
    if check_type == "command_on_path":
        return check_command_on_path(resolve_name_target(raw_target, roots))
    if check_type == "file_parses_json":
        return check_file_parses_json(resolve_path_target(raw_target, roots, toml_dir))
    if check_type == "file_parses_toml":
        return check_file_parses_toml(resolve_path_target(raw_target, roots, toml_dir))
    if check_type == "node_syntax":
        return check_node_syntax(resolve_path_target(raw_target, roots, toml_dir))
    if check_type == "python_module":
        return check_python_module(resolve_name_target(raw_target, roots))
    if check_type == "vendor_stamp":
        target_path = resolve_path_target(raw_target, roots, toml_dir)
        stamp_path = resolve_path_target(check["stamp_target"], roots, toml_dir)
        return check_vendor_stamp(target_path, stamp_path)

    # Should be unreachable — load_declaration() already validated known types.
    raise MiseEngineError(f"unhandled check type '{check_type}' for check '{check['id']}'")


def classify_status(check: dict[str, Any], state: str) -> str:
    if state == "ok":
        return "PASS"
    if state == "na":
        return "N/A"
    if state == "agent":
        return "UNCHECKED (agent)"
    # state == "broken" -> map through the check's declared severity.
    return check["severity"]


# --------------------------------------------------------------------------
# Report generation
# --------------------------------------------------------------------------


def evaluate(decl: dict[str, Any], toml_dir: Path) -> list[dict[str, Any]]:
    raw_roots = decl.get("roots", {})
    roots = resolve_roots(raw_roots, toml_dir)
    results = []
    for check in decl["checks"]:
        state, detail = run_check(check, roots, toml_dir)
        status = classify_status(check, state)
        results.append(
            {
                "id": check["id"],
                "description": check["description"],
                "executor": check["executor"],
                "type": check["type"],
                "target": check["target"],
                "severity": check["severity"],
                "mode": check.get("mode", "static"),
                "remedy": check["remedy"],
                "status": status,
                "detail": detail,
            }
        )
    return results


def format_human_report(
    results: list[dict[str, Any]], decl_path: Path, live: bool
) -> str:
    lines = []
    lines.append("mise — readiness check")
    lines.append(f"declaration: {decl_path}")
    lines.append("")

    id_width = max((len(r["id"]) for r in results), default=2)
    status_width = max((len(r["status"]) for r in results), default=6)

    lines.append(f"{'STATUS'.ljust(status_width)}  {'ID'.ljust(id_width)}  DESCRIPTION")
    lines.append(f"{'-' * status_width}  {'-' * id_width}  {'-' * 11}")
    for r in results:
        lines.append(
            f"{r['status'].ljust(status_width)}  {r['id'].ljust(id_width)}  {r['description']}"
        )
        if r["status"] != "PASS":
            lines.append(f"{' ' * status_width}  {' ' * id_width}  remedy: {r['remedy']}")

    fail_n = sum(1 for r in results if r["status"] == "FAIL")
    warn_n = sum(1 for r in results if r["status"] == "WARN")
    na_n = sum(1 for r in results if r["status"] == "N/A")
    unchecked_n = sum(1 for r in results if r["status"] == "UNCHECKED (agent)")
    pass_n = sum(1 for r in results if r["status"] == "PASS")

    lines.append("")
    lines.append(
        f"summary: {pass_n} PASS, {warn_n} WARN, {fail_n} FAIL, "
        f"{na_n} N/A, {unchecked_n} UNCHECKED (agent)"
    )

    if fail_n:
        lines.append("FAIL present -> this brigade must refuse `service start`.")
    else:
        lines.append("no FAIL -> static gate clears (agent-executor checks still need verifying).")

    if live:
        live_checks = [r for r in results if r["mode"] == "live"]
        lines.append("")
        lines.append("--live: checks the calling agent should run itself (mode=live):")
        if live_checks:
            for r in live_checks:
                lines.append(f"  - {r['id']}: {r['description']} (target: {r['target']})")
        else:
            lines.append("  (none declared in this brigade's mise.toml)")

    return "\n".join(lines) + "\n"


def format_json_report(
    results: list[dict[str, Any]], decl_path: Path, exit_code: int, live: bool
) -> str:
    fail_n = sum(1 for r in results if r["status"] == "FAIL")
    warn_n = sum(1 for r in results if r["status"] == "WARN")
    na_n = sum(1 for r in results if r["status"] == "N/A")
    unchecked_n = sum(1 for r in results if r["status"] == "UNCHECKED (agent)")
    pass_n = sum(1 for r in results if r["status"] == "PASS")
    payload = {
        "engine_version": MISE_ENGINE_VERSION,
        "declaration": str(decl_path),
        "live": live,
        "checks": results,
        "summary": {
            "pass": pass_n,
            "warn": warn_n,
            "fail": fail_n,
            "na": na_n,
            "unchecked_agent": unchecked_n,
        },
        "exit_code": exit_code,
    }
    return json.dumps(payload, indent=2) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mise.py",
        description=(
            "mise en place — readiness check for a skill-agent-brigade. "
            "Runs the static (script-executor) checks in a brigade's mise.toml "
            "declaration and reports PASS/WARN/FAIL/UNCHECKED(agent) per check."
        ),
    )
    parser.add_argument(
        "declaration",
        nargs="?",
        default=None,
        help="path to the mise.toml declaration (default: mise.toml next to this script)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help=(
            "also print which declared checks (mode=live) the calling agent "
            "should run itself. mise.py itself never performs live/paid probes."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="machine-readable JSON report instead of the human table",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.declaration is not None:
        decl_path = Path(args.declaration).expanduser().resolve()
    else:
        decl_path = (Path(__file__).parent / "mise.toml").resolve()

    try:
        decl = load_declaration(decl_path)
        results = evaluate(decl, decl_path.parent)
    except MiseEngineError as e:
        print(f"mise: engine error: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # defensive: never let an unexpected exception look like a FAIL
        print(f"mise: unexpected engine error: {e!r}", file=sys.stderr)
        return 2

    fail_n = sum(1 for r in results if r["status"] == "FAIL")
    exit_code = 1 if fail_n else 0

    if args.json:
        print(format_json_report(results, decl_path, exit_code, args.live), end="")
    else:
        print(format_human_report(results, decl_path, args.live), end="")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
