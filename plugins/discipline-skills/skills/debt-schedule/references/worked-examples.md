<!-- iteration: 2 -->

# Worked examples

Four fully-derived fixtures spanning the skill's four sub-capabilities. Pattern-match against these before answering a multi-part debt-mechanics build. Every intermediate figure below is actually computed, not asserted — the arithmetic is shown so you can re-derive it, not just copy the boxed answer.

---

## Fixture A — Level-payment amortization with dual balance cross-check

**Instrument:** $500,000 principal, 6% fixed annual rate, 5-year term, monthly level-payment amortization (60 periods).

**Setup:** `r = 0.06 / 12 = 0.005` per month. `n = 60`.

`PMT = P·r / (1 − (1+r)^−n) = 500,000 × 0.005 / (1 − 1.005^−60) = 2,500 / 0.258628... = $9,666.40`

**First four rows** (`Interest = Beginning × r`; `Principal = PMT − Interest`; `Ending = Beginning − Principal`):

| Period | Beginning | Interest | Principal | Ending |
|---|---|---|---|---|
| 1 | $500,000.00 | $2,500.00 | $7,166.40 | $492,833.60 |
| 2 | $492,833.60 | $2,464.17 | $7,202.23 | $485,631.37 |
| 3 | $485,631.37 | $2,428.16 | $7,238.24 | $478,393.13 |
| 4 | $478,393.13 | $2,391.97 | $7,274.43 | $471,118.70 |

Interest declines and principal rises monotonically each period, as expected for a constant payment against a shrinking balance.

**Balance cross-check at period 4:**

`Balance(4) = P(1+r)^4 − PMT × [((1+r)^4 − 1)/r]`
`= 500,000 × 1.020150500625 − 9,666.40 × [0.020150500625 / 0.005]`
`= 510,075.25 − 9,666.40 × 4.030100125`
`= 510,075.25 − 38,956.56`
`= $471,118.69`

Iterative table gives $471,118.70; closed-form gives $471,118.69 — a 1-cent drift, expected and explained: the iterative table rounds interest to the cent every period, which very slightly changes how much principal is applied each period versus the continuous closed-form formula. Not an error.

**Total interest over the life:** `PMT × n − P = 9,666.40 × 60 − 500,000 = 579,984.00 − 500,000 = $79,984.00`

**Boxed answer:** PMT = **$9,666.40**; total interest (60 periods) = **$79,984.00**; balance after period 4 = **$471,118.70** (iterative) / **$471,118.69** (closed-form), 1-cent rounding drift explained.

---

## Fixture B — Floating-rate ACT/360 vs. 30/360, the day-count trap

**Instrument:** $2,000,000 principal, SOFR + 250bps, quarterly resets, ACT/360 (confirmed from the governing document). Four quarterly resets over one year, with these actual SOFR fixings and actual calendar days per quarter:

| Quarter | Actual days | SOFR fixing | All-in rate (SOFR + 2.50%) |
|---|---|---|---|
| Q1 | 90 | 5.31% | 7.81% |
| Q2 | 91 | 5.28% | 7.78% |
| Q3 | 92 | 5.20% | 7.70% |
| Q4 | 92 | 5.10% | 7.60% |

(90 + 91 + 92 + 92 = 365 actual calendar days — a standard, non-leap year.)

**ACT/360 interest per quarter** (`Interest = Principal × All-in rate × Actual days / 360`):

- Q1: `2,000,000 × 0.0781 × 90/360 = 2,000,000 × 0.0781 × 0.25 = $39,050.00`
- Q2: `2,000,000 × 0.0778 × 91/360 = 155,600 × 0.252778 = $39,332.22`
- Q3: `2,000,000 × 0.0770 × 92/360 = 154,000 × 0.255556 = $39,355.56`
- Q4: `2,000,000 × 0.0760 × 92/360 = 152,000 × 0.255556 = $38,844.44`

**Full-year ACT/360 total:** `$39,050.00 + $39,332.22 + $39,355.56 + $38,844.44 = $156,582.22`

**30/360 comparison** — same rates, but each quarter treated as a fixed 90/360 = 0.25 fraction regardless of the actual calendar (`Interest = Principal × All-in rate × 0.25`):

- Q1: `2,000,000 × 0.0781 × 0.25 = $39,050.00` (identical to ACT/360 here — Q1 actually was 90 days)
- Q2: `2,000,000 × 0.0778 × 0.25 = $38,900.00` (vs. $39,332.22 actual — Q2 was really 91 days)
- Q3: `2,000,000 × 0.0770 × 0.25 = $38,500.00` (vs. $39,355.56 actual — Q3 was really 92 days)
- Q4: `2,000,000 × 0.0760 × 0.25 = $38,000.00` (vs. $38,844.44 actual — Q4 was really 92 days)

**Full-year 30/360 total:** `$39,050.00 + $38,900.00 + $38,500.00 + $38,000.00 = $154,450.00`

**The trap, quantified:** 30/360 understates the true ACT/360 interest by `$156,582.22 − $154,450.00 = $2,132.22`, a `$2,132.22 / $156,582.22 = 1.36%` understatement — and note that applying the naive "annual rate ÷ 4" shortcut per quarter reproduces this exact same 30/360 result (since annual-rate-÷-4 is mathematically just assuming every quarter is a flat 90/360 = 0.25 fraction), so that shortcut carries the identical 1.36% understatement. This gap would not have been obvious from checking any single quarter in isolation — only Q1, which happened to actually be 90 days, matches exactly between the two conventions; Q2 through Q4 each individually look like unremarkable, plausible dollar figures under either convention.

**Boxed answer:** Full-year ACT/360 interest = **$156,582.22**; full-year 30/360 comparison = **$154,450.00**; difference = **$2,132.22 / 1.36%** understatement if 30/360 (or annual-÷-4) were wrongly applied to this ACT/360-governed instrument.

---

## Fixture C — Covenant compliance, DSCR and leverage, both-direction headroom

**Instrument / agreement inputs:** CFADS = $4,200,000; Debt Service = $3,000,000; minimum DSCR covenant = 1.25x. Total Debt = $32,000,000; EBITDA = $10,000,000; maximum leverage covenant = 3.50x. (CFADS and EBITDA figures per the specific credit agreement's own stated definitions.)

**DSCR:** `DSCR = CFADS / Debt Service = 4,200,000 / 3,000,000 = 1.40x` vs. minimum 1.25x → **PASS**.

Both-direction headroom:
- CFADS-cushion (holding Debt Service constant): minimum required CFADS = `1.25 × 3,000,000 = 3,750,000`; headroom = `4,200,000 − 3,750,000 = $450,000`.
- Debt-Service-cushion (holding CFADS constant): maximum supportable Debt Service = `4,200,000 / 1.25 = 3,360,000`; headroom = `3,360,000 − 3,000,000 = $360,000`.

**Leverage:** `Leverage = Total Debt / EBITDA = 32,000,000 / 10,000,000 = 3.20x` vs. maximum 3.50x → **PASS**.

Both-direction headroom:
- Debt-cushion (holding EBITDA constant): maximum supportable debt = `3.50 × 10,000,000 = 35,000,000`; headroom = `35,000,000 − 32,000,000 = $3,000,000`.
- EBITDA-cushion (holding Debt constant): minimum required EBITDA = `32,000,000 / 3.50 = 9,142,857.14`; headroom = `10,000,000 − 9,142,857.14 = $857,142.86`.

**Raw-dollar-vs-ratio-cushion trap note:** the leverage covenant's debt-cushion headroom ($3,000,000) looks much larger in raw dollars than the DSCR covenant's CFADS-cushion headroom ($450,000) — but on a ratio-cushion basis, leverage (3.20x vs. 3.50x max) has an 8.6% cushion while DSCR (1.40x vs. 1.25x min) has a 12% cushion. DSCR is actually the *more* comfortable covenant on a percentage basis despite the smaller raw-dollar headroom — comparing raw dollars alone across covenants of very different base size would have suggested the opposite conclusion.

**Boxed answer:** DSCR **1.40x** vs. **1.25x** minimum → **PASS**, headroom **$450,000** (CFADS direction) / **$360,000** (Debt-Service direction). Leverage **3.20x** vs. **3.50x** maximum → **PASS**, headroom **$3,000,000** (debt direction) / **$857,142.86** (EBITDA direction).

---

## Fixture D — Refinance breakeven with existing-loan exit-cost judgment flag

**Instrument:** existing loan, $1,000,000 outstanding principal, 7.50% fixed rate, 3.0 years remaining term. Refinance offer: 6.25% fixed rate, all-in upfront cost on the new financing (origination fee + closing costs) = $35,000. The existing loan's own exit cost (prepayment penalty, breakage, make-whole) is **not given**.

**Naive strawman (rate-only, no costs):** 6.25% < 7.50% — looks favorable on rate alone, with no information about whether it's actually worth doing.

**All-in-cost view:**
- Rate differential = `7.50% − 6.25% = 1.25%`.
- Annual savings = `1,000,000 × 0.0125 = $12,500`.
- Breakeven = `Total upfront cost / Annual savings = 35,000 / 12,500 = 2.8 years` — compare to the 3.0-year remaining term. Breakeven (2.8 years) is shorter than the remaining term (3.0 years), so the new-loan costs alone are recovered before the existing loan would have matured anyway.
- Net savings over the remaining 3.0-year life = `(12,500 × 3.0) − 35,000 = 37,500 − 35,000 = $2,500`.

**Judgment layer — the existing loan's exit cost:** the $2,500 net savings figure only accounts for the new loan's costs. It does not include any prepayment penalty, breakage cost (if the existing loan is hedged), or make-whole provision the *existing* loan might carry for being retired early — that information was not given and has not been confirmed as zero. $2,500 on a $1,000,000 principal over 3 years is a thin margin: even a modest unconfirmed exit cost on the existing loan (a fraction of a percent of principal) could turn this net-positive result net-negative. The computed breakeven and net savings above are determinate arithmetic; whether the refinance is actually worth doing remains an open question pending confirmation of the existing loan's own exit cost, and should not be presented as a closed recommendation.

**Boxed answer:** Breakeven = **2.8 years** vs. **3.0 years** remaining term; net savings = **$2,500** (thin positive), with an explicit open-question flag on the existing loan's unconfirmed exit cost given the thin margin.
