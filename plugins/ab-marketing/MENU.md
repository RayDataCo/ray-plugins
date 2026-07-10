# ab-marketing — Menu

**Status:** live · 1 station shipped (eval-proven, the first exemplar-graded generative
station in the marketplace) · 5 held-for-refire with real measured evidence and named
defects · **drafting + coverage-review skills; never legal advice**

This is the packaged menu (source of truth, versioned with the plugin). It is the
**station roster** the [expo](skills/expo/) reads to decompose a request, select which
stations to fire, and compose their outputs. Every station ships only with two-arm
execution-eval evidence (see `evals/`); held stations stay held until refired and
re-verified — honest status over roster size.

Two station kinds in this discipline:
- **Generative** — DRAFT marketing work product, graded in eval against rubrics derived
  from real gold exemplars (GAO campaign evaluations, S-1 positioning narratives). The
  quality bar is encoded in the skill; thin inputs get questions, never invented facts.
- **Structural** — check content against enumerated public standards (FTC rules) and
  report per-element PRESENT/ABSENT/DEFICIENT coverage. Structural, not advisory: no
  compliance verdicts, no legal advice — gaps route to counsel.

Brigade surface: `mise` (readiness gate) → `service` (on/off) → `expo` (composes the
stations below).

## Route to a station (live, eval-proven)

| When the situation is… | Route to | Eval headline (sonnet, strict grading) |
|---|---|---|
| Draft a campaign-effectiveness narrative or measurement plan — objectives tied to measurable outcomes, methodology stated, evidence marshaled honestly (incl. null results), limitations named, recommendations traceable to findings | `effectiveness-narrative-draft` | **win +1.00**: base 0/5 → skill 5/5 on rubric criteria derived from real GAO campaign-evaluation gold structure. Base failed every fixture incl. the null-result and activity-metrics-only traps; the skill's findings-evidence-recommendation discipline passed all five |

## Held for refire (real measured evidence, named defects — do not ship, do not improvise)

| station | evidence | why held |
|---|---|---|
| `positioning-narrative-draft` (generative) | **+1.00** (base 0/5 → skill 5/5) — strongest eval of the roster | Critic refire ×4, all named: an uncited near-verbatim exemplar sentence used as a reusable instruction (public-record license violation — the exact failure class the license discipline exists to catch), an over-claimed provenance preamble, build-process notes embedded in the shipped file, and a false self-certification. All text-level; ships after refire + re-verify |
| `marketing-brief-draft` (generative) | **+0.80** (base 0/5 → skill 4/5) | Critic refire ×1: private build-pipeline file paths leaked into a reference file. Trivial fix; ships after refire + re-verify |
| `email-telemarketing-compliance-review` (structural) | **+0.20** (base 0/5 → skill 1/5); critic advance | Eval below the ship bar: near-perfect coverage tables failing strict all-element set-match on single discriminator rows (an unsubscribe-window discriminator; two TSR row statuses). Named misses; refire targets precision on those rows |
| `digital-disclosure-review` (structural) | **+0.20** (base 0/5 → skill 1/5) | Critic refire: the skill's reference invented a "health/safety substantiation" scope not present in the grounding standard — a grounding-infidelity blocker for a public coverage skill. Plus one arguable multimedia-element call. Refire re-grounds scope |
| `advertising-claims-endorsement-review` (structural) | **0.00** (base 0/5 → skill 0/5) | Two compounding causes, both named: the eval arm summarized its report instead of emitting it (output-contract too heavy for in-answer delivery — skill needs a leaner emit-in-full contract) and real trap misses (a substantiation-flag handling rule, a ranking condition); critic also caught private build filenames hardcoded in the output template. Full refire |

## Out of scope

Legal advice or compliance determinations (structural stations report coverage; counsel
decides) · creative-execution/award-caliber campaign concepts (no gold exemplar surface
exists yet — the upstream domain-research brigade's award libraries are subscription-gated;
the expo says so honestly rather than improvising) · company-specific market research
(that is company-research work, not a drafting/review skill).
