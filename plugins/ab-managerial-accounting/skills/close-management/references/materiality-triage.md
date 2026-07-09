<!-- iteration: 1 -->
# Materiality Triage & Close-Lock Process — Full Method

Read this when executing SKILL.md Steps 1, 6, and 7.

## The three-axis triage method

Every open item at a close checkpoint gets exactly one verdict — **BLOCK** (hold the close open), **POST-CLOSE ADJUST** (let close proceed; handle via a controlled entry now or shortly after), or **WAIVE** (no special entry needed) — determined by applying all three axes below, in order, to each item individually. The axes are co-equal and independently decisive: any one of them alone can determine the verdict, and none of them should be treated as a tie-breaker subordinate to the others.

**Axis (a) — quantitative threshold.** The stated materiality threshold, expressed as a flat dollar amount or a percentage of a stated base (e.g. revenue, net income, total assets). An item's point estimate is compared against this threshold as the first-pass read. This axis alone is the naive/incomplete approach — it is necessary but never sufficient.

**Axis (b) — estimation-uncertainty width.** Look at the item's *plausible range*, not just its point estimate. Two failure directions:
- A **point estimate under threshold but with a wide range that crosses or approaches the threshold** should be treated as unresolved (lean toward POST-CLOSE ADJUST or BLOCK depending on how close and how uncertain), even though the point estimate alone would waive it.
- A **point estimate over threshold but with a very tight, well-bounded range** (a firm number is imminent, or the range barely moves) can safely proceed as POST-CLOSE ADJUST rather than BLOCK — the size is real, but there's no meaningful risk that waiting to book it changes the close's overall reliability, because the number won't move.

**Axis (c) — qualitative overrides.** Two categories that can force BLOCK regardless of dollar size:
- **Control-integrity concerns** — an unexplained reconciliation variance, a suspected error, a process breakdown. These indicate the underlying data might not be trustworthy at all, which is a different kind of risk than "we don't know the exact number yet."
- **Disclosure/classification concerns** — items requiring special handling regardless of size, most commonly **related-party transactions**, which carry disclosure obligations independent of their dollar materiality. A $500 related-party payment can still require disclosure-level scrutiny that a $50,000 arm's-length item doesn't.

Run the qualitative-override check on **every item**, not only the ones that already cleared the dollar threshold — a qualitative override is exactly what catches the item that looks safely immaterial by size alone.

## Naming the deciding factor

Every verdict must state which axis actually drove it — never a bare "BLOCK" or "WAIVE" with no reasoning attached. Use one of: "quantitative threshold" (the point estimate alone crossed it and nothing else is in play), "estimation-uncertainty width" (the range, not the point estimate, drove the call), or the specific named qualitative override ("related-party disclosure," "unexplained reconciliation variance," etc.). This is what makes the triage table auditable — a reviewer should be able to read the deciding-factor column alone and understand why each verdict landed where it did, without re-deriving the reasoning.

## Close-lock and post-close-adjustment process

**Documentation requirements.** Any item routed to POST-CLOSE ADJUST or discovered after lock must be documented with: the proposed entry (full Dr/Cr), its dollar impact, its justification (why the entry is needed and how the amount was derived), the approver (controller or CFO, scaled to the item's materiality — larger or more sensitive items need higher sign-off), and the posting date. This creates an audit trail that survives review; a locked period is never edited silently.

**Immaterial-vs-material routing.** Immaterial items discovered after lock are typically **not** posted back into the locked period at all — they're picked up in the current open period instead, since reopening a closed period for something below materiality isn't worth the audit-trail cost. Material items, by contrast, go through the formal post-close-adjustment process into the period they actually belong to, precisely because leaving them in the wrong period would itself become a material misstatement.

**Restatement escalation.** If a material item is discovered after the period has already been externally reported (financials issued, filed, or shared with external stakeholders), the process escalates beyond a normal post-close adjustment into restatement territory — this requires disclosure, typically legal/audit involvement, and is a materially higher-stakes process than adjusting a period that's merely internally locked but not yet externally reported. Flag this distinction explicitly whenever an item's locked period has already been externally reported.

## Soft-close vs. hard-close judgment

Not every month-end close carries the same rigor. A **soft close** (common in interim months) may accept looser estimates, skip some reconciliations, or tolerate a wider triage tolerance band, on the understanding that the numbers are directional and will be tightened at the next hard close. A **hard close** (typically quarter-end and year-end, especially when externally reported) demands full rigor — every item triaged properly, every reconciliation complete, no shortcuts.

The risk with soft closes is **accumulating drift**: if the same looseness that's appropriate for a single soft-close month gets applied repeatedly, small unaddressed items compound, and by the time a hard close arrives, what should have been a routine tightening becomes a scramble to catch multiple periods' worth of deferred rigor at once. When operating in soft-close mode, name it explicitly and flag any item that's being carried forward on the assumption "we'll deal with this at hard close" — don't let that assumption go unstated.

## Close-calendar dependency-management responses

When a triage decision turns on whether to hold the close open for a late input (a subledger not yet closed, a vendor confirmation not yet received, an estimate not yet firm), three responses are available, and the choice should be named explicitly as part of the verdict:

1. **Absorb-with-buffer** — the close calendar has slack (e.g., not yet at the final close day), so simply wait for the input; no compromise needed. Appropriate early in the close window.
2. **Proceed-on-flagged-preliminary** — close on schedule using a preliminary/estimated figure for the late item, explicitly flagged as preliminary, with a committed follow-up to true it up in the next period or via post-close adjustment once the firm number arrives. Appropriate when the estimate is reasonably tight (low estimation-uncertainty width) and the close calendar has no slack left.
3. **Escalate-and-hold** — stop the close and escalate to the controller/CFO for a go/no-go call, appropriate when the missing input carries high estimation-uncertainty width or a qualitative override (control-integrity, disclosure) that makes proceeding on an estimate genuinely risky.

The close-day position noted in SKILL.md Step 1 (e.g. "day+3 of a five-day close") is what determines how much slack remains for option 1 versus needing to fall back to option 2 or 3.
