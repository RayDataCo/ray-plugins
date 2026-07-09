<!-- iteration: 0 -->
# Response-Tier Framework: Override, Then Grid

Read this when deciding a response tier (SKILL.md Step 5).

## Apply in order — the consumption override is checked BEFORE the grid, never after

**(1) Consumption override.** If any downstream consumer has already acted on the bad data before detection (a report was sent, an automated decision fired, a number was already relied on, an email already went out), silent-fix is NOT available — escalate to at least quarantine-and-continue regardless of how the grid below would otherwise classify it. This check happens first, unconditionally, before criticality or impact is even considered.

**(2) Consumer criticality.**
- **HIGH** — financial reporting, regulatory/external delivery, production ML training or serving, customer-facing billing/compliance.
- **LOW** — internal exploratory use, unshipped/unlaunched surfaces, dev/staging.

**(3) Data-correctness impact.**
- **SEVERE** — wrong in a way that cannot be cheaply isolated or filtered, risks being silently trusted, often embedded in an aggregate.
- **BOUNDED** — isolable to an identifiable subset/partition, or degrades gracefully (e.g., mechanically identifiable exact-duplicate keys removable by a dedup pass).

**(4) Decision.**
| Criticality | Impact | Tier |
|---|---|---|
| HIGH | SEVERE | **stop-the-line** — halt the pipeline and block downstream consumption immediately, even at the cost of delaying delivery entirely |
| HIGH | BOUNDED | **quarantine-and-continue** — isolate/flag the specific bad partition while letting unaffected data and consumers keep running |
| LOW | SEVERE or BOUNDED, AND no prior consumption | **silent-fix** — patch and rerun with no special ceremony |

**Silent-fix requires ALL THREE of** LOW criticality, bounded-or-otherwise-acceptable impact, AND no prior consumption — never just low criticality alone or bounded impact alone.

## Kills

- Defaulting to quarantine as a "safe middle choice" for any low-stakes incident even with zero consumers and zero criticality — if nothing is HIGH and nothing was consumed, silent-fix is correct, not quarantine ceremony.
- Letting a high-profile consumer's dashboard alone trigger stop-the-line when the impact is actually a mechanically-isolable duplicate-key problem — criticality and impact are weighed together, not criticality alone.
- Missing that a "trivial-looking" incident already had its number consumed via an automated weekly email or report — always ask explicitly whether any consumer has already acted, never assume "probably not yet."
