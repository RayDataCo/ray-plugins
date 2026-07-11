# Implementation notes — walk-port convergence (2026-07-11)

Build executed per the queued walk-port build plan (founder-greenlit
2026-07-10 ~21:23 ET) from the design doc that became WALK-SPEC.md. One
motion closes adversarial finding H1 (assessment lease divergence) and the
resolver's Gen-A gap, and converges the two walk generations onto one port.

## Decisions

1. **Canon absorbed the multi-phase semantics as parameters instead of the
   walk reimplementing rail mechanics.** `rail_adapter` 1.2.0 → 1.3.0:
   `pull(ticket_id=…)` + the in-build/no-lease workable state;
   `ack(terminal=…, phases=…, phase_field=…, artifact_refs=…)` +
   `refire-to-author` as a rail disposition. Every prior caller's behavior
   is byte-identical (all new params default to the old semantics). This is
   what let ab-assessment's `pull()`/`ack()` become pure delegation — the
   alternative (walk.py re-owning selection/claiming) would have recreated
   the divergence class the build exists to kill.
2. **Exit-set VALIDATION is brigade policy, not rail mechanics.** Canon
   accepting `refire-to-author` surfaced a hidden coupling: ab-company-research
   relied on canon to reject intra-build exits. Its `ack()` now rejects them
   itself (test caught it — `test_intra_build_exits_are_rejected`).
   Assessment keeps its `reroute-to-spec` dormancy guard locally for the
   same reason.
3. **`STATUS_BY_EXIT` the constant is unchanged.** `refire-to-author` is
   handled as its own branch (mirroring assessment's own prior structure)
   so every existing reader of the constant sees exactly the map it always
   saw. `reroute-to-spec` remains unhandled — M3 stays honestly open.
4. **`refire_round` resets on every non-refire disposition** (kill /
   reroute-to-steward / escalate / terminal advance) when the field exists —
   assessment's own table, now canon. Single-phase tickets without the
   field are untouched (no field injection).
5. **`resolve_context` is a module-level primitive**, not only a `Walk`
   method — the Gen-A wrappers call it directly at their own Gate-A-pass
   points (assessment `_process_one` + `pass_driver._gate_a_recheck`,
   CR/SC `_process_one`), which is how the resolver's Gen-A gap actually
   closes without forcing those brigades onto the `Walk` class wholesale.
   Snapshot-dedupe by entry id (`_snapshotted_ids`) is what makes it safe
   to run at every phase entry of a five-phase ticket.
6. **The agent-runner interface is pinned** (WALK-SPEC "Dispatch"):
   `run_agent(prompt, *, schema=None) -> dict`. `make_expo_dispatcher()`
   adapts any such runner; the walk never knows which harness it runs in.
   This answers the design doc's open question.
7. **Workflow driver = executor doctrine.** It cannot avoid agents (a
   Workflow script cannot run shell), so agents became command executors
   returning CLI output VERBATIM while the script parses the fixed shapes
   (`pulled <id> (<path>)` / `rail is dry` / `acked -> `) and owns every
   judgment, fail-loud on unrecognized output. New optional
   `args.allowed_artifacts` removes the per-run menu-derivation agent call
   (fallback derivation runs once up front, not per ticket).

## Deviations from the build plan (stated, not silent)

- **Step 4 ran in-session, not as a subagent fan-out.** The remaining work
  after the canon-side pieces was byte-exact vendoring (cp + stamp + sha
  verify) plus formulaic small edits; deterministic shell with sha
  verification beats agent-output verification cost for that shape. The
  plan's fan-out language was written when the step looked like the
  symmetric build's per-brigade SKILL.md rewrites.
- **Step 3 folded into Step 1** (resolution was built into walk.py from the
  start, then extracted to module level in the Gen-A wiring pass).
- **Assessment's `_next_workable` survives dry-run-only** (docstring says
  so, and that canon wins any disagreement). The dry-run path needs a
  claim-free scanner and canon deliberately has no non-claiming pull.

## Verification (all literal-output-read, no batched declarations)

- Suites: adapter 111 (24 new walk-port tests) · mise 69 · assessment 328+6
  (incl. the NEW H1 race regression: two real OS processes ×10 iterations
  through `RailClient.pull`, exactly-one-winner + single-physical-file
  invariant every time) · company-research 247 · sales-collateral 177+15.
- sha-uniform: rail_adapter ×10, walk.py ×9, driver ×6 — all identical to
  canon, stamped (stamps follow `CANON_PATHS`, walk.py added there FIRST
  per the drift-detection guardrail).
- mise: 8/8 brigades 0 FAIL (CR under its own .venv; the two WARNs are the
  known pre-existing menu-freshness ones).
- Live fire A (Gen-A kind, scratch cellar): claim-by-rename observed at
  `.claimed/<worker>/`, 5-phase chain step0→c4 through the converged
  pull/ack, resolution snapshot present EXACTLY once (deduped across 5
  re-pulls, sha-stamped), terminal ack filed to subject, close-out sweep
  found + signed it.
- Live fire B (Gen-B kind, scratch cellar): the refactored Workflow driver
  run via the real Workflow tool against a real rail — pull executor
  returned the CLI line verbatim, script parsed the claim path, resolution
  agent snapshotted the static source with sha, expo served. (Result
  recorded in the PR once the run completed.)
- Leak sweep: plain `grep -rn` (never `git grep`) over all 10
  public-manifest plugins — client watchlist 0 hits, private paths 0 hits.
- `claude plugin validate` center tree: passed.

## Open questions / follow-ons (not this build)

- Adversarial findings H2 (shell-building from ticket strings), H3
  (untrusted ticket text spliced into expo prompt — note: the executor
  refactor NARROWS this: mechanical agents no longer receive judgment
  authority, but the serve prompt still embeds ticket text), M2, M3, M4.
- Gen-B brigades still default to the Workflow adapter; first live
  rail-mode fire of a Gen-B walk on the HOUSE rail (not scratch) remains
  on the queued follow-ons list from the symmetric build.
- `rail-walk.run.js` (the factory's own build-kind Workflow walk) has not
  had the executor-doctrine refactor — same class of work, separate ticket.
- Whether the Workflow adapter is kept long-term: WALK-SPEC keeps the
  design doc's "one release, measure, drop if unused" stance.
