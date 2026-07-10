---
name: advertising-claims-endorsement-review
description: Reviews marketing copy, influencer briefs, testimonials, case studies, and expert/organizational endorsement content against FTC 16 CFR Part 255 (Endorsement Guides) for PRESENT/ABSENT/DEFICIENT element coverage — material-connection disclosure, consumer/expert/organizational endorsement duties, and efficacy-claim substantiation. Use before publishing anything with a testimonial, influencer partnership, "#ad"-style disclosure, expert or practitioner endorsement, or efficacy language like "clinically tested," "proven," "guaranteed," or "backed by research." Emits ONE compact coverage table (element, status, citation, defect detail) in full every time, never a prose summary and never referenced as already produced. Reports coverage, not a compliance verdict, and is not legal advice — route ABSENT/DEFICIENT findings to counsel.
---

# Advertising Claims & Endorsement Review

Coverage-checking skill, not a legal-advice skill. It reads submitted marketing
content (ad copy, influencer brief, testimonial page, case study, social post
draft, etc.), determines which sections of 16 CFR Part 255 (the FTC's
Endorsement Guides) apply, and reports element-by-element whether the content
addresses each applicable requirement. It never issues a compliance verdict —
it reports coverage and routes gaps to counsel.

Grounding lives in two bundled reference files, both distilled from
public-domain US federal material (17 U.S.C. § 105 — no copyright, fully
excerptable with citation):

- `references/16-cfr-255-elements.md` — the enumerated 255.0–255.6
  requirements, each with a plain-language summary, a directly quotable
  line, and the per-element status decision rules that resolve the
  cases most likely to be scored wrong.
- `references/substantiation-defect-patterns.md` — four named
  efficacy-claim defect patterns (drawn from a real FTC enforcement
  complaint) plus the mechanical detection tests and carve-outs for each,
  used as the 255.1-substantiation sub-check whenever the content makes an
  efficacy or results claim.

## When to use this skill

Trigger on any request to review, audit, or check the compliance of: ad copy,
landing-page or product-page claims, influencer/creator briefs, testimonial or
case-study content, social posts quoting a customer or an expert, or any
content where someone other than the advertiser appears to be vouching for a
product or service. Also trigger proactively whenever content contains
efficacy language ("clinically tested," "proven," "guaranteed," "doctor
recommended," "backed by science/research") even without an explicit request.

## Inputs

Before starting, establish:

1. **The submitted content** — the actual copy/brief/page text to review. If
   pasted inline, that is the input; if referenced by file or URL, read it in
   full — this skill quotes from it, so a summary is not enough.
2. **content_type** — a short label (e.g. "Instagram influencer brief,"
   "product landing page," "case-study one-pager"). If not stated, infer it
   and say so. Note explicitly when content_type is a brief or instruction
   set for a not-yet-published post — Step 4 rule 5 governs how those are
   scored differently from a finished, published piece.
3. **jurisdiction_confirmation** — whether the content is confirmed
   US-targeted. If not stated, default to unconfirmed and add a
   `jurisdiction_note` to the header.
4. **endorser_context** (optional) — whether the endorser's compensation,
   free product, employment, or personal-use status is confirmed one way or
   the other. If this is not provided and the content itself doesn't resolve
   it, do not guess PRESENT or ABSENT — carry it into Step 4 as an unresolved
   fact and say so explicitly in the affected element's defect detail.

If the content is too sparse to evaluate anything (a one-line product name,
no claims, no endorser, no testimonial), say so plainly instead of forcing
findings.

## Procedure

### Step 1 — Load grounding, every time, no exceptions

Read both reference files in full before evaluating anything. Every citation
in the report must trace back to text in one of these two files — never cite
16 CFR 255 language, an FTC quote, or a substantiation pattern from memory or
prior familiarity. If you have not actually opened both files in this run,
stop and open them before writing a single finding. A report that admits it
reconstructed citations without reading the files is a failed report, not a
report with a caveat.

### Step 2 — Trigger determination

Decide, for each conditional element, whether it applies:

| Element | Triggers when the content... |
|---|---|
| 255.2 (consumer endorsement) | Depicts, quotes, or references an actual (named or anonymized) ordinary consumer's own experience or results being showcased as an endorsement. A generic, population-level marketing statistic or claim ("many customers feel relief," "9 out of 10 users agree") with no specific consumer's experience actually depicted does NOT by itself trigger 255.2 — see Step 4 rule 2 before marking this triggered. |
| 255.3 (expert endorsement) | Invokes a professional credential, title, or claimed expertise as the source of an endorsement |
| 255.4 (organizational endorsement) | Depicts an organization, association, or institution (not an individual) as endorsing, approving, or recommending the product |
| 255.5 (material connection) | Is sponsored, gifted, paid, an influencer/creator brief, an affiliate arrangement, or otherwise involves a relationship a consumer would not assume |

255.0, 255.1-honest-opinion, 255.1-substantiation, and 255.6 are always
evaluated, never conditional. This determination becomes one compact line in
the report header — do not give it a separate section. **The reason named in
this line and the status later written in that element's table row must
never contradict each other** (see Step 4 rule 1).

### Step 3 — Element findings: status definitions

For every always-evaluated element and every triggered element, decide:

- **PRESENT** — the content demonstrably satisfies the element; no gap.
- **ABSENT** — the element is required by the trigger determination and
  nothing in the content — not even an incomplete attempt — addresses it.
- **DEFICIENT** — the content makes an attempt at the element (a disclosure
  exists but isn't clear-and-conspicuous; a typicality claim with no
  substantiation and no expected-results disclosure; a credential asserted
  with no evaluation rigor described; a brief's instructions gesture at an
  organizational endorsement without addressing how it reflects collective
  judgment; an open question the input never resolved) but the attempt has a
  specific, nameable defect.

The dividing line between ABSENT and DEFICIENT is "did the content try and
fall short" (DEFICIENT) vs. "did the content never address this at all"
(ABSENT) — not how serious the gap is. A serious gap in an attempted
disclosure is still DEFICIENT, not ABSENT.

Split 255.1 into two independent elements — do not merge them, they check
different things, and do not invent a third:

- **255.1-honest-opinion** — does the endorsement read as the endorser's
  actual, genuinely held opinion, with nothing an advertiser couldn't say
  directly? Casual, enthusiastic, or informal phrasing ("this stuff is
  amazing," "obsessed with it") is ordinary genuine-opinion language, not
  evidence of fabrication — never mark this element DEFICIENT for tone,
  hype, or lack of hedging alone, and never import a weak- or
  unsubstantiated-*efficacy* concern into this element; that always belongs
  to 255.1-substantiation, even when the shaky claim appears inside a
  first-person quote. Mark 255.1-honest-opinion DEFICIENT/ABSENT only when
  the content shows actual evidence of a fabricated, scripted, or coerced
  opinion (e.g. a brief instructing an endorser to say something they
  haven't experienced).
- **255.1-substantiation** — the advertiser's liability for false or
  unsubstantiated statements made through the endorsement. Run the Step 5
  four-pattern check against this element whenever an efficacy claim is
  present. If 255.5 is also triggered, 255.5 alone owns the
  material-connection-disclosure question — do not re-litigate disclosure
  under 255.1-substantiation and do not create a second element for the same
  open question. If 255.2 is triggered or triggerable, 255.2 alone owns any
  typicality/aggregate-customer-count language — see Step 4 rule 2 for the
  exact routing test before running the four-pattern check.

### Step 4 — Boundary rules (apply all relevant ones before finalizing any status)

These eight rules resolve the specific places this check most often goes
wrong. Apply all that are relevant before writing a status, in this order:

1. **255.2's typicality duty is conditional on a typicality representation
   — and once triggered by one, the row must evaluate it, not wave it off.**
   255.2 only requires substantiation-of-typical-results or a
   disclosed-expected-results line when the content actually represents or
   implies the depicted experience is what other consumers can expect
   ("you'll get this too," "most people see...," an implied general
   promise). A single first-person account with no such generalizing
   language does not trigger that specific duty — mark 255.2 PRESENT with a
   one-line note that no typicality representation was made, not DEFICIENT.
   But if the trigger-determination line names a specific typicality/
   generalizing phrase as the reason 255.2 fired, the row can never then say
   "PRESENT — no typicality representation was made"; that is a direct
   self-contradiction. In that case, apply the substantiate-or-disclose test
   for real: DEFICIENT unless the content actually substantiates the
   typical result or clearly discloses generally-expected results.
2. **255.2 requires an actual depicted endorser; route aggregate/typicality
   language to whichever of 255.2 or 255.1-substantiation actually governs
   it, never both.** 255.2 exists to police an endorsement — it needs a
   specific consumer (named or anonymized) whose experience is being shown.
   A population-level statistic or generic claim phrased in the advertiser's
   own marketing voice ("many customers feel relief within hours," "9 out
   of 10 users agree") with no depicted individual endorser anywhere in the
   content is ordinary advertiser copy, not a consumer endorsement — leave
   255.2 NOT TRIGGERED and evaluate that language, if it asserts an efficacy
   outcome, under the Step 5 four-pattern check instead. If the content DOES
   depict at least one actual endorser/testimonial elsewhere, then aggregate/
   typicality phrasing ("join thousands of happy customers") is the very
   typicality representation that governs 255.2 under rule 1 above — score
   it there. Never score the same aggregate-customer phrase under both
   255.2 and the 255.1-substantiation four-pattern check, and never pull an
   individual endorser's own bounded first-person quote into the four-pattern
   check merely because a separate headline elsewhere makes a typicality
   claim — evaluate each passage under the one element it actually belongs to.
3. **255.0 is a definitions element, not an independent content
   obligation.** It establishes what "endorsement" and "material connection"
   mean for the rest of the review — the submitted content does not "do"
   anything to satisfy or fail it on its own terms. Mark it PRESENT in
   virtually every review, with a one-line note that the endorsement/
   material-connection definitions apply to the content as evaluated below.
   Reserve DEFICIENT/ABSENT for the rare case where the content's own framing
   actively defeats the definitional concepts (e.g. content that relabels an
   obviously sponsored placement as organic in a way that undermines what
   "endorsement" even means here) — this should be uncommon.
4. **255.6 is a liability-allocation section, not a content checklist.** It
   asks whether the endorser or an intermediary (ad agency, PR firm, review
   broker, reputation-management company) is shown creating or spreading a
   deceptive or undisclosed-connection endorsement. Absent that specific
   signal in the content, mark 255.6 PRESENT by default — do not read it as
   a generic "does the advertiser train/monitor endorsers" duty and do not
   mark it DEFICIENT without a concrete intermediary-conduct quote. An
   unresolved or even undisclosed material connection scored under 255.5 is
   not, by itself, evidence for a 255.6 finding — 255.6 needs its own
   intermediary-conduct signal.
5. **Brief/instruction content is scored on the instructions actually given,
   not on a hypothetical finished post.** When content_type is a brief,
   script, or instruction set for a not-yet-published piece, evaluate what
   the brief's language actually says and omits — not what a compliant or
   noncompliant final post might look like. If the brief's instructions
   gesture toward triggering conduct (e.g. tells the endorser to imply an
   organization's or employer's endorsement, or to share a testimonial)
   without any instruction addressing the element's duty (e.g. nothing about
   how the organizational view was actually formed, or about disclosure),
   that is an attempt with a gap — DEFICIENT, not ABSENT. Reserve ABSENT for
   elements the brief's language never touches in any form.
6. **Unresolved endorser_context gets one DEFICIENT element, not two.** When
   compensation/relationship/personal-use status was not provided and the
   content doesn't resolve it, mark the single most relevant element (usually
   255.5, or 255.1-substantiation if 255.5 isn't triggered) DEFICIENT and say
   plainly in its defect detail that the fact wasn't provided and needs
   confirmation before publishing. Never duplicate that same open question
   under a second, invented element.
7. **Severity ranking draws only from ABSENT/DEFICIENT rows, using a fixed
   tier order.** PRESENT elements are never ranked or tagged with a severity
   marker. When more than one row is ABSENT/DEFICIENT, assign each to a tier
   below, then rank most-severe-tier-first; break ties within a tier by table
   row order (255.0 → 255.6):
   - Tier 1 — undisclosed or unresolved material connection (255.5)
   - Tier 2 — an unsubstantiated claim in a health/financial/legal/safety
     category (255.1-substantiation with any of patterns a/b/c/d flagged in
     one of those categories), or a 255.6 finding backed by concrete
     intermediary-conduct evidence
   - Tier 3 — a fabricated/scripted/coerced opinion (255.1-honest-opinion
     DEFICIENT/ABSENT) or an unsubstantiated typicality representation
     (255.2 DEFICIENT/ABSENT)
   - Tier 4 — an expert-credential defect (255.3) or an
     organizational-collective-judgment defect (255.4)
   - Tier 5 — softer definitional or wording/precision gaps (255.0, or a
     255.1-substantiation gap outside a health/financial/legal/safety
     category)
   Rank and tag every ABSENT/DEFICIENT row if there are 5 or fewer; if more
   than 5 exist, tag only the top 5 by tier and leave the rest ABSENT/
   DEFICIENT with no severity tag.

### Step 5 — Substantiation four-pattern sub-check

Run this only against 255.1-substantiation, and only when the content
contains an efficacy, results, or outcome claim that Step 4 rule 2 has
routed here (not a typicality/aggregate-customer claim, and not a
depicted endorser's own bounded personal account — see below). Open
`references/substantiation-defect-patterns.md` and check the content against
each of the four detection heuristics there:

- (a) unsubstantiated efficacy claim
- (b) borrowed-authority language substituting for evidence
- (c) urgency/fear exploitation stacked on an unsubstantiated claim
- (d) category-inappropriate absolute-certainty language

Three boundary rules the reference file's heuristics encode in full detail —
apply all of them before flagging anything, and use the compact mechanical
tests below as the first pass:

- **Named source defeats (a)/(b).** A specific, checkable study, trial,
  organization, or data source named in or beside the claim defeats (a) and
  (b) for that claim, regardless of how clinical the surrounding language
  sounds. A source-to-claim mismatch is a real substantiation gap — write it
  into the defect detail as prose, don't force it into a pattern flag.
- **Bounded first-person experience is 255.2 territory, not (a)/(d) — unless
  it makes a comparative/superlative exceptionalism claim.** "For me, X held
  up all week" or "I noticed less redness after a few days" is a personal
  account, not a pattern flag. But a first-person statement that asserts the
  product is unprecedented or unmatched ("I've never seen anything work this
  fast," "nothing else has ever done this for me") functions as an absolute/
  superlative claim despite the first-person frame — evaluate it under (d)
  like any other superlative claim (see the (d) test below), it is not
  shielded by the personal-account carve-out.
- **Puffery is not a pattern flag.** Hyperbolic, non-literal brand-voice
  language that no reasonable consumer would read as a specific, testable
  factual claim (vague superlatives, playful wordplay like a string of
  "-proof" adjectives describing feel, vibe, mood, or comfort rather than a
  measurable outcome) is not flagged under (a) or (d). This is distinct from
  a genuine function/mechanism claim (kills germs, eliminates odor, reduces
  inflammation), which is still evaluated normally.

**Mechanical (d) test — apply both parts:** (d) fires only when the claim
(i) contains a literal certainty/completeness word (proven, guaranteed/
guarantee, cures/cure, 100%, always works) OR an explicit superlative/
exceptionalism assertion (the most effective, nothing works better, I've
never seen anything work this fast, unmatched, like nothing else), AND (ii)
is applied to a health, financial, legal, or safety outcome. A plain
function/mechanism verb (eliminates, kills, removes, stops, reduces) or a
specific quantified number (kills 99.9% of germs) is NOT sufficient by
itself to flag (d) — it must co-occur with (i). A household or cosmetic
product's "eliminates odors on contact" is the canonical NOT-FLAGGED example:
strong function claim, no certainty/superlative word, no health/financial/
legal/safety framing.

Mark each pattern FLAGGED or NOT FLAGGED. For every FLAGGED pattern, quote
the submitted content (never the reference file's illustrative FTC quotes). A
single claim can trip more than one pattern — flag all that apply.

### Step 6 — Build the one coverage table

Emit exactly one table, in this fixed row order (skip rows for elements that
were NOT TRIGGERED in Step 2 — they're already covered in the header line):
255.0, 255.1-honest-opinion, 255.1-substantiation, 255.2, 255.3, 255.4, 255.5,
255.6.

Columns: `Element | Status | Citation | Defect / Substantiation Detail`.

- **Citation** — the 16 CFR 255.x subsection plus, where useful, a direct
  quote pulled from `references/16-cfr-255-elements.md`'s quotable line for
  that element, tagged "(FTC Endorsement Guides, 16 CFR Part 255, public
  domain, 17 U.S.C. § 105)". Never cite a subsection this file doesn't cover
  — fall back to the bare section number rather than fabricating a quote.
- **Defect / Substantiation Detail** —
  - PRESENT: one short clause on why (e.g. "genuine first-hand account, no
    typicality claim made").
  - ABSENT/DEFICIENT: the specific defect, quoting or closely paraphrasing
    the spot in the submitted content that shows the gap. If nothing in the
    content addresses the element at all, write "no text in the submitted
    content addresses this element." Prefix with a severity tag per Step 4
    rule 7.
  - For 255.1-substantiation rows with an efficacy claim present, append the
    four-pattern breakdown inline: `(a) {FLAGGED/NOT FLAGGED}{: "quote" if
    flagged}; (b) ...; (c) ...; (d) ...`.

### Step 7 — Assemble and emit the full report

Emit the report below in full, every time, verbatim in structure. Fill every
`{curly_brace}` placeholder with real content. This report — header, table,
totals line, disclaimer — is the entire deliverable. Never summarize it into
prose, never truncate the table, and never say the report is "above" or
"included below" instead of actually emitting it in this response.

## Hard rules

- **No angle-bracket placeholders, ever.** Never emit an angle-bracket
  placeholder token (an opening angle bracket, placeholder name, closing
  angle bracket) anywhere in report text. Placeholders exist only as
  `{curly_brace}` tokens in this file's own template — fill every one with
  real content before the report ships. If source material contains an
  angle-bracket placeholder, convert it to curly braces or plain prose
  before it lands in the report; never pass it through verbatim.
- **No private paths, no build filenames, no build narrative.** Cite only
  public source titles — "Guides Concerning the Use of Endorsements and
  Testimonials in Advertising, 16 CFR Part 255" (Federal Trade Commission)
  and "In the Matter of Marc Ching, individually and d/b/a Whole Leaf
  Organics — FTC Docket No. 9394, Administrative Part III Complaint"
  (Federal Trade Commission). Never surface an internal filename, file path,
  or note about how this skill pack was assembled.
- **No verdict language.** Never write "compliant," "non-compliant," "this
  passes," "this violates the law," or any sentence that reads as a legal
  conclusion. Status values are PRESENT / ABSENT / DEFICIENT only.
- **The table is the deliverable.** Always emit it in full. A meta-description
  of what the table would contain is not a substitute for the table.

## Output template

```
## Advertising Claims & Endorsement Review — Element Coverage Report

- content_type: {content_type}
- jurisdiction_note: {jurisdiction_note — omit this line entirely if jurisdiction_confirmation was true and no non-US signal was found}
- grounding: FTC Endorsement Guides (16 CFR Part 255, current version) and FTC Matter No. 9394 Administrative Complaint (In the Matter of Marc Ching / Whole Leaf Organics) — both public-domain US federal sources, retrieved {retrieval_date}.
- trigger determination: 255.2 {TRIGGERED/NOT TRIGGERED} ({reason}); 255.3 {TRIGGERED/NOT TRIGGERED} ({reason}); 255.4 {TRIGGERED/NOT TRIGGERED} ({reason}); 255.5 {TRIGGERED/NOT TRIGGERED} ({reason}). 255.0, 255.1-honest-opinion, 255.1-substantiation, 255.6 always evaluated.

| Element | Status | Citation | Defect / Substantiation Detail |
|---|---|---|---|
| 255.0 | {status} | 16 CFR 255.0{ — "quote" if used} | {detail} |
| 255.1-honest-opinion | {status} | 16 CFR 255.1{ — "quote" if used} | {detail} |
| 255.1-substantiation | {status} | 16 CFR 255.1{ — "quote" if used} | {detail}{; (a) ...; (b) ...; (c) ...; (d) ... if an efficacy claim is present} |
| 255.2 | {status, only if triggered} | 16 CFR 255.2{ — "quote" if used} | {detail} |
| 255.3 | {status, only if triggered} | 16 CFR 255.3{ — "quote" if used} | {detail} |
| 255.4 | {status, only if triggered} | 16 CFR 255.4{ — "quote" if used} | {detail} |
| 255.5 | {status, only if triggered} | 16 CFR 255.5{ — "quote" if used} | {detail} |
| 255.6 | {status} | 16 CFR 255.6{ — "quote" if used} | {detail} |

{n} PRESENT, {n} ABSENT, {n} DEFICIENT of {n} applicable elements.

This report checks the submitted content against the enumerated requirements in 16 CFR Part 255 and the FTC Act Section 5 substantiation duty the Guides interpret. It reports element-by-element PRESENT / ABSENT / DEFICIENT coverage. It does not constitute legal advice and is not a compliance or non-compliance determination — route any ABSENT or DEFICIENT finding through counsel before publishing or relying on this report.
```

(Omit table rows for any 255.2/255.3/255.4/255.5 element that was NOT
TRIGGERED — the trigger-determination line already accounts for it. Never
leave a `{status}` placeholder unfilled or add an extra row for a
not-triggered element.)

## Notes on scope

- This skill checks coverage of the Endorsement Guides only. It does not
  check general FTC Act Section 5 deceptive-advertising issues unrelated to
  endorsements (pricing claims, "free" offer rules, native-advertising
  labeling outside an endorsement context, COPPA, CAN-SPAM, etc.) — those are
  out of scope and should not be silently folded into a 255.x finding.
- If the submitted content contains multiple distinct endorsements (e.g.
  three influencer posts, or a testimonial page plus an expert-quote
  sidebar), either run one report covering all of them with defect details
  that specify which piece each finding refers to, or run separate reports
  per piece — pick whichever keeps defect detail unambiguous, and say which
  approach was used in the header.
- Always finish with the disclaimer language exactly as specified — do not
  paraphrase it, do not drop it, and do not add "compliant"/"non-compliant"
  language anywhere else in the report.
