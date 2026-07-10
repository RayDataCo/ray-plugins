# Tasting — effectiveness-narrative-draft

*A retired eval fixture, deliberately spent for demonstration (see the factory's
EVAL-SPEC): run the `effectiveness-narrative-draft` station on the input below in YOUR environment (mise first),
then compare against the expected coverage and the graded criteria. This fixture never
grades again — it exists to SHOW, not to test.*

## The input

Mode: not specified (infer). Campaign context: Acme Cloud Storage, a B2B SaaS company, ran "Backup Everything," a LinkedIn + email nurture campaign across Q1 2026 (Jan 1 - Mar 31, 2026), targeting IT directors at mid-market companies (500-5,000 employees). Stated objective: "increase free-trial signups among mid-market IT directors by 25% over the Q1 2026 baseline (120 signups/month) within the Jan-Mar 2026 flight window." Budget: $180,000 planned, $178,400 actually spent over 12 weeks.

Results data: Impressions 4.2M, click-through rate 1.8%, engagement rate 3.1%. Free-trial signups averaged 158/month across Jan-Mar 2026 versus a 120/month baseline (Oct-Dec 2025 average) — a 31.7% increase, exceeding the 25% target. Of trials started during the campaign window, 22% converted to a paid plan within 60 days, versus an 18% historical conversion baseline.

Evaluation_context: Assessed internally by Acme's marketing analytics team using Salesforce attribution data (last-touch model) cross-referenced against the Oct-Dec 2025 pre-campaign baseline. No third-party evaluator was used.

Known_limitations supplied by user: no control group or geographic/segment holdout was used; the attribution model is last-touch, so some signups may be influenced by other concurrent brand activity; a company-wide product-launch PR push ran concurrently in February 2026, overlapping the campaign window; channel attribution data is drawn from Salesforce and is self-reported by sales reps in some cases.

audience_and_use: internal leadership, deciding whether to renew the campaign budget for Q2 2026.

## What good output covers (the rubric this station is graded on)

RUBRIC — derived from four grounding exemplars (GAO-25-106719 military recruiting digital marketing; GAO-25-107845 ONDCP media-campaign expert forum; effectiveness-narrative-1 restatement of GAO-25-106719; effectiveness-narrative-2 restatement of GAO-06-818 anti-drug media campaign). Each criterion is binary (met / not-met) and checkable against the candidate skill's literal output text.

1. SEVEN-SECTION FIXED ARCHITECTURE. Output contains, in this order, Title+framing, Scope/Objectives, Methodology, Findings, Limitations, Recommendations, and (if requested) a self-check appendix — with no section dropped, merged, or reordered. Demonstrated by both GAO reports' consistent "Why GAO Did This Study / What GAO Found / What GAO Recommends" skeleton and effectiveness-narrative-1's restated Challenge/Audience-insight/Strategic-idea/Execution/Results arc — both exemplars never skip straight from framing to results without a stated method.

2. OBJECTIVE MEASURABILITY TEST APPLIED HONESTLY. Every stated objective is tested for whether it has a metric, direction, audience, and threshold/timeframe; objectives that pass are stated as measurable (not silently reworded to look measurable when they aren't), and objectives that fail are explicitly flagged as a structural gap. Demonstrated by GAO-25-106719: "some strategic goals... such as building a connection to the STEM field — do not have specific targets or performance measures... it will be difficult for these services to assess their progress."

3. EVALUATOR IDENTITY AND INDEPENDENCE NAMED. Methodology section states who evaluated the campaign and whether that evaluator is independent of the program (or explicitly flags this as unstated/absent). Demonstrated by GAO-25-107845 point 5: independence "does not require complete organizational separation... but does require reporting outside the program's own funding chain," and by effectiveness-narrative-2: Westat (independent contractor) evaluated, reviewed by GAO.

4. EVALUATION TIMING NAMED (PROCESS VS. SUMMATIVE). Methodology states whether the assessment is a process evaluation (ongoing/mid-course), a summative evaluation (post-campaign), or — in prospective mode — proposes which of these the future measurement design will use. Demonstrated by GAO-25-107845 point 6: "process evaluations (ongoing, allowing mid-course correction) and summative evaluations (post-campaign assessment)."

5. ACTIVITY-VS-OUTCOME TAGGING WITH EXPLICIT GAP CALLOUT. Every finding is tagged OUTCOME-SUPPORTED / ACTIVITY-ONLY / NEGATIVE-NULL / GAP, and if the stated objective demands an outcome but supplied evidence is activity-only, the document says so in plain language rather than letting activity metrics stand in for the outcome claim. Demonstrated by GAO-25-106719's core finding that "social media engagement did not consistently correlate with successful recruiter contact" — activity (engagement) explicitly shown not to prove outcome (recruitment).

6. NEGATIVE/NULL RESULTS SURVIVE UNDIMINISHED. Where input evidence shows no effect or a contrary effect, the finding preserves that substance without softening, hedging, or burying it under adjacent positive metrics. Demonstrated by effectiveness-narrative-2: Westat's evaluation "yielded no evidence of a positive outcome in relation to teen drug use" — stated flatly across both the full campaign period and the narrowed 2002-2004 phase, not qualified away.

7. LIMITATIONS ARE SPECIFIC AND SECTION-TRACEABLE. Each limitation names a concrete constraint tied to a specific piece of the draft (a named data gap, a named confound, a named evaluator-independence issue) rather than generic boilerplate ("results may vary"). Demonstrated by GAO-25-106719's branch-specific finding that the Air Force "manages risk on a case-by-case basis" (vs. the other services' standardized process) — a named, specific gap, not a vague caveat.

8. RECOMMENDATIONS CITE FINDINGS AND SCALE TO EVIDENCE STRENGTH. Every recommendation names the specific finding number(s) it derives from, and its confidence/strength does not exceed what that finding supports (an ACTIVITY-ONLY or GAP-tagged finding cannot support a strong "scale this up" recommendation). Demonstrated by effectiveness-narrative-2: GAO's recommendation was that Congress "consider limiting further appropriations pending credible evidence of effectiveness" — a recommendation scaled exactly to a null finding, not an overreach.

9. NO FABRICATED SPECIFICS; GAPS ARE FLAGGED NOT INVENTED. No statistic, dollar figure, benchmark name, or specific claim appears that was not present in the supplied input; anything the architecture needs but wasn't supplied is rendered as an explicit gap marker. Demonstrated by effectiveness-narrative-1's own annotation practice: "[tag: none-present as a single quantified topline]" rather than manufacturing a plausible number GAO didn't have.

10. NAMED EXTERNAL BENCHMARK OR ITS ABSENCE IS FLAGGED. Methodology states what standard/benchmark the evaluation was measured against, or explicitly notes none was supplied (as a limitation), rather than silently omitting the question. Demonstrated by GAO-25-106719 ("assessed military services' efforts against commercial best practices for assessing advertising effectiveness") and effectiveness-narrative-2 (Westat assessed "against generally accepted social-science research standards").

11. ANALYTICAL/EVIDENTIARY REGISTER, NOT PROMOTIONAL. Voice reads as third-person/organizational and evidentiary ("GAO found," "the evaluation showed") throughout, with no self-congratulatory or awards-entry framing. Demonstrated by both source reports' consistent "GAO found / GAO recommends" construction, explicitly contrasted in the exemplar files against "an entrant-submitted campaign case (which grades its own creative and its own results)."

12. PLACEHOLDER HYGIENE — CURLY BRACE ONLY. Every unresolved gap or unspecified value uses curly-brace notation (e.g., {input needed: outcome metric for objective 2}); zero angle-bracket placeholders appear anywhere in the output. Mechanical formatting check drawn from the skill's own output contract and consistent with the exemplar files' own curly-brace convention (e.g. {cellar_root} in their Lands-at paths).

GRADING: for each fixture, an arm's output is scored criterion-by-criterion (met/not-met, strict, evidence-quoting — the grader must quote the exact output text supporting each verdict). An arm is judged CORRECT on a fixture if at least 80% of the 12 criteria are met AND no fixture-specific fact in the oracle is violated (no contradicted number, no laundered anecdote into a hard finding, no invented evaluator/benchmark, no suppressed negative result). Falling below 80% or violating any fixture-specific fact fails the fixture regardless of overall polish.

## How it was graded

Score all 12 rubric criteria against the draft; correct if >=80% (10 of 12) met and none of the fixture-specific facts above are contradicted or omitted from a place the architecture requires them (evaluator independence in Methodology/Limitations, the Feb PR confound in Limitations, the exact baseline/lift numbers in Findings). Special adversarial check: verify criterion 2 is NOT incorrectly triggered — the objective here IS measurable and a good output should say so, not manufacture a false gap flag.

*Eval evidence for this station (headline numbers, residuals, honest history): see
[`../evals/`](../evals/) in this plugin.*
