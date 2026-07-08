# Finance vertical — execution-eval evidence (2026-07-08)

Ten finance skills were built by the skill-agent-brigade (spec → tests → author ⇄ critic →
expo, all tickets `advance`) and then measured by the execution-eval station: two-arm
ablation (base model vs base model + skill) on the oracle fixtures from each skill's
acceptance contract, n=3 samples per arm, fixed per-fixture output schemas graded
deterministically in code (no name-matching), tier sweep (haiku/sonnet/opus) on two
skills. 334 eval agents, 0 errors.

**This PR ships only the four skills whose evals demonstrated lift.** Per-fixture classes
follow the execution-eval station contract: `win` (base had headroom, lift ≥ +0.33 at
n=3) · `non-discriminating` (base at ceiling — proves nothing either way) · `flat` ·
`regression`.

## Shipped (eval evidence)

| skill | deployment-tier evidence | headline |
|---|---|---|
| annual-budget-build | fixture B **win +0.33** (sonnet); A/C/D non-disc | Base fell for the no-proration trap on mid-year hires (answered $458,961 vs $365,613); skill arm 3/3 clean |
| close-management | A **win +0.33**, C **win +0.67** (sonnet); B non-disc; D flat | Base sign-errors on accrual-reversal and correcting-entry P&L effects; skill arm enforced the conventions. D (materiality triage) unlifted — both arms under-applied the stated threshold rule; known gap, documented |
| treasury-liquidity-analysis | A **win +0.67** (sonnet); B/C/D non-disc | Base literally hit the documented restricted-cash trap (quick ratio 1.30 vs 1.23); skill arm excluded restricted cash 3/3 |
| debt-schedule | haiku: A **win +1.00**, B **win +0.33**; sonnet/opus at ceiling | The tier-floor asset: haiku base 0/3 on the annuity payment formula → 3/3 with skill; ACT/360 discipline lifts haiku too. Value = minimum-viable-tier reduction, not sonnet-tier lift — deploy on cheap tiers with confidence |

## Held back (honest reasons, not failures)

- **management-reporting-package** (generative): real quality lift — base packs scored
  5–7/10 rubric criteria, skill packs 9/10 in all 3 samples — but all three fail exactly
  criterion 8 (every number traces to the input dataset). One named, fixable gap;
  refire before shipping.
- **rolling-forecast-update, financial-statements, cash-flow-forecasting,
  reconciliation, capital-budgeting-analysis**: INCONCLUSIVE — the 2026 sonnet base
  model is at ceiling on their textbook fixtures (all non-discriminating), so nothing
  could show lift. Not kills; fixtures need hardening (messier inputs, weaker-tier
  arms) before these can be judged. Two apparent negatives were verified false: a
  "regression" caused by a grading key demanding a magnitude where the source teaches a
  signed convention, and a "flat" caused by a tolerance tighter than the oracle's own
  disclosed rounding drift.

## Method notes (for reproducing)

- Oracle fixtures extracted from each skill's competency worked-examples (inputs +
  boxed answers only; judgment answers as fixed-option multiple choice).
- Grading is code, not LLM judgment, for computational skills; the generative skill is
  graded by rubric agents against 10 binary criteria with ground-truth key facts.
- Two kinds of lift observed, consistent with the 2026-06-29 findings: judgment lift
  (shrinks as models strengthen) and convention lift (persists — day-count, sign
  conventions, exclusion rules). A third measured this round: **tier-floor lift**
  (debt-schedule), where the skill's value is making the cheapest tier reliable.
