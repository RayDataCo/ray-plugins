<!-- iteration: 0 -->
# Worked examples

Pattern-match against these four fixtures before answering a multi-component build.
Each is fully derived, cross-footed two ways where the inputs support it, and carries
named trap notes for the wrong answers a naive build would produce. Fixtures A–C feed
into Fixture D's rollup, so together they trace one coherent budget end to end.

All figures in whole dollars. Quarters are calendar-aligned (Q1 = Jan–Mar … Q4 =
Oct–Dec) with "mid-year" events landing at the July 1 / Q3 boundary.

---

## Fixture A — Revenue, mid-year price change

**Inputs.** One segment. Volume: Q1 100, Q2 100, Q3 110, Q4 110 units. Price: $500/unit
through Q2, increasing to $550/unit effective July 1 (start of Q3).

**Build.**
| Quarter | Volume | Price | Revenue |
|---|---|---|---|
| Q1 | 100 | 500 | 50,000 |
| Q2 | 100 | 500 | 50,000 |
| Q3 | 110 | 550 | 60,500 |
| Q4 | 110 | 550 | 60,500 |
| **FY** | | | **221,000** |

**Cross-foot, two ways.**
1. Sum of quarters: 50,000+50,000+60,500+60,500 = 221,000.
2. Recomputed at half-year grain, aligned to the effective-date boundary: H1 (old
   price) = 200 units × $500 = 100,000; H2 (new price) = 220 units × $550 = 121,000;
   100,000 + 121,000 = 221,000.
Both agree. ✓

**Boxed answer: FY revenue = $221,000.**

**Named trap — "averaged-price trap."** Blending the price to a flat $525
(midpoint of 500 and 550) and applying it to all four quarters' actual volumes gives
100×525 + 100×525 + 110×525 + 110×525 = 52,500+52,500+57,750+57,750 = **220,500** —
wrong by $500, and silently so. The error exists because averaging hides the
interaction between the price step and the volume step landing at the same boundary;
it would be larger still if the two steps landed in different quarters.

---

## Fixture B — Personnel, loaded rate with prorated mid-year hire

**Inputs.** One role group: Customer Success Rep. Base salary $80,000/year. Benefits
load 18%. Employer payroll tax 8%. Hire date July 1 (start of Q3).

**Build.**
- Loaded annual cost = 80,000 × (1 + 0.18 + 0.08) = 80,000 × 1.26 = **$100,800**.
- Employed 2 of 4 quarters (Q3, Q4) → proration = 2/4 = 50%.
- Prorated budget-year cost = 100,800 × 50% = **$50,400**.

| Quarter | Employed? | Cost |
|---|---|---|
| Q1 | no | 0 |
| Q2 | no | 0 |
| Q3 | yes | 25,200 |
| Q4 | yes | 25,200 |
| **FY** | | **50,400** |

**Cross-foot, two ways.**
1. Sum of quarters: 0+0+25,200+25,200 = 50,400.
2. Recomputed from the annual driver: 100,800 × (2 quarters ÷ 4) = 50,400.
Both agree. ✓

**Boxed answer: FY prorated loaded cost = $50,400.**

**Named trap 1 — "base-salary trap."** Using base salary instead of the loaded rate:
80,000 × 50% = **$40,000** — understates true cost by $10,400 because it drops the 26%
benefits-and-tax load entirely.

**Named trap 2 — "no-proration trap."** Applying the full loaded rate with no proration
for the July 1 start: **$100,800** — overstates true cost by $50,400 because it pays the
rep for two quarters they were never on payroll.

Both traps compound if made together (using base salary, unprorated: $80,000 — which
happens to look "more reasonable" than either single trap, which is exactly why both
errors must be checked independently rather than sanity-checked against each other).

---

## Fixture C — Opex (fixed / variable / stepped) + mid-year capex depreciation

**Opex inputs.**
- **Fixed:** Rent, $10,000/quarter flat.
- **Variable:** Sales commission, 5% of that quarter's revenue (uses Fixture A's revenue).
- **Stepped:** Support-software licensing, tied to headcount. Threshold: headcount ≤ 20
  → $2,000/quarter; headcount > 20 → $3,200/quarter. Headcount is 18 in Q1–Q2 and rises
  to 22 in Q3 (reflecting the Fixture B hire plus other planned hires), holding at 22 in Q4.

**Opex build.**
| Quarter | Rent (fixed) | Commission (variable, 5% of revenue) | Software (stepped) |
|---|---|---|---|
| Q1 | 10,000 | 2,500 (5%×50,000) | 2,000 (headcount 18, tier 1) |
| Q2 | 10,000 | 2,500 (5%×50,000) | 2,000 (headcount 18, tier 1) |
| Q3 | 10,000 | 3,025 (5%×60,500) | 3,200 (headcount 22, tier 2 — jump lands here) |
| Q4 | 10,000 | 3,025 (5%×60,500) | 3,200 (headcount 22, tier 2) |
| **FY** | **40,000** | **11,050** | **10,400** |

**Cross-foot.** Rent: 10,000×4 = 40,000. ✓ Commission: 2,500+2,500+3,025+3,025 =
11,050, and recomputed as 5% × FY revenue (221,000) = 11,050. ✓ Software: 2,000+2,000+
3,200+3,200 = 10,400. ✓

**Named trap — "stepped-as-variable trap."** Smoothing the $1,200/quarter jump into an
implied per-head rate (e.g., ($10,400 ÷ 4 quarters) ÷ ~20 average headcount ≈ $130/head,
then reapplying that rate) invents cost behavior the license contract doesn't have and
misprices every quarter, not just the ones after the threshold.

**Named trap — "stepped-as-fixed trap."** Holding the license cost flat at $2,000/quarter
all year because "that's what it was in Q1" ignores the Q3 threshold crossing —
understates FY opex by (3,200−2,000)×2 quarters = **$2,400**.

**Capex / depreciation inputs.** One asset: cost $60,000, salvage value $10,000, useful
life 5 years, in-service date July 1 (start of Q3).

**Build.**
- Full annual straight-line depreciation = (60,000 − 10,000) ÷ 5 = **$10,000/year**.
- In service 2 of 4 quarters → proration = 50%.
- Budget-year depreciation = 10,000 × 50% = **$5,000**.

| Quarter | In service? | Depreciation |
|---|---|---|
| Q1 | no | 0 |
| Q2 | no | 0 |
| Q3 | yes | 2,500 |
| Q4 | yes | 2,500 |
| **FY** | | **5,000** |

**Cross-foot, two ways.** Sum of quarters: 0+0+2,500+2,500 = 5,000. Recomputed:
10,000 × (2÷4) = 5,000. Both agree. ✓

**Boxed answer: FY depreciation = $5,000 (D&A line; excluded from EBITDA, included in EBIT).**

**Named trap — "full-year-depreciation trap."** Applying the full $10,000 with no
in-service proration overstates D&A by $5,000 and, if EBITDA and EBIT get conflated
downstream, misstates operating profitability by the same amount.

---

## Fixture D — CM / EBITDA / EBIT rollup + target-gap lever judgment

**Rollup, using Fixtures A–C (FY figures).**

| Line | Amount |
|---|---|
| Revenue (Fixture A) | 221,000 |
| less Variable costs — commission (Fixture C) | (11,050) |
| **= Contribution Margin** | **209,950** |
| less Fixed + Stepped opex — rent 40,000 + software 10,400 (Fixture C) | (50,400) |
| less Personnel (Fixture B) | (50,400) |
| **= EBITDA** | **109,150** |
| less D&A (Fixture C) | (5,000) |
| **= EBIT** | **104,150** |

**Cross-foot.** CM: 221,000 − 11,050 = 209,950. ✓ EBITDA: 209,950 − 50,400 − 50,400 =
109,150. ✓ EBIT: 109,150 − 5,000 = 104,150. ✓

**Boxed answer: FY EBITDA = $109,150; FY EBIT = $104,150.**

### Target-gap lever judgment

Leadership target: EBITDA = **$115,000**. Initial gap = 115,000 − 109,150 = **$5,850**.

**Option 1 — legitimate.** A signed sublease reduces rent from $10,000 to $8,500/quarter
for Q3–Q4 (a completed, documented renegotiation — traceable operational cause).
Savings = 1,500 × 2 quarters = $3,000. *Legitimate — apply it.*
EBITDA recomputed: 109,150 + 3,000 = **112,150**. Residual gap = 115,000 − 112,150 =
**$2,850**.

**Option 2 — legitimate, but only partially closes the gap.** Confirmed pipeline
supports 5 additional units in Q4 at the existing $550 price, sold as a signed house
account under contract terms with no rep commission attached (driver-supported,
evidence-backed — traceable operational cause, and specific enough to confirm it
doesn't flow through the Fixture C commission line). Incremental revenue = 5 × 550 =
$2,750, commission-exempt per the contract terms, so the full amount flows to EBITDA.
*Legitimate — apply it.* EBITDA recomputed: 112,150 + 2,750 = **114,900**. Residual gap
= 115,000 − 114,900 = **$100** — reported honestly rather than rounded away or papered
over with an unsupported top-up. (If a lever instead touches ordinary commissioned
revenue, its commission must be netted out before adding it to EBITDA — this house
account is deliberately structured so that step doesn't apply here.)

**Option 3 — red flag.** A proposed $2,850 opex-to-capex reclassification (moving a
cost off the P&L with no underlying asset acquired or capitalization event) that
happens to close the *original* $2,850 gap remaining after Option 1, exactly. *Reject.*
**Named trap — "near-closure trap."** The fact that this lever closes the gap almost
exactly, with zero operational cause behind it, is itself the reason to reject it — not
a coincidence to be reasoned past. No asset was purchased, no capitalization event
occurred; the size of the number was chosen to fit the gap, not derived from a business
event.

**Final reported result.** EBITDA after legitimate levers only = **$114,900**.
Residual gap to target = **$100**, reported honestly (candidates: escalate for a small
target reset, or continue searching for one more small legitimate lever — not
manufactured by accepting Option 3).
