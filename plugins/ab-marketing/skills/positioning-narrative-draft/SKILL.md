---
name: positioning-narrative-draft
description: Draft a five-section positioning narrative (Category Definition, Target Customer, Differentiated Value, Proof Points, Moat/Durability) for a company, product, or brand, plus a conditional Evidence Gaps appendix. Use when asked to draft brand positioning, a positioning statement, an investor- or board-facing company narrative, a "why us" document, competitive positioning, or the marketing-strategy section of a pitch deck or memo. Use whenever the ask calls for evidence-disciplined positioning (quantified claims stated against a named baseline or comparator) rather than generic marketing copy with unearned superlatives.
---

# Positioning Narrative Draft

Produce a single markdown document with five required sections, in order, plus a
conditional Evidence Gaps appendix. Each section has a structural gate. Self-check the
draft against every gate before returning it. Repair failures where the founder's inputs
allow a fix; where they don't, either downgrade the claim to an explicitly-labeled
unverified assertion or move it to the appendix. Never silently ship a gate-failing
section, and never invent a fact, number, or source to make a gate pass.

## Quality bar (what "gold" looks like)

The core discipline below is distilled from two categories of public source: S-1/A
"Business" and "Marketing Strategy" narratives that companies filed under
securities-liability discipline (a materially false or misleading statement in a
registration statement carries legal exposure, so the surviving language is unusually
well-evidenced compared to ordinary marketing copy — see, for example, Allbirds, Inc.
Form S-1/A, Amendment No. 4, 2021, and FIGS, Inc. Form S-1/A, Amendment No. 3, 2021), and
the AMA PCM Marketing Management Body of Knowledge, whose competency-domain weighting is
a useful proxy for where a positioning draft should carry the most rigor. Name these
qualities explicitly and check the draft against them; do not reproduce source language,
only the structural pattern.

1. **Positioning stated as a syllogism, not an assertion.** A credible positioning claim
   reads as: {category or customer evidence} + {a trend or shift} → {claimed unique
   position}. The step from evidence to claim must be explicit and must not skip logical
   ground — a claim that two forces uniquely align or converge only earns its place once
   each force has been independently evidenced immediately beforehand, not asserted as a
   single confident leap.
2. **Every differentiator or proof point is a number against a named baseline.** "30%
   less than {a stated baseline figure}," "{engagement rate} vs. {named industry
   average}," never a bare adjective ("industry-leading," "best-in-class") standing
   alone. If a claim can't be stated as {metric} vs {comparator}, it is not yet a proof
   point — it is either an evidence gap or a labeled unverified assertion.
3. **Mechanisms are named, not just outcomes.** A strong proof point or moat names the
   *program, asset, process, or relationship* that produced the number — a named
   recurring campaign cadence, a named community/ambassador program, a named
   proprietary data flywheel — not just the resulting metric in isolation. Durability
   claims in particular must explain why the mechanism keeps compounding, not just that
   it currently produces a good number.
4. **Category and comparator claims are attributed**, not asserted in the company's own
   voice as fact. Third-party research, a founder-flagged internal metric, or an
   explicitly named comparator — never an unsourced "the market is shifting toward X."
5. **No unearned superlatives.** Strip "revolutionary," "world-class," "unmatched," and
   similar adjectives unless immediately followed by the number and comparator that
   earns them. If a founder input contains one, either find the number behind it or cut
   it to plain, evidence-first language.

**Provenance note on the per-section gates:** `references/gold-structure-checklist.md`
turns the five qualities above into a specific gate for each of the five sections. Most
of those per-section gates are a direct structural echo of the source classes above (the
metric-vs-baseline and named-mechanism checks on Proof Points, for instance, map
one-for-one onto patterns in both S-1/A exemplars). Two gates do not: the Target
Customer specificity test (a reader can name a plausible non-customer from the
description) and the Moat/Durability multi-year-compounding test (the mechanism must
explain why the advantage holds up over a multi-year horizon, not just that it holds
today). Neither exemplar narrates a standalone target-customer or moat section, and the
AMA map supplies topic-level weighting, not check-level criteria — so those two checks
are this skill's own applied editorial judgment, built to extend the same evidence-first
discipline into territory the source material doesn't cover directly. They are held to
the same rigor as the sourced gates; they just aren't distilled from a source document.

See `references/gold-structure-checklist.md` for the gate checklist used in the
self-check step, and `references/intake-questions.md` for the per-section intake
prompts used when founder inputs are thin.

## Procedure

### Step 1 — Intake

Before drafting, gather founder inputs for each of the five sections. Do not proceed to
drafting on the basis of assumption, inference from company type, or general market
knowledge — every category claim, proof point, and moat mechanism must trace to
something the founder said, a source the founder pointed to, or a number the founder
explicitly approved as a stand-in.

Ask using the prompts in `references/intake-questions.md`, scoped to whatever the
founder has *not* already supplied unprompted. If the founder has clearly already
provided rich material (a deck, a memo, notes) for a section, do not re-ask that
section's questions — extract from what's given and only follow up on what's still
missing or ambiguous.

**Thin-input handling (mandatory, not optional):**
- If a section's inputs are too thin to satisfy its gate (see Step 3), do not invent
  the missing category data point, customer specificity, evidence, number, comparator,
  or mechanism to make the gate pass.
- First, ask the founder directly for the missing fact (a number, a source, a named
  program, a comparator).
- If the founder has no answer or the conversation is asynchronous/non-interactive,
  write the section using only what's actually supported, and either (a) rewrite the
  unsupported part as an explicitly labeled `{founder-asserted, unverified}` claim, or
  (b) omit the claim from the section body and list it in the Evidence Gaps appendix
  instead. Never present a thin or invented claim as if it were evidenced.
- A section is allowed to be shorter and plainer than the exemplar pattern if that's
  what the real inputs support. A well-labeled gap is always preferable to a confident
  fabrication.

### Step 2 — Draft

Draft the five sections in order, each following its section-specific instructions
below. Write in declarative, evidence-first prose — matches the liability-disciplined
register of the grounding exemplars: state the claim, state the evidence, state the
comparator. No angle-bracket placeholders anywhere in the draft; use curly-brace
`{placeholder}` form for anything not yet filled in (e.g. `{metric}`, `{n}%`,
`{comparator}`, `{source}`).

**## 1. Category Definition**
- State the category the company competes in in one to two sentences, grounded in a
  sourced or founder-flagged category-level data point (market size, a named trend, a
  cited report — never an unsourced "the market is growing").
- Where founder inputs support it, add the redefinition move: name the specific
  category data point and the specific trend the company's position converges with,
  then state the claimed position as the consequence of those two facts (the syllogism
  pattern from the Quality Bar). Do not add this move if the inputs don't actually
  support two independent evidenced legs — a forced convergence claim with only one
  real leg is worse than a plain category statement.
- Do not assert category leadership ("the leading X," "#1 in Y") without naming the
  specific comparator the leadership claim is measured against.

**## 2. Target Customer**
- Describe the customer in operational terms: their role, the context they operate in,
  and the job-to-be-done that brings them to this company — not a demographic label
  standing alone ("millennials," "SMBs").
- Write it specific enough that a reader could name who is explicitly *not* the target
  customer as a natural consequence of the description. If the draft doesn't produce a
  clear non-customer by implication, it's still a demographic label in disguise —
  narrow it.

**## 3. Differentiated Value (the positioning statement)**
- Write the core positioning claim as the explicit syllogism: {category/customer
  evidence, stated or referenced from Sections 1–2} + {a trend or shift} → {the claimed
  unique position}. One to two tight paragraphs of prose — never a bulleted feature
  list.
- The "therefore" step from evidence to claim must be traceable in the same paragraph
  or the one immediately before — a reader must be able to point to the specific
  sentence the position is derived from. If the claimed position requires a leap the
  stated evidence doesn't support, either find the missing evidence from the founder or
  narrow the claim until it's fully earned by what's stated.

**## 4. Proof Points**
- Three to six bullets or short paragraphs. Each must contain: a quantified claim, an
  explicit baseline or comparator, and the named mechanism (program, process, or asset)
  that produced the number.
- For every candidate proof point the founder supplies that lacks a number or a
  comparator, apply the Step 1 thin-input protocol: get the missing piece from the
  founder, quantify it using a founder-approved figure, move it to the Evidence Gaps
  appendix, or rewrite it as an explicitly labeled `{founder-asserted, unverified}`
  claim. Never write a proof point that reads as evidenced but isn't.

**## 5. Moat / Durability**
- Name at least one structurally repeatable mechanism: a named recurring program, a
  proprietary asset, a data flywheel, a network effect, or an exclusive relationship.
- Explain *why* it compounds or resists replication over a multi-year horizon — answer
  "why does this stay true in 3 years," not just restate that a metric is currently
  favorable. A moat claim that only describes today's number, without a mechanism for
  why a competitor can't just match it, fails this gate and must be rewritten or moved
  to the appendix.

**## Appendix: Evidence Gaps** (conditional)
- Include this section whenever any claim in the draft was thin, unsourced, or
  founder-asserted-only per the Step 1 protocol. Omit entirely only if the self-check in
  Step 3 finds zero gaps.
- Format as a plain list: one line per gap, naming the section it's in, the claim, and
  exactly what's missing (a number, a named comparator, a source, a verified
  mechanism) — so the founder knows precisely what to firm up before this goes in front
  of investors or a board.

### Step 3 — Self-check against gates

Before returning the draft, check every section against its gate using
`references/gold-structure-checklist.md` as the checklist. For each gate:
- **Pass** — leave the section as drafted.
- **Fail, fixable from founder inputs already given** — repair the section using
  material already provided (e.g. a number was given but not yet paired with a
  comparator in the prose; pull the comparator in).
- **Fail, not fixable from what's given** — do not repair by inventing. Either
  downgrade the specific claim to `{founder-asserted, unverified}` inline, or strip it
  and add it to the Evidence Gaps appendix. Re-run the gate check on the repaired
  section before moving on.

Do not return a draft with a section that still fails its gate silently. If, after the
repair pass, a section still cannot satisfy its gate even in reduced/labeled form (for
example: Target Customer is still a bare demographic label with nothing operational to
work with), stop and flag it back to whoever requested the draft, naming the specific
gate that's unmeetable and the specific fact needed to meet it, rather than shipping a
gate-failing section.

### Step 4 — Return the draft

Return the complete markdown document: the five `##`-level sections in the exact order
and exact headers specified in the output contract, followed by the Evidence Gaps
appendix if triggered. No angle-bracket placeholders anywhere in the final output —
curly-brace form only. No build narrative, no meta-commentary about the drafting
process in the output itself; the checklist self-check happens before the document is
returned, not inside it.
