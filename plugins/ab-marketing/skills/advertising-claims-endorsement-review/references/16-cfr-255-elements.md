# 16 CFR Part 255 — Endorsement Guides, Enumerated Elements

Source: Federal Trade Commission, "Guides Concerning the Use of Endorsements and
Testimonials in Advertising," 16 CFR Part 255 (eCFR), current version reflecting the
2023 revision (Federal Register July 26, 2023), codified 2024. Also includes the
related "Trade Regulation Rule on the Use of Consumer Reviews and Testimonials," 16
CFR Part 465 (finalized 2024) — a separate rule, cross-referenced here because its
subject matter (fake/incentivized reviews, review-management intermediaries) is
adjacent to Part 255. Retrieved 2026-07-10. License: public domain, 17 U.S.C. § 105
— US federal government work, full text excerptable with citation, no restriction to
record.

Each element below carries a plain-language `requirement_summary` (safe to restate
freely), a `paraphrase (verified against eCFR; not verbatim regulatory text)` field
(safe to restate — not quote — in a report's `citation` field, tagged "public domain,
17 U.S.C. § 105"), and — where the element is easy to mis-score — a
`status_decision_rule` spelling out exactly when it is PRESENT vs. ABSENT vs.
DEFICIENT vs. NOT APPLICABLE (not-triggered). Do not invent additional 16 CFR 255 or
16 CFR 465 language beyond what's here — if a report needs a citation this file
doesn't cover, fall back to the general section reference (e.g. "16 CFR 255") without
a quote rather than fabricating one.

## 255.0 — Definitions (always evaluated)

- requirement_summary: Establishes what counts as an "endorsement" (any advertising
  message consumers would likely believe reflects a non-advertiser's genuine opinion,
  belief, finding, or experience — this includes verbal statements, demonstrations,
  and depictions of trade or brand names, not just explicit spoken testimonials) and
  what counts as a "material connection" (any business, family, or personal
  relationship, or free/discounted product or service, that might materially affect
  the weight or credibility consumers give the endorsement and that consumers would
  not reasonably expect).
- status_decision_rule: This is a definitions element, not an independent content
  obligation — the submitted content does not "do" anything to satisfy or fail it on
  its own terms; it simply supplies the definitions the rest of the review applies.
  **Default to PRESENT in virtually every review**, with a one-line note that the
  endorsement/material-connection definitions apply to the content as evaluated in
  the rest of the table. Reserve DEFICIENT/ABSENT for the rare case where the
  content's own framing actively defeats the definitional concepts themselves (e.g.
  content that relabels an obviously sponsored placement as organic in a way that
  undermines what "endorsement" even means for the rest of the review) — this should
  be uncommon; do not mark this element DEFICIENT merely because other elements in
  the report have defects.
- paraphrase (verified against eCFR; not verbatim regulatory text): "Defines 'endorsement' (any advertising message consumers are likely
  to believe reflects the opinions/experience of a party other than the advertiser)
  and 'material connection' (any relationship that might materially affect the
  weight/credibility of the endorsement and would not reasonably be expected by
  consumers)"
- citation: 16 CFR 255.0

## 255.1-honest-opinion — Honest-opinion / no-indirect-deception duty (always
evaluated)

- requirement_summary: An endorsement has to reflect the endorser's actual, honestly
  held opinion, finding, belief, or experience. It cannot say anything through the
  endorser that would be deceptive, or that could not be substantiated, if the
  advertiser said it directly in its own voice.
- status_decision_rule: This element checks whether the opinion itself is genuine —
  never whether the efficacy claim inside it is well-substantiated (that is
  255.1-substantiation's job, even when the shaky claim is phrased as a first-person
  quote). Casual, enthusiastic, or informal phrasing ("this stuff is amazing,"
  "obsessed with it," no hedging language) is ordinary genuine-opinion phrasing, not
  evidence of fabrication — never mark DEFICIENT for tone or lack of hedging alone,
  and never import a weak-substantiation or unproven-efficacy concern into this
  element just because it appears inside an endorser's quote. Mark this element
  DEFICIENT or ABSENT only when the content shows actual, concrete evidence the
  opinion is fabricated, scripted, or coerced (e.g. a brief instructing an endorser
  to say something they haven't experienced, or language revealing the "endorser"
  never used the product). Absent that concrete evidence, default to PRESENT.
- paraphrase (verified against eCFR; not verbatim regulatory text): "An endorsement must reflect the honest opinions, findings, beliefs,
  or experience of the endorser; it may not contain any representation that would be
  deceptive (or could not be substantiated) if made directly by the advertiser"
- citation: 16 CFR 255.1

## 255.1-substantiation — Advertiser liability duty (always evaluated)

- requirement_summary: The advertiser carries liability for false or unsubstantiated
  statements delivered through an endorsement, and for any failure to disclose a
  material connection between itself and the endorser. Liability does not shift away
  from the advertiser just because an endorser said the words.
- status_decision_rule: If there is no efficacy, results, or outcome claim anywhere in
  the content, this element is ordinarily PRESENT (nothing to substantiate). When an
  efficacy claim IS present, first route it correctly before scoring: (1) if 255.5 is
  also triggered, 255.5 alone owns the connection-disclosure question — never re-score
  the same disclosure gap here; (2) if the claim is aggregate/typicality language
  ("many customers feel relief," "thousands of happy customers," "9 out of 10 users")
  or a specific depicted endorser's own bounded first-person account, that belongs to
  255.2, not here — see 255.2's status_decision_rule and substantiation-defect-
  patterns.md's boundary rules for the exact split; only claims phrased as the
  advertiser's own general/objective statement about what the product does are scored
  here. Once correctly routed, run the Step 5 four-pattern sub-check in
  substantiation-defect-patterns.md; mark DEFICIENT if any pattern is FLAGGED, PRESENT
  if all four are NOT FLAGGED.
- paraphrase (verified against eCFR; not verbatim regulatory text): "Advertisers are subject to liability for false or unsubstantiated
  statements made through endorsements, or for failing to disclose material
  connections between themselves and endorsers"
- citation: 16 CFR 255.1

## 255.2 — Consumer endorsements (triggered only when content depicts an actual
ordinary consumer's testimonial, named or anonymized — see status_decision_rule)

- requirement_summary: If an ad represents or implies that a consumer endorser's
  experience is typical of what other consumers can expect, the advertiser must
  either (a) have substantiation that the experience is in fact generally
  representative, or (b) clearly and conspicuously disclose what results consumers
  should generally expect in the depicted circumstances.
- status_decision_rule: **Trigger test** — this element requires an actual endorser
  (a specific consumer, named or anonymized) whose experience is being shown or
  quoted. A generic, population-level marketing statistic or claim phrased in the
  advertiser's own voice ("many customers feel relief within hours," "9 out of 10
  users agree"), with no depicted individual anywhere in the content, is NOT a
  consumer endorsement — mark 255.2 NOT TRIGGERED and evaluate that language (if it
  asserts an efficacy outcome) under 255.1-substantiation instead. **Status test once
  triggered** — the substantiate-or-disclose duty itself is conditional on an actual
  typicality representation: language implying other consumers get the same result
  ("you'll see this too," "most people notice...," an implied general promise). A
  single first-person account with no such generalizing language does not trigger
  that specific duty; mark PRESENT with a note that no typicality representation was
  made. If a typicality representation IS what triggered this element in the first
  place, the row can never say "PRESENT — no typicality representation was made" —
  that is self-contradictory; instead mark DEFICIENT unless the content actually
  substantiates the typical result or clearly and conspicuously discloses the
  generally-expected results. When the content depicts both an individual endorser's
  bounded personal account and separate aggregate/typicality language (e.g. a
  headline claim near a named testimonial), score the aggregate/typicality language
  here and leave the endorser's own bounded quote out of any substantiation-pattern
  flag (see substantiation-defect-patterns.md's first-person boundary rule).
- paraphrase (verified against eCFR; not verbatim regulatory text): "When an advertisement represents that an endorser's experience is
  typical, the advertiser must either have substantiation that the experience is
  generally representative or clearly and conspicuously disclose the generally
  expected results in the depicted circumstances"
- citation: 16 CFR 255.2

## 255.3 — Expert endorsements (triggered when content invokes a professional
credential or claimed expertise as the basis for an endorsement)

- requirement_summary: An endorser held out as an expert must actually possess the
  qualifications the ad represents, and the expert's evaluation of the product has to
  be conducted with the rigor that experts in that specific field would normally
  apply — a credential alone doesn't satisfy this if the underlying evaluation was
  cursory.
- status_decision_rule: A bare claim that a product was "tested" or "formulated" by
  unnamed professionals, with no description of the evaluation process, is a
  DEFICIENT attempt, not PRESENT (the credential is asserted without the rigor the
  Guide requires being shown) and not ABSENT (an attempt was made). Mark ABSENT only
  when the content contains no expert-credibility language addressing this element at
  all despite the trigger firing on some other basis. A phrase describing testing OF
  the product by a third party in generic terms (e.g. "dermatologist tested") without
  naming or depicting a specific expert endorsing the product is a testing/
  substantiation claim about the product, not a 255.3 expert endorsement — do not
  trigger 255.3 on that basis alone; route it to 255.1-substantiation instead.
- paraphrase (verified against eCFR; not verbatim regulatory text): "An expert endorser's qualifications must in fact give the expertise
  represented, and the expert's evaluation must be conducted with the same degree of
  rigor normally employed by experts in that field"
- citation: 16 CFR 255.3

## 255.4 — Organizational endorsements (triggered when an organization, association,
or institution — not an individual — is depicted as endorsing)

- requirement_summary: An endorsement attributed to an organization has to reflect
  that organization's actual collective judgment, reached through whatever process
  the organization normally uses to form positions — not the opinion of one member or
  employee dressed up as the organization's official view.
- status_decision_rule: For a finished piece, mark DEFICIENT (not ABSENT) when the
  content attributes an endorsement to an organization but says nothing about how
  that view reflects the organization's actual collective judgment. For brief/
  instruction-type content (a not-yet-published post), evaluate the brief's actual
  instructions, not a hypothetical finished post: if the brief instructs or implies
  that an organizational endorsement should appear (e.g. "mention that your gym
  recommends this") without any instruction addressing how that reflects the
  organization's collective judgment or normal decision process, that is an
  inadequate attempt — DEFICIENT, not ABSENT. Reserve ABSENT for content whose
  language never touches the organizational-endorsement question in any form despite
  the trigger firing.
- paraphrase (verified against eCFR; not verbatim regulatory text): "An organization's endorsement must reflect the collective judgment
  of the organization, arrived at through a process the organization normally
  follows"
- citation: 16 CFR 255.4

## 255.5 — Material connection disclosure (triggered by sponsored content, influencer
/ creator briefs, affiliate arrangements, gifted product, employment relationships,
or any other endorser-advertiser relationship a consumer would not already assume)

- requirement_summary: Any material connection between an endorser and the advertiser
  that consumers would not reasonably expect on their own — payment, free or
  discounted product, employment, a family relationship — must be disclosed fully,
  clearly, and conspicuously. The disclosure needs to be hard to miss, not
  technically present somewhere in the content.
- status_decision_rule: Mark ABSENT when a material connection is confirmed to exist
  (paid, gifted, affiliate, employment) and the content makes zero attempt at
  disclosure anywhere. Mark DEFICIENT when a disclosure attempt exists but isn't
  clear-and-conspicuous (buried in a hashtag pile, below a "see more" fold, ambiguous
  wording). If whether a connection exists at all is not confirmed by the review's
  inputs and the content itself doesn't resolve it, do not mark this ABSENT (that
  overclaims a violation the evidence doesn't support) or PRESENT (that overclaims
  compliance) — mark it DEFICIENT and say plainly that the fact was not provided and
  needs confirmation before publishing. Handle this as a single finding on this
  element — do not also raise the same open question under 255.1-substantiation or
  any other element.
- paraphrase (verified against eCFR; not verbatim regulatory text): "Any material connection between an endorser and the advertiser that
  consumers would not reasonably expect (e.g. payment, free product, employment,
  family relationship) must be fully disclosed"
- citation: 16 CFR 255.5

## 255.6 — Endorsements directed to children (triggered when the submitted content is
addressed to, or plainly targets, a child audience)

- requirement_summary: Endorsements used in advertising addressed to children may
  warrant special scrutiny. A practice that raises no concern when directed to adults
  can be unfair or deceptive when directed to children, because children may have a
  more limited ability to evaluate the persuasiveness of an endorsement or a
  representation's truthfulness.
- status_decision_rule: **Trigger test** — this element only applies when the
  submitted content is addressed to or plainly targets a child audience: a
  children's-product ad, an endorsement delivered by or featuring a child, a brief
  instructing content be posted to a channel or placement that plainly skews to a
  child audience. Content with no child-audience signal — the ordinary case — is NOT
  TRIGGERED; mark it NOT APPLICABLE and omit the row per Step 6, the same as any
  not-triggered 255.2-255.5 element. Never default this element to PRESENT for
  adult-directed content — "PRESENT" implies the element was evaluated and satisfied,
  which only makes sense once the child-audience trigger has actually fired. **Status
  test once triggered** — mark PRESENT when the content shows some accommodation for
  the heightened-scrutiny concern (nothing that exploits a child's limited ability to
  evaluate the endorsement or claim, no representation asked of a child endorser
  beyond a plausible genuine experience). Mark DEFICIENT when the content is
  child-directed and contains an endorsement, but nothing in it addresses the
  child-audience concern in any form — an attempt at the surrounding endorsement
  exists, the child-specific angle is simply never engaged. Mark ABSENT only when the
  content is child-directed, contains an endorsement, and shows zero engagement with
  the endorsement's suitability for a child audience.
- paraphrase (verified against eCFR; not verbatim regulatory text): "Advertising or promotional messages that are directed to children
  may need to be evaluated with special care, because a practice that would not
  ordinarily be questioned when applied to advertising directed to adults might be
  unfair or deceptive if directed to children"
- citation: 16 CFR 255.6

## 465 — Consumer reviews and testimonials (16 CFR Part 465, a separate rule from
Part 255; triggered when the submitted content involves consumer reviews, a review
platform, or an intermediary role in creating, procuring, or managing reviews)

- requirement_summary: The FTC's 2024 Trade Regulation Rule on the Use of Consumer
  Reviews and Testimonials (16 CFR Part 465) prohibits writing, selling, purchasing,
  or otherwise disseminating fake or false consumer reviews and testimonials, and
  prohibits an advertiser (or a company-controlled review venue) from suppressing
  genuine reviews or otherwise materially misrepresenting the balance of reviews for
  a product. It reaches intermediaries — ad agencies, PR firms, review brokers,
  reputation-management companies — who create, procure, buy, sell, or manage
  reviews on an advertiser's behalf, not just the advertiser itself.
- status_decision_rule: **Trigger test** — this element only applies when the content
  involves consumer reviews, a review platform, or a named/implied intermediary
  review-management role (an agency/broker/reputation-management vendor creating,
  buying, selling, filtering, or otherwise managing reviews; instructions to solicit,
  filter, or suppress reviews; any signal of an incentivized-but-undisclosed review
  program). Ordinary single-endorser testimonial or influencer content with no
  review-platform or intermediary angle does not trigger this element — mark NOT
  TRIGGERED and omit the row per Step 6. **Status test once triggered** — this
  element allocates liability across parties involved in review creation/management;
  it is not a content checklist the submitted material must affirmatively satisfy.
  Default to PRESENT unless the content itself shows a concrete instance of fake,
  purchased, or undisclosed-incentivized reviews, review suppression, or an
  intermediary orchestrating, instructing, or ignoring a deceptive or
  undisclosed-connection review — only then mark DEFICIENT/ABSENT, quoting the
  specific evidence. Do not mark this DEFICIENT merely because the content is silent
  on review-vetting practices (silence is the default state, not a defect), and do
  not mark it DEFICIENT merely because a separate 255.5 finding is ABSENT or
  DEFICIENT — an undisclosed connection scored under 255.5 is not, by itself,
  intermediary/review-conduct evidence for this element.
- paraphrase (verified against eCFR; not verbatim regulatory text): "Prohibits writing, selling, purchasing, or otherwise
  disseminating fake or false consumer reviews or testimonials, and prohibits an
  advertiser or a company-controlled review venue from suppressing genuine reviews or
  materially misrepresenting the overall balance of reviews; reaches intermediaries
  such as ad agencies, PR firms, review brokers, and reputation-management companies
  who create, procure, buy, sell, or manage reviews on an advertiser's behalf"
- citation: 16 CFR Part 465

## Trigger quick-reference

| Element | Fires when the content... |
|---|---|
| 255.2 | Depicts or quotes an actual ordinary consumer's own experience or results (named or anonymized). Population-level marketing statistics with no depicted individual do NOT fire this element. |
| 255.3 | Invokes a professional credential, title, or claimed expertise (doctor, scientist, practitioner, certified specialist, "expert-formulated") as the source of an endorsement — not a generic "[professional] tested" claim about the product with no depicted expert endorser. |
| 255.4 | Depicts an organization, association, or institution — not an individual — as endorsing, approving, or recommending the product |
| 255.5 | Is sponsored, gifted, paid, an influencer/creator brief, an affiliate arrangement, or otherwise involves a relationship between endorser and advertiser a consumer would not assume |
| 255.6 | Is addressed to or plainly targets a child audience — a children's-product ad, a child endorser, or a brief instructing posting to a clearly child-skewing channel/audience |
| 465 | Involves consumer reviews, a review platform, or a named/implied intermediary role (agency, PR firm, review broker, reputation-management company) creating, buying, selling, filtering, or managing reviews |

255.0, 255.1-honest-opinion, and 255.1-substantiation are never conditional —
evaluate them on every review regardless of what else triggers. 255.2, 255.3, 255.4,
255.5, 255.6, and 465 are all conditional on their trigger firing.
