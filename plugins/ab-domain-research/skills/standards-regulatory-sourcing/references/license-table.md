# License table — standards / regulatory source class

Classify license BEFORE judging content. This table is specific to statutes, regulations,
official standards, and government publications; it is a superset detail of the cross-cutting
5-class table (`public-domain` / `permissive-cc` / `restrictive-cc` / `copyrighted-accessible` /
`restricted`) with the issuer-specific mapping this station needs. The rightmost column states
the disposition each license class supports — do not default to `POINTER-ONLY` or `EXCLUDE`
for a class that supports `INCLUDE`/`INCLUDE-WITH-RESTRICTION`, and do not default to
`INCLUDE`/`INCLUDE-WITH-RESTRICTION` for `restricted` without applying the split below.

| Issuer class | License class | Terms / handling | Disposition |
|---|---|---|---|
| US federal statutes, regulations (U.S.C., CFR), agency guidance, SEC/IRS/FTC publications | `public-domain` | 17 U.S.C. § 105 (US government works). Full text excerptable with citation. | `INCLUDE` |
| NIST publications (SP 800-series, CSF, AI RMF) | `public-domain` | US government work. | `INCLUDE` |
| GAO / CRS reports | `public-domain` | US government works; CRS public via crsreports.congress.gov. Tier is T2 (government analytic body), not T1 — see authority tiering in SKILL.md section 3. | `INCLUDE` |
| US state statutes/regulations (the operative law text) | `public-domain` | Public edict per *Georgia v. Public.Resource.Org*, 590 U.S. ___ (2020) — extends to official annotations authored by a legislature's own agent. | `INCLUDE` |
| Third-party commercial annotated state code editions | `restricted` | The annotations layer is copyrighted even though the underlying statute text is not — don't conflate the two. This is non-primary material (a third-party wrapper, not the issuing legislature) AND an open substitute exists (the plain statute text at the official state site — see `source-directory.md`). Per boundary rule 5 that combination does NOT earn the T1-no-open-substitute carve-out. | `EXCLUDE: license-restricted` — point to the plain statute at the official site instead, not to this wrapper |
| Court opinions | `public-domain` | Edicts of government — not copyrightable. | `INCLUDE` |
| EU legislation (EUR-Lex: regulations, directives — e.g. GDPR) | `permissive-cc`-equivalent (`permissive`) | Reuse permitted per Commission Decision 2011/833/EU and the EUR-Lex reuse notice. Attribute to EUR-Lex. | `INCLUDE` (attribution noted, not a disposition-level restriction) |
| ISO / IEC / ANSI standards | `restricted` | Copyrighted AND paywalled. This IS the T1 primary authority itself, and there is no open/free substitute for the standard's own clause text — the narrow carve-out in boundary rule 5 applies. Title, number, scope, edition year only. Never reproduce clause text. Note "purchase required." | `POINTER-ONLY` |
| FASB Accounting Standards Codification | `copyrighted-accessible` | Free "Basic View" access. Cite by Topic/Subtopic (e.g. ASC 606); restate requirements in own words — the restate-only obligation is itself a recorded restriction. | `INCLUDE-WITH-RESTRICTION` |
| IFRS Foundation standards | `copyrighted-accessible` | Unaccompanied standards freely accessible with registration. Cite by standard (e.g. IFRS 15); restate. | `INCLUDE-WITH-RESTRICTION` |
| W3C specifications (Recommendations and Working Group Notes) | `permissive` | W3C Document License — reproduction permitted with attribution. Applies equally to a narrow-scope WG Note within a broader domain — narrow scope is noted in the landing plan's scope section, not grounds for `off-domain` exclusion (boundary rule 7). | `INCLUDE` (attribution noted, not a disposition-level restriction) |
| A specific document/course/model on an otherwise closed or paywalled platform, carrying its OWN stated CC license (e.g. CC BY-NC-SA in the fine print under a "free download, no login" banner) | Whatever the stated item license actually is | Boundary rule 4: the stated item license governs, not the platform's usual posture. Judge the item on its own terms. | Per the item's actual license class (commonly `INCLUDE-WITH-RESTRICTION` if restrictive-cc) |

## Notes that generalize beyond this table

- A source whose terms cannot be determined is never landed as content — default to
  `POINTER-ONLY`, same as the cross-cutting rule.
- Public-domain status of the *statute text* never transfers to a third party's editorial
  wrapper (annotations, commentary, formatting) around that text. Triage the two layers
  separately even when they're bundled in the same product.
- `copyrighted-accessible` and `restrictive-cc` sources both land as
  `INCLUDE-WITH-RESTRICTION` — never `POINTER-ONLY` or `EXCLUDE` merely because the license
  carries an obligation (boundary rule 3). `permissive-cc`/`permissive` sources land as plain
  `INCLUDE`; note the attribution requirement in the landing block's notes, but it is not a
  disposition-level restriction.
- The `restricted` class is never a single default disposition — it splits three ways
  (boundary rule 5):
  1. Explicit restriction (all-rights-reserved, login gate, paywall) on non-primary material,
     with an open substitute available elsewhere → `EXCLUDE: license-restricted`.
  2. Explicit restriction on the T1 primary authority itself with NO open substitute (ISO,
     IEC, ANSI) → `POINTER-ONLY`.
  3. Freely viewable material with NO stated license at all → `POINTER-ONLY` (viewable is not
     the same as licensed).
