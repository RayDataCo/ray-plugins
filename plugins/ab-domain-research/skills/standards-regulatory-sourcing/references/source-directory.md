# Source directory — standards / regulatory issuers by domain

Canonical primary-text access points. Always search/fetch from these directly — never from
an aggregator or mirror site layered on top.

| Domain | Regime / instrument | Primary repository (T1) |
|---|---|---|
| Privacy / data protection (EU) | GDPR (Regulation (EU) 2016/679) | eur-lex.europa.eu |
| Privacy / data protection (US state) | CCPA/CPRA and other state privacy acts | Official state legislature site (e.g. leginfo.legislature.ca.gov) and the implementing agency where one exists (e.g. cppa.ca.gov for CCPA regulations) |
| Privacy / data protection (US federal sectoral) | HIPAA, GLBA, COPPA | ecfr.gov (Code of Federal Regulations), govinfo.gov |
| Financial reporting (US GAAP) | FASB Accounting Standards Codification | asc.fasb.org (free Basic View) |
| Financial reporting (international) | IFRS standards | ifrs.org (registration required for unaccompanied standards) |
| Securities disclosure | Securities Act / Exchange Act rules, Reg S-K/S-X | ecfr.gov, sec.gov/rules (including proposed rules — land these as INCLUDE/context-only per SKILL.md section 6, never as enumerated requirements) |
| Information security | NIST SP 800-series, CSF, AI RMF | nist.gov/publications, csrc.nist.gov |
| AI governance | NIST AI RMF; EU AI Act (Regulation (EU) 2024/1689) | nist.gov/itl/ai-risk-management-framework; eur-lex.europa.eu — two distinct regimes, never blended into one landing plan |
| Safety / quality management | ISO 9001, ISO/IEC 27001, ISO 31000, ANSI/ASSP standards (e.g. Z359.1) | iso.org, ansi.org / webstore.ansi.org (paywalled — POINTER-ONLY per the T1-no-open-substitute carve-out) |
| Workplace safety (US) | 29 CFR 1910 (OSHA General Industry Standards) | osha.gov, ecfr.gov |
| Food safety (US) | FSMA rules under 21 CFR (e.g. Part 117 Preventive Controls, Part 1 Subpart S Traceability) | fda.gov, ecfr.gov — check for compliance-date amendments before locking `version_or_date` |
| International food standards | Codex Alimentarius and equivalent international standard-setting councils | The council's own publication page; treat as its own `jurisdiction` bucket, distinct from any single country's regime |
| Web standards | HTML, CSS, WCAG, W3C Recommendations and Working Group Notes | w3.org/TR — a narrow-scope WG Note is still in-domain for a broader web-standards fill (boundary rule 7), not off-domain |
| Government analysis / oversight | GAO reports | gao.gov — T2, in-domain wherever the specific report's subject matches the current fill (boundary rule 8), not scoped to any one row in this table |
| Government analysis / oversight | CRS reports | crsreports.congress.gov — same cross-domain rule as GAO |
| Case law (any domain) | Court opinions interpreting a statute/regulation | Official court reporter or courtlistener.com (public-domain opinion text; CourtListener is a repository, not the authority — cite the court as publisher) |
| General federal regulatory text | Any CFR title | ecfr.gov (electronic, continuously updated) or govinfo.gov (official, dated PDF) |
| General federal statutory text | Any U.S.C. title | uscode.house.gov |

## Off-domain vs on-topic-but-narrow — telling them apart

A source can be T1, public-domain, and current, and still be the wrong pick:

- **Off-domain** (boundary rule 7, EXCLUDE): the source is authoritative but about a
  genuinely different subject than the fill domain — e.g. an FDA medical-device
  quality-system regulation (21 CFR Part 820) surfacing in an AI-risk-management bundle, or
  an EPA hazardous-waste regulation (40 CFR Part 261) surfacing in a food-safety bundle.
  Strong authority does not rescue a source about the wrong subject.
- **On-topic-but-narrow** (boundary rule 7, INCLUDE with scope noted): the source is
  authoritative and IS about the fill domain, just a subtopic of it — e.g. a WG Note on one
  narrow technical mechanism within a broader web-standards fill, or a syllabus subsection
  within a broader professional-discipline fill. Note the narrow scope in the landing plan's
  `## Scope / applicability` section; do not exclude.

When in doubt, ask: does this instrument regulate/define the fill domain's actual subject
matter (even a slice of it), or a different subject matter entirely that happens to share an
issuer, era, or adjacent keyword? The former is on-topic-but-narrow; the latter is
off-domain.

## Known aggregator / secondary traps to route around

These are T3 at best — usable only as a pointer trail toward the primary instrument above.
Per boundary rule 2, a reputable one of these is `POINTER-ONLY`, never `EXCLUDE:
not-authoritative` — that reason class is reserved for the untiered tier below:

- Law-firm client alerts and "what you need to know about [regulation]" explainers
- Compliance-vendor blogs and marketing pages
- Wikipedia-style summaries of a statute (fine for orientation, not for citation)
- Subscription newsletters/blogs discussing a regulation, even when the first few paragraphs
  are free — POINTER-ONLY if reputable, independently capped there by paywalled/undetermined
  terms too (both grounds point the same direction, no need to pick one)

**Untiered** (EXCLUDE: not-authoritative, never POINTER-ONLY — boundary rule 1), regardless
of how comprehensive, well-ranked, or "trusted by N professionals" the framing claims to be:

- Prep-course / exam-dump / certification-prep vendor pages that restate regulatory content
  as flashcards or study guides, even ones that borrow a real standard's name in their title
- Content farms and SEO listicles
- Any site that reproduces "the full text of [regulation]" without being the issuing body —
  verify against the primary repository even when the mirror looks complete; mirrors drift
  out of date silently when a regulation is amended, and an out-of-date mirror is
  `stale-superseded` (the more specific, decisive reason — boundary rule 6) rather than a
  generic `not-authoritative`, when the mirror's specific claim has gone stale

## Jurisdiction discipline reminder

When the same topic spans regimes (e.g. privacy: GDPR vs CCPA vs a third state's act; AI
governance: NIST AI RMF vs the EU AI Act vs a technical standard like a W3C note), resolve
each candidate to exactly one issuer/regime/instrument row above. Never build a landing plan
that blends citations across regimes or instruments — one landing plan per `jurisdiction`,
including distinct technical-standard instruments that aren't legal jurisdictions in the
geographic sense.
