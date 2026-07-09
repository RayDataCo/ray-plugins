<!-- iteration: 0 -->

# Budget Hierarchy — Static vs Flexible vs Actual

Read this for the Level 0→3 decomposition and the flexing mechanics behind Steps 3–4.

## The three budgets

- **Static (master) budget** — built once at the start of the period for *budgeted* output.
  Fixed quantities, fixed volume. Never compare price/efficiency against this directly.
- **Flexible budget** — the static budget *re-flexed to actual output*: standard prices and
  rates held constant, but quantities/hours scaled to what actual production should have used.
  `flexible-budget cost = standard cost per unit × actual units`.
- **Actual results** — what really happened (actual prices × actual quantities).

## Flexing mechanics

```
SQ allowed = standard qty per unit × ACTUAL output     (materials)
SH allowed = standard hours per unit × ACTUAL output   (labor / VOH)
```

Everything in price/efficiency analysis compares **actual vs flexible**, never **actual vs
static**. Comparing against the static budget conflates a volume difference with an
efficiency/price difference — that is the static-vs-flex error Step 3 exists to kill.

## Level 0 → 3 decomposition

```
Level 0   STATIC-BUDGET VARIANCE              = actual result − static budget
                 │
                 ├── Level 1a  SALES-VOLUME VARIANCE
                 │             = (actual units − budgeted units) × budgeted CM/unit
                 │             (pure volume effect; standards held constant)
                 │
                 └── Level 1b  FLEXIBLE-BUDGET VARIANCE
                               = actual result − flexible budget at actual volume
                                       │
                       Level 2/3 ──────┴── price/rate + efficiency/quantity per element
                                           (DM price+qty, DL rate+eff, VOH spend+eff, FOH)
```

**Reconciliation identity:** sales-volume variance + flexible-budget variance = static-budget
variance. Use this as the top-level integrity check (SKILL.md Step 6).

## Sales-volume variance with budgeted CM

The sales-volume variance is measured at **budgeted contribution margin per unit** (not price,
not actual CM) so it isolates the volume effect from any price/cost effects:

```
sales-volume variance = (actual sales units − budgeted sales units) × budgeted CM per unit
```

Favorable when actual units exceed budget (more volume ⇒ more contribution). For a
multi-product firm this further splits into **sales-mix variance + sales-quantity variance**
— load `mix-yield.md`.
