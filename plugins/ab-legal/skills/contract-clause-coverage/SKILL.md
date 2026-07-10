---
name: contract-clause-coverage
description: >-
  Structural clause-coverage check for a commercial contract against the standard
  expected clause set for its type. Given a contract and its type (NDA, MSA,
  SaaS, or generic commercial), report PRESENT / ABSENT / DEFICIENT for every
  standard clause of that type, naming the specific missing load-bearing sub-part
  for deficient ones. Use when asked to check whether a contract "has the standard
  clauses", find "missing or incomplete clauses", run a "clause completeness /
  coverage check", or "what's missing from this NDA/MSA/SaaS agreement". Structural
  only: it does NOT assess fairness, enforceability, or legal sufficiency, and is
  NOT legal advice. If asked to judge whether a term is good/bad for a party or
  whether a contract is enforceable, decline that part and run only the coverage check.
---

# Contract Clause Coverage

Check a contract against the **standard expected clause set** for its type and report,
per clause, whether it is PRESENT, ABSENT, or DEFICIENT. This is a completeness check
against a conventional clause set, not a legal opinion.

## What this skill is (and is not)

- IN scope: "which standard clauses for a contract of this type are present, missing,
  or present-but-incomplete." Purely structural.
- OUT of scope: whether a clause is fair/favorable to either side, whether the contract
  is enforceable, whether a term is legally sufficient, or any recommendation to sign or
  redline. Do not opine on any of these. If asked, run the coverage check and refer the
  fairness/enforceability question to a lawyer.
- The clause set is **conventional** (what a complete agreement of this type is normally
  expected to contain), NOT a statement of legal requirement. Frame it that way.

## Inputs

- The contract text.
- The contract type: `NDA`, `MSA`, `SaaS`, or `Generic`. If the caller supplies it, use
  it and mark the source `caller-provided`. Otherwise infer it from the title/preamble and
  mark the source `inferred from title/preamble` (see type inference below).

## Procedure

1. **Fix the type.** Use the caller-provided type if given. Else infer:
   - Title/preamble mentions "Non-Disclosure", "Confidentiality Agreement", "NDA" → `NDA`.
   - "Master Services Agreement", "Master Agreement", "Professional Services", SOW-driven → `MSA`.
   - "Subscription", "SaaS", "Software-as-a-Service", "Cloud Services", "Order Form + hosted
     access" → `SaaS`.
   - None clearly match → `Generic`.
2. **Select the canonical clause set** for that type from the tables below. Use it verbatim.
   Do **not** rename, merge, split, add, or drop clauses. The number of rows you output MUST
   equal the set size: NDA = 9, MSA = 12, SaaS = 12, Generic = 12.
3. **(NDA only) Determine the designation:** `Mutual` if both parties owe confidentiality
   obligations as discloser and recipient; `One-way` if only one party discloses / only one is
   bound; `Unspecified` if the text does not make it determinable.
4. **For each canonical clause, in canonical order, scan the whole contract by SUBSTANCE, not
   heading.** A clause counts as addressed if its substance appears anywhere, even folded under
   a different or combined heading (e.g. "Term" inside a "Term and Termination" section). Then
   assign exactly one status from the closed enum:
   - `PRESENT` — the clause's substance is there and its load-bearing sub-parts are present.
   - `DEFICIENT` — the clause is present but missing a load-bearing sub-part (see deficiency
     triggers). Deficient is still "there", so it is never also ABSENT.
   - `ABSENT` — the clause topic is entirely missing from the contract.
5. **Record the Location.** For PRESENT and DEFICIENT, cite the contract's own heading and/or
   section number where the substance was found — a short quoted heading (e.g. "Term and
   Termination") and/or `§N`. For ABSENT, use `—`.
6. **Record the Defect.** For DEFICIENT only, write one specific line naming the missing
   load-bearing sub-part (e.g. "limitation-of-liability present but states no cap amount").
   For PRESENT and ABSENT, use `—`. Every DEFICIENT row MUST have a non-empty specific defect;
   no PRESENT or ABSENT row may carry a defect.
7. **Assemble the report** exactly per the Report Template. Compute the summary counts.
8. **Run the equivalence self-check** (below) before returning. Fix any violation.

## Canonical clause sets (verbatim — do not rename or merge)

Use the clause name in the "Expected Clause" column exactly as written here.

### NDA / confidentiality agreement (9)

| # | Expected Clause |
|---|---|
| 1 | Definition of Confidential Information |
| 2 | Standard exclusions from confidential information |
| 3 | Permitted use / purpose limitation |
| 4 | Confidentiality obligations (non-use, non-disclosure, standard of care) |
| 5 | Term of agreement and duration of confidentiality obligation |
| 6 | Return or destruction of materials |
| 7 | Remedies (injunctive / equitable relief) |
| 8 | Governing law |
| 9 | Mutual vs one-way designation |

### MSA / master services agreement (12)

| # | Expected Clause |
|---|---|
| 1 | Scope of services (SOW mechanism) |
| 2 | Fees, invoicing, and payment terms |
| 3 | Term and termination |
| 4 | Confidentiality |
| 5 | Intellectual-property ownership |
| 6 | Warranties and disclaimers |
| 7 | Indemnification |
| 8 | Limitation of liability |
| 9 | Insurance |
| 10 | Governing law and dispute resolution |
| 11 | Assignment |
| 12 | Independent-contractor / relationship of the parties |

### SaaS / subscription (12)

| # | Expected Clause |
|---|---|
| 1 | Grant of access / subscription and usage restrictions |
| 2 | Fees, auto-renewal, and price changes |
| 3 | Data protection and security (DPA reference) |
| 4 | Service levels (SLA) / uptime and credits |
| 5 | Data ownership and return / deletion on termination |
| 6 | Intellectual-property ownership of the service |
| 7 | Warranties and disclaimers |
| 8 | Indemnification |
| 9 | Limitation of liability |
| 10 | Term, termination, and suspension |
| 11 | Governing law |
| 12 | Confidentiality |

### Generic commercial agreement — fallback set (12)

Use only when the type is `Generic`. This is a conventional general-commercial-contract set.

| # | Expected Clause |
|---|---|
| 1 | Parties and recitals |
| 2 | Definitions |
| 3 | Subject matter / scope of the agreement |
| 4 | Consideration / payment terms |
| 5 | Term and termination |
| 6 | Confidentiality |
| 7 | Representations and warranties |
| 8 | Limitation of liability |
| 9 | Indemnification |
| 10 | Governing law and dispute resolution |
| 11 | Assignment |
| 12 | Notices and general provisions |

## Deficiency triggers (load-bearing sub-parts)

DEFICIENT = the clause topic is present but a load-bearing sub-part is missing. Apply these
specific triggers; if the trigger fires, mark DEFICIENT and name the missing sub-part as the
defect. If none fires and the substance is present, mark PRESENT.

**NDA**
- #4 Confidentiality obligations — DEFICIENT if it states only one of non-use / non-disclosure,
  or states neither a standard of care nor an equivalent protection obligation.
- #5 Term + duration of confidentiality obligation — DEFICIENT if it states an agreement term
  but no survival/duration for the confidentiality obligation (or states the obligation duration
  but no agreement term). Defect example: "term stated but no survival period for the
  confidentiality obligation."
- #2 Standard exclusions — DEFICIENT if an exclusions provision exists but omits load-bearing
  categories (public, already-known, independently developed, rightfully received).

**MSA**
- #3 Term and termination — DEFICIENT if it lacks effect-of-termination/survival language, or
  omits either termination-for-convenience or termination-for-cause.
- #5 Intellectual-property ownership — DEFICIENT if it assigns/allocates work product but is
  silent on background IP (or silent on the license grant to use background IP).
- #8 Limitation of liability — DEFICIENT if it states no liability cap amount, OR contains no
  exclusion of consequential/indirect damages.

**SaaS**
- #2 Fees, auto-renewal, and price changes — DEFICIENT if it states auto-renewal but no
  notice-to-cancel window / cancellation window.
- #5 Data ownership and return/deletion — DEFICIENT if it states data ownership but is silent
  on return or deletion of customer data on termination.
- #9 Limitation of liability — DEFICIENT if no cap amount, OR no consequential-damages exclusion.
- #10 Term, termination, and suspension — DEFICIENT if it lacks effect-of-termination/survival.

**Generic**
- #5 Term and termination — DEFICIENT if it lacks effect-of-termination/survival language.
- #6 Confidentiality — DEFICIENT if it states confidentiality but no survival period.
- #8 Limitation of liability — DEFICIENT if no cap amount, OR no consequential-damages exclusion.

For any clause without an enumerated trigger above, use judgment sparingly: DEFICIENT only when
a genuinely load-bearing sub-part of that clause is missing; otherwise PRESENT or ABSENT.

## Substance-not-heading rule (the main trap)

Do NOT mark a clause ABSENT just because there is no heading with that name. Match by substance:
a "Term" folded into "Term and Termination", confidentiality living inside a "Proprietary
Information" section, or an IP grant buried in "Ownership" all count as PRESENT/DEFICIENT, not
ABSENT. Only mark ABSENT when the substance appears nowhere.

## Report Template (exact structure)

Output the report with these five sections, in this order. Section markers are literal.

```
--- HEADER ---
Contract type: <NDA | MSA | SaaS | Generic> (<caller-provided | inferred from title/preamble>)
Designation: <Mutual | One-way | Unspecified>          # NDA only; omit this line for other types
Basis: Standard expected clauses for a complete <type> agreement — conventional, not a statement of legal requirement.

--- COVERAGE TABLE ---
| # | Expected Clause | Status | Location | Defect |
|---|---|---|---|---|
| 1 | <canonical clause name> | <PRESENT|ABSENT|DEFICIENT> | <"heading" and/or §N, or —> | <defect line for DEFICIENT, else —> |
| … one row per canonical clause, in canonical order … |

--- SUMMARY ---
Summary: PRESENT <p>, DEFICIENT <d>, ABSENT <a> (of <total>).

--- OTHER CLAUSES (non-graded) ---
Other clauses observed (not part of the standard set for this type):
- <extra clause heading found>            # optional; omit the whole section if none, no quality commentary

--- DISCLAIMER ---
This is a structural clause-coverage check against a standard clause set for this contract type. It does not assess fairness, enforceability, or legal sufficiency, and is not legal advice.
```

Rules for the template:
- `<type>` in the Basis line is the resolved token (NDA / MSA / SaaS / Generic).
- The `Designation:` line appears ONLY for NDA. Do not emit it for MSA/SaaS/Generic.
- The coverage table has EXACTLY one row per canonical clause — no omissions, no duplicates,
  no additions. `#` is the canonical ordinal; `Expected Clause` is verbatim from the set above.
- `Status` is uppercase, from the closed enum {PRESENT, ABSENT, DEFICIENT} only.
- The "Other clauses observed" section is explicitly non-graded and may be omitted. It lists
  only extra headings found; it must contain no fairness or quality commentary.
- The disclaimer line is mandatory and reproduced verbatim.

## Machine-readable equivalence self-check

The report must be losslessly reducible to three sets:
`PRESENT{clause}`, `ABSENT{clause}`, `DEFICIENT{clause: defect}`. Before returning, verify:

1. Every canonical clause for the type appears in exactly one of the three sets — none omitted,
   none duplicated, none added.
2. `|PRESENT| + |DEFICIENT| + |ABSENT| == total == set size` (9 for NDA, 12 for MSA/SaaS/Generic),
   and the Summary line's p + d + a equals that total.
3. Every DEFICIENT entry has a specific, non-empty defect naming the missing load-bearing
   sub-part; no PRESENT or ABSENT entry has a defect.
4. Statuses are only from {PRESENT, ABSENT, DEFICIENT}; Locations are present for PRESENT and
   DEFICIENT rows and `—` for ABSENT rows.
5. The report contains no fairness, favorability, enforceability, or advice language anywhere
   except the mandatory disclaimer.

If any check fails, correct the table and re-emit before returning.

## References (progressive disclosure)

- `references/clause-sets.md` — the four canonical sets expanded: per-clause substance cues
  (what phrases indicate the clause is addressed) and the designation/type-inference detail.
- `references/status-and-deficiency-rules.md` — the full status enum, the deficiency catalog,
  the substance-not-heading examples, and worked set-reduction examples.