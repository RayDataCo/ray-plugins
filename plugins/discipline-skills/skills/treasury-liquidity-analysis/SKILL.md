---
name: treasury-liquidity-analysis
description: 'Assess near-term liquidity from financial statements and facility terms: the ratio battery (current/quick/cash ratios and NWC, restricted cash excluded from quick- and cash-ratio numerators only), cash conversion cycle (DSO + DIO - DPO on AVERAGE balances, stated days convention), available liquidity (unrestricted cash + undrawn committed revolver, net of letters of credit), and covenant headroom in ratio and dollar form, both directions. On trend data, ranks red flags by structural root cause over symptom (e.g. inventory-driven CCC lengthening hidden by an improving current ratio). Use whenever the user gives balance sheets, income-statement figures for CCC, or facility/covenant terms and wants liquidity ratios, a CCC, available liquidity, covenant headroom, or a trend read (incl. CTP/CFA-style problems). Do NOT use for cash-flow-forecasting (forward weekly receipts/disbursements projection), debt-schedule (single-instrument amortization mechanics), or financial-statements (statement preparation).'
---

# Treasury Liquidity Analysis

One job: given a balance sheet (single or multi-period), income-statement figures for CCC, and/or credit-facility and covenant terms, produce the full liquidity read — ratio battery, cash conversion cycle, available liquidity, covenant headroom, and (on trend data) a red-flag ranking by structural cause, not symptom.

## Scope fence — decline these, don't attempt them

- **Cash-flow-forecasting** (forward-looking, weekly bottoms-up receipts/disbursements build) — redirect; this skill's liquidity read is a snapshot/structural gut-check, not a substitute for that granular forecast.
- **Debt-schedule** (single-instrument amortization/rate/covenant mechanics on its own contractual terms) — redirect; this skill consumes debt-schedule outputs (total funded debt, current portion, scheduled principal) as inputs, it does not build or maintain the instrument-level schedule.
- **Financial-statements** (GAAP/IFRS statement preparation — recognition, measurement, classification) — redirect; this skill takes the balance sheet and income statement as given inputs.
- **No concrete statement or facility figures given** (e.g. "explain what a current ratio is") — ask for the actual numbers rather than computing on nothing.

## Procedure

**1. Confirm scope, decline neighbors.** Identify which sub-capability(ies) are wanted — ratio battery / CCC / available liquidity / covenant headroom / multi-period judgment read (or a combination) — on which entity and period(s). If the ask is actually one of the three neighbors above, stop and redirect, stating the reason. State which sub-capability(ies) you will compute before computing them.

**2. Ratio battery — restricted cash out of quick/cash ONLY.**
Actively check for a restricted-cash disclosure (often footnote-only, not a face-of-balance-sheet line: cash pledged as collateral, escrowed, or otherwise contractually restricted from general use). Name it "none disclosed" if absent — never silently assume zero when a footnote reference exists but is unquoted.
- `Current ratio = Total CA / Total CL` (full reported CA — restricted cash stays in)
- `NWC = Total CA − Total CL` (same, full CA)
- `Unrestricted cash = Reported cash − Restricted cash`
- `Quick ratio = (Unrestricted cash [+ marketable securities] + AR) / Total CL`
- `Cash ratio = (Unrestricted cash [+ marketable securities]) / Total CL`

The restricted-cash exclusion applies to quick ratio and cash ratio ONLY — never to current ratio or NWC, which correctly retain it as a current asset.

**3. Cash conversion cycle — AVERAGE balances, stated days convention.**
Use `(Beginning + Ending) / 2` for AR, Inventory, and AP — never the ending balance alone (AR/Inventory/AP are stock figures measured against revenue/COGS, which are full-period flow figures). Name the days convention explicitly: 365-day annual is the default for a full-year period; 91-day (365/4) applies to a single-quarter period with quarter-over-quarter averages. Hold the convention consistent within one analysis — mixing conventions across components or periods silently distorts the result. A quarterly-convention CCC is NOT expected to reconcile to a differently-convention'd annual CCC; state that explicitly rather than treating a mismatch as an error.
- `DSO = (Average AR / Revenue) × Days`
- `DIO = (Average Inventory / COGS) × Days`
- `DPO = (Average AP / COGS) × Days`
- `CCC = DSO + DIO − DPO`

When both beginning and ending balances are available, also compute the ending-balance-only CCC (same formulas, ending balance in place of average) and quantify the distortion: `Ending-balance CCC − Average-balance CCC`. Don't just assert the average figure is right — show the delta. If only an ending balance is available, state that limitation explicitly rather than silently treating it as the average.

**4. Available liquidity — net LCs from revolver availability, committed facilities only.**
- `Undrawn committed revolver availability = Commitment − Amount drawn − LCs outstanding`
- `Available liquidity = Unrestricted cash and equivalents + Undrawn committed revolver availability`

Only COMMITTED facilities count. An uncommitted line is a convenience product the bank can decline exactly when it's needed most — if present, label it separately and never blend it into the same total as committed capacity.

**5. Covenant headroom — ratio-form AND dollar-form BOTH directions.**
`Total funded debt = drawn, interest-bearing debt only` (revolver draws + term-loan current and long-term portions) — excludes LCs outstanding (contingent obligations, not drawn borrowings) even though LCs were netted from availability in Step 4. Both treatments are simultaneously correct — they answer different questions. State both explicitly; don't conflate into one generic "LCs affect X" line.
- `Leverage = Total funded debt / TTM EBITDA`, compared to the covenant maximum
- Ratio-form headroom: `Covenant maximum − Current leverage ratio`
- Dollar-form (a), debt-side, holding EBITDA constant: `(Covenant maximum × TTM EBITDA) − Total funded debt`
- Dollar-form (b), EBITDA-side, holding debt constant: `TTM EBITDA − Minimum required EBITDA`, where `Minimum required EBITDA = Total funded debt / Covenant maximum`

Both (a) and (b) are required whenever leverage-covenant headroom is in scope. Ratio-form plus only ONE dollar figure does NOT satisfy "both directions." If EBITDA is itself declining, note that headroom is shrinking from both directions simultaneously — faster than either component moving alone would suggest. Apply the same both-direction dollar logic to coverage covenants (minimum interest coverage, minimum FCCR) when they're in scope and inputs support it — see `references/formulas.md` for those forms.

**6. Multi-period — full battery per period, rank flags by structural cause.**
Run Steps 2–5 for every period, not just the latest. Before calling a rising current ratio or NWC "improving," cross-check it against the quick ratio and CCC for the same periods — a current ratio/NWC that rises purely because inventory is building will show quick ratio flat-to-falling and CCC lengthening, and THAT combination is the flag, not the headline ratio. Rank identified flags:
1. The structural, root-cause signal that a shorter-cycle metric (quick ratio, CCC) reveals but a broader one (current ratio, NWC) can hide.
2. The funding-side or otherwise downstream signal that is a consequence of the root-cause flag — note explicitly that it's derivative, not independent.
3. Signals that are ambiguous without more context (e.g., a vendor-level breakdown) — flag for investigation, don't weight equal to (1)/(2).

Never rank a derivative/symptom signal above the structural cause it flows from, even when it looks more urgent in isolation.

**7. Window-dressing awareness (a flagging gate, not a separate computation).**
On multi-period data, note that the ratio battery is structurally vulnerable to period-end window dressing (a revolver paydown-then-redraw, accelerated collections or delayed payables right at period-end, receivables factoring shortly before period-end). A metric that improves sharply right at a reporting date deserves scrutiny, not automatic credit. Don't claim manipulation is proven, and don't imply access to intra-period (daily/weekly) balances beyond what the given periods actually show.

**8. Emit the deliverable.** Always show the formula and the actual numbers plugged in per line, not just the answer. Structure per the Output contract below.

## Output contract

1. **Scope line** — sub-capability(ies) being computed, entity, period(s).
2. **Ratio battery** — current/quick/cash/NWC; unrestricted cash shown as its own line when the exclusion applies; a trap note if a footnote-only restricted-cash disclosure was found and applied.
3. **CCC** (if applicable) — DSO/DIO/DPO/CCC, days convention named, average-balance arithmetic shown per component, ending-balance distortion quantified when computable.
4. **Available liquidity** (if applicable) — LC-netting arithmetic shown; committed-vs-uncommitted noted if mixed facilities are present.
5. **Covenant headroom** (if applicable) — leverage (plus any coverage ratios in scope), PASS/breach vs. threshold, ratio-form headroom, and BOTH dollar-form headroom figures.
6. **Multi-period trend + ranking** (if applicable) — full battery per period, identified flags, ranked list with structural/derivative/ambiguous rationale.
7. **Caveats** — any assumed or missing inputs (restricted-cash disclosure, missing beginning balance, committed/uncommitted status, covenant definitions), stated explicitly, never silently resolved.

**Non-negotiables:** restricted cash excluded from quick/cash only, never current ratio/NWC · CCC built on average balances, ending-only flagged as a limitation rather than silently used · days convention named and held consistent, a cross-convention mismatch flagged as expected, not "fixed" · LCs netted from availability AND excluded from funded debt — both statements appear, never conflated into one · both dollar-form covenant-headroom directions computed whenever leverage headroom is in scope · a rising current ratio/NWC never reported as unqualified good news without the quick-ratio/CCC cross-check · red flags ranked structural-cause > derivative-symptom > ambiguous, never reversed.

## Reference files (load when needed)

- `references/formulas.md` — full formula card, including interest-coverage and FCCR both-direction headroom forms not inlined above. Read when a formula beyond the ratio-battery/CCC/liquidity/leverage basics is needed.
- `references/interpretation.md` — the average-vs-ending distortion judgment (when it's largest/smallest, growing vs. shrinking business), committed-vs-uncommitted reliability nuance (MAC clauses, borrowing-base mechanics), and why profitable companies die of illiquidity. Read when reasoning through Steps 3, 4, or 6 beyond the mechanical formula.
- `references/window-dressing-and-covenant-mechanics.md` — period-end window-dressing patterns and the trend-discipline defense; covenant cure mechanics (cure periods, equity cures, waivers/amendments) and why a technical-trigger distance isn't the same as a forced-outcome distance. Read when applying Steps 5 and 7 in depth.
- `references/worked-examples.md` — four fully-derived fixtures (ratio-battery restricted-cash trap; CCC average-vs-ending; available liquidity + covenant headroom both directions; quarterly-trend judgment/ranking). Pattern-match against these before answering a multi-part liquidity-analysis build.
