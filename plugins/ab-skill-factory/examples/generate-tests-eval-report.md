# Execution-eval report — generate-tests (second skill)

The execution-eval station run on a **second, different-type skill** to check it generalizes beyond `variance-analysis`. `generate-tests` is a *transform* skill (Scope×Basis matrix → dbt tests), not a computational one. Run via [`../workflow/execution-eval-generate-tests.run.js`](../workflow/execution-eval-generate-tests.run.js), three model tiers, 3 samples per arm, deterministic grading against fixed output schemas.

> Note: `generate-tests` is an external RDCO skill referenced by absolute path in the workflow (path-coupled, like the canonical stations — a genericization follow-up). The oracle answers are grounded in the skill's own documented rules (severity mapping absolute/relative→error, temporal→warn, human→skip-no-code; flag any scope with zero tests).

## Result — identical across all three tiers

| Tier (base) | base all-fixtures | +skill | aggregate lift | **fixture S3: base → +skill** |
|---|---|---|---|---|
| Haiku 4.5 | 83% | 100% | +16.7 pp | **50% → 100% (+50 pp)** |
| Sonnet 4.6 | 83% | 100% | +16.7 pp | **50% → 100% (+50 pp)** |
| Opus 4.8 | 83% | 100% | +16.7 pp | **50% → 100% (+50 pp)** |

Per fixture (same at every tier):
- **S1 — severity mapping + human-skip → non-discriminating.** Base models already answer amount→error, temporal→**warn**, human→no-code correctly (9/9). The skill adds nothing here; these are conventions the base model knows.
- **S2 — coverage-gap flagging → non-discriminating.** Base correctly flags transformation-level as the zero-test scope. (Mild grader caveat: the count field uses contains-matching, which one verbose base run that *deviated and generated 3 tests* slipped through. Non-material — S2 is non-discriminating regardless.)
- **S3 — test-type + relative-severity → clean +50 pp win, every tier.** Base correctly uses `accepted_values` for the enum (universal) but defaults the relative sum-of-amount check to severity=`warn`; the skill's rule (relative→**error**) flips it. Skill 100%, base 50% (1 of 2 keys). Verified from transcripts: base says "warn," skill says "error."

## The insight: two *kinds* of lift

This skill plus `variance-analysis` give two distinct lift signatures — and the station's tier curve tells them apart:

| Skill | Where the lift is | Tier behavior | What it means |
|---|---|---|---|
| `variance-analysis` | the **judgment** fixture (management-by-exception controllability) | lift **grows as the model weakens** (Opus 0 → Sonnet +33 → Haiku +22 on D) | the model *has the capability* but doesn't reliably *apply the judgment*; stronger models apply it more often |
| `generate-tests` | the **convention** fixture (relative→error severity) | lift is **flat across tiers** (+50 pp even on Opus) | a **house/arbitrary rule** the model *cannot know* — no amount of model strength guesses your convention |

So a skill earns its keep in (at least) two ways: encoding **judgment** the model under-applies, or encoding **conventions/rules** the model cannot infer. The flat-vs-declining tier curve is the tell — convention-lift survives the strongest model; judgment-lift erodes as the model improves. Both are exactly what the static critics (which only read the artifact) cannot see, and exactly what the execution-eval station measures.

## Process note — fixed output schemas (the grading fix)

The first run of this skill used free-form `{name, value}` "figures" and the grader matched values to keys by token. It produced garbage on S1/S2: models name fields wildly differently (`test_1_severity` vs `severity_row_level_absolute` vs `severity_amount_gte_0`), so the grader matched the wrong slot or missed it — manufacturing a fake S1 "lift" and a fake S2 "0/0". Reading the transcripts caught it (the *values* were correct; the *matching* was broken). The fix: a **fixed per-fixture output schema** (enum fields for severities and yes/no, named fields graded by exact lookup). No name-matching, no fragility. This is the general lesson for the station — **constrain the eval's output to the exact gradeable fields**, don't grade free-form prose.
