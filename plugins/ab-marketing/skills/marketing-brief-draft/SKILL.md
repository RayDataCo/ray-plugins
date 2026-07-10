---
name: marketing-brief-draft
description: Drafts a complete one-page marketing brief (objective, situation summary, STP, positioning statement, single-minded proposition, offering, channel strategy, success metrics, constraints, assumptions, self-check) from founder-supplied inputs about a product or service. Use when asked to draft, write, or update a marketing brief, campaign brief, positioning brief, or creative/agency brief; to prep a one-pager before briefing an agency, freelancer, or ad platform; or to turn thin/rough notes about a product, audience, or objective into a structured brief grounded in AMA PCM competency weighting and Saylor Academy marketing methodology. Always produces all 11 sections even when inputs are thin, flagging assumptions explicitly rather than inventing silently. Not for full campaign plans, finished ad copy, media buys, or budget execution — this produces the strategic brief that precedes those.
---

# marketing-brief-draft

## Purpose

Produce exactly ONE markdown marketing brief document per invocation. The brief has 11
fixed sections, in fixed order, every field always populated (never left blank, never
left as an unfilled placeholder). When an input is thin or missing, the skill either asks
the founder for the missing fact or — if asking isn't possible in this context — fills the
gap with an explicitly labeled assumption and logs it in Section 10. It never invents a
fact silently and presents it as given.

## Inputs this skill accepts

Required for a usable brief (ask if missing rather than guessing):
- `product_or_service` — name and one-line description of what's being marketed
- `objective` — the business objective this brief exists to serve

Strongly recommended (thin handling applies if absent):
- `business_context` — company/brand situation, stage, resources
- `market` — market size/shape, trends, buyer environment
- `competitive_context` — named or categorical competitors, their positioning
- `known_audience_signals` — anything already known about who buys/uses this (demographics, behavior, existing customer data, stated pains)
- `offer_terms` — pricing/packaging/promise specifics
- `service_delivery_expectations` — only if `product_or_service` is a service
- `digital_emphasis` — one of `digital-forward`, `mixed`, `traditional-forward`; defaults to `mixed` if unstated (log as an assumption)
- `constraints` — budget, timeline, legal/brand mandatories, channel exclusions
- `prepared_for` — who the brief is written for (a person, a team, an agency)

## Quality bar (what a strong brief gets graded on — hold every draft to these)

These are the structural qualities encoded from the AMA PCM competency weightings and the
Saylor course methodologies (see reference files). A brief that violates any of these is
not done yet:

1. **One primary objective, not a list.** Marketing Management BOK Domain 1 (Marketing
   Strategy) treats a brief as situation → plan, anchored to a single objective; secondary
   objectives are named but explicitly subordinated, never co-equal.
2. **STP is the pivot, not a formality.** Segmentation, targeting, and positioning is
   sequenced before offering depth and channel choice, and every downstream section
   (offering, channel strategy) must trace back to the targeting decision — never assert a
   channel or benefit claim from nowhere.
3. **Situation summary is evidence, not scene-setting.** Every claim used later in the
   brief (especially channel choice) must be traceable to a bullet in Section 3.
4. **Positioning statement is fully resolved.** All four frame slots (target segment,
   category frame, key benefit, reason to believe) are filled with scenario-specific
   language in the delivered brief — never left as an open frame.
5. **SMP narrows, it doesn't restate.** The single-minded proposition is a strict
   narrowing of the positioning statement's key benefit, not a paraphrase of the whole
   positioning line. Mechanical test: place the key-benefit clause and the SMP side by
   side. If the SMP mostly reuses the same words or clause structure with a few words
   dropped, it is a compression, not a narrowing, and fails this check — rewrite it around
   one dimension the positioning line doesn't already spell out (a use-occasion, a stake,
   an urgency, a proof point) so the two sentences are visibly distinct claims, not one
   claim said twice at different lengths.
6. **Offering gets proportionally the most depth.** Marketing Management BOK Domain 5
   (The Offering) is the largest single domain (21%); Section 6 should read as the most
   thoroughly reasoned section in the brief relative to its length elsewhere.
7. **Digital channel strategy is a mix, not a paid-media reflex — in either direction.**
   Digital Marketing BOK weights Email at 20% and Metrics/Social/UX at 15% each against
   Online Advertising at only 10%. Any digital-forward or mixed brief that proposes paid
   media alone without touching measurement, UX/landing surface, or lifecycle/email fails
   this check. The reverse failure is just as real: a `traditional-forward` brief is under
   no obligation to name any digital channel at all, and bolting on a token digital line
   "as a light-touch addition" purely to look complete is itself a violation, not a safe
   default — every channel named, digital or not, must earn its place from the Section 4
   targeting rationale.
8. **No orphan metrics.** Every metric in Section 8 must name which objective (Section 2)
   or channel (Section 7) it is measuring — a metric with no home is cut or fixed.
9. **Honesty over completeness theater.** Thin inputs are disclosed as assumptions, not
   smoothed over. A confident-sounding brief built on invented facts is a worse output
   than one that visibly flags its gaps.
10. **Zero unfilled placeholders in the delivered document.** Every brace-frame is resolved
    to real content before the brief is returned; nothing that looks like a template blank
    ships to the founder.
11. **The self-check note is Section 11 in name, not just in position.** It gets a numbered
    header — "11. Self-Check Note" — matching the format of Sections 1-10. A horizontal
    rule plus unlabeled bold text is visual separation, not a numbered section, and does
    not satisfy "11 sections, numbered 1 through 11."

## Procedure

### Step 1 — Intake and completeness pass
Read every input provided. For each required or strongly-recommended field:
- If present and substantive, use it directly.
- If thin (a fragment, a guess, "not sure") or absent: prefer asking the founder a short,
  specific question before drafting, when the invocation context allows a round trip.
- If asking isn't possible (single-shot dispatch, batch run, or the founder has said
  "just draft it") — do not invent a fact and present it as given. Instead, write the
  most reasonable, scenario-grounded assumption, mark it inline in the relevant section
  with the word "assumption:" plus one clause of reasoning, and add it to the running
  assumptions log that becomes Section 10.
Never silently backfill a gap with generic marketing boilerplate dressed as fact.

### Step 2 — Draft the Brief header and Objective (Sections 1-2)
Section 1: product/service name, prepared-for, a one-line objective statement, and today's
date.
Section 2: one paragraph. Restate the business objective precisely (not a rephrase of the
product description), then name the ONE marketing objective this brief serves. If more
than one objective was supplied, choose the primary by asking "which one, if achieved
alone, most moves the business objective" and name the rest as secondary/subordinated in
the same paragraph — do not let them compete with the primary for space or emphasis.

### Step 3 — Draft the Situation summary (Section 3)
Synthesize `business_context`, `market`, and `competitive_context` into 3-6 bullets — a
compact situation analysis (strength/weakness/opportunity/threat-flavored, not a formal
SWOT grid). Every bullet should be something a later section can point back to. If
`competitive_context` was thin, write the competitive bullet as a reasoned assumption
about the likely competitive set given the category, flagged per Step 1.

### Step 4 — Draft STP (Section 4)
This is the pivot section — spend real effort here, everything downstream depends on it.
- **Segmentation:** identify 2-4 candidate segments from `market` and
  `known_audience_signals`, each with one defining trait (behavioral, needs-based, or
  demographic — pick whichever the input signals actually support, don't force
  demographics if the signal is behavioral).
- **Targeting:** name which segment(s) are primary vs. secondary and give the one-sentence
  rationale — this rationale must reference something from Section 3 or the segmentation
  list, not a bare assertion.
- **Positioning statement:** fill the frame completely — "For {target_segment},
  {product_or_service} is the {category_frame} that {key_benefit}, because
  {reason_to_believe}." Every slot must carry scenario-specific language pulled from the
  targeting decision and the situation summary. Do not ship any slot unresolved.

### Step 5 — Draft the SMP (Section 5)
Write one sentence: the single most persuasive, ownable claim the brief commits to. Run
the mechanical distinctness test from quality-bar item 5 before moving on: put the
positioning statement's `key_benefit` clause next to the SMP draft. If the SMP is
recognizably the same clause with words trimmed or reordered, it is a restatement, not a
narrowing — rewrite it to isolate one sharper claim (a use-occasion, a specific stake, an
urgency, a proof point) that the positioning line does not already say outright. Do not
finalize Section 5 until the two sentences read as distinct claims.

### Step 6 — Draft The offering (Section 6)
Explain how `product_or_service`, its `offer_terms`, and (if a service)
`service_delivery_expectations` support the SMP. Per the quality bar, this is the largest
domain in the underlying competency model — give it proportionally more explanatory depth
than any other single section. Don't just list features; connect each offer element back
to why it makes the SMP credible.

### Step 7 — Draft Channel strategy and run the digital-mix self-check (Section 7)
Name primary channel(s) first, with the reason each reaches the specific segment chosen in
Step 4 — trace explicitly back to STP, don't select channels by category convention. Then
name secondary/supporting channels.
**Self-check A (digital-forward or mixed only):** if `digital_emphasis` is
`digital-forward` or `mixed`, confirm the section addresses at least one of: measurement/
analytics, UX or landing surface, or lifecycle/email — in addition to any paid or organic
acquisition channel named. If the draft is 100% paid-media/acquisition with none of those
three present, it fails this check: add the missing dimension before moving on.
**Self-check B (`traditional-forward` — the opposite failure mode):** do not add a digital
channel, landing page, or tracking line as a hedge "to cover bases" or to make the brief
look modern. A `traditional-forward` brief may legitimately name zero digital channels. If
a digital element is genuinely justified by the Step 4 targeting decision, name it and say
why; if it isn't, leave digital out entirely rather than appending a token mention. A
gratuitous digital add-on fails this check exactly like a missing-measurement gap fails
Self-check A.
Note in your own working notes (for the Section 11 self-check note) whether Self-check A or
B applied, whether it passed on the first draft, and whether anything was added or removed
because of it.

### Step 8 — Draft Success metrics and run the orphan-metric check (Section 8)
List 2-5 metrics. For each one, name in the same bullet which objective (Section 2) or
which channel (Section 7) it measures. Discard or rewrite any metric that doesn't have a
named home — that is an orphan metric and fails the quality bar.

### Step 9 — Draft Constraints/mandatories and Assumptions/gaps (Sections 9-10)
Section 9: restate `constraints` as supplied, plus any brand/legal mandatories implied by
the category (e.g., regulated-industry disclosure norms) if relevant. If `constraints` was
thin or absent, explicitly say so and name the default assumed (e.g., "no budget ceiling
specified — brief assumes a modest single-channel test budget").
Section 10: compile the running assumptions log from every step above into a short
explicit list — one line per assumed or inferred field, naming the field and the
reasoning. This section may be empty only if literally nothing was assumed anywhere in the
draft; that should be rare.

### Step 10 — Assemble, scan for placeholders, and write the self-check note (Section 11)
Assemble all 11 sections in fixed order with numbered/lettered markdown headers matching
the section numbers above. Before returning the brief, re-scan the entire document for any
unfilled brace-frame or template-looking blank (especially in Section 4's positioning
statement) — resolve or fix anything found. Confirm the brief body (everything excluding
the self-check note) lands in the 500-900 word target; if the scenario is unusually
complex and it runs longer, add one explicit line stating why.
Write the self-check note last, and give it a real numbered header — "11. Self-Check
Note" — in the same style as Sections 1-10, not an unnumbered bold line after a horizontal
rule. Keep it 3-5 lines, stating plainly which checks from the quality bar passed as-drafted
and which required an adjustment — at minimum cover Section 7's Self-check A or B (state
which one applied and its outcome) and Section 8's orphan-metric check, plus the
offering-depth, STP-traceability, and SMP-distinctness checks if anything about them was
non-obvious. This note is for the founder's trust in the structure, not part of the
brief's business content.

## Output format rules

- Markdown only. Numbered/lettered section headers matching 1 through 11 exactly —
  including Section 11 (the self-check note), which must carry the literal header "11."
  like every other section, never just a rule-plus-bold-text convention.
- Plain prose plus bullets — no tables required, none forbidden.
- Never leave a template placeholder unresolved anywhere in the delivered document.
- If you must show an example or a still-open slot while drafting internally, use curly
  braces like `{target_segment}` — never angle brackets — and resolve it before the final
  document ships. No angle-bracket placeholder should ever appear in the returned brief.
- Return exactly one document per invocation. If the founder asks for revisions, redraft
  the same 11-section document rather than appending a second one.

## Reference files

- `references/ama-competency-weights.md` — restated (facts-only) domain structure and
  weightings from the AMA PCM Marketing Management and Digital Marketing competency maps,
  citing the public AMA PCM program pages by name; underlies the offering-depth and
  digital-mix self-checks.
- `references/stp-brief-method.md` — restated methodology from Saylor Academy BUS203 and
  BUS632 (CC BY 3.0, attributed with public course URLs), underlying the STP-pivot
  sequencing, situation-summary traceability, and monitoring/evaluation-closes-the-loop
  principles this skill enforces.
