# License-class table and disposition mechanics — award-case-study-exemplars

Reference detail for Step 2 (license gate) and Step 4 (disposition vocabulary) of
`award-case-study-exemplars`. This is the general cross-cutting license table,
annotated with this class's specific meaning for each row. Load this when you need
the exact wording for a license/terms determination.

## License classes (general meaning → this class's instance)

| License class | General meaning | What it looks like in award/case-study sourcing |
|---|---|---|
| `public-domain` | US federal government works (17 U.S.C. § 105), statutory/regulatory text, court opinions, expired copyright | Agency-authored public-service campaign case reports; GAO evaluations of federal ad campaigns (e.g. military recruiting advertising reviews) |
| `permissive-cc` | CC BY, CC BY-SA (record the SA obligation) | Rare in this class — a specific case study or award-body publication explicitly marked CC BY/BY-SA. Always check the item's own stated license before assuming the platform default applies (rule 4) |
| `restrictive-cc` | CC BY-NC, CC BY-NC-SA, any -ND variant | An award body or publisher releasing a specific report under NC/ND terms. Lands as `INCLUDE-WITH-RESTRICTION` — record the exact obligation, never downgrade for carrying one (rule 3) |
| `copyrighted-accessible` | Publicly published, all-rights-reserved | The default state for public winner lists, case summaries, and gallery entries at Effie/Cannes/D&AD/One Show/Clio/Webby. Extract facts and structure, restate in your own words, cite precisely — never bulk-copy expression |
| `restricted` | Paywalled, ToS-restricted platforms, undetermined terms | Full Effie/WARC cases, gated Cannes "The Work," IPA databank/published volumes. `EXCLUDE(license-restricted)` unless the rule-5 T1-no-substitute carve-out applies (then `POINTER-ONLY`) |

A source whose terms cannot be determined is never landed as content — default to
`POINTER-ONLY` if freely viewable, `EXCLUDE(license-restricted)` if gated.

## Disposition vocabulary — exact strings

- `INCLUDE`
- `INCLUDE-WITH-RESTRICTION`
- `POINTER-ONLY`
- `EXCLUDE(license-restricted)`
- `EXCLUDE(not-authoritative)`
- `EXCLUDE(unreliable-derived-data)`
- `EXCLUDE(injection-suspect)`
- `EXCLUDE(off-domain)`
- `EXCLUDE(stale-superseded)`

## EXCLUDE reason-class priority (rule 6)

When more than one EXCLUDE reason is genuinely decisive, name the most specific,
in this priority order:

`injection-suspect` > `unreliable-derived-data` > `stale-superseded` >
`license-restricted` > `not-authoritative` > `off-domain`

## Provenance frontmatter contract (required on every landed artifact)

```yaml
source_name:      # the case/publication name
publisher:        # the award body or issuing publisher
url:              # canonical URL (the award body's own record, not an aggregator mirror)
retrieved:        # YYYY-MM-DD
license: {class, terms}   # from the table above; exact restriction text if any
authority_tier:   # T1 | T2
version_or_date:  # award tier/category/year, or case_age_years-derived year
```

Exemplar artifacts additionally require `why_gold:` — 2-4 sentences naming the
specific juried recognition (award, tier, category, year, judging body) and the
specific case-structure qualities that make it a grading reference. Never just
"it's real."

## Results tagging (ties to the derived-data EXCLUDE)

- `entrant-reported` — default for award-case results; never presented as
  independently audited.
- `IPA-peer-scrutinized` — IPA papers only; the notable partial exception.
- `none-present` — no quantified results claim in the case.
- `third-party-estimated` — a blog/tool's own estimate laid on top of a case, not
  the entrant's figure → forces `EXCLUDE(unreliable-derived-data)` regardless of
  how strong the rest of the case looks.
