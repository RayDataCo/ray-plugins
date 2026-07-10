# Canonical clause sets — expanded, with substance cues

This file expands the four canonical clause sets from SKILL.md. The clause **names are
authoritative and verbatim** — never rename, merge, split, add, or drop them. The "substance
cues" are only aids for deciding PRESENT vs ABSENT by substance (not by heading). A clause is
addressed if its substance appears anywhere, even under a different or combined heading.

Set sizes are fixed: NDA = 9, MSA = 12, SaaS = 12, Generic = 12. The coverage table must have
exactly that many rows.

## Type inference (when the caller did not supply a type)

Infer from the title and preamble, then mark the source `inferred from title/preamble`:

- `NDA` — "Non-Disclosure Agreement", "Confidentiality Agreement", "Mutual NDA", "Proprietary
  Information Agreement".
- `MSA` — "Master Services Agreement", "Master Agreement", "Professional Services Agreement";
  work is ordered via Statements of Work / SOWs / Order Schedules.
- `SaaS` — "Subscription Agreement", "SaaS Agreement", "Software-as-a-Service", "Cloud Services
  Agreement", hosted access via an Order Form, per-seat/usage subscription fees.
- `Generic` — a commercial agreement that fits none of the above cleanly (supply, reseller,
  partnership, general services without an SOW spine, etc.).

When the caller supplies the type, use it and mark the source `caller-provided` — do not
second-guess it.

## NDA designation

Report on the `Designation:` header line (NDA only):

- `Mutual` — both parties act as discloser and recipient and both owe the confidentiality
  obligations ("each party", "Discloser and Recipient" defined reciprocally).
- `One-way` — only one party discloses / only one party is bound as recipient.
- `Unspecified` — the text does not make the direction determinable.

The clause "#9 Mutual vs one-way designation" is a separate table row about whether the
agreement *states* its designation; the header `Designation:` line reports your read of it.

## NDA / confidentiality agreement (9)

1. **Definition of Confidential Information** — what information is covered; marking rules;
   oral disclosures. Cue: "Confidential Information means…".
2. **Standard exclusions from confidential information** — carve-outs for info that is public,
   already known, independently developed, or rightfully received from a third party.
3. **Permitted use / purpose limitation** — use only for the defined Purpose/evaluation.
4. **Confidentiality obligations (non-use, non-disclosure, standard of care)** — obligations
   not to use and not to disclose, plus a standard of care (e.g. "reasonable care" / same care
   as own confidential info); need-to-know limits.
5. **Term of agreement and duration of confidentiality obligation** — how long the agreement
   lasts AND how long the confidentiality obligation survives (often longer than the term).
6. **Return or destruction of materials** — on request/termination, return or destroy
   confidential materials and copies.
7. **Remedies (injunctive / equitable relief)** — acknowledgment that breach causes
   irreparable harm; entitlement to injunctive/equitable relief.
8. **Governing law** — the law that governs the agreement.
9. **Mutual vs one-way designation** — whether the agreement states it is mutual or one-way.

## MSA / master services agreement (12)

1. **Scope of services (SOW mechanism)** — services delivered, usually ordered via SOWs/Order
   Forms; SOW precedence.
2. **Fees, invoicing, and payment terms** — rates/fees, invoicing cadence, payment due dates,
   late fees, expenses.
3. **Term and termination** — term; termination for convenience; termination for cause;
   effect of termination / survival / wind-down.
4. **Confidentiality** — mutual confidentiality obligations (may reference a separate NDA).
5. **Intellectual-property ownership** — ownership of work product/deliverables; background IP;
   license grants.
6. **Warranties and disclaimers** — performance/services warranties and disclaimers of implied
   warranties.
7. **Indemnification** — indemnities for IP infringement and third-party claims; procedure.
8. **Limitation of liability** — a liability cap amount AND an exclusion of consequential/
   indirect damages (plus any carve-outs).
9. **Insurance** — required coverage types and minimum limits.
10. **Governing law and dispute resolution** — governing law plus venue/arbitration/dispute
    process.
11. **Assignment** — restrictions on assignment/transfer; change-of-control.
12. **Independent-contractor / relationship of the parties** — no agency/partnership/joint
    venture; each party independent.

## SaaS / subscription (12)

1. **Grant of access / subscription and usage restrictions** — right to access the service;
   authorized users; prohibited/usage restrictions.
2. **Fees, auto-renewal, and price changes** — subscription fees; auto-renewal terms with a
   notice-to-cancel window; how/when prices may change.
3. **Data protection and security (DPA reference)** — security measures; processing of personal
   data; reference to or incorporation of a Data Processing Addendum.
4. **Service levels (SLA) / uptime and credits** — uptime commitment; service credits/remedies.
5. **Data ownership and return / deletion on termination** — customer owns its data; export/
   return and deletion of data on termination.
6. **Intellectual-property ownership of the service** — provider owns the service/software and
   any improvements; feedback license.
7. **Warranties and disclaimers** — service warranty and disclaimers of implied warranties.
8. **Indemnification** — IP-infringement and third-party-claim indemnities.
9. **Limitation of liability** — cap amount AND consequential-damages exclusion.
10. **Term, termination, and suspension** — subscription term; termination rights; suspension
    for non-payment/breach; effect of termination.
11. **Governing law** — governing law (and venue if stated).
12. **Confidentiality** — mutual confidentiality of non-public information.

## Generic commercial agreement — fallback set (12)

Use only for `Generic`. A conventional general-commercial-contract skeleton.

1. **Parties and recitals** — identification of the parties and background/recitals.
2. **Definitions** — defined terms section.
3. **Subject matter / scope of the agreement** — what the agreement is about; deliverables/
   obligations.
4. **Consideration / payment terms** — price/consideration and payment mechanics.
5. **Term and termination** — duration; termination rights; effect of termination/survival.
6. **Confidentiality** — confidentiality of exchanged information; survival.
7. **Representations and warranties** — the parties' reps/warranties and disclaimers.
8. **Limitation of liability** — cap amount AND consequential-damages exclusion.
9. **Indemnification** — indemnities and procedure.
10. **Governing law and dispute resolution** — governing law plus dispute/venue mechanism.
11. **Assignment** — assignment/transfer restrictions.
12. **Notices and general provisions** — notices; entire agreement; severability; waiver;
    amendment (boilerplate).
