<!-- iteration: 1 -->
# Prepaid Amortization — Full Mechanic

Read this when executing SKILL.md Step 5.

## Capitalize-then-amortize mechanic

A prepaid expense is a payment made in advance of the benefit period it covers — an annual insurance premium, a software license, a prepaid rent block. GAAP treatment capitalizes the payment as an asset at the cash date, then recognizes it as an expense gradually, matched to the periods that actually receive the benefit.

**At the payment date:**
```
Dr Prepaid [type]                 [payment]
    Cr Cash                           [payment]
```

The full payment sits on the balance sheet as an asset — nothing hits the income statement yet, because no benefit has been consumed yet.

## Straight-line schedule-building method

1. Compute the monthly rate: **payment ÷ number of months in the benefit period.**
2. For each month inside the benefit period, book:
```
Dr [Expense account]              [monthly rate]
    Cr Prepaid [type]                 [monthly rate]
```
3. Track three running columns month by month: **amortization booked this month**, **cumulative amortization to date**, and **remaining prepaid balance** (payment − cumulative amortization).

Example schedule shape (values illustrative, not tied to any specific fixture):

| Month | Amortization booked | Cumulative amortization | Remaining prepaid balance |
|---|---|---|---|
| 1 | rate | rate | payment − rate |
| 2 | rate | 2 × rate | payment − 2 × rate |
| … | … | … | … |
| N (last month of benefit period) | rate | payment | $0 |

## The zero-out check

The schedule's remaining balance in the final month of the benefit period must equal exactly **$0**. This is not optional bookkeeping hygiene — it's the mechanical proof that the full payment was allocated across the correct number of months and no more. Always state this check explicitly as part of the schedule output, even when it passes cleanly. If the schedule does not zero out on the final month, or if the remaining balance ever goes negative, that is itself a close-quality signal worth flagging — it usually indicates either an arithmetic error in the monthly rate, a benefit-period date that was entered wrong, or a mid-stream change to the underlying contract (e.g. an early cancellation or a renegotiated term) that hasn't been reflected in the schedule.

## Splitting the schedule across a fiscal year boundary

When the benefit period straddles a fiscal year-end, report two sub-totals in addition to the full schedule:

- **Fiscal-year expense** — the sum of monthly amortization booked from the payment/start date through the fiscal year-end.
- **Year-end prepaid balance** — the remaining, unamortized portion still on the balance sheet at fiscal year-end, which will continue amortizing into the next fiscal year.

These two numbers must sum to the total payment: FY expense + year-end prepaid balance = full payment amount, exactly.

## Quantified distortion of expensing in full at the cash date

If, instead of capitalizing and amortizing, the full payment is expensed in one shot at the payment date (`Dr Expense / Cr Cash`, full amount), two equal-and-offsetting misstatements result, each exactly equal to the unamortized remainder as of the point of comparison:

- **P&L overstatement in the payment period** — the payment period absorbs the full expense immediately, rather than just that period's pro-rata share (the monthly rate). The overstatement in that single period equals (payment − monthly rate for that period).
- **P&L understatement in every later period within the benefit window** — those periods show $0 expense for something that is, in substance, still being consumed. The cumulative understatement across the remaining months equals the same amount, spread across those months.
- **Balance-sheet asset understatement at any point in between** — because nothing was ever capitalized, there's no Prepaid asset on the balance sheet at all, even though real future benefit remains. This balance-sheet understatement, at any single point in time, equals exactly the schedule's "remaining prepaid balance" that would have existed under proper treatment at that same date.

These three numbers are not independent coincidences — they are the same misallocation viewed from three different statements, which is exactly why a bad prepaid treatment simultaneously distorts trend analysis (front-loaded expense recognition makes the payment period look artificially worse and every subsequent period look artificially better) and understates real assets on the balance sheet for the remainder of the benefit period.
