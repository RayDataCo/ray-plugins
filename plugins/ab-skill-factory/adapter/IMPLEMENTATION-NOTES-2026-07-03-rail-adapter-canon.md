# Implementation notes — rail_adapter canon v1 (2026-07-03)

Founder-directed build: extract the single canonical rail-port implementation BRIGADE-INTERFACE.md's
"Adapter distribution" section calls for, killing the 3+-way hand-rolled drift across the house
brigades (the 7/2 Acme shakedown's "inherited fix" was the receipt that made the drift visible).

## What landed

| artifact | role |
|---|---|
| `adapter/rail_adapter.py` | NEW — the canon: stdlib-only rail port (list/enqueue/pull/append/ack/release/find_unclosed/stamp) + Gate A `ticket_lint` (8 rules), with both known drift bugs fixed |
| `adapter/ADAPTER-SPEC.md` | NEW — vendoring procedure, stamp format, the honest lease caveat, parameterized-vs-fixed table, supersedes table |
| `adapter/tests/` | NEW — pytest, tmp_path-only; 61 tests, all green |
| this file | design rationale, deviations, limitations, open questions |

## Reading order for this build

RAIL-SPEC.md + TICKET-CONTRACT.md + BRIGADE-INTERFACE.md's "Adapter distribution" section (specs);
`company-research-workspace/brigade/rail_walk.py` (Company Research), `sales-collateral-workspace/
brigade/rail_walk.py` + `brigade/batch.py` (Sales-Collateral), `assessment-workspace/
brigade/pass_driver.py` (Assessment), `skills/service/rail-walk.run.js`'s inline `rail` object (this
factory's JS walk) — the four prior implementations this canon supersedes. Two real filed tickets
for shape truth: `cellar/brigades/skill-agent-brigade/tickets/factory-menu-restamp-2026-07-03.ticket.md`
(2-space-indent context entries) and `cellar/rail/acme-collateral-stress-2026-07-02.ticket.md`
(0-indent context entries, `type: cellar`, folded/quoted `when:` values — the shape that exposed the
parser drift).

## The one big fork the task didn't hand me: none of the three Python references are usable as-is

All three Python references (`rail_walk.py` ×2, `pass_driver.py`) `import yaml` and call
`yaml.safe_dump`/rely on a full YAML parse for frontmatter access. That's disqualified outright by
the stdlib-only, marketplace-vendoring constraint (`mise.py`'s own docstring makes the identical
argument for why its declaration format is TOML, not YAML — "YAML has no stdlib parser"). So for the
actual *mechanics* of frontmatter read/write, the true prior art is the **JS reference**
(`rail-walk.run.js`'s `fm`/`fmField`/`setFmField`/`contextEntries` + `rail` object), ported to
Python — with its two documented drift bugs fixed. The three Python references still won almost
every *behavioral* decision below (lease-expiry reclaim, append-section semantics, subject
resolution, the five-exit map) — they just couldn't donate their literal frontmatter-access code.

## Decisions — which reference won, and why

1. **Frontmatter access: JS reference's regex-and-string-surgery approach, ported to Python.**
   Only flat scalar fields (`ticket`/`artifact`/`status`/`lease`/`subject`) are read/written;
   everything else in the frontmatter is left untouched. This is the only stdlib-compatible option
   — see above. `set_field()`/`get_field()` are direct ports of `setFmField`/`fmField`.

2. **Context-entry parsing: NEW indent-agnostic entry-boundary scanner — drift fix (a).** The JS
   reference's `contextEntries()` splits on `/^\s{2}- /m` — hardcoded 2-space indent. That's exactly
   why the acme ticket (0-indent `context:\n- id: ...`, a legal YAML block-sequence-at-mapping-
   indent PyYAML itself emits) silently produced ZERO parsed entries under the old logic: zero
   entries means zero eager sources checked, meaning rule 5 always trivially "passed" on that shape
   — a false green, not a real check. Fix: `parse_context_entries()` finds entry boundaries by
   scanning for `- id:` lines regardless of leading whitespace (`_ENTRY_START_RE`), and
   `_context_block()` extracts the raw `context:` lines by walking forward from the `context:` key
   until a line that is neither blank, indented, nor a 0-indent dash — i.e., the next real top-level
   key. Both real tickets lint 8/8 under this parser (`test_factory_menu_shape_2space_indent_lints_8_of_8`,
   `test_acme_shape_0indent_context_lints_8_of_8`).

3. **`allowed_artifacts`/`resolver_types` as parameters — drift fix (b), per TICKET-CONTRACT's own
   SF-1 amendment text.** The JS reference hardcoded `['skill', 'brigade', 'menu']` directly into
   `ticketLint()` — TICKET-CONTRACT.md documents this as the exact stress-test finding that broke a
   company-research ticket (`artifact: company-jobs-snapshot`) against a contract that was supposed
   to be universal. None of the three Python references got this right either, independently, in
   their own way: each just hardcodes its OWN brigade's `ARTIFACT_REQUIRED_FIELDS`/menu instead of
   accepting the caller's menu as a parameter (fine for a single-brigade rail_walk.py, wrong for a
   shared canon). This module makes both `allowed_artifacts` and `resolver_types` parameters,
   defaulting to *this* brigade's own live menu — proven by `test_menu_driven_artifact_enum_accepts_and_rejects`,
   which lints the SAME acme ticket text twice and gets opposite Gate-A-rule-2 verdicts depending
   on which menu is passed.

4. **`append()`/section-boundary rewriting: Company Research / Sales-Collateral's `_append_to_section`
   wins over the JS reference's insert-before-`## Artifacts`.** The JS reference's `append()` does
   `text.slice(0, idx) + line + '\n' + text.slice(idx)` where `idx = text.indexOf('## Artifacts')` —
   it never looks at section boundaries, just the literal string `## Artifacts`. Traced by hand: every
   call inserts one NEW blank line right before `## Artifacts`, so N appends leave N accumulated
   blank lines between work-log bullets instead of the consecutive-bullets-then-one-blank-line shape
   the real filed tickets actually show (`factory-menu-restamp` and `acme-collateral-stress` both
   have zero blank lines between their own work-log bullets, one blank line before `## Artifacts`).
   The Python references' `_append_to_section()` is section-heading-aware (find `## Work log`'s own
   span via `_h2_line_indices`, strip trailing blank lines from the existing section content, append
   the new line, re-add exactly one blank-line separator) — ported here as `_append_to_section()`,
   generalized slightly (targets any named H2 section by regex-found position rather than a
   precomputed line-index list, but same normalize-then-append shape). `test_append_never_corrupts_
   existing_lines` asserts no `\n\n\n` ever appears after repeated appends — the JS behavior would
   fail that assertion by the third call.

5. **`pull()`: oldest-mtime-first scan + lease-expiry reclaim — Company Research / Sales-Collateral
   win over the JS reference.** The JS reference's `pull()` walks `readdirSync()` order (whatever the
   OS returns) and explicitly punts expired-lease reclaim to "a human sweep" (its own module comment).
   RAIL-SPEC's lease-semantics section is unambiguous that this is NOT optional — "Expired leases
   make the ticket workable again — the next `pull` may reclaim it (and appends a `lease-reclaimed`
   entry...)" — so the JS behavior is a documented-but-real gap, not a legitimate alternative. Both
   Python `rail_walk.py` copies implement oldest-mtime-first (`sorted(..., key=lambda p:
   p.stat().st_mtime)`) as "a reasonable FIFO proxy" (their own comment) plus reclaim-on-expiry; ported
   directly. `test_pull_reclaims_expired_lease` and `test_pull_picks_oldest_mtime_queued_first` cover
   both halves.

6. **Lease TTL default: 60 minutes, not 120 — Python references win, spec is silent on the number.**
   A genuine disputed VALUE, not just a disputed pattern: `rail-walk.run.js` hardcodes `LEASE_TTL_MIN
   = 120`; both Python `rail_walk.py` copies independently default to `DEFAULT_LEASE_TTL_MIN = 60`.
   TICKET-CONTRACT/RAIL-SPEC don't pin a number at all. Per this build's own judgment rule ("where the
   spec is silent, prefer the ACF implementation... note the choice"): two independent Python
   references agreeing on 60 outweighs the one JS reference's 120, so `DEFAULT_LEASE_TTL_MIN = 60`
   here. It's a parameter either way (`pull(..., ttl_min=...)`) — this is only the *default*.

7. **Five-exit → status map: unanimous, straight from TICKET-CONTRACT/RAIL-SPEC prose.** All four
   references agree: `advance→done`, `kill→killed`, `reroute-to-steward→needs-context`,
   `escalate→escalated`. No dispute here — `STATUS_BY_EXIT` is a direct transcription.

8. **Filing-to-subject: current spec prose wins over all four references, which predate the
   2026-07-03 scan-only simplification.** This is the one place where NONE of the four references is
   actually current. `rail-walk.run.js`'s own comment already reads "on `done`/`killed` also files the
   ticket to its subject" (correct, matches today's spec) — but the two `rail_walk.py` copies and
   `pass_driver.py`'s docstring both still talk about a `runner`/notification gap that a since-dropped
   pass-shelf-pointer design was meant to fill (BRIGADE-INTERFACE.md's close-out contract was rewritten
   TWICE on 2026-07-03 itself — first to a pass-shelf pointer draft, then to the scan-only design this
   canon implements — mid-session, confirmed by re-reading RAIL-SPEC.md/BRIGADE-INTERFACE.md partway
   through this build and finding the pass-shelf language gone). `ack()` here does exactly what the
   CURRENT spec says and no more: clear the lease, append the ack line, and on a TERMINAL exit
   (`done`/`killed` only) file to `<cellar_root>/<subject>/tickets/<id>.ticket.md` — no pointer file
   anywhere. `find_unclosed()` (new, see decision 11) is the entire discovery mechanism.

9. **Subject resolution: TICKET-CONTRACT's own prose wins over both Python references' narrower
   rules.** TICKET-CONTRACT.md's `subject:` field documentation is explicit: "optional... Fallback
   when absent: derived from the first cellar-typed context source." Company Research's
   `_resolve_subject()` implements a fallback, but a `companies/<id>`-shaped one specifically (its own
   docstring flags this as "something to fold into TICKET-CONTRACT.md proper, not decided
   unilaterally" — i.e., even that reference doesn't claim its version is the final word). Its Sales-
   Collateral fork DROPS the fallback entirely (explicit field only). Since this canon has to serve
   every cellar section (`companies/`, `assessments/`, `brigades/`, `competencies/` — CELLAR-SPEC's
   organization table), `_resolve_subject()` here generalizes the fallback to the first TWO path
   segments of the first `type: cellar` source's ref (`<section>/<key>`), matching the spec prose
   without being company-research-specific. `test_ack_derives_subject_from_first_cellar_source_when_
   no_explicit_field` exercises this against an `assessments/...` ref, not a `companies/...` one, on
   purpose.

10. **Lease encoding: single-line JSON — a new choice, no reference to arbitrate.** None of the two
    real filed tickets shows what a LIVE lease looks like on disk (both show `lease: null` — neither
    was ever actually mid-lease when filed/escalated at their captured snapshot). The three Python
    references write `lease` as a native nested YAML mapping via `yaml.safe_dump` — unavailable here.
    `lease: {"worker": "...", "at": "...", "ttl_min": N}` (single-line JSON) is a legal YAML flow
    mapping, so it doesn't break the ticket's YAML-ness, and `json.loads`/`json.dumps` do the encode/
    decode work instead of a hand-rolled nested-mapping parser. Documented as a new convention this
    canon introduces, not a ported one.

11. **`find_unclosed()`: authored fresh against the current spec text — no reference implementation
    existed.** This op postdates all four references (it's the discovery mechanism for the
    2026-07-03 scan-only close-out design, steward SKILL.md's "The close-out sweep" section).
    Implementation: `cellar_root.rglob("tickets/*.ticket.md")`, filtered to `mtime` within
    `since_days`, `status` in `{done, killed}`, and no line matching `^[ \t]*-\s*close-out:`.

12. **Gate B / mechanical floors / multi-phase pass choreography: deliberately NOT ported.** Company
    Research's `_gate_b_floor()`, Sales-Collateral's `refire_rounds` dict, and all of
    `pass_driver.py`'s `PassState`/phase-chaining/inner-rail fan-out are per-brigade WALK concerns
    (BRIGADE-INTERFACE.md: "the walk's *orchestration* is per-brigade... [that] is not" the rail-
    adapter's job) — out of scope for a rail-PORT canon by the task's own framing. Gate B itself
    (phase-0 sufficiency) is an LLM judgment call per TICKET-CONTRACT.md, not a deterministic check a
    stdlib module should approximate; this canon stops at Gate A.

## Deviations from the four references (beyond the two named drift fixes)

- **`now` is a parameter, not always `datetime.now()`.** Every mutating op (`append`/`pull`/`ack`/
  `release`/`enqueue`) accepts an optional `now: str | None` ISO string, defaulting to the real clock.
  None of the four references needed this (the JS reference takes `args.now` from its Workflow-tool
  caller since workflow scripts can't call `Date.now()`; the Python references just call
  `datetime.now()`/`now_iso()` inline). Added here purely for deterministic, hermetic tests — every
  timing-sensitive test in `tests/` passes a fixed `now` rather than sleeping or racing the real clock.
- **`stamp()` is new** — none of the four references vendor themselves; this is this canon's own
  distribution mechanism (BRIGADE-INTERFACE.md "Adapter distribution"), modeled on `skills/mise/
  mise.py`'s `check_vendor_stamp` check type's expected `sha256` field so the two are drop-in
  compatible without `mise.py` needing changes.
- **Rule 1's uniqueness check is a `startswith(f"{id}.")` heuristic, ported as-is from the JS
  reference** rather than tightened to an exact `{id}.ticket.md` match. Kept for parity with the
  documented reference behavior; flagged below as a known limitation, not silently "fixed" without
  discussion since it's a real (if narrow) behavior change.

## Known limitations (stated honestly, not fixed in v1)

- **Flat-fields-only frontmatter.** `context:` is read-only; any field this module doesn't
  specifically read/write (`menu`, `requested_by`, `type_hint`, `audience`, `kind`, `refire_rounds`,
  house extensions) survives untouched but is also invisible to this module's own logic. A brigade
  that needs to branch on one of those fields reads the raw text itself.
- **`when:` folded/quoted YAML scalars are read for their first physical line only.** Sufficient for
  every Gate-A check here (presence, "starts with always") but not a faithful reconstruction of a
  wrapped, `\u`-escaped string. Do not use this module to re-emit a `when:` value verbatim.
  Documented in the module docstring and here rather than silently truncating without a trace.
- **Advisory lease — scan-then-write race window.** See ADAPTER-SPEC.md's "honest lease caveat"
  section in full; not re-litigated here.
- **Subject-derivation assumes a 2-segment canonical key (`<section>/<key>`).** True for every
  section CELLAR-SPEC.md documents today (`companies/<id>`, `assessments/<subject>`,
  `brigades/<name>`, `competencies/<domain>`). If a 3+-segment canonical-key convention is ever
  introduced, `_resolve_subject()`'s fallback needs revisiting — flagged, not guessed at pre-emptively.
- **No live verification of `url`/`mcp`/`qmd` sources.** Gate A rule 5 only checks `file`/`cellar`
  refs against the local filesystem; live source types are steward-side per TICKET-CONTRACT's own
  rule-5 note, unchanged from the JS reference's stance.
- **Filesystem mtime resolution bounds `pull()`'s FIFO ordering.** Two tickets enqueued within the
  same mtime tick (coarse on some filesystems) tie-break in whatever order `Path.glob` returns, not a
  guaranteed enqueue-order FIFO. Same limitation both Python references carry ("a reasonable FIFO
  proxy," their words).

## Open questions for the founder

1. **Rule 1's `startswith` uniqueness heuristic** — tighten to an exact `{id}.ticket.md` match now
   that this is a shared canon (vs. kept for JS-reference parity)? Low-stakes either way; a ticket id
   that's a strict prefix of another (`foo` / `foo-bar`) is the only case where the current behavior
   over-counts.
2. **`stamp()`'s `version` parameter currently must be passed explicitly by the vendoring build** to
   mean anything beyond "the version this exact module file declares." Once multiple canon versions
   exist across brigades (post-retrofit), should there be a central canon-version registry `stamp()`
   reads instead of trusting the caller?
3. **`find_unclosed()`'s `since_days=30` default** — pin a house-wide number in RAIL-SPEC/steward
   SKILL.md, or leave it purely an adapter-level default the steward's sweep cadence overrides per
   call? Currently the latter, un-blessed by any spec text.
4. **Gate A rule 5's `cellar_root=None` fallback passes eager `type: cellar` sources rather than
   failing closed.** Chosen so `ticket_lint()` stays usable in a lightweight context that doesn't care
   about cellar-relative verification (e.g., a quick shape check), but it is a real judgment call, not
   a spec-mandated default — flagging rather than asserting it's obviously right.
5. **The retrofit pass itself** (swap the three brigades' hand-rolled rail code for a vendored copy of
   this canon, all four suites green) is out of scope for this build per the task's own framing
   ("sequenced after the founder's P1 port validates") — this canon is ready to be vendored, but no
   existing brigade has been touched yet.
