<!-- iteration: 0 -->

# Worked Examples — Fully Reconciled

Pattern-match against these before answering any multi-element problem. Each shows
inputs → formula → value → F/U → reconciliation. Sign rule: cost variance is **U if actual >
standard, F if actual < standard** (operating-income effect).

---

## Scenario A — DM price + quantity, AQ purchased ≠ AQ used (the trap)

**Inputs:** SP = $4.00/lb; standard 2 lb/unit; actual output 5,000 units;
AQ **purchased** = 12,000 lb @ AP = $4.10; AQ **used** = 10,200 lb.

**Flex:** SQ allowed = 2 × 5,000 = **10,000 lb**.

| element | variance | formula | inputs used | $ | F/U | owner |
|---|---|---|---|---|---|---|
| DM | price | (AP − SP) × **AQ purchased** | (4.10 − 4.00) × **12,000** | 1,200 | U | purchasing |
| DM | quantity | (**AQ used** − SQ allowed) × SP | (**10,200** − 10,000) × 4.00 | 800 | U | production |

- **DM price = $1,200 U** — computed on **12,000 purchased**.
- **DM quantity = $800 U** — computed on **10,200 used** vs 10,000 allowed.
- **TRAP:** computing price on AQ used (10,200) gives $1,020 — that is WRONG and must not
  appear. Price uses purchased (12,000); quantity uses used (10,200).

**Reconciliation note:** price + quantity = $2,000 U, but because **purchased (12,000) ≠ used
(10,200)** these do NOT form one clean flexible-budget variance. State the inventory-timing
difference (1,800 lb bought-but-not-yet-used sits in inventory) rather than forcing a single
tie-out.

---

## Scenario B — FOH spending vs production-volume

**Inputs:** budgeted FOH = $100,000; denominator capacity = 20,000 std hrs ⇒
std FOH rate = 100,000 ÷ 20,000 = **$5.00/hr**; standard 2 hr/unit; actual output 9,000 units;
actual FOH = $104,000.

**Flex:** SH allowed = 2 × 9,000 = **18,000 hr**; applied FOH = 18,000 × 5.00 = **$90,000**.

| element | variance | formula | inputs used | $ | F/U | owner |
|---|---|---|---|---|---|---|
| FOH | spending | actual FOH − budgeted FOH | 104,000 − 100,000 | 4,000 | U | facilities |
| FOH | production-volume | budgeted FOH − applied FOH | 100,000 − 90,000 | 10,000 | U | **none — capacity artifact** |

- **FOH spending = $4,000 U.**
- **FOH production-volume = $10,000 U** → labeled a **denominator/capacity artifact,
  non-controllable**, assigned NO controllable spending owner.
- **TRAP:** production-volume is **budgeted − applied** ($10,000), NOT actual − applied
  ($14,000); and the spending line uses budgeted, not applied.

**Reconciliation:** spending + production-volume = 4,000 + 10,000 = **$14,000** = total
under-applied FOH = actual − applied = 104,000 − 90,000 = $14,000 ✓.

---

## Scenario C — multi-input materials mix + yield

*(Reached only via the mix/yield branch — load `mix-yield.md`.)*

**Inputs:** Material X 60% @ $3.00, Material Y 40% @ $5.00 ⇒ std weighted price =
0.6×3 + 0.4×5 = **$3.80**; std total input for actual output = 10,000 lb; actual total input =
10,500 lb; actual X = 7,000, actual Y = 3,500.

**Std-mix at actual total (10,500):** X = 60% × 10,500 = 6,300; Y = 40% × 10,500 = 4,200.

| variance | formula | inputs used | $ | F/U |
|---|---|---|---|---|
| MIX | Σ (actual − std-mix) × std price | (7,000−6,300)×3 + (3,500−4,200)×5 = +2,100 − 3,500 | 1,400 | F |
| YIELD | (actual total − std total) × std wtd price | (10,500 − 10,000) × 3.80 | 1,900 | U |

- **MIX = $1,400 F**, **YIELD = $1,900 U**, **total usage = −1,400 + 1,900 = $500 U.**

**Reconciliation (direct method cross-check):**
X (7,000 − 6,000) × 3 = 3,000 U; Y (3,500 − 4,000) × 5 = 2,500 F ⇒ 3,000 − 2,500 = **$500 U** ✓
(matches mix + yield).

---

## Scenario D — management-by-exception ranking (materiality × controllability)

**Materiality threshold:** ≥ $1,000 absolute **AND** ≥ 2% of that element's standard cost base
(both gates).

| variance | $ | F/U | owner | % of base | material? | exception action |
|---|---|---|---|---|---|---|
| DL efficiency | 9,500 | U | production | 11.9% | YES | **#1 investigate** |
| DM quantity | 8,000 | U | production | 4.0% | YES | **#2 investigate** (link to DM price) |
| FOH production-volume | 10,000 | U | capacity artifact | n/a | NO (non-controllable) | **excluded; labeled artifact** |
| DM price | 1,200 | F | purchasing | 0.6% | NO alone | surfaced only via gaming-linkage to DM qty |
| DL rate | 300 | F | labor market | 0.4% | NO | drop (noise) |
| VOH spending | 500 | U | production | 1.2% | NO | drop (noise) |

**Correct interpretation behaviors:**

- The largest absolute number ($10,000 FOH production-volume) is **NOT ranked #1** and is **not
  assigned a controllable owner** — the controllability filter demotes it to an excluded
  capacity artifact. Ranking purely by absolute dollars would be wrong.
- **DM price $1,200 F + DM quantity $8,000 U** is flagged as the **cheap-material-drives-waste**
  gaming signature: purchasing's cheap buy may have caused production's overusage. Cross-link the
  two owners (purchasing ↔ production) even though DM price alone is immaterial.
- **DL rate $300 F** (0.4%) and **VOH spending $500 U** (1.2%) fall below the absolute and/or %
  threshold ⇒ **dropped as noise** (both gates applied, not just one).
- Every line is framed as a **signal to investigate, not a verdict** — e.g. "DL efficiency
  $9,500 U (11.9%): ask production what changed," not "production failed."

**Ranked investigation list:** (1) DL efficiency $9,500 U; (2) DM quantity $8,000 U + its
linkage to DM price. FOH production-volume excluded as artifact; DL rate and VOH spending
dropped as noise.
