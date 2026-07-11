# WALK-SPEC — the walk as a port

*Ratified 2026-07-10 (founder greenlight on the design doc's "promote the
Python walk shape"); built 2026-07-11. Supersedes the informal split between
the Gen-A Python walks and the Gen-B Workflow-script walk — those are now
two ADAPTERS of one port. Companion specs: RAIL-SPEC.md (the queue port this
one drives), TICKET-CONTRACT.md (Gate A + the exit set), BUNDLE-SPEC.md
(resolution/replayability), ADAPTER-SPEC.md (claim model, vendoring
discipline), AGENT-BRIGADE-STANDARD.md (the symmetry guarantee this port
completes).*

## The role

A **walk** is not a technology — it is a role: *drive tickets from the rail
through the brigade to a terminal ack.* Every brigade's service surface runs
a walk; which adapter it runs is a deployment choice the brigade's mise
reports, not a fork of the machinery.

## The contract (every adapter, in order)

| # | step | nature |
|---|------|--------|
| 1 | Take the service lock (`<rail>/.service/<brigade>.lock`; advisory today, one walker per brigade per rail) | deterministic |
| 2 | Pull-with-lease, scoped to the brigade's menu's live artifact types (+ `menu` discovery) | deterministic |
| 3 | Gate A at pull — must match enqueue-side; a mismatch is itself a caught defect | deterministic |
| 4 | Resolve context — snapshot eager sources into `## Resolved-context snapshot` (static via adapter sha; live via tools) | mixed |
| 5 | Dispatch to the expo/stations — decompose, run, compose | **agent** |
| 6 | Ack on the brigade's exit set; terminal tickets file to subject | deterministic |
| 7 | Stop-flag check between tickets (`<rail>/.service/<brigade>.stop`); release lock on exit | deterministic |

**Steps 2, 3 and 6 MUST NOT be laundered through an LLM.** They are the
rail's mechanical guarantees; a model transcribing their results reintroduces
exactly the fabrication surface the deterministic gates exist to remove.
Step 5 is the only irreducibly agentic step. Step 4 is split by nature:
static sources are the adapter's own code, live sources need tools.

## The two adapters

### Python in-process — the REFERENCE (`adapter/walk.py`)

`Walk(WalkConfig).run()` performs steps 1–4, 6–7 by calling the sibling
canon `rail_adapter` functions in-process, and invokes step 5 through an
injected **dispatcher**. This is the shape a partner should read as
canonical, and the default every brigade vendors (stamped; canon inferred by
filename via `CANON_PATHS["walk.py"]`).

Per-brigade variance arrives ONLY through `WalkConfig`:

- `allowed_artifacts` — the menu's live set (scope for pull + Gate A).
- `dispatchers` — station key → dispatcher. Key = the artifact type, or
  `"<artifact>:<phase>"` for phased artifacts.
- `phased_artifacts` — artifact → ordered phase list. **Phase-chaining is a
  parameter, not a fork**: a single-dispatch brigade leaves it empty; a
  multi-phase brigade (one ticket spanning N phase stations behind a
  `current_phase` field — ab-assessment's shape) declares its sequence and
  the walk re-pulls the ticket for each next phase
  (`ack(advance, terminal=False)` → `in-build`, no lease, workable again).
- `exit_map` — dispatcher exit vocabulary → rail disposition. The
  discipline-kind table ships as `DISCIPLINE_EXIT_MAP`
  (`answered`/`partial-with-gaps` → advance, `needs-clarification` →
  reroute-to-steward, `out-of-scope` → kill).
- `gate_b` — the brigade's mechanical sufficiency floor (optional).
- `live_fetch` — the live-source resolver for step 4 (optional; a miss is
  work-logged, never fatal — the expo's sufficiency judgment still stands
  between a miss and a bad build).

`"hold"` is not an ack: it is the brigade-internal wait state (inner-rail
merge pending) — release the lease, no refire increment, no filing.

### THE AGENT-RUNNER INTERFACE (pinned)

A dispatcher is any callable
`dispatch(handle, phase) -> {"exit": ..., "detail"?, "terminal"?, "cellar_refs"?}`.
For an in-process brigade the dispatcher IS the station function. For a
discipline brigade, `make_expo_dispatcher()` adapts an **agent runner**:

```python
run_agent(prompt: str, *, schema: Optional[dict] = None) -> dict
```

— "run an agent with this prompt, optionally force a JSON schema, return
the parsed result." In a Claude Code session that is the Task/Agent tool; in
a headless deployment, the SDK; in a test, a stub. The walk never cares
which.

### Workflow script — the harness-native adapter (`skills/service/discipline-rail-walk.run.js`)

For deployments that ARE a Claude Code session with the Workflow tool and no
Python process wanted. A Workflow script cannot run shell commands itself,
so agents remain the EXECUTORS of the vendored `rail_adapter.py` CLI — but
they are instructed to relay command output and exit codes VERBATIM, and
the SCRIPT does every judgment: it parses the CLI's fixed output shapes
(`pulled <id> (<path>)` / `rail is dry` / `acked -> ` / `EXIT=<code>` for
the Gate-A lint), decides found/dry/pass/fail, maps exits, and fails loud
on anything unrecognized. Honest limit: the transcription surface (an agent
relaying a string) still exists — this is the closest the harness shape can
get to the reference, which is exactly why the Python walk is the
reference. Kept one release to serve Python-less targets; measured, dropped
if unused.

## Multi-phase semantics (rail_adapter v1.3.0)

- `pull(..., ticket_id=)` scopes the scan to one ticket — the multi-phase
  driver's resume primitive (an explicit id is a deliberate act; walker
  scope is skipped for it).
- Workable states: `queued`; `leased`/`in-build` with an EXPIRED lease
  (reclaim, logged); `in-build` with NO lease (between phases — immediately
  workable). Single-phase brigades never produce the third state.
- `ack(advance, terminal=False, phases=[...])` → `in-build`, `current_phase`
  advances, `refire_round` resets, ticket returns to the rail root.
- `ack("refire-to-author")` → `queued`, `refire_round` increments — the
  five-exit set's same-station re-run budget as a rail disposition.
  `reroute-to-spec` remains unhandled (adversarial finding M3, open by
  design; enforcing a refire BUDGET is brigade policy, not walk mechanics).

## Resolution (step 4) — replayability

Before dispatch, the walk freezes the ticket's EAGER sources into
`## Resolved-context snapshot`: static (`file`/`cellar`) sources get an
integrity sha computed by the adapter; live (`url`/`mcp`/`qmd`) sources are
fetched (via `live_fetch` / the harness agent's tools) and frozen verbatim.
Already-snapshotted entry ids are skipped, so multi-phase re-pulls and
refires do not duplicate the section. Same ticket → same build is a
*mechanism* here, not a claim (architectural-review concern #1, closed).

## Honesty notes

- The service lock is ADVISORY (create-exclusive file). The atomic guarantee
  in this stack is the pull's rename-claim (ADAPTER-SPEC "Claim model"),
  which is LOCAL-FILESYSTEM-ONLY — never run a rail on a sync drive.
- `walk.py`'s CLI is plan-mode only (`plan` — what WOULD run, no claims, no
  writes). A real run needs the brigade's Python dispatcher wiring; that is
  each brigade's service skill's job.
- Gen-A brigades (assessment, company-research, sales-collateral) keep their
  own `brigade/rail_walk.py` service wrappers — those wrappers now delegate
  the contract's mechanical steps to the same canon (assessment's in-place
  lease converged to rename-claim, closing adversarial finding H1); the
  vendored `walk.py` is the reference their wrappers are measured against.
