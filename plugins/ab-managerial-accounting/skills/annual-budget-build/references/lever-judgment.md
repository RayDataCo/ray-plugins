<!-- iteration: 0 -->
# Lever judgment — legitimate vs. red-flag gap-closing moves

Read this when executing Step 9 of `SKILL.md` (only relevant when a target and
candidate levers are given). This is the full discriminator, the tell it hinges on, and
why the distinction matters — not just the one-line summary in the SKILL.md body.

## The discriminator

For each candidate lever, ask one question: **is it traceable to a specific,
verifiable operational cause?**

**Legitimate — traceable operational cause.** Examples:
- A hiring-date change (pushing a planned hire from Q2 to Q3, if the hiring plan
  actually supports that timeline).
- A signed sublease or a completed vendor renegotiation (a document exists; the
  savings are contractual, not aspirational).
- A driver-supported volume or price change backed by pipeline, backlog, or capacity
  evidence — a specific set of customer commitments or a specific capacity expansion,
  not "we think we can sell more."

**Red flag — backward-solved from the target.** Examples:
- An unsupported volume or price assumption with no pipeline, backlog, or capacity
  change behind it — the number moved because the target needed it to, not because
  anything in the business changed.
- An opex-to-capex reclassification with no underlying capitalization event — nothing
  was actually acquired or built; a cost simply got relabeled to leave EBITDA (which
  the reclassification doesn't touch the same way D&A does).
- Holding a stepped cost flat through a threshold that operational data already show
  will occur — quietly declining to apply Step 5's stepped-cost jump because
  recognizing it would blow the target.

## The tell: near-closure without cause

**A lever that closes the gap almost exactly, with no operational cause offered, is
itself the diagnostic tell.** Reject it *on that basis* — the suspicious precision is
the evidence, not something to be reasoned around. A real operational change (a
contract, a hiring date, a signed lease) was sized by the business event that caused
it, not by the size of the gap it happens to close. When a candidate lever's dollar
value lines up unusually well with the residual gap and there's no paper trail behind
it, that alignment is diagnostic of backward-solving, not evidence of a well-timed
coincidence.

## Applying the gate

1. Evaluate every candidate lever independently against the discriminator above.
2. Apply legitimate levers only, and recompute EBITDA after each one.
3. If a residual gap remains after all legitimate levers are applied, **report it
   honestly** — options are to escalate for a target reset, search for additional
   legitimate levers, or flag the shortfall plainly in the narrative. Do not manufacture
   or accept a lever sized specifically to close the remaining number.
4. This discriminator is a general rule, not a lookup table — apply it to any lever the
   user proposes, including ones that don't resemble a prior example.

## Why this matters: the underlying dynamic

The legitimate/red-flag line exists because budgeting sits at the intersection of two
kinds of asymmetric information: **operator knowledge** (the people building the
budget know the real drivers better than whoever set the target) and **approval
authority** (the target-setter controls whether the budget gets approved). Two
corruptions of that tension point in opposite directions but share the same root cause:

- **Sandbagging / padding** — building slack into the *original* budget (understating
  revenue, overstating cost) so the bar is easy to clear later. This is a bias risk at
  budget-construction time, before a target comparison even happens.
- **Ratchet effect / target-forcing** — once a target is set and a gap appears, using
  operator knowledge not to report the true state of the business but to reverse-engineer
  whatever combination of assumptions makes the arithmetic match what approval requires.
  This is the dynamic Step 9's discriminator exists to catch.

Both corruptions use the same lever — the fact that the budget-builder knows more about
the true drivers than the reviewer does — to defeat the purpose of budgeting as an
honest planning and coordination tool. The discriminator (cause-traceable vs.
backward-solved) is the check that keeps the gap-closing step from becoming a second,
hidden channel for the same corruption.
