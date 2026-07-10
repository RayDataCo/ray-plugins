# ab-domain-research — Menu

**Status:** live · 6 stations shipped (eval-proven, residual weaknesses named below) ·
**fills a cellar with domain competency + gold exemplars — curation, never bulk
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
| Source GOLD EXEMPLARS for CREATIVE/subjective domains (marketing, advertising, design, PR, digital/UX) from juried award libraries (Effie, Cannes Lions, D&AD, IPA) and published case studies — award metadata as `why_gold`, entrant-reported results tagged | `award-case-study-exemplars` | **win +0.60**: base 1/5 → skill 4/5. The one miss was the hardest license-boundary-precision fixture (public abstract vs gated databank; INCLUDE vs INCLUDE-WITH-RESTRICTION labeling) — both arms failed the same sources; residual named in evals/ |

## The freshness watch (live, eval-proven)

| When the situation is… | Route to | Eval headline (per-element bar) |
|---|---|---|
| Re-verify landed grounding against PRIMARY sources — weekly cron, before a client-facing tasting/deployment, or "is our cellar grounding stale?" / "what needs a refire?" | `freshness-watch` | **win +48pts**: base 51% → skill **99% per-element** (strict 4/5) on fixtures covering moved/superseded/unverifiable/provenance-gap boundaries, redirect-vs-moved, injection handling, and action-routing. Detect-and-route only — it never lands new content |

This station owns EVAL-SPEC's third regression trigger (world change): a moved or
superseded source flags every downstream skill and oracle and routes factory refire
tickets. Verification is PRIMARY-source-only — a cellar "verified" stamp is a claim,
not a fact.

## Per-domain growth note

`award-case-study-exemplars` ships with the marketing/advertising source set (Effie,
Cannes Lions, D&AD, One Show, Clio, IPA) plus PR (SABRE) and digital/UX (Webby, Awwwards)
extensions; its source directory grows per domain as fills demand — the discipline
transfers unchanged.

## Where fills land

- Methodology/competency: `$CELLAR_ROOT/competencies/<domain>/`
- Gold exemplars: `$CELLAR_ROOT/competencies/<domain>/exemplars/`
- Every run: `SOURCING-DECISIONS-<date>.md` beside its artifacts — the full per-candidate
  decision sheet. `CELLAR_ROOT` unset → the brigade serves in-answer (mise WARNs).

## The tasting

A packaged soft opening lives in [tasting/](tasting/): retired eval fixtures (input +
expected coverage/rubric + grading), run by the expo in YOUR environment after mise —
the same machinery and the same bar the eval evidence reports. See tasting/README.md
for which stations have plates.

## Out of scope

Company-centric research (jobs/filings/GitHub about a COMPANY) → that is a
company-research brigade's job, not this one. Skill building itself → the factory
(`ab-skill-factory`); this brigade only supplies the competency + exemplars a skill build
consumes. Bulk mirroring of any corpus → refused by the curation discipline.
