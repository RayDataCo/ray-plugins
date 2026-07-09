---
name: annual-budget-build
iteration: 0
description: 'Construct an annual operating budget from driver assumptions: driver-based revenue build (price x volume by segment, mid-year changes), loaded-rate personnel build with mid-year hire/departure proration, opex classified fixed/variable/stepped, capex-to-depreciation schedule (mid-year proration), and a quarterly-phased contribution-margin/EBITDA rollup - plus judging which moves legitimately close a budget-to-target gap and which are red flags. Use whenever the user gives revenue drivers, a headcount plan, an opex list needing cost-behavior classification, or a capex plan and wants a full-year or multi-quarter operating budget constructed from scratch (including CMA-style master-budget problems). Do NOT use for rolling-forecast-update (re-projecting an approved budget against actuals), variance-analysis (after-the-fact actual-vs-budget explanation), or capital-budgeting-analysis (NPV/IRR/payback appraisal of a capital project).'
---

# Annual Budget Build

## The one job

Given segment revenue drivers, a headcount/hiring plan, a classified opex list, and a
capex plan, build a correct, quarterly-phased annual operating budget — revenue,
personnel, opex, capex/depreciation, and a CM/EBITDA/EBIT rollup — and, when a target
is given, a defensible legitimate-vs-red-flag judgment on candidate gap-closing levers.
Every mid-year event is prorated to the exact fraction of the year it affects, every
schedule cross-foots, and no lever gets a pass just because it makes the arithmetic
close.

**Scope fence — do NOT use this skill for:**
- **Rolling-forecast-update** — re-projecting an *already-approved* budget against actuals in-year.
- **Variance-analysis** — after-the-fact actual-vs-budget decomposition.
- **Capital-budgeting-analysis** — NPV/IRR/payback appraisal of a single capital project in isolation. (Folding an *already-decided* capex line into the Step 6 depreciation bridge IS in scope; deciding whether to make the purchase is not.)

If the ask is one of these three, or a bare "give us a budget template" with no driver
data to build from, say so and redirect — don't attempt it here.

## Procedure

**Step 1 — Confirm scope.** Decide which of {revenue, personnel, opex,
capex/depreciation, EBITDA-vs-target} are in play from the ask + data present. If the
ask is actually rolling-forecast-update, variance-analysis, or
capital-budgeting-analysis, stop and redirect — wrong skill. State which schedules you
will build before building them.

**Step 2 — Build the input inventory.** Per segment: volume/price by period + effective
date of any mid-year change. Per role group: headcount, base salary, start/end date,
benefits load %, payroll tax %. Per opex line: fixed/variable/stepped, rate or flat
amount, driver, and (if stepped) threshold + tier pricing. Per asset: cost, salvage,
useful life, in-service date. If a target is given: the figure + candidate levers. Name
missing inputs explicitly — never assume silently.

**Step 3 — Revenue schedule.** `Revenue = Price × Volume`, per segment per period,
summed to company total. A mid-year price or volume change lands only in periods at/after
its effective date — never averaged across the full year, never applied retroactively.

**Step 4 — Personnel schedule.**
`Loaded annual cost = Base salary × (1 + benefits load % + payroll tax %)`. Use the
loaded rate — never base salary alone — in every downstream cost line. Prorate any
mid-year hire/departure to the exact fraction of the year on payroll (months ÷ 12, or
quarters ÷ 4): a July 1 hire contributes 50% of annualized loaded cost, not 100%.

**Step 5 — Opex schedule.** Fixed = flat/period, independent of driver. Variable = rate
× that period's driver value. Stepped = flat within a band, then a discrete jump the
exact period the driver crosses the threshold, tied to the same driver used elsewhere
in the budget. A stepped cost is never smoothed into a per-unit rate, and never held
flat through a threshold it has already crossed. See `references/cost-classification.md`
for the full decision tree and threshold-sensitivity discipline.

**Step 6 — Capex / depreciation bridge.**
`Annual straight-line depreciation = (Asset cost − Salvage value) / Useful life`.
Prorate to the asset's actual in-service duration within the budget year, keyed to the
**in-service date** (not purchase date, not fiscal year start): a July 1 in-service
asset gets 50% of full annual depreciation. Track depreciation as its own line —
excluded from EBITDA, included in EBIT — so it's a clean add-back.

**Step 7 — Cross-foot everything.** Every quarterly schedule (revenue, personnel,
opex, depreciation) must sum to its stated annual total, arithmetic shown. Where inputs
support it, build the annual figure two ways — sum of quarters vs. recomputed from the
annual driver — to confirm they tie. A mismatch means a proration, classification, or
arithmetic error upstream; resolve before rolling up. Don't skip this to save steps.

**Step 8 — Roll up to CM / EBITDA / EBIT, fixed order:**
`Revenue → less Variable costs → Contribution Margin → less Fixed and Stepped opex →
less Personnel → EBITDA → less D&A → EBIT.`
Only true variable costs (a consistent unit rate against the driver) belong in the CM
subtraction — fixed, stepped, and personnel are excluded from CM by definition. If a
target is given: `Gap = Target − Budgeted EBITDA`. Full formula card:
`references/formulas.md`.

**Step 9 — Judge target-gap levers by cause, not arithmetic fit** (only when a target
+ candidate levers are given). Legitimate = traceable to a specific, verifiable
operational cause (hiring-date change, signed sublease/vendor renegotiation,
driver-supported volume/price backed by pipeline/backlog/capacity evidence). Red flag =
backward-solved from the target (unsupported assumption with no operational backing, an
opex-to-capex reclassification with no capitalization event, a stepped cost held flat
through a threshold operational data already show will occur) — **a lever that closes
the gap almost exactly with no operational cause offered is itself the diagnostic
tell; reject it on that basis, not despite it.** Apply legitimate levers only, recompute
EBITDA, and report any residual gap honestly rather than manufacturing a lever sized to
close it. Full discriminator + why it matters: `references/lever-judgment.md`.

**Step 10 — Emit the deliverable.** Always show the formula and the actual inputs
plugged in per line, not just the answer. Presentation discipline (units, negative-number
convention, rounding, cross-foot display habits): `references/presentation-conventions.md`.

## Output contract

Deliver, in order: (1) scope line — schedules being built, phasing grain, target/lever
analysis or not; (2) revenue schedule, cross-footed to FY; (3) personnel schedule,
loaded-rate + proration shown, cross-footed to FY; (4) opex schedule, classification
per line, cross-footed to FY; (5) capex/depreciation schedule, in-service proration
shown, cross-footed to FY; (6) CM/EBITDA/EBIT rollup, fixed order, cross-footed two
ways; (7) gap-to-target analysis if a target was given — every lever labeled
legitimate/red-flag with its discriminator, EBITDA recomputed after legitimate levers
only, residual gap reported honestly; (8) caveats — missing or assumed inputs and any
simplifying assumptions made (e.g., ignoring the FICA wage-base cap is a standard,
defensible simplification at the annual-budget level — but state it, don't leave it
silent).

## Reference files (load only what the step needs)

- `references/formulas.md` — read for Steps 3, 4, 6, 8: the full formula card (revenue timing example, generalized proration formula, depreciation proration, rollup order with CM inclusion/exclusion rules).
- `references/cost-classification.md` — read for Step 5: fixed/variable/stepped decision tree, stepped-cost cliff behavior, relevant-range and near-threshold sensitivity discipline.
- `references/lever-judgment.md` — read for Step 9: the legitimate/red-flag discriminator in full, the near-closure-is-the-tell rule, and the sandbagging/padding/ratchet dynamics that motivate it.
- `references/budgeting-approaches.md` — read only when the ask concerns *which budgeting methodology to apply* (incremental/zero-based/driver-based/flexible), not a standard driver-based build.
- `references/presentation-conventions.md` — read for Step 10: unit discipline, rounding, cross-foot display habits.
- `references/worked-examples.md` — pattern-match against these four fully-derived, cross-footed fixtures (revenue mid-year change, personnel proration with named traps, opex/stepped-cost + capex depreciation, EBITDA rollup + lever judgment) before answering a multi-component build.

## Reminder — three near-misses this skill declines

Rolling-forecast-update (re-projecting an approved budget against actuals),
variance-analysis (explaining an actual-vs-budget gap after the fact), and
capital-budgeting-analysis (appraising a single project's NPV/IRR/payback in
isolation) are different jobs. This skill builds the once-per-cycle baseline from
drivers; it does not re-project it, explain variances against it, or appraise a single
project's return. Redirect at Step 1 rather than attempting any of the three.
