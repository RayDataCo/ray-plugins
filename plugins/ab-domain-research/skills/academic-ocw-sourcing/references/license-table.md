# Academic OCW/OER license directory

Full per-source license reality for the academic-ocw-sourcing station. Always verify
against the source's OWN current license page before landing anything — publishers change
licensing terms per title/edition, and this table can drift.

| Source | Typical license | `license_class` | Handling |
|---|---|---|---|
| MIT OpenCourseWare | CC BY-NC-SA 4.0 (site-wide default; verify per-course) | `restrictive-cc` | `INCLUDE-WITH-RESTRICTION`; record NC (no commercial use) + SA (share-alike, viral) every time — never downgraded to POINTER-ONLY just because it carries obligations (boundary rule 3) |
| OpenStax textbooks | CC BY 4.0 (most titles) | `permissive-cc` | `INCLUDE`; TASL attribution required (Title, Author, Source, License) |
| Saylor Academy | CC BY 3.0/4.0 | `permissive-cc` | `INCLUDE`; TASL attribution required |
| Open Textbook Library (UMN) | Varies per title — check each book's own license page | Per-title call | Never assume; treat as undetermined until the specific title's page is checked; undetermined + freely viewable → `POINTER-ONLY` |
| Khan Academy | Site content generally ToS-governed (ARR by default); treat as `restrictive-cc` (CC BY-NC-SA) ONLY where a specific resource is explicitly marked | Per-resource call | Check the SPECIFIC resource, not the site generally. If freely viewable with no mark → `POINTER-ONLY`. If explicitly marked → `INCLUDE-WITH-RESTRICTION` per boundary rule 4 (item beats platform default) |
| Coursera / Udemy / LinkedIn Learning | Platform ToS, all rights reserved, login-gated | `restricted` | `EXCLUDE(license-restricted)` — always, for content AND for a bare "course exists" pointer. Login-gated + ARR on non-primary material never earns a `POINTER-ONLY` consolation entry (boundary rule 5). No signal-of-coverage exception in this station. |
| edX / MITx course content | Generally ToS-restricted despite the open-source delivery platform; a minority of courses are individually CC-marked | `restricted` unless proven otherwise | Default `EXCLUDE(license-restricted)`. Exception: THAT specific course states its own CC license on its own syllabus/license page → judged on the item license, not the platform default (boundary rule 4) → `INCLUDE`/`INCLUDE-WITH-RESTRICTION` per whatever that license actually is. Don't distrust a clean item-level badge just because the platform is normally closed. |
| University departmental lecture-note pages (non-OCW) | Usually no stated license | Undetermined | `POINTER-ONLY` unless a license is stated on the page — absence of a paywall is NOT a license, but absence of a login-gate also means this is NOT `EXCLUDE(license-restricted)`; it's the "freely viewable, no stated license" case |
| "Free course" content farms, SEO listicles, prep/exam-dump vendors | N/A — untiered | Untiered | `EXCLUDE(not-authoritative)` regardless of any license claim made. Authority screens first (boundary rule 1) — never give an untiered source a `POINTER-ONLY` consolation, even if it "signals coverage exists." |

## Quick disposition math

- `permissive-cc` → max `INCLUDE`
- `restrictive-cc` (any NC/SA/ND combination), authoritative source → `INCLUDE-WITH-RESTRICTION`, restriction recorded verbatim (never downgraded — boundary rule 3)
- undetermined / no stated license, freely viewable → `POINTER-ONLY`
- explicit restriction (ARR / login-gated / paywalled) on non-primary material → `EXCLUDE(license-restricted)` (boundary rule 5) — the narrow carve-out to `POINTER-ONLY` applies only when the source is the T1 primary authority with no open substitute anywhere; justify that explicitly if invoked, don't default to it
- untiered authority regardless of license → `EXCLUDE(not-authoritative)` (boundary rule 1) — this screen runs BEFORE the license check, not after
- a specific item's own stated license always overrides its platform's usual default (boundary rule 4)

SA (share-alike) is viral: anything derived from SA-licensed content must itself carry the
same license. Always spell this out in `restriction_detail` so a downstream commercial
consumer of the cellar knows what they inherit, not just that "SA applies."

**The two failure modes this table exists to prevent:**
1. Treating "freely viewable, no license stated" the same as "openly licensed" (it's
   `POINTER-ONLY`, not `INCLUDE`).
2. Treating "explicit restriction" (login gate, paywall, ARR ToS) the same as "no license
   stated" (it's `EXCLUDE(license-restricted)`, not `POINTER-ONLY`). These are different
   facts about a source and get different dispositions — round-1 conflated them.
