# Domain-research vertical — execution-eval evidence (2026-07-10)

Four sourcing stations were built by the skill factory (spec → tests → author → critic)
and measured by a two-arm execution-eval: base model alone vs base model + the skill, on
oracle fixtures the test station produced, graded by strict per-source set-match against
each fixture's known-answer disposition set. Two rounds ran: round 1 exposed a shared root
cause (the disposition boundary POINTER-ONLY vs EXCLUDE vs INCLUDE-WITH-RESTRICTION was
under-specified), the discipline gained explicit **§4b boundary rules**, and the refire
round re-ran the SAME oracles against the revised skills. The oracles already encoded the
§4b resolutions in round 1 — the skills were fixed to the oracles, never the reverse.
Round 1: 76 agents, 0 errors. Round 2 (refire): 72 agents, 0 errors. All arms sonnet.

**What makes sourcing eval-able:** each fixture is a fully synthetic candidate-source
bundle (4-6 sources with license/terms metadata + snippets; placeholder orgs for anything
non-public; real public institutions named only where the license fact about them — MIT
OCW's CC BY-NC-SA, EDGAR's public-record status — is itself the thing under test). The
oracle is the exact per-source disposition (`INCLUDE / INCLUDE-WITH-RESTRICTION /
POINTER-ONLY / EXCLUDE` + reason class). Fixtures plant traps: freely-viewable-but-
unlicensed content, embedded prompt injections (must yield EXCLUDE `injection-suspect`),
polished content-farm/prep-vendor sources, model-estimated numbers presented as fact,
superseded versions. Grading is all-or-nothing per fixture: ONE mis-dispositioned source
fails the arm.

**The base-model story:** base arms passed 1 of 20 fixtures in round 1 and 0 of 20 in
round 2 (20 = 5 fixtures × 4 stations per round; the "base 0/10" in the
public-filings-exemplars row below pools that one station's 5 round-1 + 5 round-2
fixtures). This discipline is not latent in the base model — which is the brigade's
reason to exist.

## Shipped (eval evidence)

| station | deployment-tier evidence | headline |
|---|---|---|
| standards-regulatory-sourcing | **win +1.00** (r2): base 0/5 → skill 5/5 | Round 1 scored 0/5 on systematic boundary misses (T3 commentary excluded instead of POINTER-ONLY'd, restrictive-CC demoted via an invented rule, reason-class imprecision); the §4b rules fixed all five, including the injection, proposed-rule-as-context, and stale-superseded-precision traps |
| cert-body-sourcing | **win +0.60** (both rounds): base 0/5 → skill 3/5 | Stable lift across rounds. Named residuals: (1) restrictive-CC material from authoritative-but-non-canonical bodies (a state society, an institute absent from the canonical table) still gets demoted to POINTER-ONLY — rule-3 under-application under tier uncertainty; (2) landing blocks must be emitted in full frontmatter, not asserted ("full landing block provided" is not a landing block) |
| academic-ocw-sourcing | **win +0.60** (r2, from +0.20 r1): base 0/5 → skill 3/5 | The CC-licensed-only gate now grades clean on the platform-restriction and stated-license-overrides-platform traps. One r2 miss (f2) sits on a self-contradictory fixture key — see Fixture defects below; under the oracle's own summary line the arm passes (would be +0.80). Named residual: an SA-only stated license was labeled plain INCLUDE with the SA obligation noted parenthetically — the label must be INCLUDE-WITH-RESTRICTION (f4) |
| public-filings-exemplars | **win +0.40 (r2) / +0.60 (r1)** — base 0/10 → skill 5/10 pooled | The weakest evidence on the roster, flagged honestly. Every r2 miss was a single source on a 6-source strict fixture (arm matched ≥5/6 sources on each): an NC restriction on a quasi-official portal treated as disqualifier instead of recorded obligation (pfe-01), a grants.gov NOFO judged off-domain where the competency places FOAs in the proposal-structure exemplar domain (pfe-02), a reputable-T3 vs untiered call (pfe-03). Round-1 critic nits (a 3-7 vs 5-15 count contradiction; GAO/CRS mis-tiered T1) fixed and re-verified clean in r2. Ship rationale: real lift in both rounds over a 0/10 base, r2 critic clean on all six axes, every miss named and in one boundary-judgment family the expo carries as a documented weakness |

## Station 5 addendum — award-case-study-exemplars (built same day, separate run)

Built through the same factory line (19 agents, 0 agent errors) after the first four
shipped, from its own competency doc (award libraries as the external quality oracle for
creative domains; award METADATA is fact, case CONTENT is copyrighted expression;
entrant-reported results tagging). Same two-arm method, same §4b inheritance,
in-answer-only arms.

| station | deployment-tier evidence | headline |
|---|---|---|
| award-case-study-exemplars | **win +0.60**: base 1/5 → skill 4/5 | Critic advance on all six axes (license/access facts verified against the competency doc, incl. the paywalled-T1 rule-5 carve-out and the government-authored public-domain corner). The one miss (f5, hardest license-boundary fixture) failed BOTH arms on the same 3 sources — named residuals: a T1 body's public ABSTRACT is itself the copyrighted-accessible candidate (the arm over-applied the gated-databank POINTER-ONLY carve-out to it), and the recurring plain-INCLUDE vs INCLUDE-WITH-RESTRICTION labeling precision |

Run note: this build surfaced a third eval-integrity failure mode — structured-output
calls carrying angle-bracket placeholders (`<task>-<n>`) can corrupt the tool-call parse
(only the first field survives, validation fails). Fixed with an explicit
curly-brace-placeholder instruction to all authoring agents; the run then completed
clean. Logged alongside the pointer-return and shared-scratchpad modes in the method
notes below.

## Fixture defects (logged, keys NOT silently edited)

- **f2 (academic-ocw, r2):** the oracle's reasoned per-row text requires row 1 = EXCLUDE
  `stale-superseded` (superseded edition of an already-landed offering), but the oracle's
  own summary line says "Expected landed_count: 3 (rows 1, 2, 5)" — self-contradictory,
  and the skill arm's landed set exactly matched the summary line. The grader flagged the
  contradiction and weighted the per-row text (the stricter reading); we report +0.60
  accordingly and log the key defect for the hardener pass with provenance. The per-row
  reading also encodes a real discipline nuance worth adopting: check candidates against
  prior sourcing decisions for edition drift.

## Critic findings across rounds (critic-advises / expo-decides, working as designed)

- r1 public-filings-exemplars: eval +0.60 but critic **refire** on two concrete
  copy-paste contradictions (dual exemplar-count targets; GAO/CRS tier). Fixed in the
  refire; r2 critic advance on all axes.
- r2 standards-regulatory-sourcing: critic flagged ONE factual mismatch — the skill's
  license table dispositions commercial annotated state-code editions as EXCLUDE
  `license-restricted` while the parent competency doc said POINTER-ONLY. Resolution: the
  SKILL was right by §4b rule 5 (non-primary wrapper with an open substitute — the official
  statute text — gets no POINTER-ONLY carve-out); the competency doc line predated §4b and
  was corrected to match. The +1.00 eval and the skill text are unchanged.

## Method notes

- Two-arm ablation: arm A = base model + fixture; arm B = base model + SKILL.md + fixture;
  a third agent grades both against the oracle disposition set, strict per-source.
- Round-2 arms were instructed to answer entirely in-message (no file writes) after round-1
  graders caught cross-fixture contamination from arms writing decision sheets into a
  shared scratch directory — one round-1 miss (a skipped landing block "already landed")
  was traced to an arm seeing another arm's files.
- All fixtures fully synthetic; no real company's non-public information appears anywhere.
  Real public institutions are named only for their public, verifiable license/access
  facts.
- Competency sources, round-by-round fixture sets, and both raw result sets are preserved
  privately (oracle keys stay out of the public repo so future evals stay uncontaminated).
