# Legal vertical — execution-eval evidence (2026-07-09)

Three structural legal skills were built by the skill-agent-brigade (spec → tests → author
→ critic) and measured by a two-arm execution-eval: base model alone vs base model + the
skill, on the oracle fixtures the test station produced, graded by set-match against each
fixture's known-answer oracle. The competency for each skill was authored from cited
authority (GDPR Art. 13/14 text, CCPA/CPRA Cal. Civ. Code §1798.100 et seq., standard
commercial-contract clause taxonomies) so the oracles are defensible, not invented. All
fixtures are fully synthetic (placeholder parties: Acme, Contoso, Globex, Initech).
57 build+eval agents, 0 errors.

**Scope discipline:** every skill is *structural* — it checks a document against an
explicit enumerated standard and reports coverage/gaps. None gives legal advice, opines on
fairness or lawfulness, or makes a compliance determination. This is what makes them
eval-able: "does the notice state the legal basis for each purpose" is a checkable fact,
not a legal opinion. The judgment side of legal (is this fair, should I sign, what's the
risk) is deliberately out of scope — it isn't objectively gradeable and would be advice.

## Shipped (eval evidence)

| skill | deployment-tier evidence | headline |
|---|---|---|
| contract-clause-coverage | **win +1.00** (sonnet): base 0/5 → skill 5/5 | The base model missed every fixture — heading-vs-substance traps (Term folded under "Term and Termination"), a missing limitation-of-liability clause, a deficient termination clause with no survival, an IP clause silent on background IP. The skill's expected-clause-set discipline (by contract type) caught all five. |
| regulatory-notice-coverage | **win +0.60** (sonnet): base 1/5 → skill 4/5 | Base under-grades deficiencies (purposes stated with no legal basis — GDPR's most-missed element; retention as "as long as necessary" with no criteria; a CCPA "last updated" date >12 months). The skill applies the enumerated Art. 13/14 and §1798.100 element rules. **One named weakness:** on a hard Art. 14 broker fixture the skill mis-graded a never-disclosed element (categories of personal data) as DEFICIENT rather than ABSENT — a severity mis-grade, not a coverage miss; net +0.60 still advances. Worth a hardening pass. |

## Held for refire (measured lift, one named defect)

- **redline-against-playbook** — eval **+1.00** (base 0/5 → skill 5/5), but the independent
  critic returned **refire** on a real defect the fixtures didn't exercise: a worked example
  in `references/classification-standard.md` ("18-month cap … → ACCEPTABLE") contradicts the
  skill's own direction-of-benefit rule (Trap 2). A higher liability cap is more favorable
  to a customer, so an 18-month cap against a 12-month standard is **COMPLIANT**, not
  ACCEPTABLE — the adjacent "24mo → COMPLIANT" example is right, this one is wrong, and it
  mis-models the exact trap the skill grades. **Named fix:** any cap ≥ standard is COMPLIANT;
  the fallback band must lie *below* standard (a "24mo or greater" fallback is degenerate).
  Ships once refired + re-verified. This is the critic-advises/expo-decides gate working as
  designed: strong eval, and the critic still caught a latent quality defect the fixtures
  missed — exactly why both gates exist.

## Method notes

- Two-arm ablation: arm A = the base model given the fixture with no skill; arm B = the base
  model given the skill's SKILL.md; each answer graded by a third agent as a strict
  set-match against the fixture's known-answer oracle (did the answer identify exactly the
  oracle's set — no more, no fewer).
- The test station planted deliberate traps: commonly-missed elements, clauses under
  unexpected headings, and direction-of-benefit tricks (a term that reads worse but is
  actually more favorable). Base-model failures cluster on exactly these.
