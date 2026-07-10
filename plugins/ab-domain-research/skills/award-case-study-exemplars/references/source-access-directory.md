# Source / access directory — award-case-study-exemplars

Reference detail for Step 1 (authority tiering) and Step 2 (license gate) of
`award-case-study-exemplars`. Load this when a candidate's handling isn't already
obvious from the SKILL.md summary tables. Every row is consistent with the
competency doc this skill was built from.

## Marketing / advertising (ship-first vertical)

| Source | Access / license reality | Handling |
|---|---|---|
| Effie Awards (effie.org case database) | Winner lists + case summaries public; FULL cases largely behind the Effie/WARC subscription; all content copyrighted | Public summaries: `copyrighted-accessible` — extract and restate the case's STRUCTURE (challenge → insight → strategy → execution → results), cite the case + award tier/year. Paywalled full cases: `restricted` → `POINTER-ONLY` via the rule-5 carve-out (the award body IS the T1 primary with no open substitute) |
| Cannes Lions (The Work / lovethework.com) | Predominantly subscription-gated; some winner galleries public; copyrighted | Same posture as Effie: public gallery entries `copyrighted-accessible` (structure/facts restated), gated work `POINTER-ONLY` |
| D&AD, The One Show, Clio, Webby | Winner showcases publicly browsable; content copyrighted, no open license | `copyrighted-accessible`: restate structure + craft observations, cite; never mirror creative assets |
| IPA Effectiveness Awards / databank | The methodologically strongest effectiveness cases (rigorous, results peer-scrutinized relative to other award bodies); databank + published volumes are paywalled | `POINTER-ONLY` via the rule-5 T1-no-substitute carve-out; public abstracts `copyrighted-accessible`. Results from IPA cases get the `IPA-peer-scrutinized` tag, not `entrant-reported` |
| WARC | Publisher/aggregator of effectiveness cases (licenses Effie/IPA content); subscription | `restricted`. It is a licensed publisher, not an untiered scraper — but never the landing source; point to it or to the originating award body |
| Brand/agency self-published case studies (agency sites) | Freely viewable, virtually never carry a license statement | Rule 5: viewable ≠ licensed → `POINTER-ONLY`. Self-published cases are ALSO self-interested (marketing about marketing) — record that caveat in the pointer description and in any landing plan's scope/restriction notes |
| Trade-press case writeups (established marketing/advertising publications) | Copyrighted; secondary commentary on the work | T3 → `POINTER-ONLY` per rule 2 (pointer toward the award body's own record) |
| Government-agency campaign material + evaluations (agency-authored public-service campaign case reports, GAO evaluations of federal ad campaigns, e.g. military recruiting advertising reviews) | US-government-authored = public domain (17 U.S.C. § 105) | `public-domain` — the one corner of this class where full excerpts land freely; niche but genuinely useful for effectiveness-narrative structure |
| "Top 10 best campaigns" SEO listicles, marketing-blog roundups, prep-course galleries | Untiered content farms | `EXCLUDE(not-authoritative)` (rule 1) — never a pointer |

## Authority tiers for this class

- **T1** — the award body itself and its own library: Effie, Cannes Lions, D&AD,
  One Show, Clio, IPA. The juried judgment is theirs.
- **T2** — established effectiveness-research publishers and industry bodies
  publishing ABOUT the awarded work with editorial standards: WARC as publisher, a
  national advertising-industry association's own case library, GAO/CRS-class
  government analytic bodies wherever the report's subject matches the domain.
- **T3** — trade-press coverage and reputable practitioner commentary →
  `POINTER-ONLY`.
- **Untiered** — SEO roundups, content farms, scraped galleries → `EXCLUDE`.

## Per-domain extension (grow this table, don't replace the discipline)

The source list below is not yet populated with live URLs — extend it as each
domain's fill demands. The license-gate / tiering / boundary-rule discipline in
SKILL.md transfers unchanged; only the concrete source list changes per domain.

| Domain | T1 award bodies | Notes |
|---|---|---|
| Marketing / advertising | Effie, Cannes Lions, IPA, D&AD | Ship-first vertical, table above is authoritative |
| Design | D&AD, Red Dot | Winner showcases typically public-browsable, copyrighted; apply the same `copyrighted-accessible` restate-structure handling |
| PR | SABRE Awards, PRWeek Awards | Case summaries typically public; full case studies often behind trade-publication paywalls — apply the same T1-no-substitute `POINTER-ONLY` carve-out |
| Digital / UX | Webby Awards, Awwwards | Winner galleries public; site/craft screenshots are the "creative asset" here — describe UX/IA choices, never mirror screenshots as if they were licensed content |
