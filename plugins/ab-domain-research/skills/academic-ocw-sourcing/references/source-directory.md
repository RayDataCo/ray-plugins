# Standing source directory — academic-ocw-sourcing

Accumulated notes on the recurring sources this station draws from. Update this file as
new per-source quirks are discovered across domain runs; it is not a fixture, it is a
living reference this station's own SKILL.md points to for progressive disclosure.

## T1 sources (primary authority, university/publisher's own courseware)

- **MIT OpenCourseWare** (ocw.mit.edu) — course-by-course browsing; check the license
  footer on each individual course page, not just the site-wide default, since older
  archived courses sometimes carry different terms. Site-wide default is CC BY-NC-SA 4.0
  → `INCLUDE-WITH-RESTRICTION` every time; never downgrade this to POINTER-ONLY for
  carrying NC/SA obligations (boundary rule 3).
- **OpenStax** (openstax.org) — browse by subject; each book's copyright page states the
  exact CC BY version. Strong T1 fit for intro/core curriculum in most quantitative and
  social-science domains.
- **Saylor Academy** (saylor.org) — course catalog by subject; check the specific course's
  license badge, most are CC BY.

## T2 sources (recognized aggregators — license call always made on the underlying item)

- **Open Textbook Library** (open.umn.edu) — aggregates many publishers; ALWAYS click
  through to the individual title's own license statement, never trust the aggregator's
  summary badge alone.
- **MERLOT** / **OER Commons** — similar aggregator caveat; useful for candidate discovery,
  never as the license source of record.
- **GAO / CRS reports**, if one surfaces as an OCW-adjacent candidate in a policy-flavored
  domain — treat as T2 wherever the report's subject matches the fill domain; don't dismiss
  as "not academic courseware" (boundary rule 8 travels here too, even though it's rare in
  this station's usual candidate pool).

## Conditional / per-resource sources

- **Khan Academy** (khanacademy.org) — most content is ToS-governed with no explicit CC
  mark; treat unmarked content as freely-viewable-no-stated-license → `POINTER-ONLY`. Only
  land as content if a SPECIFIC resource carries an explicit CC BY-NC-SA (or similar) mark
  — check the resource itself, not the site's general reputation.
- **edX / MITx** — delivery platform is open-source but course CONTENT is usually
  ToS-restricted (login-gated for graded content, ARR by default) → default
  `EXCLUDE(license-restricted)`. BUT check each course individually first: if that specific
  course states its own CC license on its own page, judge it on that stated license
  (boundary rule 4 — item beats platform default), which can land it as `INCLUDE` or
  `INCLUDE-WITH-RESTRICTION` depending on what the badge says. Don't let "the platform is
  usually closed" override a clean item-level license statement you can actually see.

## Default-EXCLUDE sources (no POINTER-ONLY consolation)

- **Coursera, Udemy, LinkedIn Learning** — all-rights-reserved, login-gated by platform
  ToS. This is an EXPLICIT restriction on non-primary material → `EXCLUDE(license-
  restricted)`, always. Do NOT land a `POINTER-ONLY` entry just because "the course's
  existence signals domain training coverage" — that is the consolation-pointer pattern
  boundary rule 5 exists to forbid. The decision sheet still records the candidate (with
  its EXCLUDE disposition and reason), it just doesn't get a pointer entry treated as
  differently-privileged than any other exclusion.
- **University departmental pages outside a formal OCW program** — this is a DIFFERENT
  case from the platforms above: no login gate, no paywall, just silence on licensing.
  That's "freely viewable, no stated license" → `POINTER-ONLY`, not `EXCLUDE`. Don't
  conflate an unlicensed-but-open page with a gated-and-restricted platform; they get
  different dispositions.
- **"Free course" content farms / SEO listicles / prep-exam-dump vendors** — Untiered
  authority. The authority screen runs FIRST (boundary rule 1): `EXCLUDE(not-
  authoritative)` regardless of any license claim on the page, and regardless of whether
  it "looks" openly licensed. Never a `POINTER-ONLY` consolation for an untiered source —
  pointing at junk is worse than silence.
