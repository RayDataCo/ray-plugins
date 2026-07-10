# ab-domain-research — Menu

**Status:** live · 4 stations shipped (eval-proven, residual weaknesses named below) · 1
planned · **fills a cellar with domain competency + gold exemplars — curation, never bulk
scraping**

This is the packaged menu (source of truth, versioned with the plugin). It is the
**station roster** the [expo](skills/expo/) reads to decompose a domain-fill order, select
which sourcing stations to fire, and compose their outputs into one fill. Every live
station shipped with two-arm execution-eval evidence (see `evals/`).

This is a **fill brigade** (kitchen kind, domain-centric analog of a company-research
brigade): its stations PRODUCE cellar artifacts from external public sources under a
strict curation discipline — license gate before content, authority tiering (T1/T2/T3),
per-source dispositions (`INCLUDE / INCLUDE-WITH-RESTRICTION / POINTER-ONLY / EXCLUDE` with
reason classes), provenance frontmatter on everything, fetched content treated as untrusted
data. Its purpose: give the skill factory what it needs to build and eval GENERATIVE
skills — competency notes ground the spec, **gold exemplars are what the tests station
grades generative output against**.

Brigade surface: `mise` (readiness gate, incl. the `CELLAR_ROOT` landing-target check) →
`service` (on/off) → `expo` (composes the stations below). A single-station request routes
to one; a full domain fill fires every station whose source class the domain offers.

## Route to a station (live, eval-proven)

| When the situation is… | Route to | Eval headline (strict all-source set-match, sonnet) |
|---|---|---|
| Source a domain's competency STRUCTURE (topic outlines, exam content specs, bodies of knowledge, weightings) from its credentialing/professional bodies | `cert-body-sourcing` | **win +0.60** both rounds: base 0/5 → skill 3/5. Residuals named: restrictive-CC material from authoritative-but-non-canonical bodies still gets demoted to POINTER-ONLY; landing blocks must be emitted in full, not asserted |
| Source the CHECKABLE-STANDARD layer — statutes, regulations, official standards, with enumerated cited requirements and version/effective dates | `standards-regulatory-sourcing` | **win +1.00** (round 2): base 0/5 → skill 5/5, all five trap fixtures (injection, license, staleness, off-domain, reason-class precision). Round-1 gaps fixed by the §4b disposition-boundary rules |
| Source methodology from open courseware / OER under the CC-licensed-only hard gate (TASL attribution, NC/SA restrictions recorded) | `academic-ocw-sourcing` | **win +0.60** (round 2, up from +0.20): base 0/5 → skill 3/5. One miss sits on a self-contradictory fixture key (logged in evals/ — under the oracle's own summary line it is a pass). Residual: SA-only stated licenses can get labeled plain INCLUDE instead of INCLUDE-WITH-RESTRICTION |
| Source GOLD EXEMPLARS — real professional work product from public filings and public records (EDGAR exhibits/MD&A, SAM.gov RFP/SOWs, court briefs, patents, GAO/CRS reports) with `why_gold` on every exemplar | `public-filings-exemplars` | **win +0.40–0.60 across two rounds**: base 0/10 → skill 5/10 total; every round-2 miss was a single source on a 6-source strict fixture (per-source ≥5/6), same named boundary-judgment family. Weakest evidence on the roster — flagged honestly; evidence detail in evals/ |

## Planned (not live — do not improvise a substitute)

- **award-case-study-exemplars** — published gold exemplars for creative domains
  (advertising/marketing award libraries, agency case studies). Deferred per the build
  spec: added per-domain, later. Until it ships, creative-domain exemplar requests get
  `partial-with-gaps` from the expo, with `public-filings-exemplars` covering what public
  records can (real marketing-adjacent artifacts: S-1 business sections, proxy CD&A).

## Where fills land

- Methodology/competency: `$CELLAR_ROOT/competencies/<domain>/`
- Gold exemplars: `$CELLAR_ROOT/competencies/<domain>/exemplars/`
- Every run: `SOURCING-DECISIONS-<date>.md` beside its artifacts — the full per-candidate
  decision sheet. `CELLAR_ROOT` unset → the brigade serves in-answer (mise WARNs).

## Out of scope

Company-centric research (jobs/filings/GitHub about a COMPANY) → that is a
company-research brigade's job, not this one. Skill building itself → the factory
(`ab-skill-factory`); this brigade only supplies the competency + exemplars a skill build
consumes. Bulk mirroring of any corpus → refused by the curation discipline.
