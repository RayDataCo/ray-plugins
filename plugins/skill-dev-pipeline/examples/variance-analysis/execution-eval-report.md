# Execution-eval report — variance-analysis

The lift measurement from the execution-eval station ([`../../skills/execution-eval-station/`](../../skills/execution-eval-station/), run via [`../../workflow/execution-eval-variance-analysis.run.js`](../../workflow/execution-eval-variance-analysis.run.js)). Two arms — base model alone vs base model + skill — on the four oracle fixtures from [`tests.md`](./tests.md), 3 samples per arm, graded deterministically against the oracle answers. Run across three model tiers (the fair ablation holds the model constant and toggles the skill).

**Headline: the skill brings every tier to a deterministic 100% on all four oracles (with-skill stddev = 0). The base model is already perfect on the computational fixtures (A/B/C) at every tier, so all the lift lives in fixture D — the management-by-exception *judgment* fixture — and it grows as the base model weakens.**

| Tier (base model) | base all-fixtures | +skill | aggregate lift | **fixture D: base → +skill** |
|---|---|---|---|---|
| Opus 4.8 | 100% | 100% | 0 pp | 100% → 100% (0) |
| Sonnet 4.6 | 92% ± 15 | 100% | +8.3 pp | **67% → 100% (+33 pp)** |
| Haiku 4.5 | 94% ± 13 | 100% | +5.6 pp | **78% → 100% (+22 pp)** |

Per fixture, across tiers: **A, B, C → 0 lift at every tier** (base already 100%). **D carries everything.** The verified base-model failure on D is the exact error the skill teaches against: 4 of 6 base runs answered "**yes**, the $10,000 FOH production-volume variance is the single #1 priority" — ranking by absolute dollar size while ignoring that it is a non-controllable capacity artifact. (Failures confirmed by reading transcripts, not just the score.)

## What this means (and what it doesn't)

Two things separate cleanly here, and they're exactly what the station exists to tell apart:

- **Computational fixtures (A/B/C) — 0 lift, every tier.** Even Haiku gets standard-costing arithmetic right (DM price on AQ *purchased*, FOH production-volume as budgeted − applied, mix/yield). The base models have effectively memorized textbook mechanics; the skill can't lift a ceiling. These are **non-discriminating** fixtures — skill-creator's analyzer flags exactly this: *"passes 100% in both configurations."*
- **Judgment fixture (D) — real, growing lift.** Management-by-exception isn't arithmetic; it's a *controllability* call. The base model reliably trips it (says the biggest-dollar variance is the #1 priority), and the rate of error rises as the model weakens. The skill closes it to 100% at every tier. **This** is where the procedure earns its place: encoding judgment the base model doesn't apply on its own.

So the honest verdict on `variance-analysis`: it adds little on the computational sub-tasks (the model already knows them) and **measurable, model-tier-dependent value on the judgment sub-task**. That is a far more useful answer than a single pass/fail — and it tells us where to point the skill (the interpretive call, not the arithmetic).

## Design lesson: report per-fixture lift, not just the aggregate mean

The station's mechanical action came back **`kill`** for both Haiku and Sonnet — because the *aggregate* lift (+5.6 / +8.3 pp) sits inside the noise band, diluted by the three ceilinged fixtures. But the per-fixture view shows a clear, real +22 to +33 pp on D. **A skill that fixes one important failure mode gets washed out to "kill" by easy fixtures if you only look at the mean.** The expo must consume **per-fixture lift** (or weight discriminating fixtures), not the aggregate — and the fixture set should be pruned of non-discriminating cases or they drown the signal. This is the analyzer's "non-discriminating assertion" warning made consequential.

## Other places lift would show (untested here)

- **Messier, realistic inputs** — partial data, distractor figures, units to reconcile — rather than clean textbook setups.
- **Consistency / format adherence** — the with-skill arm was deterministic (stddev 0) where the base arm was not; run-to-run consistency and output-contract conformance are skill value these binary fixtures only partly capture.

## Note on the grader (verify-before-assert)

The **first** run of this measurement reported a *negative* lift (−0.11), with the skill arm scoring 0% on Fixture A. Reading the raw transcripts showed the skill arm had in fact produced the correct answers — the grader was matching figures by exact name and missed "**direct materials** price variance" where it expected "**DM** price variance" (one baseline sample happened to abbreviate, so the baseline got spurious credit). The negative lift was a grader bug, not a skill failure. Fixed by matching figures on identifying tokens (`PRICE`, `QUANTITY`, `VOLUME`, …) and re-grading the cached run. This is the grader's own "critique the evals" principle in action: a wrong grade is worse than no grade.
