# Worked Examples (Golden Fixtures)

Each example is a `{ inputs → expected outputs }` pair with a known-correct answer. These seed the acceptance contract and, once execution-eval is wired, are what the skill is *run against* and graded on.

## Example A — Direct materials, AQ purchased ≠ AQ used (the trap)

**Inputs:** SP = $5.00/lb, std qty = 2 lb/unit, actual output = 1,000 units → SQ allowed = 2,000 lb. AP = $5.30/lb, AQ **purchased** = 2,500 lb, AQ **used** = 2,150 lb.

**Expected:**
- DM price variance = (AP − SP) × AQ **purchased** = (5.30 − 5.00) × 2,500 = **$750 U**
- DM quantity variance = (AQ **used** − SQ allowed) × SP = (2,150 − 2,000) × 5.00 = **$750 U**
- **Trap check:** using AQ used (2,150) for the price variance gives $645 — wrong. Price uses *purchased*, quantity uses *used*.
- **Reconciliation:** because purchased ≠ used, price + quantity do NOT tie to one flexible-budget variance — the gap is an inventory-timing effect. State it; do not force a tie-out.

## Example B — Fixed overhead: spending vs production-volume

**Inputs:** budgeted FOH = $100,000, denominator (normal) capacity = 10,000 std hrs → std FOH rate = $10/hr. Actual output → SH allowed = 9,000 hrs. Actual FOH = $104,000.

**Expected:**
- FOH spending (budget) variance = actual − budgeted = 104,000 − 100,000 = **$4,000 U**
- Applied FOH = SH allowed × std rate = 9,000 × 10 = $90,000
- FOH production-volume variance = budgeted − applied = 100,000 − 90,000 = **$10,000 U** — a **capacity/denominator artifact** (operated below the 10,000-hr denominator), NOT controllable spending; must not be ranked by raw dollars against controllable lines.
- **Reconciliation:** total under-applied = actual − applied = 104,000 − 90,000 = $14,000 = $4,000 spending + $10,000 volume. Ties. ✓

## Example C — Materials mix & yield (two substitutable inputs)

**Inputs:** materials X ($3/lb) and Y ($5/lb). Standard mix 60% X / 40% Y. Std total input for actual output = 1,000 lb (→ SQ allowed: X 600, Y 400). Actual: total 1,050 lb, X = 700 lb, Y = 350 lb. Std weighted price = 0.6×3 + 0.4×5 = $3.80/lb.

**Expected:**
- **Yield variance** = (actual total − std total) × std weighted price = (1,050 − 1,000) × 3.80 = **$190 U**
- **Mix variance** = Σ (actual qty − std-mix qty at actual total) × std price
  - X: (700 − 630) × 3 = +$210 ; Y: (350 − 420) × 5 = −$350 → **$140 F** (shifted toward cheaper X)
- **Reconciliation:** total DM quantity variance = Σ (actual − SQ allowed) × std price = X (700−600)×3 = $300 U + Y (350−400)×5 = $250 F = **$50 U**; and mix + yield = $140 F + $190 U = **$50 U**. Ties. ✓
