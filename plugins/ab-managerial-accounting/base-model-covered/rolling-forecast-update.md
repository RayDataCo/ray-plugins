# rolling-forecast-update — base-model covered

Rolling-forecast-update takes actuals through a partial period and re-projects the remainder of
the year against a stated go-forward assumption: a seasonal index applied to a growth factor
derived from Q1 actuals-vs-budget, a unit-economics roll-forward (subscriber adds/churn × price,
including an in-year price change), a budget-to-reforecast variance bridge decomposed into YTD
variance and go-forward change, or a per-line treatment call (snap to run-rate / hold at original
plan / re-plan-and-rephase) plus where a one-time item belongs in the outlook. Output is the
reforecast dollar figures plus the intermediate math or classification that produced them.

## Exemplar prompts

### Exemplar 1 (fixture A — seasonal reforecast)

> GreenLeaf Lawn & Garden Supply is a seasonal retailer. Spring (March–May) is the peak selling season, the shoulder months are light, and December carries a secondary bump from holiday indoor-plant and gift-card sales. The FY budget was phased using a twelve-month seasonal index (index values sum to 12.00, so multiplying the index by the average month's dollar value reproduces the annual total).
>
> Annual budget revenue: $12,000,000. Average month = $12,000,000 ÷ 12 = $1,000,000. Monthly budget = seasonal index × $1,000,000.
>
> | Month | Seasonal index | Budget revenue |
> |---|---|---|
> | Jan | 0.55 | $550,000 |
> | Feb | 0.60 | $600,000 |
> | Mar | 1.90 | $1,900,000 |
> | Apr | 1.75 | $1,750,000 |
> | May | 1.50 | $1,500,000 |
> | Jun | 1.05 | $1,050,000 |
> | Jul | 0.85 | $850,000 |
> | Aug | 0.75 | $750,000 |
> | Sep | 0.65 | $650,000 |
> | Oct | 0.55 | $550,000 |
> | Nov | 0.50 | $500,000 |
> | Dec | 1.35 | $1,350,000 |
> | Total | 12.00 | $12,000,000 |
>
> Q1 actuals (three months closed):
>
> | Month | Actual revenue | Budget revenue | $ vs. budget |
> |---|---|---|---|
> | Jan | $570,000 | $550,000 | +$20,000 |
> | Feb | $610,000 | $600,000 | +$10,000 |
> | Mar | $2,022,500 | $1,900,000 | +$122,500 |
> | Q1 total | $3,202,500 | $3,050,000 | +$152,500 |
>
> Re-forecast April–December revenue and the full-year total.

### Exemplar 2 (fixture B — subscriber roll-forward with in-year price change)

> A B2B SaaS company forecasts monthly subscription revenue from two drivers: active subscriber count and price per subscriber (ARPU). Stated convention: monthly revenue = subscriber count at the start of the month × the price in effect that month. New adds in a given month begin contributing revenue the following month (beginning-of-period billing simplification).
>
> Q1 actuals (closed, given):
>
> | Month | Beginning subs | Adds | Churn | Ending subs | Price | Revenue (beg. subs × price) |
> |---|---|---|---|---|---|---|
> | Jan | 9,700 | 320 | 210 | 9,810 | $50 | $485,000 |
> | Feb | 9,810 | 310 | 205 | 9,915 | $50 | $490,500 |
> | Mar | 9,915 | 305 | 220 | 10,000 | $50 | $495,750 |
> | Q1 total | | | | | | $1,471,250 |
>
> Go-forward assumptions for the reforecast (April–December):
>
> - Beginning base for April = March's ending subscriber count = 10,000.
> - Gross new adds: 300/month, flat, every month.
> - Churn: 200/month flat (a unit-count churn assumption, not a percentage).
> - Price: $50/month through May. Announced price increase to $54/month effective June 1, applied across the entire active base (existing and new subscribers both pay the new price from June forward — no grandfathering).
>
> Re-forecast the subscriber roll-forward and revenue for April–December, and the full-year revenue total.

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
fill. No anomalies on this task in `EVAL-RESULTS-2026-07-08.json`.

## Regression note

This coverage claim holds for sonnet-tier, 2026-07-08. On any base-model or tier change adopted
for finance work, re-run `eval/fixtures.json` for this task against the new model. If any fixture
drops below 3/3, promote rolling-forecast-update to a built skill via the skill-agent-brigade
factory, using the regressing fixture as the oracle case.
