<!-- iteration: 0 -->

# Formula Card — Treasury Liquidity Analysis

Read this when you need a formula beyond the ratio-battery / CCC / available-liquidity / leverage basics already inlined in `SKILL.md` — in particular the coverage-covenant (interest coverage, FCCR) both-direction headroom forms, which are not inlined in the body.

## Ratio battery

- `Current ratio = Total CA / Total CL`
- `NWC = Total CA − Total CL`
- `Unrestricted cash = Reported cash − Restricted cash`
- `Quick ratio = (Unrestricted cash [+ marketable securities] + AR) / Total CL`
- `Cash ratio = (Unrestricted cash [+ marketable securities]) / Total CL`

The restricted-cash exclusion applies to quick ratio and cash ratio ONLY. Current ratio and NWC always use the full reported current-asset total — restricted cash is still a current asset, it just isn't near-cash liquidity, which is what quick/cash ratio isolate.

## Cash conversion cycle

Average balance for each component: `(Beginning + Ending) / 2`.

Days convention — pick one, name it, hold it consistent within one analysis:

| Convention | Days | When |
|---|---|---|
| Annual | 365 | Full-year period, full-year revenue/COGS |
| Quarterly | 91 (365/4) | Single-quarter period, quarter-over-quarter average balances |

These two conventions are **not expected to reconcile**. Running the quarterly convention four times across a year will not equal a single annual-convention CCC computed from full-year figures — they answer different questions (quarter-to-quarter trend-spotting vs. one full-year figure), not the same question at different precision.

- `DSO = (Average AR / Revenue) × Days`
- `DIO = (Average Inventory / COGS) × Days`
- `DPO = (Average AP / COGS) × Days`
- `CCC = DSO + DIO − DPO`

Ending-balance-only version (same formulas, ending balance substituted for average balance):

- `Ending-balance CCC = Ending DSO + Ending DIO − Ending DPO`
- `Distortion = Ending-balance CCC − Average-balance CCC`

For a growing business this overstates CCC (balances built up toward period-end look larger than their period average). For a shrinking business it understates CCC. Quantify the distortion whenever both beginning and ending balances are available — don't just present the average-balance figure silently as if the ending-balance version wasn't computable.

## Available liquidity

- `Undrawn committed revolver availability = Commitment − Amount drawn − LCs outstanding`
- `Available liquidity = Unrestricted cash and equivalents + Undrawn committed revolver availability`

Only COMMITTED facilities count toward this total. Uncommitted lines are excluded and, if present in the inputs, labeled separately rather than blended in.

## Leverage and covenant headroom (maximum-leverage covenants)

- `Total funded debt = drawn, interest-bearing debt only` (revolver draws + term-loan current and long-term portions). Excludes LCs outstanding — LCs are contingent obligations, not drawn borrowings, even though they reduce revolver availability above.
- `Leverage = Total funded debt / TTM EBITDA`, compared to the covenant maximum.

Ratio-form headroom:
- `Covenant maximum − Current leverage ratio`

Dollar-form headroom, BOTH directions (both required whenever leverage-covenant headroom is in scope):
- **(a) Debt-side** — incremental debt capacity, holding EBITDA constant: `(Covenant maximum × TTM EBITDA) − Total funded debt`
- **(b) EBITDA-side** — incremental EBITDA cushion, holding debt constant: `TTM EBITDA − Minimum required EBITDA`, where `Minimum required EBITDA = Total funded debt / Covenant maximum`

If EBITDA is itself declining, both directions shrink simultaneously — faster than either component moving in isolation would suggest, because the covenant test is a ratio, not two independent thresholds.

## Coverage covenants (minimum-threshold covenants — when in scope)

Coverage covenants run the opposite direction from a leverage maximum: the ratio must stay ABOVE a stated minimum, so ratio-form headroom is `Current ratio − Covenant minimum` (not the reverse).

**Interest coverage** — `Interest coverage = TTM EBITDA / Interest expense`, vs. covenant minimum.
- Ratio-form headroom: `Current interest coverage − Covenant minimum`
- Dollar-form (a), EBITDA-side, holding interest expense constant: `Current EBITDA − Minimum required EBITDA`, where `Minimum required EBITDA = Covenant minimum × Interest expense`
- Dollar-form (b), interest-expense-side, holding EBITDA constant: `Maximum permitted interest expense − Current interest expense`, where `Maximum permitted interest expense = Current EBITDA / Covenant minimum`

**Fixed Charge Coverage Ratio (FCCR)** — `FCCR = (EBITDA − Unfinanced capex) / (Interest expense + Scheduled principal + Cash taxes)`, vs. covenant minimum. **The fixed-charges definition is agreement-specific** — always use the credit agreement's own stated definition (which items are included/excluded) rather than a generic default.
- Ratio-form headroom: `Current FCCR − Covenant minimum`
- Dollar-form (a), numerator-side, holding fixed charges constant: `Current numerator − Minimum required numerator`, where `Minimum required numerator = Covenant minimum × Fixed charges`
- Dollar-form (b), fixed-charges-side, holding the numerator constant: `Maximum permitted fixed charges − Current fixed charges`, where `Maximum permitted fixed charges = Current numerator / Covenant minimum`

Apply the same both-direction logic to any other coverage-style covenant the credit agreement defines, substituting its own numerator/denominator and threshold direction.
