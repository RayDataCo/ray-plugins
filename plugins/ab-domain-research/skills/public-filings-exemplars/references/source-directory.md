# Source directory — public filings repositories

## SEC EDGAR

- **Full-text search**: `https://efts.sec.gov/LATEST/search-index?q=...` (JSON API); human UI
  at `https://www.sec.gov/edgar/search/`.
- **Filing indexes and documents**: addressable by accession number.
- **Company API**: `data.sec.gov`.
- **Authority tier**: T1 — EDGAR is the primary authority's own repository.
- **Coverage**: full-text search only reaches back to 2001; earlier material needs different
  access paths.
- **Fair-access rules**: declared User-Agent with contact info, stay well under 10
  requests/second, no bulk mirroring. A curated exemplar pull is a handful of documents,
  never a crawl.
- **What's gold here**:
  - EX-10 material agreements (employment, supply, license, credit) — legal drafting,
    commercial terms.
  - EX-2 merger agreements, EX-4 indentures — legal drafting.
  - 10-K MD&A sections, S-1 business/risk sections, proxy-statement Compensation Discussion
    & Analysis — finance/IR writing, risk analysis, executive communication.
- **Amendment check**: always check the filing index for 10-K/A, S-1/A, or other amendments
  before locking a candidate — an amended filing supersedes the original; landing the
  superseded version unknowingly is `stale-superseded` (disposition boundary rule 6 governs
  which reason class wins when a superseded filing is also lower-tier or otherwise flawed —
  `stale-superseded` names the decisive defect).
- **Redactions**: filed exhibits frequently carry Rule 24b-2 confidential-treatment
  redactions. Prefer lightly-redacted specimens over heavily-redacted ones and record where
  redactions fall in the exemplar frontmatter/body note.
- **Narrow-scope filings**: an exhibit scoped to a subtopic of the fill domain (e.g. a single
  supply agreement inside a broad "commercial contracts" task) is included, with the scope
  noted in the landing plan — not `EXCLUDE: off-domain` (boundary rule 7).

## SAM.gov (federal procurement)

- **Authority tier**: T1 — SAM.gov is the issuing platform.
- Real RFPs, Statements of Work (SOW), Performance Work Statements (PWS) attached to live or
  archived opportunities.
- Serves: sales/proposal-shaped work, project scoping, requirements writing.

## Grants.gov / agency Funding Opportunity Announcements (FOAs)

- **Authority tier**: T1 — Grants.gov and issuing agencies are the primary authority.
- Funding opportunity announcements and their evaluation criteria.
- Serves: proposal structure, evaluation-rubric design.

## CourtListener / RECAP

- **Authority tier**: T1 — the court that issued the opinion is the primary authority;
  CourtListener/RECAP is the primary public-access repository for the docket.
- Real briefs, motions, opinions from federal (and many state) court dockets.
- Serves: legal argument and memo drafting.
- Court opinions are `public-domain` (edicts of government); briefs/motions filed by private
  parties are public record but not government-authored — still land under `public-domain`
  handling per the filed-document rule, cited to the real drafting party.

## USPTO

- **Authority tier**: T1 — USPTO is the issuing authority.
- Issued patents — full text public.
- Serves: technical claim drafting, specification writing.

## GAO / CRS

- **Authority tier**: T2, not T1 — GAO and CRS are recognized government analytic bodies
  reporting ON matters, not the primary authority issuing the underlying filing or record
  being reported on. Per disposition boundary rule 8, T2 status travels across domains: a
  GAO or CRS report is in-domain for whatever fill domain its specific subject matches, and
  must never be excluded as `off-domain` or `not-authoritative` on the theory that GAO/CRS
  "isn't a body of this discipline."
- GAO reports and Congressional Research Service reports.
- Serves: gold analytic writing — findings-evidence-recommendation structure. GAO reports are
  explicitly named as the analytic-writing gold standard in this competency.
- License class: `public-domain` (US federal government works).

## What to avoid regardless of repository

- Aggregator/mirror sites (LawInsider-style contract databases, filing-scraper sites,
  exam-dump or SEO content farms around any of the above). These fail authority entirely
  (untiered) — per disposition boundary rule 1 they are always `EXCLUDE: not-authoritative`,
  never a `POINTER-ONLY` consolation. Source primary instead.
- Reputable secondary commentary about a filing (law-firm client alerts, consultancy
  summaries, quality practitioner blogs) is T3, not untiered — per boundary rule 2 it is
  `POINTER-ONLY` (a pointer to the primary filing it discusses), not `EXCLUDE:
  not-authoritative`. Never land T3 commentary as exemplar content.
- Derived/estimated data laid on top of a real filing (estimated deal size, inferred terms)
  — `EXCLUDE: unreliable-derived-data`; land the document itself, not someone's model of it.
  Per boundary rule 6, `unreliable-derived-data` outranks `stale-superseded` and
  `license-restricted` when a source is flawed on multiple grounds at once.
