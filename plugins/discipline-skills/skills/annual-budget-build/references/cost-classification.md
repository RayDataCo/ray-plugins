<!-- iteration: 0 -->
# Cost classification — fixed / variable / stepped

Read this when executing Step 5 of `SKILL.md`. This is the full decision tree behind
the one-line definitions in the SKILL.md body.

## Decision rules

**Fixed.** A flat amount per period, independent of the value of any driver. It does
not move whether the driver moves 5% or 50%. Example: base rent under a lease with no
usage clause.

**Variable.** A rate applied to a period's driver value, so the cost moves
proportionally with the driver every period:
```
Variable cost(period) = Rate × Driver value(period)
```
Example: a sales commission of 5% of that period's revenue. If revenue changes, the
cost changes in lockstep, period by period — there is no threshold, no band, just a
continuous rate.

**Stepped (semi-fixed).** Flat within a band of the driver, then a discrete jump the
exact period the driver crosses a threshold — tied to the *same* driver used elsewhere
in the budget (usually headcount or a capacity measure), not an independent metric
invented for this line alone. Example: a support-software license tier that costs
$2,000/quarter for headcount ≤ 20, and $3,200/quarter once headcount exceeds 20.

## The two misclassification traps (both kill conditions)

1. **Stepped treated as variable** — smoothing the step into a continuous per-unit
   rate that doesn't contractually exist (e.g., dividing the tier jump by headcount to
   manufacture an implied "$/head" rate and applying it every period). This invents
   smooth cost behavior the underlying contract doesn't have, and it will misstate
   every period, not just the threshold period.
2. **Stepped treated as fixed** — holding the cost flat through a threshold the driver
   has already crossed. This understates cost in every period after the crossing. The
   step must land the exact period the driver value crosses the stated threshold — not
   the period after, not smoothed in gradually.

## Threshold timing precision

When building the stepped line, cross-reference the driver's own schedule (e.g., the
personnel schedule's headcount by quarter) period by period. The jump happens in the
first period where the driver value satisfies the threshold condition — a headcount of
21 in Q3 triggers the higher tier starting Q3, even if headcount was 20 (at the
boundary, not over it) in Q2.

## Relevant-range and near-threshold sensitivity

Stepped costs are only "flat within a band" inside the relevant range the tiering was
priced for — don't extrapolate a tier's flat rate indefinitely past volumes or
headcounts the pricing was never designed to cover. When a driver assumption sits close
to a known step threshold (e.g., planned headcount is 19–21 against a threshold of 20,
inside normal hiring-plan variance), flag it explicitly in the Caveats section as a
sensitivity risk — a small miss on the driver assumption could flip which tier applies
and change the opex line materially. This is a disclosure obligation, not a reason to
avoid picking a base case.
