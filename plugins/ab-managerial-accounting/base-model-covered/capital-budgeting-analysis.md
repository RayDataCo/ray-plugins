# capital-budgeting-analysis — base-model covered

Capital-budgeting-analysis covers project-appraisal mechanics: NPV, simple and discounted payback
period, and profitability index for a single project's after-tax cash flow stream against a
stated discount rate; derivation of annual after-tax operating cash flow from revenue, cash
operating costs, straight-line depreciation, and a tax rate; ranking of two mutually exclusive
projects by NPV and IRR (including the NPV/IRR conflict and the crossover discount rate), and
structured judgment beyond the NPV number — customer-concentration and asset-specificity risk on
an otherwise-positive-NPV contract, and real-option/pilot-entry framing on an otherwise-negative
standalone NPV.

## Exemplar prompts

### Exemplar 1 (fixture A — single-project NPV, payback, profitability index)

> A company is evaluating the purchase of a new machine with an installed cost of $400,000, paid entirely at time zero (t=0). The discount rate (hurdle rate / WACC) for this project is 10%. The machine is expected to generate the following after-tax cash flows, which are already stated on an incremental, after-tax basis:
>
> Year 1: $100,000
> Year 2: $140,000
> Year 3: $120,000
> Year 4: $110,000
> Year 5: $80,000

### Exemplar 2 (fixture C — mutually exclusive projects, NPV/IRR conflict, crossover rate)

> Two mutually exclusive projects, S and L, are being evaluated at the firm's 10% hurdle rate. Project S requires an initial outlay of $150,000 at t=0 and generates a level after-tax cash flow of $55,000 per year for 5 years (years 1-5). Project L requires an initial outlay of $400,000 at t=0 and generates a level after-tax cash flow of $125,000 per year for 5 years (years 1-5).

## Evidence

Two-arm execution eval, base model (no skill) vs. base model + draft skill, n=3 samples per
fixture, graded deterministically against a fixed answer key (kept private with the eval
harness, not reproduced here).

| fixture | base pass rate | tier | eval date |
|---|---|---|---|
| A | 3/3\* | sonnet | 2026-07-08 |
| B | 3/3 | sonnet | 2026-07-08 |
| C | 3/3 | sonnet | 2026-07-08 |
| D | 3/3 | sonnet | 2026-07-08 |

**Note:** fixture A's raw base score in `EVAL-RESULTS-2026-07-08.json` is 2/3 (`class: "flat"`,
missed on the `npv` field at its stated ±5 tolerance). The evals doc's "held back" section
documents this as one of two verified-false anomalies among the five INCONCLUSIVE tasks: the
grading tolerance was tighter than the oracle's own disclosed rounding drift, not a genuine
base-model computation error (the skill arm missed the same tolerance too, by a wider margin, so
this was not a skill-vs-base discriminator either). Corrected reading treats fixture A as
at-ceiling, consistent with the rest of the suite. (Exact figures withheld here — they double as
the fixture's grading key.)

## Regression note

This coverage claim holds for sonnet-tier, 2026-07-08. On any base-model or tier change adopted
for finance work, re-run `eval/fixtures.json` for this task against the new model. If any fixture
drops below 3/3, promote capital-budgeting-analysis to a built skill via the ab-skill-factory
factory, using the regressing fixture as the oracle case.
