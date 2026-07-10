# Tasting — regulatory-notice-coverage

*A retired eval fixture, deliberately spent for demonstration (see the factory's
EVAL-SPEC): run the `regulatory-notice-coverage` station on the input below in YOUR environment (mise first),
then compare against the expected coverage and the graded criteria. This fixture never
grades again — it exists to SHOW, not to test.*

## The input

regime = "GDPR"; collection_context = "from_subject" (scope = G1..G12, 12 elements). notice_text:
---
Acme Insights — Privacy Notice

1. Who we are. Acme Insights Ltd, 12 King Street, Dublin 2, Ireland, is the controller of the personal data described in this notice. You can reach us at privacy@acme.example. Our Data Protection Officer can be contacted at dpo@acme.example.

2. Why we process your data. We process your personal data for three purposes: (a) to create and administer your account; (b) to carry out fraud detection and security monitoring; and (c) to comply with our legal and tax obligations. Our legal basis for purpose (a) is the performance of our contract with you, and for purpose (c) is compliance with a legal obligation. We do not rely on your consent as a legal basis for any of the processing described in this notice.

3. Who receives your data. We disclose your personal data to our cloud hosting provider, our payment processor, and our external auditors.

4. International transfers. We do not transfer your personal data outside the European Economic Area.

5. How long we keep your data. We keep account records for seven years after your account is closed in order to meet statutory bookkeeping obligations, and security logs for twelve months.

6. Your rights. You have the right to access your personal data, to have inaccurate data corrected, to have your data erased, to restrict our processing of it, and to data portability.

7. Automated decision-making. We do not carry out automated decision-making or profiling that produces legal or similarly significant effects concerning you.

8. Is providing data mandatory? Providing your account and billing details is a contractual requirement; if you do not provide them we cannot open or maintain your account.
---

## What good output covers (the expected finding set)

Scope: 12 elements (G1..G12; G13/G14 out of scope for from_subject). total=12.
PRIMARY GAP SETS: deficient_ids = [G3, G8]; absent_ids = [G10].
present_ids = [G1, G2, G4, G5, G6, G7, G9, G11, G12]. counts = {present:9, deficient:2, absent:1, total:12}. coverage_verdict = GAPS_FOUND.
Per-element: G1 PRESENT (Art.13(1)(a); controller name+address+email). G2 PRESENT (Art.13(1)(b); DPO email). G3 DEFICIENT (Art.13(1)(c)) — purposes (a)(b)(c) stated and a paired Art.6(1) legal basis is given for (a) and (c) but NOT for purpose (b) fraud/security; missing_subparts=["legal basis under Art. 6(1) for purpose (b) (fraud detection and security monitoring)"]. G4 PRESENT (Art.13(1)(d)) — conditional element NOT triggered: no legitimate-interests basis is relied upon (stated bases are contract + legal obligation), so no specific interest is required to be named; this deliberately must NOT be double-counted with G3. G5 PRESENT (Art.13(1)(e); recipient categories: hosting provider, payment processor, external auditors). G6 PRESENT (Art.13(1)(f)) — explicit no-transfer statement. G7 PRESENT (Art.13(2)(a); periods+criteria given). G8 DEFICIENT (Art.13(2)(b)) — rights list gives access/rectification/erasure/restriction/portability (5 of 6); missing_subparts=["right to object (Art. 21) is not listed"]. G9 PRESENT (Art.13(2)(c)) — conditional not triggered; notice expressly does not rely on consent. G10 ABSENT (Art.13(2)(d)) — right to lodge a complaint with a supervisory authority is not disclosed anywhere; missing_subparts=["right to lodge a complaint with a supervisory authority not disclosed"]. G11 PRESENT (Art.13(2)(e); §8 states provision is a contractual requirement + consequences). G12 PRESENT (Art.13(2)(f); §7 addresses existence of ADM).
Basis: competency §GDPR items 3,8,10 + Detection-rules traps (b)(purposes-without-basis) and the missing-complaint-right common trap.

## How it was graded

Deterministic: parse candidate JSON; build sets D=set(deficient_ids), A=set(absent_ids). PASS-CORE iff D=={G3,G8} AND A=={G10} (order-independent set equality). Then check present_ids==full 12-ID set minus (D∪A), the three sets pairwise disjoint and exhaustive over G1..G12, counts sum to 12, and coverage_verdict=="GAPS_FOUND" (pure function: non-empty gaps). Sub-part precision (secondary): G8 missing_subparts must name 'object'/'objection' (not merely 'a right'); G3 must point at purpose (b)/fraud. Evidence grounding: each PRESENT/DEFICIENT evidence string must be a verbatim substring of notice_text. Discrimination trap: a candidate that puts G4 in deficient_ids/absent_ids (inventing an LI claim from 'fraud detection') FAILS core set-match — this is intended. Guardrail overlay (binary hard-fail on any fixture): output contains no lawfulness/fairness/compliance opinion, never says 'compliant'/'non-compliant', and ends with the verbatim non-advice disclaimer.

*Eval evidence for this station (headline numbers, residuals, honest history): see
[`../evals/`](../evals/) in this plugin.*
