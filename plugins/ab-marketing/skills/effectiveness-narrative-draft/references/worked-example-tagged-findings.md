# Worked Example — Findings Section (illustrative, retrospective mode)

This is a short, complete illustration of what a properly tagged Findings
section looks like in practice, using a fictional B2B campaign. It is not a
template to copy verbatim — it exists to show the tagging discipline and the
recommendation cross-referencing pattern in finished form.

---

**Campaign:** Northwind Analytics Q1 Webinar Series

**Stated objectives (from Section 2 of the fictional draft):**
- Objective A (measurable as given): increase qualified demo requests from
  mid-market data teams by 20% quarter-over-quarter following the webinar
  series.
- Objective B (measurable as given): achieve an average post-webinar
  attendee satisfaction score of 4.0/5.0 or higher.
- Objective C (NOT measurable as given): "build Northwind's thought leadership
  position in the data-quality space." Flagged in Section 2 as a structural
  gap — no target, no metric, no timeframe supplied. Carried into Findings as a
  GAP.

**Findings:**

**Finding 1: Qualified demo requests from mid-market data teams increased 9%
quarter-over-quarter following the webinar series, against a stated target of
20%.** Evidence: CRM-sourced demo-request report for Q1, segmented by company
size and by lead source, supplied as part of results_data. **Tag:
OUTCOME-SUPPORTED** (the evidence ties directly to Objective A's stated
metric, even though the target was not met — a partial or missed result tied
to the right metric is still outcome-evidence, not activity-evidence).

**Finding 2: Average registered attendance across the four webinars was 340,
with a combined 1,360 registrations and an 18% average post-event engagement
rate on follow-up email.** Evidence: webinar platform analytics export.
**Tag: ACTIVITY-ONLY** (registration and engagement volume describe what the
campaign did; neither figure is the demo-request metric or the satisfaction
score named in Objectives A or B, and no linking analysis connecting
attendance to demo requests was supplied).

**Finding 3: No post-webinar attendee satisfaction survey data was supplied
for any of the four sessions.** **Tag: GAP** — Objective B specified a
measurable 4.0/5.0 target, but {input needed: was a post-webinar satisfaction
survey run for this series, and if so, can the results be supplied?}.

**Finding 4: Objective C ("thought leadership position") has no attached
metric, target, or timeframe in the supplied campaign context and cannot be
assessed as stated.** **Tag: GAP** — carried forward from the Section 2 flag.
{input needed: what specific, measurable signal was Objective C meant to
produce — e.g., share-of-voice in a defined publication set, inbound analyst
briefing requests, branded search volume — and over what timeframe?}

**Finding 5: Session 3 ("Data Quality Benchmarks") registration was 40% below
the series average, and post-event engagement for that session was the lowest
of the four at 9%.** Evidence: same webinar platform analytics export as
Finding 2, session-level breakdown. **Tag: NEGATIVE/NULL** relative to the
implicit within-series comparison — included here even though it reflects
unfavorably on one session, because it is present in the supplied data and
Section 5 (results_data) did not authorize dropping unfavorable segments.

---

**Corresponding Recommendations (Section 6), for illustration:**

Recommendation 1 (from Finding 1): Continue the webinar-to-demo-request
funnel used in Q1, but investigate the gap between the 20% target and the 9%
actual before committing to the same target for Q2 — the evidence supports
continuing the approach, not assuming the target was simply under-hit by
execution quality, since no execution-quality evidence was supplied.

Recommendation 2 (from Finding 3): Before the next webinar series, implement a
post-event satisfaction survey so Objective B becomes assessable; this series
cannot retroactively produce that evidence.

Recommendation 3 (from Finding 4): Define a specific, measurable version of
the thought-leadership objective before the next planning cycle, using one of
the candidate metrics named in the Finding 4 gap flag — this recommendation is
scoped to "go define the metric," not to any claim about whether thought
leadership was actually achieved, since no such claim is supported by
evidence.

Recommendation 4 (from Finding 5): Review Session 3's topic and format choices
before reusing them, given the within-series underperformance — scoped as a
review recommendation, not a claim that the topic itself caused the drop,
since no causal evidence was supplied.

Note how Recommendation 1 does not claim the Q1 approach "worked" — Finding 1
shows a real but partial outcome result, and the recommendation is scoped to
that, not inflated into a success claim the evidence doesn't support.
