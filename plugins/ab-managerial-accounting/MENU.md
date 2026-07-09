# ab-managerial-accounting — Menu

**Status:** live · 5 skills shipped (eval-proven) · 5 tasks base-model-covered (registry) ·
lineage: continues `discipline-skills` 0.2.1

This is the packaged menu (source of truth, versioned with the plugin). It is the
**station roster** the [expo](skills/expo/) reads to decompose a request, select which
stations to fire, and compose their outputs. Every station listed here shipped with
two-arm execution-eval evidence (see `evals/`); every base-model-covered task carries
eval-verified coverage (see `base-model-covered/`).

Brigade surface: `mise` (readiness gate) → `service` (on/off) → `expo` (composes the
stations below). A single-station request routes to one skill; a compound request (e.g.
"complete due-diligence financial picture, last two years") fires several stations and
the expo synthesizes one answer.

## Route to a skill (live, eval-proven)

| When the situation is… | Route to | Eval headline |
|---|---|---|
| Actual vs standard/budget prices, rates, quantities, hours — compute, decompose, label F/U, assign responsibility, interpret | `variance-analysis` | 5/5 critic axes; judgment lift on management-by-exception (sonnet +0.33, haiku +0.22 on fixture D) |
| Build a full-year / multi-quarter operating budget from drivers (revenue build, personnel proration, fixed/variable/stepped opex, capex→depreciation, quarterly rollup) | `annual-budget-build` | win +0.33 — base fell for the mid-year-hire no-proration trap |
| Month-end close: accruals w/ paired reversals, prepaid amortization, cutoff corrections, BLOCK/ADJUST/WAIVE triage | `close-management` | wins +0.33/+0.67 — base sign-errors on accrual-reversal and correcting-entry P&L effects |
| Near-term liquidity from statements + facility terms: ratio battery, CCC, available liquidity, covenant headroom | `treasury-liquidity-analysis` | win +0.67 — base hit the restricted-cash trap (quick ratio 1.30 vs 1.23) |
| Single-instrument debt mechanics: amortization table, floating-rate day-count, covenant test, refinance breakeven | `debt-schedule` | the tier-floor asset: haiku 0% → 100% on the annuity payment formula; deploy on cheap tiers with confidence |

## Base-model-covered (no skill needed — exemplar prompts in `base-model-covered/`)

The 2026 sonnet-tier base model performs these smoothly without custom instructions;
each registry doc carries two verbatim exemplar prompts + the eval evidence + a
regression-tripwire re-check procedure. Coverage confirmed twice: original fixtures AND
a hardened re-eval (difficulty-hardened fixtures stayed non-discriminating).

- `rolling-forecast-update` · `financial-statements` · `cash-flow-forecasting` ·
  `reconciliation` · `capital-budgeting-analysis`

## Not on the menu (known gaps, honest status)

- `management-reporting-package` — real quality lift measured (base 5–7/10 rubric
  criteria → 9/10 with skill) but all samples fail criterion 8 (number traceability);
  held for refire. Ships when the gap closes.

## Disambiguation quick rules

- After-the-fact "why did we miss budget" → `variance-analysis`, not `annual-budget-build`.
- Re-projecting an approved budget against actuals → base-model-covered
  `rolling-forecast-update` exemplar, not `annual-budget-build`.
- Tying a balance to independent support → base-model-covered `reconciliation` exemplar,
  not `close-management`.
- NPV/IRR/payback project appraisal → base-model-covered `capital-budgeting-analysis`
  exemplar, not `debt-schedule` or `annual-budget-build`.
- Whole-org forward weekly cash view → base-model-covered `cash-flow-forecasting`
  exemplar, not `treasury-liquidity-analysis` (point-in-time ratios) or `debt-schedule`
  (single instrument).
