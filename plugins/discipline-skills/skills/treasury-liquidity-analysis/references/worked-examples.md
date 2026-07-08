<!-- iteration: 0 -->

# Worked Examples — Treasury Liquidity Analysis

Pattern-match against these four fixtures before answering a multi-part liquidity-analysis build. Each is fully derived from its inputs, shows the formula and the numbers plugged in per line (per Step 8), and boxes the known answer. Fixtures A and C and Fixture D's Q4 anchor share the same underlying period-end balance sheet — a reminder that a real liquidity read draws on the same source data across ratio battery, available liquidity, covenant headroom, and trend analysis, not four unrelated calculations.

---

## Fixture A — Ratio battery, with the restricted-cash trap

**Inputs:** Total current assets $136,200; Total current liabilities $47,000. Of the $136,200 in current assets: unrestricted cash $15,040, restricted cash $3,400 (disclosed only in a footnote — pledged as collateral against the term loan, not broken out on the face of the balance sheet), accounts receivable $42,770, other current assets (inventory, prepaid) $74,990. ($15,040 + $3,400 + $42,770 + $74,990 = $136,200 ✓.)

**Step 2 — restricted-cash check:** Footnote discloses $3,400 restricted cash pledged as loan collateral. Excluded from quick/cash numerators only.

**Current ratio** (full CA, restricted cash stays in):
`Current ratio = Total CA / Total CL = 136,200 / 47,000 = 2.8979... ≈ **2.90x**`

**NWC** (full CA):
`NWC = Total CA − Total CL = 136,200 − 47,000 = **$89,200**`

**Unrestricted cash:**
`Unrestricted cash = Reported cash − Restricted cash = 18,440 − 3,400 = $15,040`

**Quick ratio** (unrestricted cash + AR only):
`Quick ratio = (Unrestricted cash + AR) / Total CL = (15,040 + 42,770) / 47,000 = 57,810 / 47,000 = **1.23x**`

**Cash ratio** (unrestricted cash only):
`Cash ratio = Unrestricted cash / Total CL = 15,040 / 47,000 = **0.32x**`

**Trap check — naive figures if restricted cash were left in the quick/cash numerators:**
- Naive quick ratio = (15,040 + 3,400 + 42,770) / 47,000 = 61,210 / 47,000 = 1.30x → **overstated by 0.07x**
- Naive cash ratio = (15,040 + 3,400) / 47,000 = 18,440 / 47,000 = 0.39x → **overstated by 0.07x**

**Boxed answers:** Current ratio **2.90x** · Quick ratio **1.23x** · Cash ratio **0.32x** · NWC **$89,200** · naive quick/cash overstated by **0.07x each** if the footnote-only restricted cash isn't excluded.

---

## Fixture B — Cash conversion cycle, average vs. ending balance

**Inputs:** Full-year period. Revenue $310,000; COGS $198,000. Days convention: 365 (annual, default). Balances:
- AR: beginning $40,500, ending $40,500 (flat across the year)
- Inventory: beginning $46,710, ending $71,488 (inventory build during the year)
- AP: beginning $30,647, ending $30,647 (flat across the year)

**Step 3 — average balances:**
- Average AR = (40,500 + 40,500) / 2 = $40,500
- Average Inventory = (46,710 + 71,488) / 2 = $59,099
- Average AP = (30,647 + 30,647) / 2 = $30,647

**Average-balance CCC** (computed from full-precision intermediate values, each shown rounded to 2 decimals for display — the total is computed BEFORE rounding the components, so it will not always tie exactly to re-adding the rounded display figures by hand; that's a rounding-order note, not an inconsistency):
- `DSO = (40,500 / 310,000) × 365 = **47.69 days**`
- `DIO = (59,099 / 198,000) × 365 = **108.95 days**`
- `DPO = (30,647 / 198,000) × 365 = **56.50 days**`
- `CCC = DSO + DIO − DPO (unrounded) = **100.13 days**`

**Ending-balance-only CCC** (same formulas, ending balance instead of average):
- Ending DSO = (40,500 / 310,000) × 365 = 47.69 days (AR flat, no change)
- Ending DIO = (71,488 / 198,000) × 365 = 131.78 days
- Ending DPO = (30,647 / 198,000) × 365 = 56.50 days (AP flat, no change)
- Ending-balance CCC = DSO + Ending DIO − DPO (unrounded) = **122.97 days**

**Distortion:**
`Ending-balance CCC − Average-balance CCC = 122.97 − 100.13 = **22.84-day overstatement**`

AR and AP were held flat period-over-period in this fixture, so the entire 22.84-day overstatement traces to the inventory buildup — inventory grew from $46,710 to $71,488 (a ~53% increase) across the year, which the ending-balance-only calculation reads as if that elevated ending level had applied to the whole period, when in fact the period average was $59,099. **Driven entirely by inventory growth** in this fixture (AR and AP held flat by construction so the isolated effect is visible), exactly the failure mode Step 3 exists to catch — in a live analysis AR/AP typically move too, and the same average-vs-ending logic applies to each independently.

**Boxed answers:** DSO **47.69** · DIO **108.95** · DPO **56.50** · Average-balance CCC **100.13 days** · Ending-balance CCC **122.97 days** · Distortion **22.84 days**, driven by inventory.

---

## Fixture C — Available liquidity and covenant headroom, both dollar directions

**Inputs:** Revolver commitment $75,000 (committed facility); amount drawn $22,000; letters of credit outstanding $4,500; unrestricted cash $15,000. Term loan outstanding $60,000 (current portion $8,000 + long-term portion $52,000). TTM EBITDA $26,000. Leverage covenant maximum 3.5x.

**Step 4 — available liquidity, LC-netted:**
`Undrawn committed revolver availability = Commitment − Drawn − LCs outstanding = 75,000 − 22,000 − 4,500 = **$48,500**`
`Available liquidity = Unrestricted cash + Undrawn committed availability = 15,000 + 48,500 = **$63,500**`

**Trap check — naive (LC-unnetted) available liquidity:**
`Naive = Unrestricted cash + (Commitment − Drawn) = 15,000 + 53,000 = $68,000`
`Overstatement = 68,000 − 63,500 = **$4,500**` — exactly the LC amount, as expected: every dollar of LCs outstanding reduces true availability dollar-for-dollar, and skipping the netting step overstates available liquidity by precisely that amount.

**Step 5 — total funded debt and leverage** (LCs excluded from funded debt, even though they were just netted from availability above — both treatments are correct, they answer different questions):
`Total funded debt = Revolver drawn + Term loan (current + LT) = 22,000 + 8,000 + 52,000 = **$82,000**`
`Leverage = Total funded debt / TTM EBITDA = 82,000 / 26,000 = **3.15x**` (vs. 3.5x maximum — PASS, inside the covenant)

**Ratio-form headroom:**
`Covenant maximum − Current leverage = 3.5 − 3.15 = **0.35x**`

**Dollar-form headroom, direction (a) — debt-side, holding EBITDA constant:**
`Maximum permitted debt = Covenant maximum × TTM EBITDA = 3.5 × 26,000 = $91,000`
`Incremental debt capacity = 91,000 − 82,000 = **$9,000**`

**Dollar-form headroom, direction (b) — EBITDA-side, holding debt constant:**
`Minimum required EBITDA = Total funded debt / Covenant maximum = 82,000 / 3.5 = $23,428.57`
`Incremental EBITDA cushion = TTM EBITDA − Minimum required EBITDA = 26,000 − 23,428.57 = **$2,571.43**`

Both dollar figures are required — reporting the $9,000 debt-side figure alone (even alongside the 0.35x ratio-form figure) is NOT "both directions." The $2,571.43 EBITDA-side figure says something the debt-side figure doesn't: how much TTM EBITDA could fall, holding debt fixed, before the covenant breaches — a materially different (and much thinner-sounding, in percentage terms) cushion than the $9,000 debt-capacity number suggests on its own. If EBITDA is trending down, both cushions compress simultaneously.

**Boxed answers:** Available liquidity **$63,500** (naive/unnetted **$68,000**, overstated by **$4,500**) · Total funded debt **$82,000** · Leverage **3.15x** vs. 3.5x max · Ratio-form headroom **0.35x** · Debt-side dollar headroom **$9,000** · EBITDA-side dollar headroom **$2,571.43**.

---

## Fixture D — Quarterly trend: CCC lengthening hidden by an improving current ratio

**Inputs:** Same company, Q1 → Q4 quarterly trend, 91-day quarterly convention. Q4 anchors to the same period-end balance sheet as Fixtures A and C (current ratio 2.90x, NWC $89,200, available liquidity $63,500, revolver drawn $22,000) — full battery (Steps 2–5) is computed for all four quarters per Step 6; Q2/Q3 move monotonically between the Q1 and Q4 anchors shown below and are omitted here for space.

| Metric | Q1 | Q4 | Δ |
|---|---|---|---|
| Current ratio | 2.53x | 2.90x | +0.37x (rising) |
| NWC | $68,900 | $89,200 | +$20,300 (rising) |
| Quick ratio | 1.25x | 1.23x | −0.02x (flat-to-falling) |
| DSO | 42.30 | 39.76 | −2.54 days |
| DIO | 103.25 | 121.67 | +18.42 days |
| DPO | 59.15 | 53.86 | −5.29 days |
| CCC (91-day convention) | 86.40 | 107.57 | **+21.17 days (lengthening)** |
| Available liquidity | $73,700 | $63,500 | −$10,200 (**−13.8%**) |
| Revolver drawn | $14,000 | $22,000 | +$8,000 (**+57.1%**) |

**CCC check:** `CCC = DSO + DIO − DPO` → Q1: 42.30 + 103.25 − 59.15 = 86.40 ✓ · Q4: 39.76 + 121.67 − 53.86 = 107.57 ✓. Lengthening = 107.57 − 86.40 = 21.17 days, of which the DIO move (+18.42 days) accounts for ~87% (18.42 / 21.17 ≈ 0.87) — **the CCC lengthening is driven predominantly by inventory**, partially offset by a slight DSO improvement and amplified by a shortening DPO (both AR collection speeding up and vendor payment speeding up move CCC in opposite directions from the DIO story, but DIO dominates).

**Percent-change checks:** Available liquidity: (63,500 − 73,700) / 73,700 = −10,200 / 73,700 = **−13.8%**. Revolver drawn: (22,000 − 14,000) / 14,000 = 8,000 / 14,000 = **+57.1%**.

**Step 6 — the cross-check, applied:** Current ratio and NWC both rose every quarter Q1→Q4 — a naive read calls that "improving liquidity." The required cross-check: quick ratio over the same span is flat-to-slightly-falling (1.25x → 1.23x), and CCC lengthened by 21.17 days. **That combination — headline ratio rising while quick ratio and CCC don't confirm it — is itself the flag.** The current ratio/NWC improvement is being driven by the same inventory buildup that's lengthening the CCC: inventory is a current asset, so a growing inventory balance mechanically inflates current ratio and NWC even while it's a liquidity negative, not a positive (it's cash-consuming, not cash-generating, until sold).

**Step 6 — ranking the flags:**

1. **Flag A (structural, root cause) — CCC lengthening, DIO-driven.** Inventory is building faster than COGS is consuming it. This is the root-cause signal: a broader metric (current ratio, NWC) hides it by rising anyway, while a velocity-aware metric (CCC) and a near-cash metric (quick ratio, which excludes inventory entirely) both reveal it.
2. **Flag B (derivative, downstream of Flag A) — rising revolver draw / shrinking available liquidity.** The revolver draw grew 57.1% and available liquidity fell 13.8% over the same span — almost certainly funding the same inventory build identified in Flag A. This looks urgent in isolation (a fast-shrinking liquidity cushion), but it's a consequence of Flag A, not an independent problem — ranked below Flag A even though the percentage move is larger and more visually alarming.
3. **Flag C (ambiguous, needs more context) — DPO shortening (59.15 → 53.86 days).** A shortening DPO could mean the company is losing vendor negotiating leverage or being pushed to tighter terms (a stress signal) — or it could be a deliberate treasury choice (e.g., capturing early-payment discounts, or a shift in supplier mix toward vendors with shorter standard terms). Without vendor-level detail, this can't be diagnosed from the trend data alone — flagged for investigation, not weighted as heavily as Flags A or B.

**Boxed answers:** CCC 86.40 → 107.57 days (**21.17-day lengthening, ~87% DIO-driven**) · Current ratio 2.53x → 2.90x and NWC $68,900 → $89,200 both **rising** while quick ratio stays flat 1.25x → 1.23x · Available liquidity $73,700 → $63,500 (**−13.8%**) against revolver drawn $14,000 → $22,000 (**+57.1%**) · DPO 59.15 → 53.86 days · Ranking: **Flag A (CCC/inventory, structural) > Flag B (revolver/available liquidity, derivative) > Flag C (DPO shortening, ambiguous)**.
