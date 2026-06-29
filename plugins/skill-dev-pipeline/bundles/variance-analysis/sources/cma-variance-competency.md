# Standard Costing & Variance Analysis — Core Competency

CMA Part 1 (managerial accounting). This is the *body of knowledge* a management accountant holds about variances — the knowledge the skill must be translated FROM, not the procedure itself.

## The standard-costing frame

A **standard cost** is what a unit *should* cost: `standard price × standard quantity`, set per cost element — direct materials (DM), direct labor (DL), variable overhead (VOH), fixed overhead (FOH). A **variance** is the gap between actual and standard, decomposed so each piece points at a cause and an owner.

Abbreviations: AP/AR = actual price/rate · SP/SR = standard price/rate · AQ/AH = actual quantity/hours · SQ/SH = standard quantity/hours *allowed* · F = favorable · U = unfavorable.

## The budget hierarchy (this is the spine)

Three reference points, never to be confused:
- **Static (master) budget** — set before the period at *budgeted* output volume.
- **Flexible budget** — the static budget *re-flexed to ACTUAL output*. `SQ allowed = std qty/unit × actual units`; `SH allowed = std hr/unit × actual units`. Everything efficiency/price compares against the FLEXED figure, never the static one.
- **Actual results**.

Two-level decomposition of the total (static-budget) variance:
- **Sales-volume variance** = `(actual units − budgeted units) × budgeted contribution margin per unit`. Isolates the *volume* effect.
- **Flexible-budget variance** = `actual − flexible budget (at actual volume)`. Isolates *price + efficiency* effects.
- Identity: `sales-volume variance + flexible-budget variance = static-budget variance`.

## Per-element variances

**Direct materials** (note the two quantities differ when purchases ≠ usage):
- **Price (rate) variance** = `(AP − SP) × AQ PURCHASED` — owner: purchasing.
- **Quantity (usage/efficiency) variance** = `(AQ USED − SQ allowed) × SP` — owner: production.

**Direct labor:**
- **Rate variance** = `(AR − SR) × AH`.
- **Efficiency variance** = `(AH − SH allowed) × SR`.

**Variable overhead:**
- **Spending variance** = `actual VOH − (AH × std VOH rate)`.
- **Efficiency variance** = `(AH − SH allowed) × std VOH rate`.

**Fixed overhead** (the trickiest — two variances of very different character):
- **Budget (spending) variance** = `actual FOH − budgeted FOH`.
- **Production-volume variance** = `budgeted FOH − applied FOH`, where `applied FOH = SH allowed × std FOH rate`. This is a **denominator/capacity artifact** — it measures over/under-utilization of the capacity the fixed cost was spread over. It is NOT a controllable spending issue and must never be read as one.

## Mix & yield (multiple inputs or multiple products)

When inputs are substitutable or output is multi-product, the quantity/volume variance splits further:
- **Materials mix variance** = `Σ (actual mix% − standard mix%) × total actual qty × std price`.
- **Materials yield variance** = `(actual total input − standard total input for actual output) × std weighted price`.
- **Sales-mix** and **sales-quantity** variances decompose the sales-volume variance for a multi-product line.

## The favorable/unfavorable rule (one rule, applied everywhere)

A variance is **Favorable (F) if it increases operating income, Unfavorable (U) if it decreases it.** Operationally: for *cost* variances, actual > standard ⇒ U; for *revenue/contribution* variances, actual > budget ⇒ F. Apply this single operating-income test to every line so the sign never has to be guessed element-by-element.

## Reconciliation identities (the integrity check)

Sub-variances must sum to their parent:
- DM price + DM quantity = total DM flexible-budget variance *(only when AQ purchased = AQ used; otherwise the difference is an inventory-timing effect, not a tie-out failure)*.
- DL rate + DL efficiency = total DL variance (same shape for VOH spending + VOH efficiency).
- FOH spending + FOH production-volume = total over/under-applied FOH.
- Sales-volume + flexible-budget = static-budget variance.

If a reconciliation doesn't tie, a sign or an input is wrong — fix before reporting.
