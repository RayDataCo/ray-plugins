<!-- iteration: 1 -->
# Cutoff Discipline — Full Mechanic

Read this when executing SKILL.md Step 4.

## Period-assignment governing rules

Cutoff discipline means assigning a transaction to the period the underlying economic event happened, never the period a document happened to be dated or paid in.

- **Expense cutoff — receiving-date rule.** An expense belongs to the period the goods were received or the service was performed, regardless of invoice date or payment date. Goods received December 30 belong in December even if the vendor doesn't invoice until January 5.
- **Revenue cutoff — ASC-606-style performance-obligation rule.** Revenue belongs to the period the performance obligation was satisfied (control of a good transferred, or a service performed), not the period cash was collected or an invoice was issued. A December delivery recognizes December revenue even if payment arrives in January.
- **AP cutoff window.** Most close processes hold the AP subledger open a few extra business days past period-end specifically to catch invoices that arrive late but relate to the prior period — this is a mechanical control, not a judgment call, and its whole purpose is to reduce (not eliminate) the need for manual cutoff corrections. When an item still slips past the AP cutoff window, the manual correction below is what catches it.

## The two-sided correction pattern

A cutoff violation exists when an item was (or is about to be) recorded in the wrong period under invoice-date convention. The correction always has three legs, not two entries loosely related — the sequencing matters:

**Leg 1 — book the item in the period it actually belongs to.**
```
Correct period (e.g. December):
Dr [Expense account]              [amount]
    Cr Accrued Liabilities            [amount]
```
This is a correcting accrual, using exactly Step 3's accrual pattern.

**Leg 2 — reverse that correcting accrual out of the wrong period, using Step 3's own reversal mechanic.**
```
Wrong period, day 1 (e.g. January):
Dr Accrued Liabilities            [amount]
    Cr [Expense account]              [amount]
```
This is the same `Dr Accrued Liabilities / Cr Expense` reversal Step 3 always generates for an accrual — cutoff correction is not a different mechanic, it is Step 3's accrual+reversal pair applied to a period-assignment problem instead of an estimate-vs-actual problem.

**Leg 3 — leave the actual invoice standing, untouched, as its own entry.** When the real invoice genuinely posts through the AP subledger on its real invoice date, it is a real, uncorrected liability to the vendor:
```
Wrong period (e.g. January), on the invoice's real date:
Dr [Expense account]              [actual amount]
    Cr Accounts Payable               [actual amount]
```
This leg is **never touched, netted, or reversed** by the cutoff correction. The vendor is genuinely owed this amount until it's paid; a period-assignment fix corrects which period recognized the *expense*, not whether the company owes the vendor money.

## Why Leg 3 must stay separate from Legs 1–2

The single most common execution error in cutoff correction is trying to "back out" the wrong-period entry by crediting Accounts Payable instead of Accrued Liabilities — i.e., treating Leg 2 as if it reverses Leg 3. It does not. Leg 2 reverses Leg 1 (the correcting accrual), which lives in Accrued Liabilities. Accounts Payable is a different account tracking a different fact (money owed to a specific vendor for a specific invoice) and must never be zeroed out as a side effect of a period-assignment correction — doing so would make it look like the company no longer owes the vendor, which is false until the invoice is actually paid.

Net effect of the correct three-leg treatment:
- **Accrued Liabilities**: Leg 1 credits it, Leg 2 debits it by the same amount → nets to exactly $0. No stale balance.
- **Accounts Payable**: Leg 3 credits it once → correctly retains the real payable until cash settles it.
- **Correct period's P&L**: gets the expense once, via Leg 1.
- **Wrong period's P&L**: Leg 2 (−amount) and Leg 3 (+amount) net to $0 — the wrong period ends up with no net P&L effect from this item, which is exactly right, because the cost doesn't belong there.

## Before/after table method

Present the correction as a before/after table so the period-shift is visible at a glance:

| Period | P&L effect — before correction | P&L effect — after correction |
|---|---|---|
| Correct period (e.g. Dec) | $0 (nothing booked yet) | +[amount] (Leg 1) |
| Wrong period (e.g. Jan) | +[amount] (invoice booked on invoice-date convention) | $0 net (Leg 2 −amount, Leg 3 +amount) |
| **Two-period total** | **[amount]** | **[amount] — identical** |

The two-period combined total is unchanged by the correction — this is a period-assignment error, not a total-dollar error. That invariance is precisely what makes cutoff errors dangerous rather than harmless: a trailing or quarterly view shows the same total either way, so the error can look invisible at that altitude while still misstating each individual month for trend analysis, month-over-month budget comparisons, or any KPI tied to a specific month rather than a quarter.

## The "fix one side only" trap, fully worked

Suppose a preparer notices the January invoice-date booking is wrong and tries to fix it by simply reversing it — `Dr Accounts Payable / Cr Expense` in January — without ever booking Leg 1 in December. Result: the cost disappears from January (correctly) but never appears in December either (incorrectly), and the fake reversal against Accounts Payable also erases the real vendor liability. The item now shows up **nowhere** — not in the correct period, not in the wrong period, and the company's books understate what it owes the vendor by the full invoice amount. This is strictly worse than the original single-period misstatement: the original error at least recorded the cost somewhere and kept the real liability intact; the "fix one side only" attempt loses both. The guard against this trap is mechanical: always confirm all three legs are present — the correct-period accrual, its reversal, and the untouched actual-invoice entry — before calling a cutoff correction complete.
