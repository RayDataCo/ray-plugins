# Canonical cert bodies by domain (T1 anchors)

Directory of the T1 credentialing/professional bodies this station sources from, and the
specific public artifact to look for per domain. Use this to set Authority Tier and to
decide whether a domain has a strong T1 anchor or should be flagged "weak/no anchor" in
the decision sheet's opening paragraph.

| Domain | Body | The public artifact to source |
|---|---|---|
| Management accounting / FP&A | IMA (Institute of Management Accountants) | CMA exam Content Specification Outline (2 parts, weighted sections) |
| Investment/finance | CFA Institute | CFA Program curriculum topic outlines / Candidate Body of Knowledge |
| Public accounting / audit | AICPA | CPA Exam Blueprints (published, section-by-section, with skill levels) |
| Treasury | AFP (Association for Financial Professionals) | CTP body of knowledge / exam domains |
| Project management | PMI | PMP Exam Content Outline (domains/tasks/enablers). Note: the PMBOK Guide itself is a copyrighted BOOK — outline facts only, restated. GAO reports on federal project/program management maturity are T2 and in-domain here (see "Government analytic bodies" below) — they supplement, never displace, PMI as T1 |
| Operations / quality | ASQ; ASCM (APICS) | ASQ certification Bodies of Knowledge (CQE, CSSBB); CPIM/CSCP Exam Content Manuals |
| HR | SHRM; HRCI | SHRM BASK (Body of Applied Skills and Knowledge); HRCI exam content outlines |
| Internal audit / risk | IIA | CIA exam syllabus. GAO's Government Auditing Standards ("Yellow Book") work is T2 and in-domain here |
| Marketing | AMA (PCM program); DMI | WEAK ANCHOR — marketing "certs" are largely methodology/vendor training. Tier honestly; expect this station to yield thinner competency for marketing (known calibration from the skill-grid work) |
| Legal (US) | NCBE; ABA | NCBE bar exam subject-matter outlines (MBE/MEE topics); ABA Model Rules are published but copyrighted — restate + cite |

## Authority tier definitions

- **T1** — the primary authority itself: the standard-setter, the credentialing body, the
  regulator, the filing repository, the court, the university publishing its own
  courseware.
- **T2** — recognized affiliated or peer institutions: official society journals,
  government analytic bodies (GAO/CRS), established OER publishers.
- **T3** — secondary commentary: law-firm client alerts, consultancy summaries,
  prep-course vendors, quality blogs. Usable as POINTERS to primary sources only — never
  as the basis the cellar records as authoritative, and never for oracle/exemplar content.
- **Untiered/SEO** — content farms, exam-dump sites, scraped aggregators. EXCLUDE always,
  never softened to POINTER-ONLY.

## Government analytic bodies travel across domains (T2, cross-domain)

GAO (Government Accountability Office) and CRS (Congressional Research Service) are T2
wherever the specific report's subject matches the requested domain — they are not tied to
one discipline the way a credentialing body is. Do not exclude a GAO/CRS report as
`not-authoritative` or `off-domain` just because GAO isn't "a body of this discipline";
judge it by whether ITS SUBJECT matches the fill domain. Worked example: a GAO report
assessing project-management maturity/practices across federal agencies is T2 and squarely
in-domain for a "project management" fill, sourced alongside PMI's PMP Exam Content
Outline — PMI remains T1, the GAO report supplements as T2, and both can be `INCLUDE`d with
their own landing blocks. The same logic applies to a GAO Yellow Book report for "internal
audit," a CRS report on regulatory capital for "public accounting," etc.

## Versioning trap

Cert bodies revise outlines on a cycle (CPA Blueprints revise regularly; PMP ECO changed
materially in 2021; CMA CSO in 2020). Always record the outline's own version/effective
year in `version_or_date`, and prefer the current version. An outdated outline that turns
up in search is `stale-superseded` unless deliberately landed as historical context.

## When the requested domain isn't in this table

The domain requested drives which bodies apply. For a domain with no strong credentialing
body — or one not listed above — say so honestly in the decision sheet rather than
promoting a weak or tangential source to T1. Reasoned analogy to a listed domain's
authority structure is acceptable (e.g. a foreign-jurisdiction equivalent of a body above),
but record the analogy explicitly in the rationale block's "Authority:" line.
