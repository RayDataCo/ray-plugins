# financial-statements — base-model covered

Financial-statements builds the classical three-statement outputs from a trial balance or a
company's roll-forward balances — a classified multi-step income statement (revenue through cost
of goods sold to gross profit, operating expenses to operating income, non-operating items and
tax to net income), a classified balance sheet with a retained-earnings roll-forward that must
tie out exactly, and an indirect-method statement of cash flows footing to the actual change in
cash — and separately tests classification/presentation judgment on named scenarios (gain on
asset sale, one-time restructuring charge, current-portion-of-long-term-debt reclassification,
capitalize-vs-expense repair costs, loss-contingency accrual threshold).

## Exemplar prompts

### Exemplar 1 (fixture A — classified income statement from a trial balance)

> Meridian Supply Co. is a wholesale distributor. Its adjusted trial balance, Year 2, as of December 31 (pre-closing — revenue and expense accounts are not yet closed to retained earnings, and the retained earnings balance shown is still the Year 1 ending balance) is as follows:
>
> Cash: $173,000 (debit)
> Accounts receivable: $95,000 (debit)
> Inventory: $72,000 (debit)
> Prepaid expenses: $8,000 (debit)
> Equipment, gross: $240,000 (debit)
> Accumulated depreciation: $75,000 (credit)
> Accounts payable: $58,000 (credit)
> Accrued liabilities: $18,000 (credit)
> Current portion of long-term debt: $20,000 (credit)
> Long-term debt (non-current portion): $80,000 (credit)
> Common stock: $100,000 (credit)
> Retained earnings (beginning): $170,000 (credit)
> Dividends declared: $20,000 (debit)
> Sales revenue: $900,000 (credit)
> Cost of goods sold: $540,000 (debit)
> Salaries expense: $150,000 (debit)
> Rent expense: $40,000 (debit)
> Depreciation expense: $25,000 (debit)
> Supplies and other operating expense: $20,000 (debit)
> Interest expense: $9,000 (debit)
> Income tax expense: $29,000 (debit)
>
> Total debits and total credits each equal $1,421,000; the trial balance is balanced.
>
> Prepare Meridian's classified (multi-step) income statement for Year 2. Interest expense is included in the trial balance as its own account; classify it in the section of the income statement where it belongs.

### Exemplar 2 (fixture C — indirect-method statement of cash flows)

> Meridian Supply Co.'s balance sheet data:
>
> Year 1 (beginning) balances — Dec 31, Year 1:
> Cash: $150,000
> Accounts receivable: $80,000
> Inventory: $60,000
> Prepaid expenses: $10,000
> Equipment, net: $150,000
> Accounts payable: $45,000
> Accrued liabilities: $15,000
>
> Year 2 (ending) balances — Dec 31, Year 2:
> Cash: $173,000
> Accounts receivable: $95,000
> Inventory: $72,000
> Prepaid expenses: $8,000
> Equipment, net: $165,000
> Accounts payable: $58,000
> Accrued liabilities: $18,000
>
> Year 2 income statement data: Net income was $87,000. Depreciation expense of $25,000 is included within Year 2 operating expenses (a non-cash charge).
>
> Additional Year 2 cash activity, given directly (not derivable from the balance sheets alone): Meridian purchased new equipment for $40,000 cash (the only PP&E addition during the year; there were no disposals). Meridian made a $20,000 cash principal repayment on long-term debt during the year. Dividends declared of $20,000 were paid in cash during the year.
>
> Prepare Meridian's statement of cash flows for Year 2 using the indirect method. Confirm the three sections foot to the actual change in the cash balance.

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

All four fixtures classed `non-discriminating` — base at ceiling, no headroom for a skill to
fill.

**Note:** `EVAL-RESULTS-2026-07-08.json` shows no grading anomaly on this task — all four
fixtures scored a clean 3/3 with empty `baseFail`/`skillFail`. The evals doc's "held back"
section names one verified-false `flat` anomaly among the five INCONCLUSIVE tasks (a grading
tolerance tighter than the oracle's own disclosed rounding drift); that anomaly traces to
capital-budgeting-analysis fixture A in the source data, not to this task — see
`capital-budgeting-analysis.md`.

## Regression note

This coverage claim holds for sonnet-tier, 2026-07-08. On any base-model or tier change adopted
for finance work, re-run `eval/fixtures.json` for this task against the new model. If any fixture
drops below 3/3, promote financial-statements to a built skill via the skill-agent-brigade
factory, using the regressing fixture as the oracle case.
