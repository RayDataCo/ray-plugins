# Execution-eval report — variance-analysis (first measurement)

The lift measurement from the execution-eval station ([`../../skills/execution-eval-station/`](../../skills/execution-eval-station/), run via [`../../workflow/execution-eval-variance-analysis.run.js`](../../workflow/execution-eval-variance-analysis.run.js)). Two arms — base model alone vs base model + skill — on the four oracle fixtures from [`tests.md`](./tests.md), 3 samples per arm, graded deterministically against the oracle answers.

- **Base model:** Opus 4.8 (the session model — what a user actually experiences).
- **Result: lift = 0.00 pp.** Both arms scored **100%** on all four oracles (mean 1.00 ± 0.00, n=12 per arm).
- **Mechanical action:** `kill` (lift inside the noise band). **Analyst read: do not kill — the fixtures don't discriminate** (see below).

| Fixture | base model | base + skill | lift |
|---|---|---|---|
| A — DM price/qty, AQ-purchased-vs-used trap | 100% | 100% | 0 |
| B — FOH spending vs production-volume trap | 100% | 100% | 0 |
| C — materials mix + yield | 100% | 100% | 0 |
| D — management-by-exception (controllability trap) | 100% | 100% | 0 |

## What this means (and what it doesn't)

A 0-lift result here is **not** a verdict that the skill is worthless. It's the classic **non-discriminating fixture** signal — skill-creator's analyzer flags exactly this: *"passes 100% in both configurations — may not differentiate skill value."* Base Opus 4.8 is already at the ceiling on these textbook problems, including the two traps the skill was built to kill (it correctly computed the DM price variance on AQ *purchased* and the FOH production-volume variance as budgeted − applied). When the baseline is already perfect, no fixture can show lift.

This is itself the point of the station: it tells you, empirically, when a skill is **not pulling weight on a given model** — before you ship it believing it does. `variance-analysis` passed 5/5 static critics and *reads* like it adds value; on a strong base model, on these problems, it adds no measured correctness lift. That gap between "reads well" and "demonstrably helps" is precisely what execution-eval exists to expose.

## To actually measure lift, the fixtures (or the arm) have to be harder

Where a procedure skill like this should show real lift:

- **A weaker / cheaper model arm.** In production you'd run the skill on Haiku/Sonnet to save cost; a procedure skill earns its keep by lifting a smaller model up to the strong model's answer. Re-run with the baseline arm on a cheaper model.
- **Messier, realistic inputs** — partial data, distractor figures, units to reconcile, multi-step compounded problems — rather than clean textbook setups the base model has effectively memorized.
- **Consistency at scale / format adherence.** These binary correctness fixtures don't capture output-contract conformance or run-to-run consistency, which may be where the skill's value actually lives.

## Note on the grader (verify-before-assert)

The **first** run of this measurement reported a *negative* lift (−0.11), with the skill arm scoring 0% on Fixture A. Reading the raw transcripts showed the skill arm had in fact produced the correct answers — the grader was matching figures by exact name and missed "**direct materials** price variance" where it expected "**DM** price variance" (one baseline sample happened to abbreviate, so the baseline got spurious credit). The negative lift was a grader bug, not a skill failure. Fixed by matching figures on identifying tokens (`PRICE`, `QUANTITY`, `VOLUME`, …) and re-grading the cached run. This is the grader's own "critique the evals" principle in action: a wrong grade is worse than no grade.
