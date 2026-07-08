<!-- iteration: 1 -->
# Accrual + Reversal — Full Mechanic

Read this when executing SKILL.md Step 3.

## The Dr/Cr pattern

An accrual recognizes an expense (or revenue) in the period it was incurred (or earned), before the invoice or cash settlement arrives. For an expense accrual:

```
Period N (estimate booked):
Dr [Expense account]              [estimate]
    Cr Accrued Liabilities            [estimate]
```

The estimate should be built from the best available signal, named explicitly:

- **Purchase order** — the PO's committed amount, when goods/services under it were received or performed in-period.
- **Signed SOW milestone** — the contracted milestone value tied to work completed in-period.
- **Vendor verbal/email confirmation** — an informal but specific amount communicated by the vendor ahead of formal invoicing.
- **Timesheet** — hours × rate for labor performed in-period but not yet invoiced.
- **Prior-invoice run-rate** — the trailing average or most recent actual invoice amount, used only when no more specific signal exists.

Naming the signal matters because it tells the reader (and a later reviewer) how much confidence to place in the estimate — a PO-backed accrual is nearly firm; a run-rate accrual carries real estimation-uncertainty width (see `materiality-triage.md`).

## The mandatory reversal

Every accrual is followed by a reversing entry dated the first day of the next period:

```
Period N+1, day 1 (reversal):
Dr Accrued Liabilities            [same estimate]
    Cr [Expense account]              [same estimate]
```

**Systems-flagged auto-reversal.** In a real ERP, the accrual is typically flagged "auto-reversing" at entry time, and the system generates the offsetting entry automatically on the first day of the next period without anyone needing to remember. This skill has no ERP to lean on, so it must always show the reversal explicitly, as if independently verifying the auto-reversal actually fired. Never assume it happened — state it.

## Why skipping the reversal double-counts the expense

If the actual invoice later posts as its own entry (`Dr Expense / Cr Accounts Payable`, actual amount) and the original accrual was never reversed, the ledger now carries the expense twice: once from the un-reversed accrual, once from the actual invoice. The overstatement equals exactly the un-reversed estimate amount. Simultaneously, Accrued Liabilities — which should have zeroed out via the reversal — sits with a permanent, stale credit balance that never clears, because nothing ever debited it back down. A multi-period trend of Accrued Liabilities that only grows and never comes back down to a baseline is itself a red flag for a broken reversal discipline, worth flagging proactively if given multi-period history.

## Actual-invoice reconciliation

When the actual invoice amount is known:

```
Dr [Expense account]              [actual]
    Cr Accounts Payable               [actual]
```

Then compute:

- **Net next-period P&L effect** = actual − reversed estimate. If the actual comes in higher than the estimate, this is a positive (expense-increasing) true-up in the next period; if lower, negative.
- **Two-period combined total** = the accrual-period expense + the next-period net effect. This must equal the actual invoice amount exactly, regardless of how the estimate compared to the actual. If it doesn't tie out exactly, the entries are wrong — this is a hard cross-foot, not an approximation.

## Estimate-bias patterns

Two distinct bias patterns distort accrual estimates, and they pull in different directions, so distinguishing them matters:

1. **Cookie-jar smoothing (deliberate).** An estimator deliberately over- or under-accrues to smooth reported earnings across periods — banking a "cushion" in a strong quarter to release in a weak one. This is a control/ethics concern, not a mechanical error, and should be escalated as a qualitative override in triage (see `materiality-triage.md`) if suspected, not just recomputed.
2. **Anchoring (unconscious).** An estimator defaults to "last month's number" as the estimate without re-evaluating whether the current period's activity actually matches. This produces a systematic lag — the accrual chronically trails the true run-rate up or down — without any intent to manipulate. It shows up as a persistent one-directional true-up (see below), not a random noise pattern.

## True-up-direction KPI diagnostic

Track the sign and magnitude of the net next-period P&L effect (actual − reversed estimate) across several consecutive periods for the same accrual line:

- **Consistently near zero, alternating sign** — healthy estimation; normal noise.
- **Consistently one-directional (e.g., actual always higher than estimate)** — a systematic bias. If the gap is small and stable, this looks like anchoring (Step 2 above): the estimate isn't tracking a real trend. If the gap is large and appears deliberately timed around reporting periods (e.g., understated right before earnings, trued-up right after), treat it as a cookie-jar smoothing signal and escalate via triage's qualitative-override axis rather than treating it as a mechanical fix.

This diagnostic is the same "was the estimate wrong by accident or by design" question a controller asks when reviewing a recurring accrual line — the true-up direction over time is the evidence.
