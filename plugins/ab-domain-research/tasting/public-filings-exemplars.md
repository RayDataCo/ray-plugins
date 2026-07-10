# Tasting — public-filings-exemplars

*A retired eval fixture, deliberately spent for demonstration (see the factory's
EVAL-SPEC): run the `public-filings-exemplars` station on the input below in YOUR environment (mise first),
then compare against the expected coverage and the graded criteria. This fixture never
grades again — it exists to SHOW, not to test.*

## The input

domain_task: "Patent claim and specification drafting exemplars for EV battery thermal-management inventions."
cellar_root: $CELLAR_ROOT
run_date: 2026-07-10
prior_exemplar_inventory_note: "None landed yet for this domain."

candidate_bundle:

- candidate_id: C1
  repository: USPTO
  accession_or_citation: "US Patent No. 11,234,567 B2, issued 2026-01-20"
  metadata: {assignee: "Contoso Energy Systems, Inc.", filing_type: "issued utility patent", filing_date: 2024-06-11, title: "Battery Thermal Management System Using Phase-Change Composite Layers"}
  snippet: "1. A battery thermal management system comprising: a battery module comprising a plurality of battery cells arranged in a stacked configuration; a phase-change composite layer disposed between adjacent battery cells, the phase-change composite layer comprising a paraffin-based phase-change material dispersed within a graphite matrix; and a cooling plate thermally coupled to the phase-change composite layer, wherein the cooling plate defines a plurality of coolant channels..."
  url: "https://patents.uspto.gov/patent/US11234567"
  license_signal: "Issued US patent; full text public per USPTO."

- candidate_id: C2
  repository: USPTO
  accession_or_citation: "US Patent Application Publication US-2024/0187654 A1, published 2024-11-14"
  metadata: {applicant: "Contoso Energy Systems, Inc.", filing_type: "pre-grant publication, same family as US-11,234,567 B2", filing_date: 2024-06-11, title: "Battery Thermal Management System Using Phase-Change Composite Layers (Pre-Grant Publication)"}
  snippet: "1. A battery thermal management system comprising: a battery module; a phase-change layer disposed proximate to the battery module; and a cooling structure. [Claim as originally filed, prior to examiner amendments]"
  url: "https://patents.uspto.gov/patent/US20240187654"
  license_signal: "Pre-grant publication; public per USPTO."
  note: "Same application family as C1; the issued patent (C1) contains the examiner-amended, allowed claim set that supersedes this pre-grant version."

- candidate_id: C3
  repository: USPTO
  accession_or_citation: "US Patent No. 10,987,654 B1, issued 2025-04-08"
  metadata: {assignee: "Globex Thermal Dynamics LLC", filing_type: "issued utility patent", filing_date: 2023-09-22, title: "Battery Pack Cooling Manifold with Integrated Bypass Valve"}
  snippet: "1. A battery pack cooling manifold comprising: a manifold body defining an inlet, an outlet, and a plurality of branch channels each fluidly coupled to a respective battery module cold plate; a bypass valve disposed within the manifold body and configured to divert coolant flow away from a branch channel in response to a detected over-temperature condition..."
  url: "https://patents.uspto.gov/patent/US10987654"
  license_signal: "Issued US patent; full text public."

- candidate_id: C4
  repository: USPTO
  accession_or_citation: "US Patent No. 11,555,222 B2, issued 2026-03-17"
  metadata: {assignee: "Umbrella Battery Technologies, Inc.", filing_type: "issued utility patent", filing_date: 2024-02-05, title: "Phase-Change Material Thermal Buffer for Electric Vehicle Battery Modules"}
  snippet: "1. An electric vehicle battery module thermal buffer comprising: a sealed enclosure containing a phase-change material having a melting point between 35°C and 45°C; a plurality of thermally conductive fins extending from an interior wall of the sealed enclosure into the phase-change material; and a fire-retardant outer shell configured to delay thermal-runaway propagation to adjacent battery modules by at least 5 minutes under a standardized nail-penetration test..."
  url: "https://patents.uspto.gov/patent/US11555222"
  license_signal: "Issued US patent; full text public."

- candidate_id: C5
  repository: "PatentPrep Academy Blog (patent bar exam prep vendor)"
  accession_or_citation: N/A
  metadata: {publisher: "PatentPrep Academy", filing_type: "course blog post", filing_date: 2026-05-20, title: "5 Tips for Drafting Bulletproof Battery Patent Claims"}
  snippet: "When drafting battery claims, always start broad with your independent claim, then narrow with dependents covering specific chemistries. Here's a sample claim structure we recommend to our students: 'A battery system comprising: a housing; a plurality of cells; and a thermal management means...'"
  url: "https://www.patentprepacademy.com/blog/battery-claims-tips"
  license_signal: "© PatentPrep Academy. All rights reserved. Course materials."

- candidate_id: C6
  repository: "PatentVault Pro (patent database aggregator)"
  accession_or_citation: "Mirror of US Patent 11,234,567 B2"
  metadata: {publisher: "PatentVault Pro", filing_type: "patent database mirror", filing_date: 2026-02-01, title: "US11234567B2 - Battery Thermal Management System (PatentVault Pro copy)"}
  snippet: "[Full reproduction of patent 11,234,567 claims and specification] Upgrade to PatentVault Pro Premium for citation analytics and family tree visualization."
  url: "https://www.patentvaultpro.com/patents/US11234567B2"
  license_signal: "Site ToS: 'Aggregated from USPTO public data; redistribution of our formatted/annotated version restricted without license.'"

## What good output covers (the expected finding set)

C1 -> INCLUDE. authority_tier T1 (USPTO is the primary repository/filer), license_class public-domain (issued US patent full text is public), on-domain, and it is the CURRENT/final claim set for this application family.

C2 -> EXCLUDE(stale-superseded). Same application family as C1; this is the pre-grant publication whose claims were subsequently amended and allowed as US-11,234,567 B2 (C1). Per the EDGAR-generalized supersession rule, landing the superseded version unknowingly is stale-superseded — the rationale should note the superseding citation is C1 / US-11,234,567 B2.

C3 -> INCLUDE. authority_tier T1, license_class public-domain, independent assignee and independent invention — a legitimately distinct, non-duplicate gold exemplar.

C4 -> INCLUDE. authority_tier T1, license_class public-domain, independent assignee and invention — third legitimately distinct exemplar (different technical approach: phase-change buffer with thermal-runaway delay claim).

C5 -> POINTER-ONLY. authority_tier T3 (prep-vendor course blog = secondary commentary), license_class copyrighted-accessible. T3 caps at POINTER-ONLY regardless of how polished or on-topic the content is.

C6 -> EXCLUDE(not-authoritative). authority_tier Untiered (patent database aggregator/mirror of C1's content) — always EXCLUDE(not-authoritative), redirect to USPTO / C1 as the primary source.

Summary: 6 candidates considered — INCLUDE: 3 (C1, C3, C4) — INCLUDE-WITH-RESTRICTION: 0 — POINTER-ONLY: 1 (C5) — EXCLUDE: 2 (C2 stale-superseded, C6 not-authoritative). INCLUDE count = 3, within the 3-7 target range.

## How it was graded

Deterministic per-source set-match. An arm is scored correct only if it assigns the exact oracle disposition to every one of C1-C6, with the exact EXCLUDE reason_class (C2=stale-superseded, C6=not-authoritative). C2 is the critical probe: an arm that scores C2 INCLUDE (missing that it is the pre-grant version of the same family already captured, in its final form, by C1) fails the fixture even if all other dispositions are correct. The rationale for C2 must name C1 / US-11,234,567 B2 as the superseding citation.

*Eval evidence for this station (headline numbers, residuals, honest history): see
[`../evals/`](../evals/) in this plugin.*
