# ab-legal — Menu

**Status:** live · 2 stations shipped (eval-proven) · 1 held-for-refire · **structural
review only — never legal advice**

This is the packaged menu (source of truth, versioned with the plugin). It is the
**station roster** the [expo](skills/expo/) reads to decompose a request, select which
stations to fire, and compose their outputs. Every live station shipped with two-arm
execution-eval evidence (see `evals/`).

Every station in this brigade is **structural, not advisory**: it checks a document against
an explicit *enumerated* standard (regulatory elements, standard clause sets, a supplied
playbook) and reports coverage/gaps. It does not opine on fairness, lawfulness, risk, or
strategy. Those are legal judgment — out of scope, route to counsel.

Brigade surface: `mise` (readiness gate) → `service` (on/off) → `expo` (composes the
stations below). A single-station request routes to one; a compound request (e.g. "review
this SaaS agreement and check its privacy notice for GDPR coverage") fires several stations
and the expo synthesizes one answer.

## Route to a station (live, eval-proven)

| When the situation is… | Route to | Eval headline |
|---|---|---|
| Audit a privacy notice/policy for GDPR (Art. 13/14) or CCPA/CPRA disclosure completeness — which required elements are present, missing, or deficient | `regulatory-notice-coverage` | **win +0.60** (sonnet): base 1/5 → skill 4/5. Base misses deficiency-grading (purposes without legal basis, retention without criteria) + the CCPA stale-date defect; skill applies the enumerated element rules. Known weakness: one hard Art. 14 fixture mis-graded an ABSENT element as DEFICIENT (severity, not coverage) — documented |
| Check a contract against the standard expected clause set for its type (NDA / MSA / SaaS) — which standard clauses are present, absent, or deficient | `contract-clause-coverage` | **win +1.00** (sonnet): base 0/5 → skill 5/5. The base model missed every fixture (heading-vs-substance traps, missing limitation-of-liability, deficient termination/IP); the skill's expected-clause-set discipline caught all five |

## Held for refire (real measured lift, one named defect — do not ship yet)

- **redline-against-playbook** — review a contract against a *supplied* redline playbook,
  classify each issue COMPLIANT / ACCEPTABLE / FLAG, and redline the FLAGs. **Eval was
  strong (+1.00, base 0/5 → skill 5/5)** but the independent critic caught a latent defect
  the fixtures didn't happen to exercise: a worked example in its reference file
  ("18-month cap → ACCEPTABLE") contradicts the skill's own direction-of-benefit rule — a
  higher liability cap is *more* favorable to the customer, so an 18-month cap against a
  12-month standard is COMPLIANT, not ACCEPTABLE. That's the exact Trap the skill exists to
  grade, so the reference must be right. Named fix: any cap ≥ standard is COMPLIANT; the
  fallback band must lie *below* standard. Ships once refired + re-verified. This is the
  critic-advises/expo-decides gate working: the eval passed, the critic caught the defect.

## The tasting

A packaged soft opening lives in [tasting/](tasting/): retired eval fixtures (input +
expected coverage/rubric + grading), run by the expo in YOUR environment after mise —
the same machinery and the same bar the eval evidence reports. See tasting/README.md
for which stations have plates.

## Out of scope (route to counsel)

Legal *judgment* — is this term fair, should I sign, what's my risk, is this processing
lawful, what should I negotiate. This brigade checks structure against a standard; it does
not give legal advice. The expo routes these out rather than letting a station drift.
