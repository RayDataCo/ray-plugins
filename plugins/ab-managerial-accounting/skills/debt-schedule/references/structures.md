<!-- iteration: 2 -->

# Instrument structures

Read this when the instrument isn't a plain level-payment loan. Forcing the level-payment annuity formula onto a structure that doesn't use it produces a schedule that is internally consistent arithmetic but describes the wrong instrument.

## Fully amortizing — level-payment

The default case SKILL.md's Step 3 covers directly: a single constant payment `PMT` each period, computed via the annuity formula, with the interest/principal split shifting toward principal over time as the balance shrinks. Ends at (or very near) a zero balance at maturity.

## Fully amortizing — level-principal

Instead of a level payment, the *principal* portion is constant each period: `Principal (per period) = P / n`. Interest is still `Beginning balance × r`, so the total payment (`Interest + Principal`) is largest in the first period and declines every period thereafter — the opposite payment shape from level-payment, even though both structures fully amortize to zero. Do not apply the level-payment PMT formula here; there is no single constant payment to solve for.

## Bullet

No scheduled principal amortization during the term — the borrower pays interest-only each period, and the *entire* principal balance is due in a single payment at maturity. The "amortization table" for a bullet instrument is really just a periodic interest calculation (Step 5's floating-rate or a fixed-rate equivalent) repeated to maturity, plus one final principal-repayment row. There is no interest/principal split to compute period over period because there is no scheduled principal.

## Balloon

Structured like a level-payment (or level-principal) loan with amortization calculated on a *longer* notional schedule than the loan's actual maturity — e.g., payments computed as if amortizing over 20 years, but the loan actually matures (and the remaining balance comes due in full) at year 7. Two things must both be tracked and kept distinct: the notional amortization schedule (which determines the periodic payment and the interest/principal split each period, exactly as in the level-payment case) and the actual maturity date (which determines when the remaining, still-substantial balance becomes due as a single balloon payment). Compute the periodic payment off the notional schedule's `n`, but stop the table at the actual maturity period and show the remaining balance as the final balloon payment — do not let the notional `n` imply the loan actually amortizes to zero.

## Revolver

Not a fixed repayment schedule at all — a revolving credit facility where the borrower draws and repays against a commitment limit over time, and interest is calculated only on the amount actually drawn and outstanding at any given time (using the confirmed day-count convention, exactly as in Step 5), not on the full commitment. A commitment fee (typically a small bps rate) is usually charged on the *undrawn* portion of the commitment separately from interest on the drawn balance. There is no single "amortization table" for a revolver in the level-payment sense — instead, track drawn balance over time (as given or as requested) and apply the interest/fee mechanics per period to whatever is actually outstanding.

## Term Loan B (TLB) hybrid

A common leveraged-loan structure: light nominal amortization during the term — commonly a schedule around 1% of original principal per year, paid quarterly — with the large majority of principal repaid as a bullet at final maturity. Mechanically this is a level-principal (or level-payment) schedule for the small nominal-amortization portion, combined with a bullet for the remainder — treat the two pieces separately rather than trying to force one formula to cover both: compute the small periodic principal payments per the level-principal or level-payment identities against the nominal-amortization percentage, and carry the large remaining balance to maturity as a bullet exactly as in the Bullet section above.
