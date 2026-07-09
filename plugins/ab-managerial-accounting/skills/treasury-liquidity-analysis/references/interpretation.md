<!-- iteration: 0 -->

# Interpretation Notes — Treasury Liquidity Analysis

Read this when reasoning through Steps 3 (CCC), 4 (available liquidity), or 6 (multi-period judgment) beyond the mechanical formula — the "why" behind the gates, not just the arithmetic.

## Average-vs-ending balance: when the distortion is largest, and why it matters

DSO, DIO, and DPO each divide a stock figure (a balance-sheet snapshot at one instant) by a flow figure (revenue or COGS, accumulated across the whole period). Using the ending balance alone silently assumes the ending balance IS representative of the period's typical balance — which is only true if the balance didn't move much during the period.

- **Growing business:** AR and inventory balances tend to be higher at period-end than they were on average across the period (more sales, more inventory to support them, both trending up). Ending-balance DSO/DIO overstate the true velocity — the business looks like it's carrying more days of receivables/inventory than it actually averaged. This is the direction illustrated in `worked-examples.md` Fixture B: the CCC is overstated by using the ending inventory balance instead of the period average.
- **Shrinking business:** the reverse — ending balances are lower than the period average, so ending-balance DSO/DIO understate CCC, making the business look more efficient than it averaged.
- **AP works in the opposite direction** in the CCC formula (subtracted, not added) — an ending-balance-inflated DPO would understate CCC, not overstate it. When multiple components are moving, the net distortion direction isn't obvious without doing the average-balance computation; don't assume it nets to zero.

The distortion is largest when (a) the balance is genuinely volatile within the period (strong growth, seasonality, a one-time build or drawdown) and (b) only two data points (beginning, ending) are available to average — a true intra-period average would smooth further, but beginning/ending is the standard, always-available approximation and is what this skill uses.

## Committed vs. uncommitted: "committed" isn't a binary reliability signal

Only committed facilities count toward available liquidity (Step 4) because an uncommitted line is a bank convenience product, not a contractual obligation — it can be pulled with no notice, and precisely at the moment of stress when it would be needed most, since that's also the moment a bank's own risk appetite tightens.

But "committed" doesn't mean "unconditionally available on demand" either:

- **Material Adverse Change (MAC) clauses** — many committed facilities let the lender decline a draw request if a MAC has occurred. In practice this is rarely invoked for routine draws, but it means "committed" capacity carries some tail risk that a purely mechanical `Commitment − Drawn − LCs` calculation doesn't capture. Treat the computed availability figure as the contractual ceiling, not a guarantee of same-day cash.
- **Borrowing-base mechanics** — asset-based revolvers (ABL) size availability off a formula tied to eligible AR and inventory (e.g., 85% of eligible AR + 50% of eligible inventory), not the stated commitment amount alone. If the facility is borrowing-base-governed, the stated commitment can overstate true availability if eligible collateral has shrunk — flag this explicitly as a caveat when the input data references a borrowing base, rather than computing off the commitment figure alone.

The discipline: report the mechanical `Commitment − Drawn − LCs outstanding` figure per Step 4 (that's what the skill is scoped to compute), but note MAC/borrowing-base conditionality as a caveat when the facility terms given reference either — don't imply the number is a cash-in-hand guarantee.

## Why profitable, growing companies die of illiquidity

A business can be profitable on the income statement and still run out of cash. This isn't a paradox once the CCC is understood as measuring cash *velocity*, not cash *level*:

- **Revenue recognition vs. cash collection timing** — revenue is recognized when earned, not when collected. A company growing sales 40% year-over-year is also growing its AR balance at a similar (or faster, if payment terms are loosening to win the growth) rate. The income statement shows the growth as profit; the balance sheet and CCC show the same growth consuming cash.
- **Inventory funds growth before revenue confirms it** — a company anticipating demand builds inventory ahead of the sale. If the anticipated demand doesn't fully materialize, or arrives slower than planned, inventory (and DIO) balloons while the cash that funded it is already spent.
- **Seasonality** — a business with a concentrated selling season (e.g., a retailer building toward Q4) will show a CCC and available-liquidity trough well before its most profitable quarter shows up in trailing income-statement figures. A snapshot taken at the trough looks like distress; a snapshot taken after the season looks flush. This is exactly why Step 6's multi-period discipline and Step 7's window-dressing awareness both matter — a single snapshot, taken at the wrong point in a seasonal or growth cycle, can mislead in either direction.

The unifying point for the judgment layer (Step 6): profitability (income statement) and liquidity (balance sheet, CCC, available liquidity) are different lenses on the same business, and a rising current ratio or NWC driven by inventory/AR growth funding a demand bet that hasn't yet converted to cash is the single most common way a "profitable" company still runs into a liquidity crunch. That's the concrete failure mode Step 6's cross-check (current ratio/NWC against quick ratio and CCC) is built to catch.
