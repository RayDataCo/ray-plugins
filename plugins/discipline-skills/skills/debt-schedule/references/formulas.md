<!-- iteration: 2 -->

# Formulas

The full formula card for `debt-schedule`. Every formula the procedure in SKILL.md needs, in one place. Nothing narrative here — for taxonomy, definitions, and judgment framing, see the other reference files.

## Amortization (level-payment)

- Periodic rate: `r = annual rate / periods per year`
- Total periods: `n = years × periods per year`
- Payment (annuity formula, exact — never approximate): `PMT = P·r / (1 − (1+r)^−n)`, equivalently `PMT = P·r·(1+r)^n / [(1+r)^n − 1]`
- Per-period identities:
  - `Interest = Beginning balance × r` (round to the cent)
  - `Principal = PMT − Interest`
  - `Ending balance = Beginning balance − Principal`
- Total interest over the life: `Total interest = PMT × n − P`

## Balance cross-check (closed-form)

- `Balance(k) = P(1+r)^k − PMT × [((1+r)^k − 1) / r]`
- Compare against the iterative table's ending balance for period `k`. Expected drift: a few cents, from per-period cent-rounding of interest (the continuous closed-form formula assumes no rounding; the real-world iterative schedule rounds interest to the cent every period, which very slightly changes how much principal is applied each period). Explain the drift; do not chase it as an error.

## Floating-rate interest

- All-in rate for the period: `All-in rate = Reference rate (that period's reset) + Spread`
- ACT/360 (actual/360 — the dominant USD SOFR-loan convention): `Interest = Principal × All-in rate × (Actual calendar days in period / 360)`
- 30/360 (30-day-month / 360-day-year convention): `Interest = Principal × All-in rate × (30-day-count days in period / 360)`. A standard 30/360 quarter is always exactly 90/360 = 0.25, regardless of the real calendar.
- Never substitute `All-in rate / 4` (naive annual-rate-÷-4) for a quarterly ACT/360 instrument — that shortcut is mathematically identical to always assuming a 90-actual-day quarter, i.e. it silently reproduces the 30/360 result while the instrument is actually governed by ACT/360.

## Covenant compliance

- `DSCR = CFADS / Debt Service` — compare to the agreement's stated minimum DSCR.
- `Leverage = Total Debt / EBITDA` — compare to the agreement's stated maximum leverage.
- Both-direction headroom, minimum-type covenant (DSCR):
  - CFADS-cushion direction (holding Debt Service constant): `Actual CFADS − (Minimum DSCR × Actual Debt Service)`
  - Debt-Service-cushion direction (holding CFADS constant): `(Actual CFADS / Minimum DSCR) − Actual Debt Service`
- Both-direction headroom, maximum-type covenant (Leverage):
  - Debt-cushion direction (holding EBITDA constant): `(Maximum Leverage × Actual EBITDA) − Actual Total Debt`
  - EBITDA-cushion direction (holding Debt constant): `Actual EBITDA − (Actual Total Debt / Maximum Leverage)`
- CFADS, Debt Service, Total Debt, and EBITDA are always the *specific agreement's own* defined terms — see `covenants.md` for why a generic formula is unsafe.

## Refinance / prepayment breakeven

- Rate differential = existing rate − new rate.
- Annual savings = `Principal × rate differential`.
- Total upfront cost (new financing) = origination fee + closing costs + any new-loan prepayment penalty/breakage/make-whole.
- Breakeven (years) = `Total upfront cost / Annual savings` — compare against the remaining term on the existing loan.
- Net savings over the remaining life = `(Annual savings × remaining years) − Total upfront cost`.
- The existing loan's own exit cost (prepayment penalty, breakage, make-whole) is a separate line item that must be confirmed, not assumed — see `refinance-judgment.md`.
