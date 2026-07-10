# Substantiation Defect Patterns — 255.1-substantiation Sub-Check

Source: Federal Trade Commission, "In the Matter of Marc Ching, individually and
d/b/a Whole Leaf Organics," FTC Docket No. 9394, Administrative Part III Complaint
(Complaint Counsel, on behalf of the Commission), filed 2020-04-27. Retrieved
2026-07-10. License: public domain, 17 U.S.C. § 105 — the complaint is a
government-authored enforcement document, not a privately filed exhibit; full text
may be excerpted and cited without restriction.

This is a counter-exemplar: real advertising copy the FTC itself alleged was
deceptive, quoted verbatim in its own complaint, naming exactly why each statement
failed the FTC Act's substantiation standard. Use it as a detector, not a template —
the illustrative quotes below show what each defect pattern looks like in the wild;
they are not the content being reviewed. When flagging a pattern against submitted
content, quote the submitted content itself, not these illustrative examples.

Run this sub-check against the 255.1-substantiation element whenever the submitted
content contains an efficacy, results, or outcome claim (health, financial,
performance, or otherwise) that has been correctly routed here — not a typicality/
aggregate-customer claim or a depicted endorser's own bounded personal account (see
16-cfr-255-elements.md's 255.2 status_decision_rule for the routing test). A single
claim can trip more than one pattern — flag every pattern that applies, don't force a
single-pattern read.

## Boundary rules — apply all three before flagging anything

These rules resolve the most common false positives and false negatives against the
four patterns below. Check all three before marking any pattern FLAGGED or NOT
FLAGGED.

1. **A named, checkable evidence source defeats (a) and (b), regardless of style.**
   If the content names a specific study, clinical trial, research organization, or
   data source — even inside otherwise promotional-sounding language ("backed by
   real science: an independent double-blind study conducted by [named
   organization]...") — that claim does NOT get flagged under (a) or (b). Naming a
   checkable source is exactly what those two patterns require and its absence is
   what they detect; once a source is named, the marketing tone around it doesn't
   revive the flag. If the named study doesn't actually measure what the adjacent
   claim asserts (a study-to-claim mismatch), that's a real substantiation gap —
   write it into the element's defect detail as prose, but do not force it into one
   of these four pattern flags; it isn't what patterns (a)/(b) are built to catch.
2. **First-person, non-generalized personal experience is not an (a) or (d) flag —
   unless it makes a comparative/superlative exceptionalism claim.** A statement
   phrased as one person's own sensory or experiential account — "for me, these have
   held up all week," "I noticed less redness after a few days" — without language
   asserting it as a general or objective fact, belongs to 255.2 (consumer
   endorsement / typicality) territory, not this sub-check. Only flag (a) or (d) when
   the claim is phrased as a general or objective assertion ("eliminates odors on
   contact," "proven to reduce inflammation," "the most effective..."), not when it's
   framed as "in my experience" or a first-person narrative with no claim that other
   people will see the same result. The one exception: a first-person statement that
   asserts the product is unprecedented, unmatched, or better than anything else the
   speaker has tried ("I've never seen a supplement work this fast," "nothing has
   ever done this for me") functions as an absolute/superlative claim in effect,
   regardless of its first-person grammar — it is not a bounded personal account of
   sensation or duration, it is a comparative-exceptionalism assertion about the
   product's performance. Evaluate that kind of statement under pattern (d) like any
   other superlative claim.
3. **Puffery — non-literal, non-testable brand-voice language — is not a pattern
   flag.** Hyperbolic marketing language that no reasonable consumer would read as a
   specific, measurable, factual claim is not flagged under (a) or (d), even when it
   uses strong or playful wording. This covers vague superlatives used as brand voice
   and wordplay built around a formula rather than a literal claim — for example, a
   string of "-proof" adjectives describing feel, vibe, mood, or comfort ("squat-
   proof, sweat-proof, mood-proof") is understood by consumers as stylized marketing
   personality, not a literal, testable guarantee against sweat or mood failure. This
   is distinct from a genuine function/mechanism claim about what the product
   objectively does (kills germs, eliminates odor, reduces inflammation, stops pain)
   — those remain evaluated normally under (a)/(b)/(d) regardless of how casually
   they're phrased; puffery is about claims with no literal, checkable content at
   all, not about tone.

## (a) Unsubstantiated efficacy claim — no stated competent/reliable evidence

- detection_heuristic: The content asserts an outcome or efficacy result (health,
  financial, performance) AS A GENERAL OR OBJECTIVE FACT, with no named study,
  clinical trial, data source, sample size, or methodology anywhere in the content
  or in a linked/cited source. Apply boundary rule 1 (named source defeats this),
  boundary rule 2 (first-person non-generalized accounts don't trigger this, except
  superlative-exceptionalism first-person claims), and boundary rule 3 (puffery
  doesn't trigger this) before flagging.
- illustrative_quote (from the complaint, not to be reused as content): "Our
  formulations have been proven to be effective at reducing inflammation, and
  minimizing the way cancer cells manipulate neighbor cells."
- why_it_fails: The FTC complaint alleges the respondent lacked the "competent and
  reliable scientific evidence" the FTC Act requires before making claims of this
  kind — asserting the result as fact without any evidence source named.

## (b) Borrowed-authority language substituting for evidence

- detection_heuristic: The content uses credibility-signaling phrases — "clinically
  tested," "clinically researched," "clinically proven," "practitioner formulated,"
  "doctor recommended," "has been shown to," "shown to," "studies show," "research
  shows," "clinically demonstrated," "backed by science/research" — with NO actual
  study, trial, or data source cited anywhere near the phrase. See boundary rule 1:
  if a real source is named nearby, this pattern is defeated even if the surrounding
  phrasing sounds clinical or borrows credibility markers stylistically. A phrase
  implying an unnamed evidentiary basis ("has been shown to stop symptoms in their
  tracks") is a (b) flag on its own even without an explicit "clinically" token —
  the test is whether the phrasing implies evidence exists without naming it, not
  whether one specific word from this list appears verbatim.
- illustrative_quote: "practitioner formulated, and clinically tested cannabinoid
  nutraceutical line" / "Backed by scientific research and formulation, CBD Max
  delivers concentrated active CBD..."
- why_it_fails: The pseudo-clinical register does the persuasive work a real,
  named evidence citation should be doing — it borrows the credibility of "clinical"
  or "scientific" language without attaching anything a reader could verify.

## (c) Urgency/fear exploitation stacked on an unsubstantiated claim

- detection_heuristic: The content pairs an unsubstantiated claim (pattern (a) or
  (b)) with acute fear or urgency framing — a named disease outbreak, health crisis,
  "before it's too late" language, or exploitation of a live public-health or
  personal-safety fear.
- illustrative_quote: "Formulated with potent antiviral herbal extracts... the
  perfect way to strengthen your immunity against pathogens like, 'COVID-19,' THE
  CORONAVIRUS."
- why_it_fails: Naming an active public-health emergency compounds the
  substantiation defect with exploitation of acute consumer fear — flag this even
  when the base efficacy claim looks otherwise mild, since the fear-stacking is the
  aggravating factor.

## (d) Category-inappropriate absolute-certainty language

- detection_heuristic: Flag only when BOTH conditions hold together: (1) the content
  contains EITHER a literal certainty/completeness word — "proven," "guaranteed" /
  "guarantee," "cures" / "cure," "100%," "always works" — OR an explicit superlative/
  exceptionalism assertion of best-in-class or unprecedented performance — "the most
  effective," "nothing works better," "I've never seen anything work this fast,"
  "unmatched," "like nothing else" — AND (2) that language is applied to a claim
  category where absolute certainty is not realistically substantiable (health,
  financial, legal, or safety outcomes). A plain function/mechanism verb by itself
  ("eliminates," "kills," "removes," "stops," "reduces") or a specific quantified
  number that isn't the literal token "100%" ("kills 99.9% of germs") does NOT
  satisfy condition (1) on its own — it must co-occur with one of the certainty/
  superlative tokens above to flag (d). A strong or confident-sounding functional
  claim in a low-stakes category — e.g. a household or cosmetic product's
  "eliminates odors on contact" — is a mechanism/function claim, not a (d) flag,
  because it satisfies neither condition (1)'s token list nor, typically, condition
  (2)'s category test. See boundary rule 2: a bounded first-person personal account
  is not a (d) flag, but a first-person superlative-exceptionalism claim ("I've
  never seen it work this fast") IS evaluated under (d) despite its grammar. See
  boundary rule 3: puffery/wordplay with no literal testable content is not a (d)
  flag regardless of category.
- illustrative_quote: "combines the most effective cancer and immune regulating
  clinically tested components into one simple supplement" / "proven to be
  effective at reducing inflammation"
- why_it_fails: This is a claim-strength defect independent of the substantiation
  defect — even a well-substantiated result rarely supports absolute-certainty or
  unprecedented-performance phrasing in a health, financial, legal, or safety
  category; flag it on its own even if patterns (a) and (b) are NOT FLAGGED.

## Disposition note (context, not a template)

The underlying matter resolved via a consent Agreement Containing Consent Order
(filed 2020-07-10) and a final Decision and Order (issued 2020-10-19) barring the
COVID-19 and cancer-treatment/prevention claims; the respondent neither admitted nor
denied the complaint's allegations, per standard FTC consent-order practice. This
disposition detail is background only — it is not part of the four detection
patterns and should not be cited as if it were a 16 CFR 255 requirement.
