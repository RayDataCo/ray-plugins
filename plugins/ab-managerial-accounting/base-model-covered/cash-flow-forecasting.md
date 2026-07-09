# cash-flow-forecasting — base-model covered

Cash-flow-forecasting builds a direct-method, multi-week cash view: expected weekly receipts from
an accounts-receivable aging schedule run through a bucket-by-bucket collection curve, weekly
disbursement timing from mixed payment schedules (fixed monthly rent, biweekly payroll, net-30
accounts payable on a per-invoice schedule), a minimum-cash-floor revolving-credit rollforward
that draws and repays only in stated dollar increments, and lever-prioritization judgment for
closing a projected future-week shortfall against a floor (ranking discretionary-AP delay,
revolver draw, and discounted early-collection by cost and risk).

## Exemplar prompts

### Exemplar 1 (fixture A — AR aging into weekly receipts)

> Ridgeline Hardware Supply is a wholesale distributor. As of the Monday beginning Week 1 of a 13-week direct-method cash forecast, the accounts-receivable aging schedule (gross balances) is: Current (0-30 days) $800,000; 31-60 days $350,000; 61-90 days $150,000; 90+ days $100,000; total gross AR $1,400,000. Two items apply to specific accounts within these buckets: a $40,000 invoice sitting in the 61-90 day bucket is under formal customer dispute over contested billing and will not be pursued for collection until the dispute is resolved; and $60,000 of the $100,000 in the 90+ day bucket is covered by the company's allowance for doubtful accounts, per the controller. A collection curve gives the percentage of each bucket's balance expected to convert to cash in each of the next four weeks: Current 35% / 30% / 20% / 10% (Weeks 1-4); 31-60 days 20% / 25% / 25% / 15%; 61-90 days 10% / 15% / 20% / 15%; 90+ days 5% / 10% / 10% / 10%.

### Exemplar 2 (fixture C — minimum-cash-floor revolver rollforward)

> A mid-size company runs a 6-week cash rollforward. Beginning cash at the start of Week 1 is $200,000. The minimum-cash floor is $150,000. The revolving credit facility draws and repays only in $50,000 increments, and its balance starts at $0. Draws round up to the smallest increment of $50,000 that brings ending cash to at least the floor. Repayments round down to the largest increment of $50,000 that does not push ending cash below the floor, capped at the outstanding revolver balance. Weekly receipts and disbursements: Week 1 receipts $300,000, disbursements $250,000; Week 2 receipts $280,000, disbursements $320,000; Week 3 receipts $150,000, disbursements $400,000; Week 4 receipts $350,000, disbursements $200,000; Week 5 receipts $260,000, disbursements $260,000; Week 6 receipts $300,000, disbursements $230,000.

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

All four fixtures classed `non-discriminating` at sonnet tier — base at ceiling, no headroom for
a skill to fill.

This task also carried a tier sweep (haiku/sonnet/opus) — one of two skills in the 2026-07-08
run tested beyond sonnet. Additional data points from `EVAL-RESULTS-2026-07-08.json`, included
for tripwire completeness (not required for the sonnet-tier coverage claim above): haiku scored
3/3 on all four fixtures. Opus scored 3/3 on fixtures A, B, and D, but 2/3 on fixture C
(`week3_draw`, `week4_repayment` — an under-sized revolver draw/repayment call, class `win`
since the skill arm corrected it to 3/3). A stronger tier underperforming a weaker one on a
single fixture is exactly the kind of cross-tier variance the promotion rule exists to catch; it
does not change the sonnet-tier coverage claim, which is clean 3/3 across all four fixtures.

## Regression note

This coverage claim holds for sonnet-tier, 2026-07-08. On any base-model or tier change adopted
for finance work, re-run `eval/fixtures.json` for this task against the new model. If any fixture
drops below 3/3, promote cash-flow-forecasting to a built skill via the skill-agent-brigade
factory, using the regressing fixture as the oracle case.
