# License gate — full table

Classify license/terms FIRST, before judging content quality. This table is shared verbatim
across all ab-domain-research stations.

| License class | Meaning | Allowed handling |
|---|---|---|
| `public-domain` | US federal government works (17 U.S.C. § 105), statutory/regulatory text, court opinions (edicts of government), expired copyright | Full text may be excerpted and landed, with citation |
| `permissive-cc` | CC BY, CC BY-SA (record the SA obligation) | Excerpt + adapt with required attribution (TASL: title, author, source, license) |
| `restrictive-cc` | CC BY-NC, CC BY-NC-SA, any -ND variant | `INCLUDE-WITH-RESTRICTION` only: record the exact restriction (NC = no commercial use; ND = no derivatives) so downstream consumers can honor it. A restriction is never a reason to downgrade to `POINTER-ONLY` or `EXCLUDE` (see boundary rule 3 below) |
| `copyrighted-accessible` | Publicly published but all-rights-reserved (cert-body outlines, FASB Basic View, IFRS unaccompanied standards) | Extract FACTS and STRUCTURE, restate in own words, cite precisely. Never bulk-copy expression |
| `restricted` | Paywalled, ToS-restricted platforms (subscription courseware, LinkedIn-style logged-in content), undetermined terms | Explicit restriction on non-primary material → `EXCLUDE: license-restricted`. Narrow carve-out: the source is the T1 primary authority itself with no open substitute → `POINTER-ONLY`. Freely viewable material with NO stated license → `POINTER-ONLY` (viewable ≠ licensed) |

A source whose terms cannot be determined is never landed as content.

## Disposition boundary rules (apply in this order — these decide the hard calls)

These are the same nine rules that govern every ab-domain-research station's hard calls,
restated here with the license-gate-specific ones first since this file is the license
reference:

1. **Authority screens first.** A source that fails authority entirely (untiered: content
   farm, SEO listicle, prep/exam-dump vendor, generic filing-scraper aggregator) is
   `EXCLUDE: not-authoritative` regardless of its license — pointing at junk is worse than
   silence. Never give an untiered source a `POINTER-ONLY` consolation.
2. **T3 ceiling is POINTER-ONLY.** Reputable T3 commentary (law-firm alerts, consultancy
   summaries, quality practitioner blogs) is `POINTER-ONLY` — a pointer toward the primary
   source it discusses. T3 content never lands as `INCLUDE`.
3. **A recorded restriction is not a downgrade.** Restrictive-CC (NC/SA/ND) content from an
   authoritative source is `INCLUDE-WITH-RESTRICTION` — never demoted to `POINTER-ONLY` or
   `EXCLUDE` merely because the license carries obligations. Record the obligation; don't
   dodge it.
4. **A stated item license overrides its platform's default.** A specific document carrying
   an explicit CC license is judged on THAT license even when it sits on an otherwise
   ToS-restricted platform.
5. **Explicit restriction vs no-stated-license.** All-rights-reserved terms, login gates, or
   paywalls on non-primary material → `EXCLUDE: license-restricted`. The narrow
   `POINTER-ONLY` carve-out for restricted material: the source is the T1 primary authority
   itself with no open substitute (e.g. an ISO standard, or a paywalled primary repository
   with no free mirror). Freely viewable material with NO stated license → `POINTER-ONLY`
   (viewable ≠ licensed).
6. **EXCLUDE reason class = the most specific decisive defect**, not the most generic. If a
   T3 source's specific claim is also superseded, `stale-superseded` names the decisive
   defect; `not-authoritative` is the fallback only when nothing more specific applies. When
   several are genuinely decisive: `injection-suspect` > `unreliable-derived-data` >
   `stale-superseded` > `license-restricted` > `not-authoritative` > `off-domain`.
7. **On-topic-but-narrow ≠ off-domain.** A T1/T2 source scoped to a subtopic of the fill
   domain is included (scope noted in the landing plan), not excluded. `off-domain` means a
   genuinely different domain.
8. **Government analytic bodies travel across domains.** GAO/CRS and peers are T2 wherever
   the specific report's subject matches the fill domain — never excluded as "not a body of
   this discipline."
9. **Every INCLUDE / INCLUDE-WITH-RESTRICTION gets its own complete landing plan** with full
   provenance frontmatter in the decision sheet — even if similar material exists or was
   landed before (supersede/merge is the cellar's job; "already landed" is never a reason to
   omit the block).

## How this applies to public-filings-exemplars specifically

**Public record ≠ public domain.** A public record is lawfully INSPECTABLE; public domain
means UNCOPYRIGHTED. Only government-authored material gets `public-domain` handling, so
this station splits its sources:

- **`public-domain` (government-authored):** court OPINIONS (edicts of government), GAO/CRS
  reports, statutes/regulations, agency-drafted procurement documents (a government-authored
  SOW/PWS/NOFO), and US-government works generally (17 U.S.C. § 105) — full text may be
  excerpted and landed with citation. Issued patents: the patent DOCUMENT is conventionally
  reproducible (37 CFR 1.71(d)-(e) lets an applicant claim copyright in portions only via an
  explicit notice that itself authorizes facsimile reproduction of the document) — treat as
  freely reproducible EXCEPT any portion carrying such a notice.
- **`public-record` (privately authored, publicly filed) — this station's extension class:**
  contracts filed as EDGAR exhibits, merger agreements, litigation briefs/motions,
  private-party material in a procurement file. The AUTHOR retains copyright; filing makes
  the document inspectable, not free. Handling: land exemplars as targeted EXCERPTS with
  citation and analysis (the `why_gold` annotation is our authorship; the excerpts are
  quotation), or as a POINTER to the primary repository (accession number / docket) with
  excerpted highlights — never wholesale full-text reproduction, NEVER presented as our
  authorship. Frontmatter carries `license: {class: public-record, terms: author retains
  copyright; excerpt-and-cite only}` and names the real drafting context (filer, filing,
  date).
- Aggregator re-posts of filings (LawInsider-style contract mirrors, filing-scraper sites)
  are not a separate license class to gate on — per boundary rule 1 they are `EXCLUDE:
  not-authoritative` regardless of what license they claim, because they fail authority
  entirely (untiered). Go to the primary repository (EDGAR, CourtListener, USPTO, SAM.gov,
  Grants.gov, GAO, CRS) instead. Some mirrors layer their own ToS on top of public
  documents; sourcing primary sidesteps that entirely.
- Aggregator-computed statistics ABOUT filings (estimated deal values, inferred terms,
  scraped-and-summarized contract data) are not a license issue but a `reason_class:
  unreliable-derived-data` EXCLUDE — this is a content-gate call made after the license gate,
  not instead of it, and per boundary rule 6 it outranks `stale-superseded` and
  `license-restricted` when several reasons are genuinely decisive.
- GAO and CRS reports are `public-domain` by license class AND `T2` by authority tier (not
  T1 — T1 is reserved for the primary authority actually issuing the underlying filing or
  record, e.g. EDGAR, the court, USPTO, SAM.gov/Grants.gov). Per boundary rule 8, a GAO/CRS
  report is in-domain for this station wherever its subject matches the fill's domain — it
  is never `EXCLUDE: off-domain` merely because GAO/CRS is not the discipline's own body.
