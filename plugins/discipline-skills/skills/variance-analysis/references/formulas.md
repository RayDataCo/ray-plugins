<!-- iteration: 0 -->

# Formula Card — Standard-Cost Variances

Canonical formulas. Plug the actual numbers in; do not paraphrase. Variable definitions
are at the bottom. Sign is set separately by the operating-income rule (see SKILL.md Step 5),
but each formula's natural sign convention is noted.

## Table of contents

- [1. The three-column layout (use for DM and DL)](#1-the-three-column-layout)
- [2. Direct materials (DM)](#2-direct-materials-dm)
- [3. Direct labor (DL)](#3-direct-labor-dl)
- [4. Variable overhead (VOH)](#4-variable-overhead-voh)
- [5. Fixed overhead (FOH)](#5-fixed-overhead-foh)
- [6. Sales-volume and flexible-budget](#6-sales-volume-and-flexible-budget)
- [7. Variable definitions](#7-variable-definitions)

---

## 1. The three-column layout

Lay out every input-cost variance the same way so price and quantity always come from the
same scaffold:

```
   Column 1            Column 2            Column 3
   AQ × AP             AQ × SP             SQ allowed × SP
   (actual cost)       (actual qty at      (flexed standard
                        std price)          cost)

   Price variance    = Column 1 − Column 2   = (AP − SP) × AQ
   Quantity variance = Column 2 − Column 3   = (AQ − SQ allowed) × SP
   Total (flex-budget) = Column 1 − Column 3
```

**Materials caveat:** in the price column use **AQ purchased**; in the quantity column use
**AQ used**. When purchased ≠ used the three columns do NOT chain into one clean total —
see DM below.

## 2. Direct materials (DM)

- **DM price variance** = (AP − SP) × **AQ purchased** — owner: **purchasing**.
  - Uses **AQ purchased** (price is recognized when material is bought, not when used).
- **DM quantity / usage variance** = (**AQ used** − SQ allowed) × SP — owner: **production**.
  - Uses **AQ used** against the flexed standard quantity.
- `SQ allowed = standard qty per unit × ACTUAL output`.
- **Reconciliation:** DM price + DM quantity = total DM flexible-budget variance **only when
  AQ purchased = AQ used.** If purchased ≠ used, report each separately and state the
  inventory-timing difference; do not force a single total.

> The AQ-purchased-vs-AQ-used split is the #1 DM trap. Price on purchased, quantity on used —
> always. If you compute price on AQ used you will get the wrong number.

## 3. Direct labor (DL)

- **DL rate (price) variance** = (AR − SR) × AH — owner: HR / labor market.
- **DL efficiency (quantity) variance** = (AH − SH allowed) × SR — owner: production.
- `SH allowed = standard hours per unit × ACTUAL output`.
- **Reconciliation:** DL rate + DL efficiency = total DL flexible-budget variance.

## 4. Variable overhead (VOH)

- **VOH spending variance** = actual VOH − (AH × standard VOH rate).
- **VOH efficiency variance** = (AH − SH allowed) × standard VOH rate.
- **Reconciliation:** VOH spending + VOH efficiency = total VOH flexible-budget variance.
- VOH efficiency is driven entirely by labor-hour efficiency (it shares the AH vs SH driver).

## 5. Fixed overhead (FOH)

Fixed cost does not flex, so its two variances are structurally different from the variable ones.

- **FOH budget / spending variance** = **actual FOH − budgeted FOH** (budgeted = the lump-sum).
- **Applied FOH** = SH allowed × **standard FOH rate**, where
  `standard FOH rate = budgeted FOH ÷ denominator (normal-capacity) hours`.
- **FOH production-volume variance** = **budgeted FOH − applied FOH**.
  - This is a **capacity / denominator artifact**: it exists only because actual output
    differs from the denominator level used to set the rate. It is **NOT controllable
    spending** and carries no spending owner.
- **Reconciliation:** FOH spending + FOH production-volume = total over/under-applied FOH
  = actual FOH − applied FOH.

> FOH trap: do NOT compute production-volume as (actual − applied), and do NOT put applied
> FOH in the spending line. Spending = actual − budgeted; production-volume = budgeted − applied.

## 6. Sales-volume and flexible-budget

- **Sales-volume variance** = (actual units − budgeted units) × budgeted contribution margin per unit.
  - Revenue/contribution sign: actual units > budgeted ⇒ F.
- **Flexible-budget variance** = actual result − flexible budget at actual volume.
- **Reconciliation:** sales-volume variance + flexible-budget variance = static-budget variance.
- For multi-product, the sales-volume variance decomposes further into sales-mix +
  sales-quantity — see `mix-yield.md`.

## 7. Variable definitions

| Symbol | Meaning |
|---|---|
| SP | standard price per input unit (e.g. $/lb) |
| AP | actual price per input unit |
| SR | standard rate per labor hour |
| AR | actual rate per labor hour |
| AQ purchased | actual input quantity **bought** this period |
| AQ used | actual input quantity **consumed** in production |
| SQ allowed | standard qty per unit × actual output (the flexed standard quantity) |
| AH | actual labor hours worked |
| SH allowed | standard hours per unit × actual output (the flexed standard hours) |
| std FOH rate | budgeted FOH ÷ denominator (normal-capacity) hours |
| applied FOH | SH allowed × std FOH rate |
| budgeted FOH | the lump-sum fixed-overhead budget (does not flex) |
| budgeted CM/unit | budgeted contribution margin per unit |
