<!-- iteration: 0 -->
# Presentation conventions

Read this when executing Step 10 of `SKILL.md` (emitting the deliverable). These
conventions keep the output readable and — more importantly — keep rounding from
silently breaking the cross-foot discipline Step 7 requires.

## Unit discipline

Pick one display unit for the whole deliverable — $K (thousands) or $M (millions) —
and hold it throughout every schedule and the rollup. State the unit once, visibly, at
the top of the deliverable (e.g., "all figures in $000s unless noted"). Don't mix units
across schedules within the same document (e.g., revenue in $M and opex in $K) — it
invites misreads and makes a cross-foot check by eye unreliable.

## Negative numbers

Show negative or subtracted figures in parentheses, not with a leading minus sign —
`(12,500)` rather than `-12,500`. This is the standard financial-statement convention
and makes the rollup (Revenue less Variable costs, less Fixed/Stepped, etc.) readable
as a vertical subtraction at a glance.

## Rounding discipline — the cross-foot trap

**Round only for final display, never for intermediate calculation.** Carry full
precision through every formula in Steps 3–8, and apply rounding only at the moment a
number is written into the deliverable. Rounding intermediate values (e.g., rounding a
prorated personnel cost to the nearest thousand before summing it into the annual
total) is a common, quiet source of cross-foot drift — the displayed quarterly figures
won't sum to the displayed annual figure by a few dollars, and a reader will
(correctly) flag that as an arithmetic error even though the underlying math was
right. If a displayed cross-foot is going to be off by a rounding residual, say so
explicitly (e.g., "sums to annual total within rounding") rather than leaving an
unexplained few-dollar gap.

## Cross-footing as a display habit, not just a check

Don't just verify the cross-foot internally and then show only the final numbers —
show the arithmetic. A revenue schedule should visibly display the four quarterly
figures and their sum next to the stated annual total, so the reader can verify the
cross-foot without recomputing it themselves. This is the same discipline as Step 7 of
`SKILL.md`, applied to what actually gets printed, not just to what gets computed
internally.
