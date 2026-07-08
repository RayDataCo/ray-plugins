<!-- iteration: 0 -->
# Budgeting approaches — methodology taxonomy

**Lazy-load this file only when the ask concerns which budgeting methodology to
apply — not for a standard driver-based build.** If the user hands you segment
drivers, a headcount plan, an opex list, and a capex plan and asks for a budget, you
don't need this file; go straight to `SKILL.md`'s procedure. Load this file when the
question is closer to "how should we approach next year's budget process" or "is
zero-based right for us this year."

## Incremental budgeting

Start from the prior period's actual or budgeted figures and adjust by a percentage or
fixed amount ("last year plus 3%"). Fast, low-effort, and preserves continuity — but it
inherits whatever inefficiency or slack was already baked into the prior period, and it
doesn't force a fresh look at whether a cost line is still justified.

## Zero-based budgeting (ZBB)

Every line starts at zero each cycle; the owner must justify the full amount from
first principles, not just the delta from last year. Forces re-justification and can
surface costs that persisted only because nobody questioned them — but it is
significantly more effort per cycle and is usually applied selectively (a rotating
subset of cost centers each year) rather than to the entire budget every cycle.

## Driver-based budgeting

Build each line from the operational driver that actually causes it — volume × price
for revenue, headcount × loaded rate for personnel, a usage driver × rate for variable
opex — rather than from a prior-period baseline. This is the approach `annual-budget-build`
implements: it produces a budget that changes correctly when the underlying business
assumptions change, because every line is traceable back to a driver rather than to
last year's number. Most rigorous, most defensible under a lever-judgment gate (Step
9), and the natural fit whenever driver data is actually available — which is the
default case this skill is built for.

## Flexible budgeting

Instead of a single static budget, build the budget as a function of the driver (e.g.,
"opex = $X fixed + $Y per unit"), so it can be recast at different volume levels after
the fact for comparison against actuals. This is the input structure variance-analysis
consumes downstream — a flexible budget requires the same fixed/variable/stepped
classification discipline as Step 5 of this skill, but recasting it against actuals is
out of this skill's scope (see `SKILL.md`'s scope fence — that's variance-analysis's
job, not this skill's).

## Choosing among them

Driver-based is the default and the one this skill executes end-to-end. Incremental is
appropriate for genuinely stable, low-scrutiny cost centers where the effort of a full
driver rebuild isn't justified. Zero-based is appropriate when a cost center is
suspected of carrying slack and leadership wants forced re-justification. Flexible
budgeting is a presentation/analysis structure layered on top of a driver-based build,
not a competing construction method — most driver-based budgets can be recast as
flexible budgets with no additional data.
