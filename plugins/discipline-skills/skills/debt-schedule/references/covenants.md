<!-- iteration: 2 -->

# Covenant definitions and headroom mechanics

Read this whenever a DSCR or leverage covenant test is being run. The single most consequential judgment call here is refusing to substitute a remembered generic formula for the specific agreement's own defined terms.

## Why CFADS (and Debt Service, and even EBITDA/Total Debt) are not "just plug in the numbers"

CFADS (Cash Flow Available for Debt Service) is not a standardized GAAP or regulatory line item — it is defined contractually, agreement by agreement, and the definition varies in ways that materially change the computed ratio. Common axes of variance:

- **Capex treatment.** Some agreements deduct only *maintenance* capex from CFADS (growth/expansion capex is added back or excluded from the deduction); others deduct *total* capex. A company with large growth capex can show a very different CFADS depending on which convention its agreement uses — this is not a rounding difference, it can be the difference between a covenant PASS and FAIL.
- **Reserve / sinking-fund treatment.** Some agreements require deposits into a debt-service reserve or sinking fund to be deducted from CFADS before the ratio is computed; others do not.
- **Mandatory prepayments.** Whether scheduled mandatory prepayments (e.g., excess-cash-flow sweeps) count as part of "Debt Service" in the denominator, or are excluded and tracked separately, varies by agreement.
- **Non-cash addbacks.** Treatment of non-cash items (stock comp, unrealized FX, certain one-time addbacks negotiated at closing) in the CFADS build varies agreement to agreement.

Total Debt and EBITDA (for the leverage ratio) have analogous, if usually smaller, sources of variance: whether Total Debt is gross or net of cash, whether EBITDA includes negotiated pro-forma addbacks (run-rate cost synergies, add-backs for one-time items), and how off-balance-sheet or lease obligations are treated.

**The rule:** pull these definitions from the *specific* credit agreement given for this instrument. If the agreement's actual definition isn't given, say so explicitly and name the generic assumption used (e.g., "no agreement definition provided; computed using EBITDA and Total Debt as reported, unadjusted — confirm against the actual agreement's defined terms before relying on this for compliance purposes") rather than silently presenting a generic-formula result as if it were agreement-specific.

## Both-direction headroom, worked

Headroom means "how much room is there before this covenant breaches" — and because a ratio has two variables, there are two distinct, both-valid ways to ask that question, holding one variable constant at a time.

**Worked DSCR example.** Suppose CFADS = $4,200,000, Debt Service = $3,000,000 (DSCR = 1.40x), and the agreement's minimum DSCR is 1.25x.

- *CFADS-cushion direction* (how much could CFADS fall, holding Debt Service constant, before breaching): minimum required CFADS at the current Debt Service = `1.25 × $3,000,000 = $3,750,000`. Headroom = `$4,200,000 − $3,750,000 = $450,000`.
- *Debt-Service-cushion direction* (how much could Debt Service rise, holding CFADS constant, before breaching): maximum supportable Debt Service at the current CFADS = `$4,200,000 / 1.25 = $3,360,000`. Headroom = `$3,360,000 − $3,000,000 = $360,000`.

These are genuinely different numbers ($450,000 vs. $360,000) because they hold different variables fixed — neither is "more correct"; report both.

**Worked leverage example.** Suppose Total Debt = $32,000,000, EBITDA = $10,000,000 (Leverage = 3.20x), and the agreement's maximum leverage is 3.50x.

- *Debt-cushion direction* (how much could Total Debt rise, holding EBITDA constant, before breaching): maximum supportable debt = `3.50 × $10,000,000 = $35,000,000`. Headroom = `$35,000,000 − $32,000,000 = $3,000,000`.
- *EBITDA-cushion direction* (how much could EBITDA fall, holding Total Debt constant, before breaching): minimum required EBITDA at the current debt = `$32,000,000 / 3.50 = $9,142,857.14`. Headroom = `$10,000,000 − $9,142,857.14 = $857,142.86`.

## The raw-dollar-vs-ratio-cushion trap

Comparing two covenants' headroom by raw dollar amount alone, without also looking at the underlying ratio-cushion percentage, can be misleading. In the worked example above, the leverage covenant's debt-cushion headroom ($3,000,000) is a much larger dollar figure than the DSCR covenant's CFADS-cushion headroom ($450,000) — but that comparison says nothing about which covenant is actually tighter, because the two ratios have very different bases (debt in the tens of millions vs. debt service in the millions). Always pair a raw-dollar headroom figure with the percentage cushion on the ratio itself (e.g., "leverage has $3,000,000 of headroom, which is a 3.20x vs. 3.50x — an 8.6% cushion on the ratio" vs. "DSCR has $450,000 of headroom, which is 1.40x vs. 1.25x — a 12% cushion on the ratio") before concluding one covenant is more comfortable than another.
