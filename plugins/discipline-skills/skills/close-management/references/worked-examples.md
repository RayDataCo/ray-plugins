<!-- iteration: 1 -->
# Worked Examples — Four Fixtures With Traps

Pattern-match against these before answering a multi-element close request.

---

## Fixture A — Expense accrual + reversal

**Setup:** IT contractor work performed in December, $32,000 estimated per the signed SOW milestone. Invoice not yet in hand at close. The actual invoice arrives in January at $34,750.

**December (accrual):**
```
Dr IT Contractor Expense          32,000
    Cr Accrued Liabilities            32,000
```

**January 1 (reversal):**
```
Dr Accrued Liabilities            32,000
    Cr IT Contractor Expense          32,000
```

**January (actual invoice):**
```
Dr IT Contractor Expense          34,750
    Cr Accounts Payable               34,750
```

**Net January P&L effect** = actual − reversed estimate = $34,750 − $32,000 = **+$2,750**.

**Two-period combined total** = $32,000 (December) + $2,750 (net January) = **$34,750**, equal to the actual invoice exactly.

> **Boxed answer:** December expense $32,000 · Net January effect +$2,750 · Two-month total $34,750.

**Trap:** If the reversal is skipped, December still shows $32,000 and January shows the full $34,750 actual — a combined $66,750 against a real cost of $34,750, a $32,000 double-count exactly equal to the un-reversed estimate. Accrued Liabilities would also sit with a permanent $32,000 credit balance that never clears, since nothing ever debited it back to zero.

---

## Fixture B — Prepaid amortization

**Setup:** $60,000 annual insurance premium paid in April, covering an April–March policy year (12 months). Fiscal year-end is December 31.

**April (capitalize):**
```
Dr Prepaid Insurance               60,000
    Cr Cash                            60,000
```

**Straight-line monthly rate** = $60,000 ÷ 12 = **$5,000/month**.

**Monthly amortization (Apr–Dec, 9 months to fiscal year-end):**
```
Each month:
Dr Insurance Expense                5,000
    Cr Prepaid Insurance                5,000
```

| Month | Amortization | Cumulative | Remaining balance |
|---|---|---|---|
| Apr | 5,000 | 5,000 | 55,000 |
| May | 5,000 | 10,000 | 50,000 |
| Jun | 5,000 | 15,000 | 45,000 |
| Jul | 5,000 | 20,000 | 40,000 |
| Aug | 5,000 | 25,000 | 35,000 |
| Sep | 5,000 | 30,000 | 30,000 |
| Oct | 5,000 | 35,000 | 25,000 |
| Nov | 5,000 | 40,000 | 20,000 |
| Dec | 5,000 | 45,000 | 15,000 |
| Jan (next FY) | 5,000 | 50,000 | 10,000 |
| Feb (next FY) | 5,000 | 55,000 | 5,000 |
| Mar (next FY) | 5,000 | 60,000 | **0** |

**Fiscal-year expense (Apr–Dec)** = 9 × $5,000 = **$45,000**.
**Year-end (Dec 31) prepaid balance** = $60,000 − $45,000 = **$15,000**.
**Zero-out check:** balance reaches exactly $0 at month 12 (March of the next fiscal year) — confirmed.

> **Boxed answer:** Monthly rate $5,000 · FY expense $45,000 · Year-end prepaid balance $15,000 · Zero-out confirmed at month 12.

**Trap:** If the full $60,000 were expensed in April instead of capitalized, April's P&L would be overstated by $60,000 − $5,000 = $55,000 relative to proper treatment, every remaining month within the fiscal year would be correspondingly understated (the 8 months May–Dec understate by $5,000 each, $40,000 total), and at any point in between there would be no Prepaid Insurance asset on the balance sheet at all — a balance-sheet understatement equal to whatever the correctly-computed remaining balance would have been at that date (e.g. $15,000 at December 31).

---

## Fixture C — Cutoff correction

**Setup:** Goods received December 30; vendor invoice dated January 5, both for $18,750. Under naive invoice-date convention, this would be booked entirely in January.

**Leg 1 — December (correcting accrual, correct period):**
```
Dr Supplies Expense                18,750
    Cr Accrued Liabilities             18,750
```

**Leg 2 — January 1 (reversal of the correcting accrual, Step 3's mechanic):**
```
Dr Accrued Liabilities             18,750
    Cr Supplies Expense                18,750
```

**Leg 3 — January (actual invoice, untouched, real AP liability):**
```
Dr Supplies Expense                18,750
    Cr Accounts Payable                18,750
```

**Before/after table:**

| Period | P&L effect — before correction (invoice-date booking) | P&L effect — after correction |
|---|---|---|
| December | $0 | +$18,750 (Leg 1) |
| January | +$18,750 | $0 net (Leg 2 −18,750, Leg 3 +18,750) |
| **Two-period total** | **$18,750** | **$18,750 — identical** |

**Account-balance check:** Accrued Liabilities: Leg 1 (+18,750) + Leg 2 (−18,750) = **$0**, cleanly cleared. Accounts Payable: Leg 3 (+18,750) = **$18,750**, correctly retains the real, still-owed vendor liability.

> **Boxed answer:** December correcting accrual $18,750 · January reversal $18,750 · January actual-invoice entry $18,750 (untouched) · Two-month total $18,750, unchanged before/after.

**Trap:** The natural-looking but wrong shortcut is to "fix" January by crediting Accounts Payable instead of Accrued Liabilities in Leg 2 — i.e., netting the correction directly against the real invoice entry rather than against the correcting accrual. That version either (a) never books the December leg at all, in which case the cost vanishes from both periods and the real vendor liability is erased from the books — worse than the original single-period misstatement, which at least recorded the cost somewhere — or (b) leaves Accrued Liabilities permanently uncleared, which is exactly the reversal-discipline failure Fixture A's trap is built to expose. Cutoff correction is Step 3's accrual+reversal mechanic applied to a period-assignment problem; it is never a shortcut against Accounts Payable.

---

## Fixture D — Materiality triage

**Setup:** Day+3 of a five-day close. Six open items against a **$25,000** materiality threshold.

| Item | Amount / range | Quantitative read | Uncertainty-width read | Qualitative override check | Verdict | Deciding factor |
|---|---|---|---|---|---|---|
| 1. Office supplies accrual | $3,200 | Well below threshold | Tight, single-vendor estimate | None | **WAIVE** | Quantitative threshold — immaterial on every axis |
| 2. Marketing campaign accrual | $22,000 (range $18,000–$29,000) | Below threshold on point estimate | Wide — upper bound crosses $25,000 threshold | None | **POST-CLOSE ADJUST** | Estimation-uncertainty width — range brackets the threshold despite point estimate reading under |
| 3. Equipment maintenance contract accrual | $28,000 (range $27,500–$28,500) | Above threshold | Tight (±$500), firm invoice imminent | None | **POST-CLOSE ADJUST** | Low estimation-uncertainty width — size is real but the number won't move, so no need to hold the close |
| 4. Related-party consulting fee | $6,500 | Well below threshold | Tight | **Related-party — disclosure/classification concern** | **BLOCK** | Qualitative override (related-party) |
| 5. Utilities true-up | $4,000 | Well below threshold | Tight | None | **WAIVE** | Quantitative threshold — immaterial |
| 6. Unexplained AP subledger variance | $9,800 | Below threshold | Tight | **Unexplained variance — control-integrity concern** | **BLOCK** | Qualitative override (control-integrity) |

> **Boxed answer:** Items 4 and 6 BLOCK; items 2 and 3 POST-CLOSE ADJUST; items 1 and 5 WAIVE. Every verdict names its deciding factor explicitly.

**Trap:** Applying the dollar threshold alone mis-sorts two pairs here. Item 3 ($28,000, above threshold) would mechanically BLOCK on a dollar-only read, but its tight, imminent-firm range means holding the close for it buys nothing — it correctly proceeds as POST-CLOSE ADJUST. Item 4 ($6,500, well below threshold) would mechanically WAIVE on a dollar-only read, but the related-party disclosure concern forces BLOCK regardless of size. The dollar-size ranking (item 3 > item 4) and the triage-verdict ranking (item 4 blocks, item 3 doesn't) invert — proof that the deciding factor is never the dollar amount alone.
