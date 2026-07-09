"""Canon-home smoke tests for adapter/cellar.py (canonized 2026-07-06 from
the three drifted brigade copies). The full behavioral suites live with the
consuming brigades (they exercise their vendored copies on every run); this
file pins the canon's UNION surface — everything any brigade imports — so a
canon edit that drops a reconciled delta fails here first, before a
re-vendor ships it house-wide.

Union deltas pinned: the strict subject-slug lint (Company Research +
Assessment), `list()` + dotted-path filtering (Sales Collateral),
`canonical_json()` (Assessment).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cellar  # noqa: E402


def _meta(**overrides):
    meta = {
        "landed": "2026-07-06T12:00:00-04:00",
        "kind": "test-note",
        "subject": "companies/acme",
        "produced_by": {"brigade": "test", "ticket": "t-1", "station": "s"},
        "supersedes": None,
        "provenance": "canon smoke test",
    }
    meta.update(overrides)
    return meta


@pytest.fixture
def client(tmp_path):
    return cellar.CellarClient(root=tmp_path / "cellar")


def test_union_surface_is_complete():
    for name in ("CellarClient", "CellarRootError", "CellarLintError", "CellarConflictError",
                 "split_frontmatter", "now_iso", "canonical_json", "_matches_filter"):
        assert hasattr(cellar, name), f"canon lost union member {name}"
    for method in ("land", "upsert", "resolve", "list_refs", "list", "cellar_lint"):
        assert hasattr(cellar.CellarClient, method), f"CellarClient lost {method}"


def test_root_resolution_fails_loudly_when_unset(monkeypatch):
    monkeypatch.delenv("CELLAR_ROOT", raising=False)
    with pytest.raises(cellar.CellarRootError):
        cellar.CellarClient()


def test_land_markdown_roundtrip_and_append_only(client):
    ref = client.land("hello", _meta())
    text = client.resolve(ref)
    fm, body = cellar.split_frontmatter(text)
    assert fm["kind"] == "test-note" and body.strip() == "hello"
    with pytest.raises(cellar.CellarConflictError):
        client.land("again", _meta(), ref=ref)


def test_land_non_markdown_writes_meta_sidecar(client):
    ref = client.land(b"{}", _meta(kind="dump"), ref="companies/acme/2026-07-06-dump.json")
    assert (client.root / (ref + ".meta.json")).exists()
    assert client.list_refs(kind="dump") == [ref]


def test_strict_slug_lint_is_the_reconciled_union(client):
    # Company Research + Assessment's delta, kept in canon
    with pytest.raises(cellar.CellarLintError, match="lowercase alnum"):
        client.cellar_lint(_meta(subject="companies/bad_slug"))
    with pytest.raises(cellar.CellarLintError, match="lowercase"):
        client.cellar_lint(_meta(subject="companies/Acme"))
    client.cellar_lint(_meta(subject="assessments/acme/collateral/roi-value-snapshot"))


def test_list_dotted_path_filter(client):
    client.land("a", _meta())
    client.land("b", _meta(produced_by={"brigade": "test", "ticket": "t-2", "station": "s"},
                           landed="2026-07-06T13:00:00-04:00", kind="other-note"))
    hits = client.list(filter={"produced_by.ticket": ["t-2"]})
    assert [h["meta"]["kind"] for h in hits] == ["other-note"]


def test_canonical_json_is_key_sorted_and_compact():
    assert cellar.canonical_json({"b": 1, "a": [1, 2]}) == '{"a":[1,2],"b":1}'
