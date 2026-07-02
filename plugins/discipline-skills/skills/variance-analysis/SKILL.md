---
name: variance-analysis
description: >-
  Compute and interpret standard-costing cost and revenue variances: direct-materials price and quantity/usage, direct-labor rate and efficiency, variable-overhead spending and efficiency, fixed-overhead spending and production-volume, sales-volume and flexible-budget variances, plus multi-input/multi-product mix and yield. Use whenever a user gives actual vs standard (or budgeted) prices, rates, quantities, hours, or output and wants variances computed, decomposed, reconciled, labeled favorable/unfavorable, assigned to a responsibility center, or interpreted (why is X unfavorable, what to investigate) — including CMA/CFA exam-style problems and manufacturing/ops cost reviews. Do NOT use for statistical variance (σ², standard deviation, ANOVA, variance of a dataset), portfolio mean-variance / return volatility / variance-covariance, project earned-value (EVM) cost or schedule variance, or generic ETL/data-diff reconciliation between two tables.
---
<!-- iteration: 0 -->

# Variance Analysis

**One job:** turn budget-to-actual / standard-costing data into a *reconciled, signed, responsibility-assigned* variance breakdown plus a management-by-exception investigation list. The win over a naive answer: you flex to actual output before computing efficiency/price, you never flip a sign, your sub-variances provably sum to the parent, and you read each variance as a *signal to investigate*, not a verdict.

Run the steps below in order. Pull exact formulas from the reference files — do not reconstruct them from memory.

## Procedure

**Step 1 — Confirm scope and pick the variance set.** From the ask + the data present, decide which elements/levels are in play: direct materials (DM), direct labor (DL), variable overhead (VOH), fixed overhead (FOH), sales-volume/flexible-budget, mix & yield. State which variances you will compute before computing any. *Guard:* if the request is statistical variance (σ²/ANOVA/dataset dispersion), mean-variance volatility, or EVM, STOP — this is the wrong skill; redirect.

**Step 2 — Build the input inventory; name what's missing.** For each element collect SP/SR, standard qty or hours per unit, AP/AR, actual qty/hours, **actual output units**, budgeted output units, budgeted contribution margin/unit, actual + budgeted FOH, denominator/normal capacity + standard FOH rate. *Guard (AQ split):* for materials capture **AQ purchased AND AQ used as two distinct numbers** — they differ whenever purchases ≠ usage and the two DM variances use different ones. Name any missing input explicitly; never silently assume it.

**Step 3 — Flex the budget.** `SQ allowed = standard qty/unit × ACTUAL output`; `SH allowed = standard hr/unit × actual output`. Everything downstream compares against this flexed figure. *Guard (flex):* never compare efficiency/price against the static/master budget — only against the flexible budget at actual volume.

**Step 4 — Compute each variance with the canonical formula.** Read `references/formulas.md` for the exact card and the three-column layout (`AQ×AP | AQ×SP | SQ×SP`). *Guards:* DM price uses **AQ purchased**, DM quantity uses **AQ used** (the swap is the #1 DM error). FOH spending = actual − **budgeted**; FOH production-volume = **budgeted − applied** (applied = SH allowed × std FOH rate) — do not confuse budgeted with applied.
- For the static→sales-volume→flexible-budget decomposition, read `references/budget-hierarchy.md`.
- For mix & yield, read `references/mix-yield.md` — **only when >1 input or >1 product.**

**Step 5 — Label F/U with ONE rule (no sign guessing).** A variance is **Favorable (F) if it increases operating income, Unfavorable (U) if it decreases it.** Operationally: for cost variances, actual > standard ⇒ U, actual < standard ⇒ F; for revenue/contribution variances, actual > budget ⇒ F. Apply this single test to every line so signs never flip element-to-element. *Guard (sign):* if you find yourself deciding sign case-by-case, re-derive from the operating-income effect instead.

**Step 6 — Reconcile (integrity gate; do not skip).** Show the arithmetic that sub-variances sum to their parent:
- DM price + DM quantity = total DM flexible-budget variance *(only when AQ purchased = AQ used; if not, state the inventory-timing difference instead of forcing a tie-out).*
- DL rate + DL efficiency = total DL variance (same pattern for VOH spending + VOH efficiency = total VOH).
- FOH spending + FOH production-volume = total over/under-applied FOH.
- Sales-volume variance + flexible-budget variance = static-budget variance.
If a reconciliation does not tie out, a sign or an input is wrong — return to Step 4/5 before reporting.

**Step 7 — Interpret by exception (signals, not verdicts).** Read `references/interpretation.md`. For each variance apply: (a) **materiality** — flag only those large in absolute dollars AND as a % of the standard base; small ones are noise. (b) **Controllability / responsibility center** — assign each to its owner. *Guard (production-volume):* mark the **FOH production-volume variance as a denominator/capacity artifact, NOT a controllable spending issue**, and never rank it by raw dollars. (c) **Cross-variance linkage / gaming** — flag tradeoff signatures (favorable DM price + unfavorable DM usage ⇒ cheap low-quality material; favorable DL rate + unfavorable DL efficiency ⇒ lower-skill labor). (d) **Standard currency** — note whether standards look current/attainable vs ideal/stale.

**Step 8 — Emit the auditable deliverable.** Always show formula + plugged-in numbers per line, not just the answer. Before answering any multi-element problem, pattern-match against `references/worked-examples.md`.

## Output contract (every deliverable must satisfy)

- **Every variance line shows its formula and the actual numbers plugged in** (auditability).
- **Every variance line carries an F/U label** produced by the Step-5 operating-income rule.
- **A reconciliation block is present and ties out** (or the timing/rounding reason it doesn't is stated).
- **FOH production-volume variance, whenever computed, is labeled a capacity/denominator artifact** and is NOT placed on a controllable spending owner.
- **DM price uses AQ purchased; DM quantity uses AQ used** — verifiable from the "inputs used" column.

Deliverable order: (1) scope line; (2) variance table — columns `element | variance | formula | inputs used | $ | F/U | responsibility center`; (3) reconciliation proof; (4) investigation list ranked by materiality × controllability; (5) interpretation narrative (gaming/linkage flags, standard-currency caveat, "signal not verdict"); (6) caveats for any assumed/missing inputs.

## Reference files (load on demand)

- `references/formulas.md` — exact formula card per element + the three-column computation layout. **Read at Step 4** before computing any variance.
- `references/budget-hierarchy.md` — static vs flexible vs actual; Level 0→1→2→3 decomposition; sales-volume + flexible-budget split with budgeted CM. **Read at Steps 3–4** for the volume/flex level.
- `references/mix-yield.md` — materials mix & yield, sales-mix & sales-quantity. **Read at Step 4 ONLY when >1 input or >1 product.**
- `references/interpretation.md` — materiality thresholds, controllability/responsibility mapping, production-volume-not-controllable rule, gaming/linkage signatures, standard-currency check. **Read at Step 7.**
- `references/worked-examples.md` — fully reconciled numeric examples (incl. an AQ purchased ≠ used trap and an FOH production-volume case). **Pattern-match before answering a multi-element problem.**

## When NOT to use

Skip this skill (it would be a precision failure to fire) for: **statistical variance** — σ², standard deviation, ANOVA, "variance of this column/dataset"; **portfolio mean-variance** / return volatility / variance-covariance; **project earned-value (EVM)** cost variance (CV) or schedule variance (SV); and **generic FP&A commentary or ETL/data-diff reconciliation** with no standards and no price/efficiency decomposition (e.g. "explain why marketing came in over budget" with a single line-item delta, or "why don't these two tables match"). The discriminator that flips a bare "analyze this budget" into a FIRE is the presence of **standards (or budgeted prices/rates/quantities) AND actual output** to flex against.
