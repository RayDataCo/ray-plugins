# Marketing vertical — execution-eval evidence (2026-07-10)

Six marketing skills were built by the skill factory (spec → tests → author → critic) in
one run (114 agents, 0 errors) and measured by a two-arm execution-eval — base model alone
vs base model + the skill — with **two grading modes**, which is what makes this vertical
notable:

- **Structural mode** (3 skills): synthetic content fixtures with known per-element
  coverage oracles (PRESENT/ABSENT/DEFICIENT per FTC requirement), graded by strict
  all-element set-match — the same machinery that shipped the legal vertical.
- **Exemplar-rubric mode** (3 skills) — **the first exemplar-graded generative eval in
  this marketplace**: the test station derived 8-12 binary rubric criteria from real gold
  exemplars (GAO campaign evaluations' findings-evidence-recommendation architecture; S-1
  positioning narratives' syllogism/proof-point structure), then produced synthetic task
  fixtures; an arm passes a fixture only by meeting ≥80% of criteria with no
  fixture-fact violations, graded strictly with quoted evidence.

Every skill's grounding came from a knowledge cellar filled the same morning by a
domain-research sourcing brigade (public, provenance-stamped sources: FTC rules,
AMA competency structure, CC BY courseware, GAO reports, S-1 excerpts) — the full
fill → exemplars → rubric → eval chain ran end-to-end in one day.

**The base-model story:** base sonnet passed 0 of 30 fixtures across all six skills.
Marketing drafting discipline (refusing to fabricate on thin inputs, tying claims to
evidence, naming limitations) and strict FTC element-coverage review are not latent in
the base model.

## Shipped (eval evidence)

| station | mode | evidence | headline |
|---|---|---|---|
| effectiveness-narrative-draft | generative | **win +1.00**: base 0/5 → skill 5/5, critic advance on all axes | Rubric derived from GAO campaign-evaluation gold. Base failed every fixture including the null-result trap (spinning a null finding as success) and the activity-metrics-only trap (reporting impressions as outcomes); the skill's findings-evidence-recommendation discipline passed all five, including the deliberately-thin and mid-flight-ambiguous scenarios |

## Held for refire (real measured evidence, named defects)

| station | mode | evidence | named defects |
|---|---|---|---|
| positioning-narrative-draft | generative | **+1.00** (base 0/5 → skill 5/5) — the roster's strongest eval | Critic refire ×4: (1) an uncited near-verbatim exemplar sentence ("we believe we stand at the intersection of X and Y") encoded as a reusable instruction — a public-record license violation (author retains copyright; excerpt-and-cite only); (2) quality-bar preamble over-claims that ALL gates derive from the exemplars; (3) a "Notes for the author station" build-narrative section embedded in the shipped SKILL.md; (4) a false self-certification that the pack contains no verbatim exemplar text. All text-level; ships after refire + re-verify |
| marketing-brief-draft | generative | **+0.80** (base 0/5 → skill 4/5) | Critic refire ×1: four private build-pipeline absolute paths leaked into references/stp-brief-method.md. Trivial fix; the one eval miss (a medtech scenario) is a named residual for the refire |
| email-telemarketing-compliance-review | structural | **+0.20** (base 0/5 → skill 1/5); critic advance | Held on eval evidence below the ship bar, not on critic findings: coverage tables graded near-perfect but failed strict all-element set-match on single discriminator rows (the unsubscribe-window discriminator on one fixture; two TSR row statuses — 310.3(a) marked N/A where the oracle required DEFICIENT/insufficient-information — on another). Precision refire on named rows |
| digital-disclosure-review | structural | **+0.20** (base 0/5 → skill 1/5) | Critic refire: the skill's reference asserts a "health/safety substantiation" scope that the grounding standard does not contain — invented scope is a grounding-infidelity blocker for a public coverage skill. One eval miss is an arguable multimedia-element call (skill said DEFICIENT, oracle N/A for a static post) that the re-grounded scope should resolve |
| advertising-claims-endorsement-review | structural | **0.00** (base 0/5 → skill 0/5) | Two compounding causes: (1) the skill arm SUMMARIZED its six-section report and asserted the full report was "in the answer text above" — it wasn't; the output contract is too heavy for reliable in-answer delivery and the graded artifact was a meta-summary (the pointer-not-content failure mode reappearing inside an answer). Refire slims the output contract to emit-in-full. (2) Real trap misses on the fixtures that were graded on substance (a substantiation-flag handling rule; a ranking condition). Critic separately caught three private build filenames hardcoded into the report template header. Full refire |

## Method notes

- Two-arm ablation, all arms sonnet, arms instructed in-answer-only (no file reads/writes).
- Grading strict in both modes; graders quote evidence per call. An arm with a
  90%-correct coverage table still fails structural set-match — by design; a shipped
  coverage skill's value is exactness.
- All fixtures fully synthetic (Acme/Contoso/Globex/Initech/Umbrella/Vandelay). Real
  institutions appear only as the public standards/exemplar sources themselves (FTC,
  GAO, the S-1 issuers) with verifiable public facts.
- Grounding provenance, per-skill fixture sets, and the full raw result are preserved
  privately (oracle keys stay out of the public repo so future evals stay uncontaminated).
- License discipline enforced at build time: the brief/positioning skills draw structure
  from restated AMA facts + CC BY Saylor material; CC BY-NC-SA sources were deliberately
  excluded from grounding so no shipped skill carries an NC/SA obligation. The one
  violation that slipped through (the positioning exemplar sentence) was caught by the
  critic and is why that station is held.

## Round 2 — refire (same day, 90 agents, 0 errors)

All five held skills were refired against their named defects (revise → independent
re-critic → full re-eval on the SAME oracles; skills fixed to oracles, never the reverse).

**Promoted to live (ship in 0.2.0):**

| station | r1 → r2 | round-2 critic |
|---|---|---|
| positioning-narrative-draft | +1.00 → **+0.80** (9/10 pooled) | **advance** — all four round-1 defects verified fixed: the near-verbatim exemplar sentence replaced with original pattern description, provenance note now honestly names the two editorially-invented gates, build-narrative section removed, false self-certification gone. The r2 miss: the hardest thin-input fixture scored 8/12 rubric criteria (refusal-to-fabricate held; coverage dipped) |
| marketing-brief-draft | +0.80 → **+0.80** (8/10 pooled) | **advance** — private paths removed, public citations only. The r2 miss was a delivery artifact (the arm described its brief as "delivered in full above" without including it — the emit-in-full residual, documented) |

**Still held (structural trio — near-miss profile):**

- email-telemarketing-compliance-review +0.20 → **+0.40**; critic caught a NEW defect: the
  verdict-ordering guidance contradicts itself between prose and numbered list (in the
  skill and both references).
- digital-disclosure-review +0.20 → +0.20; 7 of 8 named defects verified fixed (the
  invented health/safety scope is gone); one item survived; recurring DEFICIENT-vs-ABSENT
  severity calls.
- advertising-claims-endorsement-review 0.00 → 0.00; all round-1 defects verified fixed
  (critic advance) — round-2 answers show correct schemas, exact triggers, and 5/6-element
  accuracy on several fixtures, but strict all-element set-match fails every fixture on
  1-2 statuses. Held purely on eval evidence. Round 3 should also decide whether
  per-element accuracy joins the reported evidence beside the strict fixture bar.

Method unchanged: sonnet arms, in-answer-only, strict grading, oracle keys private.
