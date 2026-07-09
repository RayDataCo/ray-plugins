# reconciliation — base-model covered

Reconciliation covers the core tie-out disciplines: bank-to-book cash reconciliation by the
adjusted-balance method (deposits in transit, outstanding checks, bank service charges, an NSF
check still booked as good funds, unrecorded interest), subledger-to-GL control-account tie-outs
that quantify each individual differencing item (an unposted batch, a direct GL-only journal
entry with no subledger mirror, a duplicate posting) to reach a true corrected balance, aging-based
policy triage on open reconciling items against tiered escalation/documentation requirements, and
classification of reconciling items as a timing difference, a bookkeeping error, or a
potential-fraud red flag.

## Exemplar prompts

### Exemplar 1 (fixture A — bank-to-book reconciliation, adjusted-balance method)

> Harborline Distributors, Inc. is reconciling its Operating Cash account for the period ended June 30, 2026. The following information is available:
>
> Bank statement balance, June 30: $182,400.00
> Book (GL) cash balance, June 30, before adjustment: $177,270.00
> Deposit in transit (mailed/processed June 30, not yet posted by the bank): $7,850.00
> Outstanding check #1042: $6,200.00
> Outstanding check #1047: $3,450.00
> Outstanding check #1051: $5,600.00
> Bank service charges per the bank statement, not yet recorded in the books: $85.00
> NSF check from customer J. Alvarez -- deposited, bounced, still shown in the books as good funds: $2,300.00
> Interest earned per the bank statement, not yet recorded in the books: $115.00
>
> Using the adjusted-balance method, determine the adjusted bank balance, the adjusted book balance, and the net dollar adjustment needed to bring the books to the true cash balance.

### Exemplar 2 (fixture B — subledger-to-GL control-account tie-out)

> Harborline Distributors, Inc. is tying out Accounts Receivable for the period ended June 30, 2026.
>
> AR subledger total (sum of open customer invoice detail): $846,930.00
> GL Accounts Receivable control account balance: $861,880.00
>
> Investigation identifies three differences between the two balances:
>
> 1. Unposted batch. Invoice batch #B-0629 ($5,600.00), billed June 29, was recorded in the AR subledger (billing system) on June 29, but the nightly interface to the GL failed due to a system outage. The batch is scheduled to interface on July 2.
> 2. Direct posting to the control account. Journal entry #GJ-4471, an intercompany AR reclassification, debited (increased) the GL AR control account by $9,850.00. It was posted directly in the GL with no corresponding entry in the AR subledger detail. The entry is legitimate -- it reflects a real intercompany billing -- but has never been mirrored into subledger detail.
> 3. Duplicate posting. The June 15 invoice interface batch (#B-0615, $10,700.00) was accidentally run twice, posting the same $10,700.00 of invoices to the GL control account a second time. The subledger reflects the batch correctly, once.
>
> Quantify the raw GL-to-subledger difference, quantify each of the three items, and determine the true, fully corrected AR balance.

## Evidence

Two-arm execution eval, base model (no skill) vs. base model + draft skill, n=3 samples per
fixture, graded deterministically against a fixed answer key (kept private with the eval
harness, not reproduced here).

| fixture | base pass rate | tier | eval date |
|---|---|---|---|
| A | 3/3 | sonnet | 2026-07-08 |
| B | 3/3 | sonnet | 2026-07-08 |
| C | 3/3 | sonnet | 2026-07-08 |
| D | 3/3 | sonnet | 2026-07-08 |

All four fixtures show the base arm at 3/3 in `EVAL-RESULTS-2026-07-08.json`.

**Note:** fixture B is labeled `class: "regression"` in the raw eval data, but the base arm
itself scored 3/3 — the label reflects the skill arm dropping to 2/3 on the
`unposted_batch_amount` field. The evals doc's "held back" section documents this as one of two
verified-false anomalies: the grading key demanded an unsigned magnitude where the source
material teaches a signed convention, so the skill arm's signed answer was actually correct and
the key was wrong, not the model. It does not affect this task's base-model coverage claim.
(Exact figures withheld here — they double as the fixture's grading key.)

## Regression note

This coverage claim holds for sonnet-tier, 2026-07-08. On any base-model or tier change adopted
for finance work, re-run `eval/fixtures.json` for this task against the new model. If any fixture
drops below 3/3, promote reconciliation to a built skill via the skill-agent-brigade factory,
using the regressing fixture as the oracle case.
