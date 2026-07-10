# ab-marketing — Menu

**Status:** live · 3 generative stations shipped (the marketplace's first exemplar-graded
generative skills, all eval-proven across two rounds) · 3 structural stations
held-for-refire with real measured evidence and named defects · **drafting +
coverage-review skills; never legal advice**

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
| Draft a brand-positioning narrative of investor/board grade — category definition, target customer, differentiated value, quantified proof points vs named baselines, moat/durability | `positioning-narrative-draft` | **win +0.80 (r2) / +1.00 (r1)**: base 0/10 → skill 9/10 across two rounds on rubrics derived from real S-1 positioning gold. Round-2 critic verified all four round-1 defects fixed (incl. the caught license violation). Residual: the hardest thin-input fixture graded 8/12 criteria in r2 — refusal-to-fabricate discipline held but coverage dipped |
| Draft a complete marketing brief from a business scenario — objective, STP, single-minded proposition, channel strategy, success metrics, mandatories | `marketing-brief-draft` | **win +0.80 both rounds**: base 0/10 → skill 8/10. The two misses across rounds were one content miss (regulated-industry scenario, r1) and one delivery artifact (the arm described its brief instead of emitting it, r2) — the emit-in-full residual is documented |

## Held for refire (real measured evidence, named defects — do not ship, do not improvise)

All three structural stations improved in round 2 and show a consistent NEAR-MISS profile:
correct schemas, correct trigger determinations, high per-element accuracy — failing the
strict all-element set-match bar on 1-2 elements per fixture. Round 3 will refire against
the newly-named defects below (and is the right place to decide whether per-element
accuracy belongs in the reported evidence alongside the strict fixture bar).

| station | evidence (r1 → r2) | why held |
|---|---|---|
| `email-telemarketing-compliance-review` | +0.20 → **+0.40** (skill 2/5) | Closest to the bar. Newly-named defect: the verdict-ordering guidance contradicts itself (prose says rule out stricter categories first; the numbered list puts NOT APPLICABLE first) — reproduced in SKILL.md and both references. Plus one emit-in-full miss and two single-row precision misses |
| `digital-disclosure-review` | +0.20 → +0.20 (skill 1/5) | 7 of 8 named round-1 defects verified fixed (incl. the invented health/safety scope — removed); one defect item survived (critic-verified), plus recurring single-element severity calls (DEFICIENT vs ABSENT on unavoidability-class elements) |
| `advertising-claims-endorsement-review` | 0.00 → 0.00 (skill 0/5) | Qualitatively transformed but not yet passing: round-2 answers use the correct 8-element schema, exact trigger determinations, and mostly-correct statuses (5/6 elements on several fixtures) — every fixture fails on 1-2 element statuses or severity calls under strict set-match. All round-1 defects (heavy output contract, template filenames, trap rules) verified fixed by the critic (advance); held purely on eval evidence |

## Out of scope

Legal advice or compliance determinations (structural stations report coverage; counsel
decides) · creative-execution/award-caliber campaign concepts (no gold exemplar surface
exists yet — the upstream domain-research brigade's award libraries are subscription-gated;
the expo says so honestly rather than improvising) · company-specific market research
(that is company-research work, not a drafting/review skill).
