<!-- iteration: 0 -->
# Formula card — annual-budget-build

Read this when executing Steps 3, 4, 6, or 8 of `SKILL.md`. These are the canonical
formulas; every schedule the skill produces is built from this card, not a
paraphrase of it.

## 1. Revenue — driver-based, price × volume

```
Revenue(period) = Price(period) × Volume(period)
```
Computed per segment per period, summed across segments for the company total, summed
across periods for the annual total.

**Mid-year change timing rule.** If price or volume changes mid-year, the new value
applies **only to periods at or after the effective date** — never averaged across the
full year, never applied retroactively to periods before the change.

*Example.* Segment volume: Q1 100, Q2 100, Q3 110, Q4 110 units. Price: $500/unit
through Q2, $550/unit effective July 1 (start of Q3).
- Correct: Q1 = 100×500 = 50,000; Q2 = 100×500 = 50,000; Q3 = 110×550 = 60,500;
  Q4 = 110×550 = 60,500. **Annual = 221,000.**
- Wrong (averaging): treating price as a blended $525 all year — Q1–Q4 at $525 ×
  actual volumes = 220,500. Silently wrong by 500, and the error compounds whenever
  volume also changes across the same boundary — the averaging hides two independent
  timing errors inside one number.

## 2. Personnel — loaded rate, generalized proration

```
Loaded annual cost = Base salary × (1 + Benefits load % + Employer payroll tax %)
```
Use the loaded rate — never base salary alone — in every downstream line (opex driven
off headcount, cross-department allocations, etc.).

**Generalized mid-year proration.** For any role with a start date and/or end date
inside the budget year:
```
Prorated cost = Loaded annual cost × (Months employed ÷ 12)
              = Loaded annual cost × (Quarters employed ÷ 4)
```
Use whichever grain matches the schedule's phasing (quarterly by default). A role that
starts July 1 and runs through year-end is employed 2 of 4 quarters → 50% of the
loaded annual cost. A role that departs September 30 is employed 3 of 4 quarters → 75%.
The same formula shape applies to hires and departures — do not invent a different
proration mechanic for one direction vs. the other.

## 3. Capex → depreciation, in-service-date proration

```
Annual straight-line depreciation = (Asset cost − Salvage value) ÷ Useful life
```
**Proration.** An asset placed in service mid-year depreciates only for the fraction of
the budget year it was actually in service, keyed to the **in-service date** — not the
purchase date, not the fiscal year start:
```
Budget-year depreciation = Annual straight-line depreciation × (Months in service ÷ 12)
```
A $60,000 asset with $10,000 salvage and a 5-year life has a full annual depreciation
of (60,000−10,000)/5 = 10,000. Placed in service July 1 → in service 2 of 4 quarters →
budget-year depreciation = 10,000 × 50% = 5,000, landing 2,500 in Q3 and 2,500 in Q4.
Depreciation is a non-cash line: **excluded from EBITDA, included in EBIT** — carry it
separately so it is a clean, visible add-back rather than buried inside opex.

## 4. Rollup — fixed order, CM inclusion/exclusion rules

```
Revenue
  less Variable costs
= Contribution Margin (CM)
  less Fixed and Stepped opex
  less Personnel
= EBITDA
  less Depreciation & Amortization
= EBIT
```
**What belongs in the CM subtraction:** only true variable costs — lines with a
consistent unit rate against a driver (e.g., a flat % of revenue, a per-unit
fulfillment cost). **What does NOT belong in CM:** fixed opex, stepped opex, and
personnel — all three are excluded from the CM subtraction by definition and instead
land after CM, before EBITDA. Do not slide a stepped or fixed cost into the CM line
because it "behaves like" a variable cost in the period being examined — classification
is set once in Step 5 and carried through the rollup consistently.

**Gap formula** (when a target is given):
```
Gap = Target − Budgeted EBITDA
```
A positive gap means the budget falls short of target; apply Step 9's lever-judgment
gate before touching this number further.
