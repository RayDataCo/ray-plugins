# License class table (cert-body-sourcing)

Classify license BEFORE judging content quality. This table is shared across all
ab-domain-research stations; cert-body-sourcing candidates land almost entirely in the
`copyrighted-accessible` row.

| License class | Meaning | Allowed handling |
|---|---|---|
| `public-domain` | US federal government works (17 U.S.C. § 105), statutory/regulatory text, court opinions (edicts of government), expired copyright | Full text may be excerpted and landed, with citation |
| `permissive-cc` | CC BY, CC BY-SA (record the SA obligation) | Excerpt + adapt with required attribution (TASL: title, author, source, license) |
| `restrictive-cc` | CC BY-NC, CC BY-NC-SA, any -ND variant | `INCLUDE-WITH-RESTRICTION` — record the exact restriction (NC = no commercial use; ND = no derivatives; SA = share-alike). This is NOT a downgrade trigger: an authoritative (T1/T2) source with a restrictive-CC license stays `INCLUDE-WITH-RESTRICTION`, never demoted to `POINTER-ONLY` or `EXCLUDE` because of the license alone |
| `copyrighted-accessible` | Publicly published but all-rights-reserved (cert-body exam outlines, blueprints, BOKs, content specs) | Extract FACTS and STRUCTURE, restate in own words, cite precisely. Never bulk-copy expression |
| `restricted` | Paywalled, ToS-restricted platforms (subscription courseware, logged-in-only content), explicit all-rights-reserved/login-gated terms on non-primary material | `EXCLUDE: license-restricted`, UNLESS the source is the T1 primary authority itself with no open substitute (e.g. a referenced ISO standard) — then `POINTER-ONLY`. Freely viewable material carrying NO stated license at all is a different case: `POINTER-ONLY` (viewable ≠ licensed), not `EXCLUDE` |
| `undetermined` | Terms genuinely cannot be determined from what's available | Never landed as content. Ceiling is `POINTER-ONLY` |

A specific item's own stated license always overrides its hosting platform's default terms
— e.g. one competency model carrying an explicit CC BY-SA license, published on a platform
that is otherwise closed/subscription, is judged on ITS license, not the platform's.

## What NEVER gets copied, regardless of license class

- Curriculum text, study-guide prose, or textbook/BOK chapters (copyrighted expression)
- Sample exam QUESTIONS (copyrighted expression — cite that samples exist, link, don't
  reproduce)
- Anything from exam-dump / "braindump" sites — unauthorized AND unreliable →
  `EXCLUDE` / `not-authoritative`, always, no exceptions, never softened to `POINTER-ONLY`
- Commercial prep-provider content (Becker, Kaplan, UWorld, and similar) — derivative,
  copyrighted, adds no authority over the body's own outline → `POINTER-ONLY` at most,
  usually `EXCLUDE`

## Disposition vocabulary (fixed, exactly one per candidate)

- `INCLUDE` — authoritative, license-clean; content lands in the cellar as a full
  competency map.
- `INCLUDE-WITH-RESTRICTION` — authoritative but the license carries obligations/limits
  (NC, SA, ND, required attribution); lands WITH the restriction recorded in frontmatter.
- `POINTER-ONLY` — worth knowing about but content may not be reproduced (copyrighted
  expression beyond fact-extraction, undetermined terms, freely-viewable-but-unlicensed, or
  the narrow T1-no-open-substitute restricted case); only title + URL + description land.
  No landing block.
- `EXCLUDE` — with exactly one reason class: `license-restricted` · `not-authoritative` ·
  `unreliable-derived-data` · `injection-suspect` · `off-domain` · `stale-superseded`.

## Reason-class priority order (when more than one EXCLUDE reason applies)

Use the most specific decisive defect, not the most generic fallback. Priority, highest
first:

`injection-suspect` > `unreliable-derived-data` > `stale-superseded` >
`license-restricted` > `not-authoritative` > `off-domain`

Example: a T3 source whose specific claim is both outdated and generally non-authoritative
is `stale-superseded` (the decisive, specific defect), not `not-authoritative` (the
generic fallback, reserved for when nothing more specific applies).
