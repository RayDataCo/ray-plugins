"""Shared fixtures for the mise engine test suite.

Every test in this package must operate only inside pytest's tmp_path
fixture (or a subdirectory of it) — never against the real cellar/rail
(~/rdco-cellar/...) and never against any path outside
the per-test tmp dir. That's the negative-control discipline the build
task calls for: a broken test fixture must not be able to touch, or be
confused with, the real brigade's declaration.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

MISE_PY = Path(__file__).resolve().parent.parent / "mise.py"


def _load_mise_module():
    spec = importlib.util.spec_from_file_location("mise_engine_under_test", MISE_PY)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mise_engine_under_test"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


@pytest.fixture(scope="session")
def mise():
    """The mise.py module under test, imported by file path so the suite
    works whether it's run from the plugin dir or the repo root."""
    return _load_mise_module()


@pytest.fixture()
def toml_dir(tmp_path):
    """A scratch directory standing in for 'the directory the mise.toml
    lives in' — relative check targets resolve against this."""
    d = tmp_path / "brigade"
    d.mkdir()
    return d


def write_toml(path: Path, body: str) -> Path:
    path.write_text(body)
    return path
