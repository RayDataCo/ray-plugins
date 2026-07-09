# Base-model-covered registry

Some finance tasks don't need a skill. Not because the discipline doesn't matter — because the
2026-era base model already performs it smoothly, without custom instructions, on the fixtures
that would otherwise anchor a skill's acceptance contract. This registry is how we say that out
loud instead of staying silent about it: for each task listed here, we're aware it's a task in
the discipline, we looked for lift, we didn't find any worth shipping instructions for, and here's
the evidence. The deliverable is documented exemplar prompts plus eval evidence, not a skill —
coverage, not code.

The registry doubles as a model-regression tripwire. "Base is fine" is a claim about a specific
model at a specific tier on a specific date, not a permanent fact — model behavior drifts across
releases, and a task that's at ceiling today could regress tomorrow. Each entry below is a
re-runnable check: point the same fixture suite at a new model and confirm the ceiling still
holds. If it doesn't, that's the signal to build the skill this registry chose not to build.

## Evidence standard

Each task's coverage claim rests on a two-arm execution eval (base model vs. base model + a
draft skill built by the ab-skill-factory) against that task's oracle fixtures — n=3 samples
per fixture, graded deterministically in code against a fixed answer key (never by name-matching
or LLM judgment). "Base at ceiling" means the base arm scored 3/3 on every fixture in the suite
at the stated tier and eval date, with no discriminating fixture available to demonstrate lift.
This is what execution-eval calls the "non-discriminating" class: the base model has no headroom
left for a skill to fill on that fixture. INCONCLUSIVE at the skill-shipping bar becomes COVERED
at the registry bar — same evidence, different question asked of it.

## Promotion rule

- **Model upgrade → re-run the fixture suite.** Before or shortly after adopting a new base
  model/tier for finance work, re-run each task's fixtures (`eval/fixtures.json` per task, same
  harness as the original eval) against the new model.
- **Any fixture regression → promote the task to a built skill.** If the new base model drops
  below 3/3 on any fixture that was previously at ceiling, that task graduates out of this
  registry. Route it through the ab-skill-factory factory (spec → tests → author ⇄ critic →
  expo) the same way the four shipped finance skills were built, using the regressing fixture as
  the oracle case that proves the skill's worth.
- Grading keys are never published alongside the exemplar prompts in this registry — they stay
  private with the eval harness so the fixtures remain usable for future regression runs.

## Coverage table

| task | fixtures | base pass rate | tier | eval date |
|---|---|---|---|---|
| rolling-forecast-update | A, B, C, D | 3/3, 3/3, 3/3, 3/3 | sonnet | 2026-07-08 |
| financial-statements | A, B, C, D | 3/3, 3/3, 3/3, 3/3 | sonnet | 2026-07-08 |
| cash-flow-forecasting | A, B, C, D | 3/3, 3/3, 3/3, 3/3 | sonnet | 2026-07-08 |
| reconciliation | A, B, C, D | 3/3, 3/3, 3/3, 3/3 | sonnet | 2026-07-08 |
| capital-budgeting-analysis | A, B, C, D | 3/3, 3/3, 3/3, 3/3\* | sonnet | 2026-07-08 |

\* capital-budgeting-analysis fixture A scored 2/3 raw (`npv`, tolerance ±5) in the eval run; the
evals doc's "held back" section documents this as a verified-false anomaly — the grading
tolerance was tighter than the oracle's own disclosed rounding drift, not a base-model miss. See
`capital-budgeting-analysis.md` for the one-line note. reconciliation fixture B carries a
separate verified-false anomaly (a `withSkill` regression, not a base miss — the grading key
demanded a magnitude where the source teaches a signed convention); see
`reconciliation.md`.

Source data: `/Users/ray/Projects/phdata-private/brigade-house/cellar/brigade-runs/EVAL-RESULTS-2026-07-08.json`.
Method and verdicts: `../evals/2026-07-08-finance-vertical-eval.md`.
