---
name: close-management
description: "Runs the month-end close: books expense accruals with mandatory paired reversals (net next-period P&L effect, two-period total), builds prepaid amortization schedules zeroing out at benefit-period end, diagnoses cutoff violations with two-sided correcting entries (correct-period booking plus wrong-period back-out, before/after P&L), and triages open items into BLOCK / POST-CLOSE ADJUST / WAIVE using a materiality threshold plus estimation-uncertainty width plus qualitative overrides (control-integrity, related-party) that can force BLOCK below threshold. Use for close-task lists, accrual/cutoff/prepaid facts, or open items at a close-day checkpoint, including CPA/CMA FAR-style problems. Do NOT use for reconciliation (tying a balance to independent support), financial-statements (building statements from a locked trial balance), variance-analysis (explaining a budget-vs-actual gap by cause), or a generic close-checklist request with no dates, amounts, or thresholds to compute."
iteration: 1
---

# Close Management

Run the month-end close: compute accruals with mandatory reversals, apply cutoff discipline, build prepaid amortization schedules, and triage open items into BLOCK / POST-CLOSE ADJUST / WAIVE. This skill runs the close process up to a clean, locked, reconciled set of GL balances. It does not perform reconciliation, build financial statements, or analyze budget-vs-actual variance — see "When NOT to use this skill" below.

## When NOT to use this skill

Redirect immediately rather than attempting the task:

- **Reconciliation** — tying an already-recorded GL balance to independent supporting detail ("why doesn't this bank rec tie out," "reconcile the subledger to the GL," "explain this reconciliation variance"). This skill triages what a reconciliation finds; it does not perform the reconciliation itself.
- **Financial-statements** — assembling the income statement, balance sheet, or cash flow statement from an already-locked, clean trial balance ("prepare our statements from this trial balance"). This skill's job ends at a clean, locked GL; what gets built from it is a separate downstream skill.
- **Variance-analysis** — explaining a budget-vs-actual gap by cause ("why did marketing come in over budget," "decompose this into price and volume effects"). This skill reads flux only as an input to catching close errors before lock, not to explain why a number moved.
- **Generic close-checklist/calendar requests** with no dates, dollar amounts, or thresholds to compute against ("build us a close calendar template"). There is nothing here to run the procedure on — say so and ask for the missing facts rather than producing a generic template.

## Procedure

Work these steps in order for whichever capability(ies) the ask requires. Each step names the pitfall it exists to kill.

**1. Confirm scope and close-day position.** Decide which capability is in play — accrual+reversal, cutoff correction, prepaid schedule, materiality triage, or a combined review touching several — and state it before computing. If given, note the close-day position (e.g. "day+3 of a five-day close") — it governs triage slack in Step 6. If the ask is actually reconciliation, financial-statements, or variance-analysis, stop and redirect (see above) instead of attempting it.

**2. Verify subledgers are cut off before trusting anything downstream.** Accruals, cutoff corrections, and triage are only reliable once every feeding subledger (AP, AR, fixed assets, payroll, inventory, revenue/billing) has closed for the period — a subledger closing late cascades forward through every later stage. If an input implies a subledger is still open, name that explicitly as a caveat; never silently compute on top of it. *(Kills: treating accrual/cutoff/triage output as final when a feeding subledger hasn't actually cut off.)*

**3. Book each expense accrual with its mandatory paired reversal.** Name the estimating signal used (PO, SOW milestone, vendor verbal confirmation, timesheet, prior-invoice run-rate). Book:
```
Dr [Expense account]              [estimate]
    Cr Accrued Liabilities            [estimate]
```
then always generate the reversing entry, dated the first day of next period:
```
Dr Accrued Liabilities            [estimate]
    Cr [Expense account]              [estimate]
```
When the actual invoice is known, show the actual-invoice entry (`Dr Expense / Cr Accounts Payable`, actual amount), the **net next-period P&L effect** (actual − reversed estimate), and the **two-period combined total**, which must equal the actual invoice amount exactly. *(Kills: presenting an accrual without its reversal — this leaves the estimate AND the actual both expensed, double-counting the cost by the full un-reversed estimate the moment the invoice posts, and leaves Accrued Liabilities permanently uncleared. Never show one without the other.)* Full mechanic + estimate-bias patterns: `references/accrual-mechanics.md`.

**4. Apply cutoff discipline; correct violations two-sided.** Assign every cost to the period the good was received or the service performed — never the invoice date or the payment date. On a violation:
1. Book a correcting accrual **in the period the item actually belongs to** (`Dr Expense / Cr Accrued Liabilities`, Step 3's pattern).
2. Reverse that correcting accrual out of the wrong period using Step 3's own reversal mechanic (`Dr Accrued Liabilities / Cr Expense`) — dated the first day of the wrong period's close-out.
3. Leave the actual invoice, when it genuinely posts through its own subledger on its real invoice date, standing untouched as its own third leg (`Dr Expense / Cr Accounts Payable`) — it is a real liability to the vendor and is never zeroed out by a period-assignment fix.

Show a before/after table of each period's P&L effect and state the two-period combined total, which is **identical before and after** the correction — a period-assignment error, not a total-dollar error. That invariance is exactly why the error is dangerous: it looks invisible in a trailing/quarterly view while still misstating each individual month for trend analysis, budget comparisons, or any month-specific KPI. *(Kills: reversing only the wrong-period entry without ever booking the correct-period one — that drops the cost from both periods entirely, a worse outcome than the original single-period misstatement. Also kills: netting the correction against Accounts Payable instead of Accrued Liabilities — that erases a real, still-owed vendor liability from the books.)* Full period-assignment rules + before/after method: `references/cutoff-discipline.md`.

**5. Build or update the prepaid amortization schedule.** Capitalize the payment (`Dr Prepaid [type] / Cr Cash`), compute the straight-line monthly rate (payment ÷ months of benefit), and produce the month-by-month schedule: amortization booked (`Dr Expense / Cr Prepaid`), cumulative amortization, and remaining prepaid balance. **Always confirm the schedule zeroes out exactly at the end of the benefit period** — a balance that doesn't zero on schedule, or goes negative, is itself a close-quality signal worth flagging. *(Kills: expensing the full payment at the cash date instead of capitalizing and amortizing — the resulting P&L overstatement in the payment period plus the P&L understatement in every later period within the fiscal year exactly equals the balance-sheet asset understatement at period-end.)* Full mechanic + distortion math: `references/prepaid-amortization.md`.

**6. Run materiality-based close triage, item by item, on all three axes — never the dollar threshold alone.** For each open item at the close-day checkpoint, apply in order: (a) the **stated quantitative threshold** (flat dollar or % of a base); (b) **estimation-uncertainty width** — if the item's plausible range (not just its point estimate) approaches or crosses the threshold, or a firm number is imminent, treat it as unresolved even if the point estimate looks acceptable; (c) **qualitative overrides** — control-integrity concerns (an unexplained reconciliation variance, a suspected error) or disclosure/classification concerns (e.g. related-party transactions) can force BLOCK regardless of dollar size. Assign each item exactly one verdict — **BLOCK** / **POST-CLOSE ADJUST** / **WAIVE** — and always name the deciding factor explicitly, never a bare label. *(Kills: mechanically applying only the dollar threshold — a large, tightly-estimable item can safely post-close-adjust while a small, qualitatively-sensitive item must block.)* Full three-axis method + close-lock process: `references/materiality-triage.md`.

**7. Route any item landing in an already-locked period through formal post-close adjustment.** Document the proposed entry, its dollar impact, its justification, the approver (controller/CFO per materiality), and the posting date — never silently edit a locked period. Immaterial items are typically picked up in the current open period instead of reopening a closed one. *(Kills: silently reopening or back-posting a locked period without an audit trail.)*

**8. Emit the deliverable.** Show every entry with full Dr/Cr, the estimate/actual reconciliation where applicable, the specific rule or threshold applied, and any period-spanning cross-foot. Never present a bare number without its derivation. Use the output contract below.

## Output contract

Include only the sections for the capability(ies) actually invoked, in this order:

1. **Scope line** — which capability(ies) were exercised, and the close-day position if given.
2. **Accrual + reversal** — Dr/Cr pairs, net next-period P&L effect, two-period-total cross-check.
3. **Cutoff correction** — the two-sided entries, the before/after P&L table, the invariant two-period total.
4. **Prepaid schedule** — the month-by-month table and the zero-out confirmation (or an explicit flag if it fails).
5. **Materiality triage table** — columns: `item | amount/range | quantitative read | uncertainty-width read | qualitative override check | verdict | deciding factor`.
6. **Post-close-adjustment note** — impact, justification, approver, posting date, for any locked-period item.
7. **Caveats** — assumed or missing inputs, including unconfirmed subledger-close status.

## Reference files

- `references/accrual-mechanics.md` — read for Step 3: the full accrual/reversal mechanic, systems-flagged auto-reversal note, estimate-bias patterns, true-up-direction KPI diagnostic.
- `references/cutoff-discipline.md` — read for Step 4: period-assignment governing rules, the before/after table method, the one-sided-correction trap fully worked.
- `references/prepaid-amortization.md` — read for Step 5: the capitalize/amortize mechanic, the zero-out check, the full expensed-at-cash-date distortion math.
- `references/materiality-triage.md` — read for Steps 1, 6, and 7: the three-axis method, the close-lock/post-close-adjustment process, the soft-close-vs-hard-close judgment, and close-calendar dependency-management responses.
- `references/worked-examples.md` — pattern-match against these four fixtures before answering a multi-element close request.
