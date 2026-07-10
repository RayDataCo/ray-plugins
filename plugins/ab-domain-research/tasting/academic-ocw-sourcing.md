# Tasting — academic-ocw-sourcing

*A retired eval fixture, deliberately spent for demonstration (see the factory's
EVAL-SPEC): run the `academic-ocw-sourcing` station on the input below in YOUR environment (mise first),
then compare against the expected coverage and the graded criteria. This fixture never
grades again — it exists to SHOW, not to test.*

## The input

domain: financial-statement-articulation
cellar_root: $CELLAR_ROOT (test harness value)
prior_sourcing_decisions: none
max_artifacts: default (5-15)

candidates:

1) source_name: "15.501 Financial Accounting"
   institution_publisher: MIT OpenCourseWare (Sloan School of Management)
   url: https://ocw.mit.edu/courses/15-501-financial-accounting-fall-2023/
   stated_license: "This course is licensed under a Creative Commons BY-NC-SA 4.0 license, per MIT OCW's site-wide terms of use."
   snippet: "15.501 introduces the mechanics of financial statement preparation: the balance sheet, income statement, and statement of cash flows, and how transactions articulate across the three. Problem sets walk through building a full three-statement model from a trial balance."

2) source_name: "Principles of Accounting, Volume 1: Financial Accounting"
   institution_publisher: OpenStax
   url: https://openstax.org/details/books/principles-financial-accounting
   stated_license: "CC BY 4.0"
   snippet: "Chapter 5 walks through the accounting cycle end to end -- from journal entry through the preparation of a classified balance sheet and multi-step income statement -- using a running example business."

3) source_name: "BUS103: Introduction to Financial Accounting"
   institution_publisher: Saylor Academy
   url: https://learn.saylor.org/course/BUS103
   stated_license: "Saylor Academy materials are made available under a Creative Commons Attribution 3.0 Unported License unless otherwise noted."
   snippet: "Unit 4 covers the preparation and articulation of the four core financial statements and introduces horizontal/vertical analysis of a completed statement set."

4) source_name: "Financial Accounting" (open textbook by C. Skousen, A. Sharratt, A. Farmer, Utah State University)
   institution_publisher: Open Textbook Library (University of Minnesota, hosting)
   url: https://open.umn.edu/opentextbooks/textbooks/financial-accounting-skousen
   stated_license: "This specific title's own license page states: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). Note: OTL hosts titles under a range of licenses that vary per book -- always check the individual book's license page, do not assume from the platform."
   snippet: "Chapter 2 walks through preparing the balance sheet, income statement, and statement of cash flows from a common trial balance, showing how each statement articulates with the others."

5) source_name: "Analyzing financial statements" unit
   institution_publisher: Khan Academy
   url: https://www.khanacademy.org/economics-finance-domain/core-finance/accounting-and-financial-stateme
   stated_license: "Page footer reads: 'Except where otherwise noted, Khan Academy content is licensed under CC BY-NC-SA 3.0 US.'"
   snippet: "This unit is free to watch and complete with no account required. It walks through reading a real 10-K's balance sheet and income statement and articulating the relationship between the two." [TRAP: freely-viewable, no-login content that a naive curator would treat as unrestricted because nothing is paywalled -- the stated CC BY-NC-SA license still caps it at INCLUDE-WITH-RESTRICTION.]

6) source_name: "Financial Accounting Fundamentals"
   institution_publisher: University of Illinois, delivered via Coursera
   url: https://www.coursera.org/learn/financial-accounting-fundamentals
   stated_license: "All course content is (c) the instructing institution and Coursera; all rights reserved per Coursera's Honor Code and Terms of Use. Video lectures require an active enrollment/login to view."
   snippet: "Module 3 walks learners through constructing the balance sheet and income statement and shows how the two statements articulate through retained earnings."

## What good output covers (the expected finding set)

1) MIT OCW 15.501: license_class=restrictive-cc (CC BY-NC-SA 4.0). authority_tier=T1 (university's own OCW). disposition=INCLUDE-WITH-RESTRICTION. restriction_detail="NC: no commercial use; SA: derivatives must carry the same CC BY-NC-SA 4.0 license (viral)." On-domain, current -> lands.

2) OpenStax Principles of Accounting Vol.1: license_class=permissive-cc (CC BY 4.0). authority_tier=T1 (established OER publisher named explicitly as T1 in the station doc). disposition=INCLUDE. restriction_detail=n/a (attribution only).

3) Saylor BUS103: license_class=permissive-cc (CC BY 3.0). authority_tier=T2 (recognized OER publisher, not university-OCW/OpenStax so not T1 per station's tiering text). disposition=INCLUDE. restriction_detail=n/a.

4) Open Textbook Library "Financial Accounting" (Skousen et al.): per-title check (NOT blanket OTL assumption) shows this specific title's own license page = CC BY-NC-SA 4.0. license_class=restrictive-cc. authority_tier=T2 (aggregator; license call made on the underlying item per cross-cutting rule). disposition=INCLUDE-WITH-RESTRICTION. restriction_detail="NC: no commercial use; SA: derivatives must carry same license (viral)."

5) Khan Academy "Analyzing financial statements": license_class=restrictive-cc (stated CC BY-NC-SA 3.0 on the resource footer -- must be checked per-resource, which the snippet does). authority_tier=T2. disposition=INCLUDE-WITH-RESTRICTION. restriction_detail="NC: no commercial use; SA: derivatives must carry same license (viral). Freely-viewable/no-login is NOT the same as unrestricted -- the stated CC BY-NC-SA terms still govern." A naive curator who reads 'free to watch, no account required' as license-clean and marks plain INCLUDE has failed the license gate.

6) Coursera "Financial Accounting Fundamentals": license_class=restricted (platform ToS, all rights reserved, login-gated). authority_tier=n/a (fails license gate before authority is relevant). disposition=EXCLUDE(license-restricted). Content quality is irrelevant -- restricted terms cap it below landing regardless of the instructing institution's prestige.

Expected landed_count: 4 (rows 1,2,3,4,5 minus... note 5 of 6 candidates pass the license gate and land: rows 1,2,3,4,5 = 5 landed artifacts (2 INCLUDE, 3 INCLUDE-WITH-RESTRICTION); row 6 EXCLUDEd). All 5 landed artifacts require full TASL + license.class + license.terms + authority_tier + version_or_date frontmatter, with NC/SA explicitly recorded and flagged as viral for rows 1, 4, 5.

## How it was graded

Deterministic per-source set-match. An arm is CORRECT only if every one of the 6 candidates receives the exact oracle disposition (INCLUDE vs INCLUDE-WITH-RESTRICTION is a real, non-synonymous distinction -- rows 1,4,5 marked plain INCLUDE are wrong) and the EXCLUDE on row 6 carries reason class license-restricted exactly. Specifically check: (i) row 5 (Khan Academy) is NOT marked INCLUDE despite being freely viewable -- this is the license trap; (ii) row 4 (Open Textbook Library) is classified from its own per-title license page, not assumed permissive from the Open Textbook Library platform's general reputation; (iii) rows 1, 4, 5 all have non-empty restriction_detail recording both NC and SA with SA explicitly flagged as a viral/share-alike obligation; (iv) landed_path exists for rows 1-5 and is absent (n/a) for row 6; (v) the run summary/decision sheet states the exemplar-thin limitation and does not emit a why_gold field on any artifact.

*Eval evidence for this station (headline numbers, residuals, honest history): see
[`../evals/`](../evals/) in this plugin.*
