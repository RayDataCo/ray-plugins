<!-- iteration: 0 -->

# Mix & Yield — Advanced Decomposition

**Load this ONLY when there is more than one input material OR more than one product.** For a
single input and a single product there is no mix or yield to compute — stop and use the plain
DM usage / sales-volume variance instead.

Mix & yield split a *quantity*-side variance into two parts: how the inputs (or products) were
**proportioned** (mix) vs how much **total** was consumed/sold (yield/quantity).

## 1. Materials mix variance

How the actual blend of inputs differed from the standard blend, priced at standard:

```
materials mix variance = Σ_i (actual qty_i − std-mix qty_i) × std price_i
  where std-mix qty_i = actual TOTAL input × standard mix % for input i
```

Equivalent form: `(actual mix% − std mix%) × total actual qty × std price`, summed over inputs.
Favorable when the blend shifts toward cheaper inputs.

## 2. Materials yield variance

How much total input was used vs the standard total input for the actual output, at the
**standard weighted-average price**:

```
materials yield variance = (actual total input − std total input for actual output) × std weighted price
  where std weighted price = Σ_i (std mix %_i × std price_i)
```

Favorable when less total input is consumed than the standard allows.

**Reconciliation:** materials mix variance + materials yield variance = total materials usage
(quantity) variance. Cross-check against the direct method:
`Σ_i (actual qty_i − std qty_i for actual output) × std price_i`.

## 3. Sales-mix and sales-quantity variances

These decompose the **sales-volume variance** (not the price variance) for a multi-product firm,
measured at budgeted contribution margin per unit:

```
sales-mix variance      = Σ_p (actual mix%_p − budget mix%_p) × total actual units × budgeted CM/unit_p
sales-quantity variance = (total actual units − total budgeted units) × budget mix%_p × budgeted CM/unit_p, summed
```

**Reconciliation:** sales-mix variance + sales-quantity variance = sales-volume variance.
Sales-mix is favorable when the actual mix tilts toward higher-CM products; sales-quantity is
favorable when total units beat budget.

## Worked numbers

The fully reconciled multi-input mix+yield example (Scenario C: Material X 60%/$3.00, Material
Y 40%/$5.00, std weighted price $3.80 — MIX $1,400 F, YIELD $1,900 U, total usage $500 U) lives
in `worked-examples.md`.
