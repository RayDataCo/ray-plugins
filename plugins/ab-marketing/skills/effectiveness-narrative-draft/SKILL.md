---
name: effectiveness-narrative-draft
description: Draft an effectiveness narrative or measurement plan for a marketing/communications campaign, structured on the GAO findings-evidence-recommendation model. Use when asked to write an effectiveness narrative, campaign evaluation report, campaign measurement plan, board/funder/renewal assessment of campaign results, or to sanity-check whether campaign evidence actually supports its stated goals. Handles both retrospective mode (evaluating a completed campaign's results) and prospective mode (designing what should be measured for a planned campaign). Tags every finding as outcome-supported, activity-only, negative/null, or gap; flags non-measurable objectives instead of silently rewriting them; never fabricates a result, statistic, or claim not present in the supplied input — surfaces missing facts as explicit input-needed flags instead.
---

# Effectiveness Narrative Draft

## What this skill produces

A single Markdown document that answers one question honestly: **does the evidence
we actually have support the claim that this campaign worked (or, for a planned
campaign, what evidence would we need to be able to say that)?**

The architecture is borrowed from GAO evaluation reports (public-domain federal
work, GAO-25-106719 and GAO-25-107845, and the retrospective evaluation model in
GAO-06-818): state the pressure that prompted the assessment, state the objective
in measurable terms, describe method, list findings as claim-plus-evidence pairs
with an honest tag on each, name real limitations, and tie every recommendation
back to a specific finding. GAO reports grade the evaluee's evidence, not the
evaluee's ambition — this skill does the same to the input it's given.

## Quality bar (what the exemplars grade, encoded as the skill's own bar)

These are the qualities a finished narrative must have. They come directly from
reading the grounding reports, not from generic report-writing advice:

1. **Un-targeted goals cannot be assessed.** GAO's military-recruiting review found
   that goals like "build a connection to the STEM field" had no specific target or
   performance measure attached, and flagged this as a structural finding in its
   own right — not something to paper over by writing a more measurable-sounding
   goal on the evaluee's behalf. This skill does the same: if an objective isn't
   measurable as given, that is Finding-worthy, not an editing problem.
2. **Activity is not outcome.** Engagement, reach, spend, and impressions describe
   what the campaign *did*. They are not evidence of what the campaign *achieved*
   unless the input explicitly ties them to the stated outcome. Conflating the two
   is the single most common failure mode in campaign self-reporting, and the
   number one thing this skill exists to prevent.
3. **Independent evaluation outranks self-report.** The ONDCP expert panel
   (GAO-25-107845) named evaluator independence as a distinct evaluation
   requirement, separate from the evaluation itself. A campaign's own marketing
   team judging its own results is a limitation worth naming, not a footnote.
4. **Process and summative timing are different questions.** Did-it-work-so-far
   (process/mid-course) and did-it-work-overall (summative/post-campaign) are not
   interchangeable, and a narrative that blurs them overstates its own certainty.
5. **Null and negative results get reported, not buried.** GAO-06-818 is the
   canonical case: a $1.2B national campaign whose own commissioned evaluation
   found no evidence of the intended behavioral effect, and GAO reported that
   flatly. A narrative that omits an unfavorable result present in its own input
   is not honest work — this skill treats omission of supplied negative evidence
   as a hard failure, not a style choice.
6. **Recommendations are scoped to the evidence, not the ambition.** GAO's
   recommendations map one-to-one back to specific findings. A recommendation with
   no finding behind it is an opinion wearing a report's clothing.

Read `references/gao-narrative-architecture.md` for the fuller structural
breakdown (the six-point ONDCP development/evaluation model, the four finding
tags with worked definitions, and how the architecture maps section-by-section).
Read `references/worked-example-tagged-findings.md` for a complete short example
of a filled-in narrative, including how a GAP-tagged finding and a
NEGATIVE/NULL-tagged finding actually read in practice.

## Inputs

Gather (ask the user directly if not already supplied — do not invent):

- `campaign_name` — required. If truly unknown, use the placeholder
  `{campaign name}`.
- `pressure_or_question` — what made this assessment necessary right now
  (recruiting shortfall, budget renewal, board question, funder report, etc.). If
  none was given, do not invent one — say so plainly in Section 1.
- `campaign_context` — audience, stated objective(s), channels, activities,
  timeframe, budget if known.
- `results_data` — whatever evidence exists: metrics, survey results, third-party
  evaluation findings, vendor reports, anecdotal signals. Absence of this input
  (or partial absence against a stated objective) is expected and handled by the
  GAP tag, not by stalling the draft.
- `known_limitations` — anything the user already knows constrains the read
  (small sample, no control group, self-reported numbers, short timeframe, etc.).
  Merge with limitations the skill infers from its own gap analysis.
- `mode` — `retrospective` (default when `results_data` is present) or
  `prospective` (default when the campaign hasn't run yet, or the user asks for a
  "measurement plan"). If ambiguous, infer from context and state the inferred
  mode at the top of the draft so the user can correct it.
- `rubric_appendix` — boolean. Only include Section 7 if explicitly requested.

## Procedure

### 1. Determine mode and confirm the framing pressure

Read `campaign_context` and `results_data`. If `results_data` is empty or
describes only planned/future activity, default to prospective mode. State which
mode you're running in in your own working notes (not necessarily in the output,
though a one-line mode note at the top of Section 1 is fine and often useful).

Do not invent a "why now" pressure. If `pressure_or_question` wasn't supplied,
Section 1 says so directly: something like "No specific triggering question or
pressure was supplied for this assessment; this narrative was requested as a
general effectiveness review of {campaign name}." That sentence is itself honest
output, not a gap to fill with a guess.

### 2. Draft Section 1 — Title + one-line framing

Campaign/program name, and a one-line statement of what the document is
(effectiveness narrative for a completed campaign, or measurement plan for a
planned one). Follow with 1-3 sentences in the GAO "Why GAO Did This Study"
register: state the pressure plainly, don't sell it.

### 3. Draft Section 2 — Scope and objective(s)

For each stated objective in `campaign_context`:

- If it is already stated as a measurable outcome (a metric, a direction, a
  magnitude, and ideally a timeframe/audience), restate it cleanly.
- If it is NOT measurable as given (e.g., "raise awareness," "build brand
  connection," "engage the community"), do **not** silently convert it into a
  measurable-sounding restatement. Flag it explicitly as a structural gap in the
  source material — name the specific missing element (no target, no metric, no
  audience segment, no timeframe) — echoing the military-recruiting finding.
  Example framing: "Objective as supplied ('build a connection to {audience}')
  has no attached target, metric, or timeframe and cannot be assessed as stated.
  {input needed: what specific, measurable change was this objective meant to
  produce?}"

List every objective this narrative will actually answer against. If an
objective is unmeasurable and no clarification is available, it still gets
listed — it just gets a GAP-class flag here and carries through as a GAP finding
in Section 4, not a silent drop.

### 4. Draft Section 3 — Methodology

Retrospective mode: describe how the assessment was actually conducted, using
only what's in the input. Cover, wherever known: data sources used, who
evaluated (internal team vs. third party), evaluator independence (does the
evaluator report outside the campaign's own funding/management chain?),
comparison standard or benchmark (prior period, control group, industry
benchmark, stated target), and evaluation timing (process evaluation during the
campaign vs. summative evaluation after it, per the ONDCP six-point structure in
the reference file). Where the input is silent on one of these, say so as a gap
rather than assuming a rigorous method that wasn't described.

Prospective mode: this section becomes the **proposed measurement design**
instead of a description of a completed method — same categories (data sources
to be collected, who will evaluate and their independence, the benchmark/target
against which results will be judged, and the process-vs-summative timing plan),
but phrased as a plan, not a past-tense description.

### 5. Draft Section 4 — Findings

Retrospective mode. For each objective from Section 2, and for any other
evidence in `results_data` that materially bears on the assessment (including
evidence the user didn't explicitly connect to an objective — connect it
yourself, or flag it as unlinked if you can't), write one or more numbered
findings: **Finding N: [claim].** Followed immediately by the evidence supporting
it, drawn only from the supplied input.

Tag every finding with exactly one of:

- **OUTCOME-SUPPORTED** — the evidence ties directly to the stated measurable
  objective (not just an adjacent activity metric).
- **ACTIVITY-ONLY** — the evidence shows marketing activity or output (reach,
  spend, impressions, engagement, content volume) but does not show the outcome
  itself. This is the activity-vs-outcome gap named in the quality bar above —
  tag generously here; this is where self-reported campaign summaries most often
  overclaim.
- **NEGATIVE/NULL** — the evidence shows no effect, or a contrary effect. Must be
  included if present anywhere in the input. Never omit a negative or null result
  to make the narrative read better — that is the single hardest rule this skill
  enforces.
- **GAP** — an objective exists (from Section 2) but no evidence was supplied
  against it. Render this as an explicit, specific input-needed flag — name
  exactly what's missing ("no post-campaign survey data was supplied for the
  stated awareness-lift objective") — never fabricate a plausible-sounding result
  to fill the hole.

Prospective mode: findings become numbered **Measurement Requirements** — for
each objective from Section 2, describe what evidence will need to exist for
that objective to be assessable, using the same four-tag logic reframed
forward-looking (e.g., "Measurement Requirement 2 [would resolve as
OUTCOME-SUPPORTED only if]: a pre/post survey of {audience} measuring {specific
metric}, run independently of the campaign team, timed as a summative evaluation
after {date}.").

### 6. Draft Section 5 — Limitations

Never write filler ("results may vary," "further research is needed"). Every
limitation must be specific and traceable to a section above: name the actual
constraint (sample size, timeframe, absence of a control group, self-reported
data, evaluator not independent of the campaign team, confounding factor
identified in the input, etc.) and say which finding(s) or objective(s) it
bears on. Merge `known_limitations` from input with limitations you can infer
directly from gaps already surfaced in Sections 2-4 — don't introduce a
limitation that isn't grounded in something already established in the draft.

### 7. Draft Section 6 — Recommendations

Numbered recommendations. Every recommendation must open with an explicit
cross-reference to the finding(s) it derives from: "Recommendation N (from
Finding X [and Finding Y]): ...". No recommendation may appear without at least
one finding citation — if you find yourself wanting to recommend something with
no finding behind it, that's a sign that either a finding is missing from
Section 4 or the recommendation doesn't belong in this document.

Scope each recommendation to what the cited evidence actually supports. A single
ACTIVITY-ONLY finding does not license a recommendation claiming outcome
certainty; a GAP finding licenses a recommendation to go collect that specific
evidence, not a recommendation to change strategy based on evidence that doesn't
exist yet.

### 8. Section 7 — Self-check appendix (only if `rubric_appendix` requested)

Build a checklist from the ONDCP six-point structure (audience understanding;
content/messengers/message testing; defined outcomes; independent evaluators;
measurement timing — see the reference file for the full six items) plus the
activity-vs-outcome discipline from Section 4's tagging. Score the draft's own
content — not the campaign in the abstract — against each item as **met /
partially met / not met / not assessable**, with a one-line reason tied to a
specific section/finding number above. This appendix grades the document you
just wrote, using only what's in it.

### 9. Final QA pass before returning the draft

- Scan for any angle-bracket placeholder (`<...>`) and convert to curly braces
  (`{...}`) — angle brackets are never acceptable output.
- Confirm every finding/claim/statistic in the document traces back to
  `campaign_context` or `results_data`, with the sole exception of explicitly
  curly-brace-flagged gap placeholders.
- Confirm no negative/null result present in the input was dropped or softened.
- Confirm every recommendation cites at least one finding number.
- Confirm section headers may have been renamed to fit the campaign's language,
  but the seven-part order and architecture is intact and nothing was collapsed
  or dropped.
- Confirm tone: analytical, third-person or organizational voice, GAO register —
  not promotional, not self-congratulatory, not award-entry voice. Re-draft any
  sentence that reads like marketing copy about the marketing.

## Handling thin input honestly

If `campaign_context` and `results_data` together are too thin to produce more
than a Scope section and a wall of GAP findings, that is a valid and honest
output — do not pad it with invented plausible-sounding detail to make the
document look more complete than the input supports. Where it's more useful to
pause and ask the user for specific missing facts (a metric they clearly have on
hand but didn't paste in) rather than draft around it, ask — a few targeted
questions beat a document full of gap placeholders the user would immediately
have to fill in anyway. Use judgment: draft-with-flags is usually better than
blocking, but a one-line "before I draft this, what does {objective} actually
measure?" is worth asking when the answer would reshape the whole document.

## Output formatting rules (non-negotiable)

- No angle-bracket placeholders anywhere in the output. All placeholders use
  curly braces: `{campaign name}`, `{date}`, `{input needed: outcome metric for
  objective 2}`.
- Every GAP finding and every limitation must be specific, never generic.
- No finding, claim, or statistic may appear that wasn't in the supplied
  `campaign_context` or `results_data`, except explicitly flagged gap
  placeholders.
- Tone is analytical and evidentiary, third-person or organizational voice,
  consistent with the GAO register described above.
- Headers may be renamed to match the user's campaign language; the underlying
  seven-part architecture and its ordering must not be dropped or reordered.
