# mise — implementation plan *(draft for founder review, 2026-07-03)*

> Everything in its place before service. This is the build plan for the `mise` command, distilled
> from the service dialogue (declared-deps manifest, rail service lock, vendored-from-canon). It is
> a PLAN — nothing below is built yet.

## Shape: one engine, one declaration, per brigade

Two files, both shipped inside every brigade (marketplace self-containment holds):

| File | What | Varies per brigade? |
|---|---|---|
| `mise.py` | the check **engine** — runs checks, prints the report, exit code | **No** — house infrastructure, **vendored from canon** exactly like `rail_adapter.py` (version+hash stamp, mise checks its own stamp too) |
| `mise.yaml` | the **declaration** — this brigade's checks + remedies | **Yes** — the machine-readable form of the declared-deps manifest; the factory *emits* it during an `artifact: brigade` build (derived from roster + walk runtime) |

This resolves a drift risk before it exists: the service SKILL.md's human-readable deps table would
otherwise duplicate the manifest. **Decision for founder (D1):** make `mise.yaml` the single source
of truth and have the SKILL.md table reference it (my rec), vs keeping the markdown table canonical
and parsing it (fragile).

## Check taxonomy

Each `mise.yaml` entry: `{id, description, executor, type, target, remedy, severity}`.

**Executor** — the key structural split:
- `script` — `mise.py` can verify it: path exists/writable, `command -v`, venv import probe,
  rail lease take/release probe, JSON/YAML parse, skillLint pass, vendor-stamp hash vs canon.
- `agent` — only the harness can verify it: Workflow tool callable, MCP server connected, model
  tier responds. `mise.py` lists these as `UNCHECKED (agent)` in script-only runs; the skill
  procedure has the agent verify them and merge results into one report.

**Severity** — the principle: **FAIL = cannot run safely; WARN = runs, but behind or degraded.**
- FAIL: rail/cellar unreachable or unwritable · walk runtime missing (python3/venv, Workflow tool) ·
  station skill missing or unparseable · credential unresolvable *by name* (never printed)
- WARN: menu missing/stale · vendor stamp behind canon (remedy: "re-stamp via `iterate-brigade`") ·
  optional tooling absent
- **Decision for founder (D2):** I put stale-adapter at WARN not FAIL — a brigade with an older
  vendored adapter still *runs correctly on its own copy*; it's behind, not broken. Veto if you want
  drift treated harder.

**Mode** — static vs live:
- `mise` (default): static checks only — fast, free, no tokens. This is what `service start` gates on
  (plus the lease probe).
- `mise --live`: adds the paid/slow probes — minimal model call per configured tier, MCP round-trips.
  Run ad hoc or on a schedule, not on every service start.
- **Decision for founder (D3):** OK that service start gates on static-only? (My rec: yes — a model
  outage will surface on ticket 1 anyway; gating every start on live probes burns tokens for little.)

## The report

One line per check: `PASS / WARN / FAIL / UNCHECKED(agent)` + the declared remedy for every non-PASS
("run `uv sync`", "connect MCP server X", "re-hang the discovery ticket", "re-stamp via
iterate-brigade"). Dual output: human table + `--json` for tooling. Exit code: 0 clean, 1 any FAIL,
2 engine error. When run as the `service start` gate, the report is appended to the service journal;
ad hoc, it's returned to the caller.

## Factory obligations (extends the existing section)

- `artifact: brigade` builds **emit `mise.yaml`** (from the roster + walk-runtime declaration) and
  **vendor `mise.py`** alongside `rail_adapter.py` — one stamp discipline for both.
- The brigade acceptance checklist gains: mise.yaml present + parses + covers the four port checks
  (rail, cellar, walk runtime, stations).

## Build sequence

1. **Canon engine** (`mise.py` + yaml schema + its own pytest suite w/ negative controls: break a
   dep, assert the right FAIL + remedy) — in this plugin.
2. **Factory's own mise** (`skills/mise/SKILL.md` + factory `mise.yaml`) — live-fire it here first;
   the factory is its own first customer.
3. **Wire the service gate** — `service start` step 2 stops being prose and calls the engine.
4. **Domain rollout** — rides the SAME retrofit pass as `rail_adapter.py` vendoring (one pass, one
   zip round: adapter canon + mise engine + per-brigade mise.yaml + their service wrappers).

Estimate: steps 1–3 = one focused session; step 4 = the already-queued retrofit pass, unchanged
sequencing (after P1 port validates, before P2).

## Out of scope (deliberately)

- Auto-FIXING failures (mise reports + remedies; it never mutates — a readiness check that installs
  things is a footgun).
- Live-probing external websites/APIs a station merely *might* call (stations own their runtime
  errors; mise checks declared deps, not the internet).
- The close-out loop (`runner`) — separate build, unchanged.
