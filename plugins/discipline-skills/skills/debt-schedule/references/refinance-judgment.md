<!-- iteration: 2 -->

# Refinance/prepayment cost taxonomy and exit-cost judgment

Read this whenever a refinance or prepayment offer is being evaluated. The single most common and consequential judgment failure in refinancing math is netting only the cost of *originating* the new loan while silently assuming the *old* loan is free to exit.

## Cost taxonomy — what "all-in cost" actually includes

**On the new financing:**
- Origination fee (often quoted in points/bps of new principal).
- Closing costs (legal, diligence, title/recording where applicable).
- Any prepayment penalty, breakage, or make-whole the *new* lender charges if the *new* loan is itself later prepaid — usually not relevant to the immediate breakeven math but worth naming if the offer includes unusual new-loan lock-up terms.

**On the existing loan being retired — the piece that's easy to miss:**
- **Prepayment penalty / call premium.** Many loan and bond instruments carry an explicit prepayment penalty for retiring debt before maturity, sometimes structured as a declining schedule (e.g., 3% in year 1, 2% in year 2, 1% in year 3, 0% thereafter). Bonds in particular often distinguish a *soft-call* period (prepayable at a premium) from a *hard-call* period (non-callable at all, or only under narrow conditions) — confirm which regime the existing instrument is in before assuming it can even be prepaid at all, let alone for how much.
- **Breakage cost.** If the existing loan is hedged with an interest-rate swap or cap, unwinding that hedge early when the underlying loan is retired can trigger a breakage payment — the cost of unwinding the swap at its current mark-to-market, which can be substantial if rates have moved significantly since the hedge was put on. This cost is entirely separate from, and in addition to, any prepayment penalty on the loan itself.
- **Make-whole provision.** Common in bonds and some institutional term loans: a make-whole clause requires the issuer to pay the present value of *all remaining scheduled interest payments* (discounted at a specified rate, often a small spread over a Treasury benchmark) if prepaid early, rather than a flat percentage penalty. This can be a very large number relative to a flat prepayment penalty, especially for a loan with a long remaining term and a wide rate differential to the discount benchmark — do not assume a make-whole is roughly equivalent in size to a percentage-based penalty without actually computing it.

## Why the existing-loan exit cost is the trap

These costs live in the *existing* loan's own governing documentation — not in the new financing offer's term sheet, which naturally only quotes costs relevant to originating itself. Nobody hands the analyst the old loan's exit cost unprompted; it has to be actively looked up or asked about. Omitting it doesn't make the refinance math wrong in an obviously-flagged way — it just makes the computed breakeven and net savings look better than they actually are, because a real cost has been left out of the "all-in" cost that was supposed to capture everything.

## The judgment framing when the exit cost isn't given

If the existing loan's exit cost is not provided:

1. Compute and present the breakeven and net savings using the costs that *are* known (new-loan costs only) — this arithmetic is still correct and useful as far as it goes.
2. Explicitly and separately flag that the existing loan's own exit cost is unconfirmed — name what it could be (prepayment penalty, breakage, make-whole) rather than a vague "there may be other costs."
3. If the computed net margin is thin (e.g., a few thousand dollars of net savings against a six- or seven-figure principal, or a breakeven close to the remaining term), state plainly that even a modest unconfirmed exit cost on the existing loan could flip the decision from net-positive to net-negative — the recommendation should be presented as "the computed numbers, pending this one open question," not as a closed decision.
4. Do not round this off with a hedge-word like "should generally be favorable" that quietly treats the open question as resolved. Keep the determinate arithmetic (breakeven, net savings as computed) visibly separate from the actual go/no-go judgment, which remains open until the missing fact is confirmed.
