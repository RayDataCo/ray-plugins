# Status enum, deficiency catalog, and set-reduction

Companion to SKILL.md. This file details how to assign the closed-enum status, the full
deficiency catalog, the substance-not-heading trap, and how the report reduces to gradeable sets.

## The closed status enum

Every canonical clause gets exactly one status, uppercase, from this set only:

- `PRESENT` — the clause's substance is in the contract and its load-bearing sub-parts are
  there. Location cited. Defect = `—`.
- `DEFICIENT` — the clause's substance is in the contract but a load-bearing sub-part is
  missing. It is still "there", so DEFICIENT is mutually exclusive with ABSENT. Location cited.
  Defect = one specific line naming the missing sub-part.
- `ABSENT` — the clause topic appears nowhere in the contract. Location = `—`. Defect = `—`.

There is no fourth status. "Partial", "weak", "unfavorable", "N/A" are not allowed. Weakness
that is about fairness (e.g. a low cap, a short survival that still exists) is NOT a deficiency —
deficiency is strictly the absence of a load-bearing sub-part, never a fairness judgment.

## Deficiency catalog (load-bearing sub-parts, per clause)

A trigger firing => DEFICIENT, and the defect line names the missing sub-part.

### NDA
- **#4 Confidentiality obligations** — DEFICIENT if only one of non-use / non-disclosure is
  present, or if there is no standard-of-care obligation.
  - defect e.g.: "obligations bind non-disclosure but state no non-use restriction."
- **#5 Term of agreement and duration of confidentiality obligation** — DEFICIENT if an
  agreement term is stated but there is no survival/duration for the confidentiality obligation
  (or the obligation duration is stated but no agreement term).
  - defect e.g.: "term stated but confidentiality obligation has no survival period."
- **#2 Standard exclusions** — DEFICIENT if an exclusions provision exists but omits
  load-bearing categories (public, already-known, independently developed, rightfully received).
  - defect e.g.: "exclusions list public/known but omit independently-developed information."

### MSA
- **#3 Term and termination** — DEFICIENT if it has no effect-of-termination/survival language,
  or omits termination-for-convenience or termination-for-cause.
  - defect e.g.: "termination clause states no effect-of-termination / survival of obligations."
- **#5 Intellectual-property ownership** — DEFICIENT if it assigns/allocates work product but is
  silent on background IP or the license to use background IP.
  - defect e.g.: "assigns work product but is silent on background-IP ownership/license."
- **#8 Limitation of liability** — DEFICIENT if no liability cap amount is stated, OR there is
  no exclusion of consequential/indirect damages.
  - defect e.g.: "limitation of liability present but states no cap amount."

### SaaS
- **#2 Fees, auto-renewal, and price changes** — DEFICIENT if auto-renewal is stated but there
  is no notice-to-cancel / cancellation window.
  - defect e.g.: "auto-renewal stated but no notice-to-cancel window."
- **#5 Data ownership and return / deletion on termination** — DEFICIENT if data ownership is
  stated but it is silent on return or deletion of data on termination.
  - defect e.g.: "customer data ownership stated but silent on deletion/return on termination."
- **#9 Limitation of liability** — DEFICIENT if no cap amount, OR no consequential-damages
  exclusion.
- **#10 Term, termination, and suspension** — DEFICIENT if no effect-of-termination/survival.

### Generic
- **#5 Term and termination** — DEFICIENT if no effect-of-termination/survival language.
- **#6 Confidentiality** — DEFICIENT if confidentiality is present but has no survival period.
- **#8 Limitation of liability** — DEFICIENT if no cap amount, OR no consequential-damages
  exclusion.

For clauses without an enumerated trigger, mark DEFICIENT only when a genuinely load-bearing
sub-part is missing; do not invent sub-parts. When unsure between PRESENT and DEFICIENT and no
listed trigger fires, prefer PRESENT.

## Substance-not-heading trap (worked)

Match by substance, not by the presence of a like-named heading.

- A section titled "Term and Termination" that also fixes the contract duration satisfies both
  the "Term" substance and the "termination" substance — do not mark a separate "Term" ABSENT.
- Confidentiality obligations living inside a "Proprietary Information" section satisfy the
  Confidentiality clause.
- An IP assignment buried in an "Ownership of Deliverables" section satisfies the IP clause.
- Governing law stated in a "Miscellaneous" boilerplate paragraph satisfies Governing law.

Only mark ABSENT when the substance appears nowhere in the document.

## Reduction to gradeable sets

The finished report reduces losslessly to three sets, which is how it is graded:

- `PRESENT{clause}` — clause names with status PRESENT.
- `ABSENT{clause}` — clause names with status ABSENT.
- `DEFICIENT{clause: defect}` — clause names with status DEFICIENT, each paired with its defect.

Invariants (verify before returning):

1. The union of the three sets == the canonical clause set for the type, with each clause in
   exactly one set. No clause omitted, duplicated, or added.
2. `|PRESENT| + |DEFICIENT| + |ABSENT|` == set size, and equals the Summary line's `p + d + a`.
3. Each DEFICIENT clause has a specific non-empty defect; no PRESENT/ABSENT clause has a defect.
4. Statuses drawn only from {PRESENT, ABSENT, DEFICIENT}.
5. No fairness/favorability/enforceability/advice language anywhere except the mandatory
   disclaimer. The optional "Other clauses observed" section is non-graded and carries no
   commentary.

## Worked reduction example (illustrative, not a fixture)

An MSA with scope, fees, term, confidentiality, IP, warranties, and indemnification present;
a limitation-of-liability clause missing entirely; and a termination clause with no survival
language reduces to:

- ABSENT = { Limitation of liability, Insurance, ... any others truly missing ... }
- DEFICIENT = { Term and termination: "no effect-of-termination / survival of obligations" }
- PRESENT = { all remaining canonical MSA clauses that are fully present }

with `|PRESENT| + |DEFICIENT| + |ABSENT| == 12`.
