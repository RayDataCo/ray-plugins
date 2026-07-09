# The Rail Adapter — vendoring spec

`rail_adapter.py` (this directory) is the canonical, single implementation of the rail port
(RAIL-SPEC.md) + Gate A ticket validity (TICKET-CONTRACT.md's `ticketLint`, 8 rules) against the v1
filesystem/vault backend (CELLAR-SPEC.md). This doc is the short version: how a brigade gets a copy,
what the stamp means, what's honest about the lease, and what's a parameter vs what's fixed. Full
design rationale and per-decision reasoning: [IMPLEMENTATION-NOTES-2026-07-03-rail-adapter-canon.md](./IMPLEMENTATION-NOTES-2026-07-03-rail-adapter-canon.md).

## Vendoring procedure

Per BRIGADE-INTERFACE.md "Adapter distribution — vendored from canon": every brigade the factory
builds ships through the Claude plugin marketplace and must be self-contained — no shared pip
package, no separately-installed CLI. So the rail port is not *imported* across brigades; it's
*copied*, once per brigade, at build time:

1. **Copy the file.** `artifact: brigade` (and `add-station`/`iterate-brigade` re-wires that touch
   the rail) copies `plugins/skill-agent-brigade/adapter/rail_adapter.py` verbatim into the new
   brigade's own tree (its `brigade/` dir, next to its stations — matching where the three prior
   hand-rolled copies already lived: `brigade/rail_walk.py`).
2. **Write the stamp.** Immediately after copying, call `stamp(path, stamped_at=<build timestamp>)`
   on the vendored copy. This writes `<path>.stamp.json` beside it — see "Stamp format" below.
   Both the `.py` file and its `.stamp.json` are committed together; the stamp is a build artifact,
   never hand-edited (same discipline as the frontend's embedded-schema test/vocab.json).
3. **The brigade imports it as a plain local module.** `from brigade.rail_adapter import enqueue,
   pull, ack, ...` (or `import rail_adapter` if it sits at the brigade's own top level) — an
   ordinary same-repo import, not a package dependency. Nothing about the module requires
   `skill-agent-brigade` to be installed or on `PYTHONPATH`.
4. **Never hand-edit a vendored copy.** If a brigade needs different behavior, that's a signal the
   canon needs a new parameter (see "What's parameterized" below), not a local fork. A fork is
   exactly the drift this canon exists to kill.
5. **`mise` closes the loop.** Each brigade's `mise.toml` declares a `vendor_stamp` check
   (`skills/mise/mise.py`'s `check_vendor_stamp`) comparing the vendored copy's live sha256 against
   the stamp's recorded one, and — once canon versions are tracked centrally — the stamp's `version`
   against the current canon `ADAPTER_VERSION`. A stale vendor copy tells on itself at `mise` time
   with a concrete remedy ("adapter vN, canon vM — re-stamp via `iterate-brigade`").

## Stamp format

`stamp(path, *, version=None, stamped_at=None)` writes `<path>.stamp.json`:

```json
{
  "file": "rail_adapter.py",
  "canon": "skill-agent-brigade/adapter/rail_adapter.py",
  "version": "1.0.0",
  "sha256": "<sha256 of the vendored file's current bytes>",
  "stamped_at": "2026-07-03T14:28:29-04:00"
}
```

- `canon` is a fixed pointer back to this file's home in the marketplace plugin — the thing every
  vendored copy is a stamped copy *of*.
- `version` defaults to the module's own `ADAPTER_VERSION` constant; a build should pass it
  explicitly once a central canon-version registry exists, so a re-stamp can detect "vendored copy
  is behind canon" (`version` mismatch) separately from "vendored copy has been hand-edited"
  (`sha256` mismatch against a copy that still claims the current version).
- `stamped_at` is accepted from the caller rather than always derived internally — a vendoring
  build's own timestamp is the single source of truth for "when was this brigade last synced to
  canon," not a second clock reading taken inside the stamping call.

## The honest lease caveat

`pull()`'s lease is **advisory, not atomic** — this is RAIL-SPEC's own "v1 honesty" note, and this
adapter does not paper over it. A markdown file has no compare-and-swap: `pull()` scans the rail
directory, picks a candidate, then writes a `status: leased` + `lease: {...}` update to that one
file. Two concurrent `pull()` calls against the *same* rail directory can still race in the gap
between the scan and the write and both come away believing they leased the same ticket.

What the lease *does* buy you:

- **Detection, not prevention.** A ticket that already carries a live (unexpired) lease is skipped by
  `pull()` — a second walker sees the lease and moves on, rather than silently double-processing the
  ticket. The failure mode this adapter can't prevent is the *race at the instant of leasing*, not a
  walker knowingly grabbing an already-leased ticket.
- **Visible abandonment.** An expired lease (now > `at + ttl_min`) makes the ticket workable again;
  reclaiming it appends a `lease-reclaimed` work-log line, so an abandoned ticket's history shows
  exactly that it was abandoned and by whom, rather than silently vanishing and reappearing.
- **The house convention that makes this safe today:** RAIL-SPEC and `service`/SKILL.md's own
  service-lock (`<rail>/.service/<brigade>.lock`) both lean on **one walker per rail by convention**
  — this adapter's advisory lease is the second, cheaper layer under that convention, not a
  replacement for it.

Real atomicity is a backend property, not something this filesystem adapter can retrofit: it arrives
with a transactional backend (RAIL-SPEC names a Snowflake Stage row-level `UPDATE ... WHERE
status='queued' LIMIT 1` as the reference shape). Until then: one walker per rail, and read this
section again before assuming otherwise.

## What's parameterized vs what's fixed

Per TICKET-CONTRACT.md's SF-1 amendment ("a company-research ticket like `artifact:
company-jobs-snapshot` failed a contract it should satisfy" — artifact vocabularies belong to
menus, not the envelope), this canon draws a hard line between what the *ticket envelope* fixes and
what the *target brigade's menu* decides:

| | fixed by this module | parameterized (caller-supplied) |
|---|---|---|
| Ticket shape | id/status/lease/context envelope, the four H2 sections, in order | — |
| Gate A rule count/order | all 8 rules always run, same numbering | — |
| `artifact` validity | — | `allowed_artifacts` (`ticket_lint`/`enqueue`) — defaults to *this* brigade's own live menu (`skill`/`brigade`/`menu`/`add-station`/`iterate-skill`); every other brigade passes its own |
| `context[].type` validity | — | `resolver_types` — defaults to the house-wide registered set (`file`/`url`/`mcp`/`qmd`/`cellar`) |
| Where `type: cellar` refs resolve | — | `cellar_root` (`ticket_lint`/`enqueue`/`ack`) |
| Five-exit → status map | `advance→done`, `kill→killed`, `reroute-to-steward→needs-context`, `escalate→escalated` | — (this is TICKET-CONTRACT's own contract, not a per-brigade choice) |
| Filing-to-subject on terminal ack | `done`/`killed` only; subject = explicit `subject:` field, else first `type: cellar` source's `<section>/<key>` | — |
| Lease TTL | — | `ttl_min` (`pull`), per-call |
| Timestamps | — | `now` (every op that appends/mutates) — defaults to the real clock; tests pass a fixed ISO string |

Never hardcoded as a "universal" enum: `allowed_artifacts` and `resolver_types`. This is drift fix
(b) — the JS reference (`rail-walk.run.js`) hardcoded `['skill', 'brigade', 'menu']` into what was
supposed to be a domain-agnostic envelope check; this canon makes both a parameter with this
brigade's own menu as the *default*, never the *only* valid set.

## What this adapter does not attempt

- **No full YAML parsing/re-serialization.** Flat scalar fields only; `context:` is read-only; long
  folded YAML scalars are read for their first line only. See the module docstring's "Frontmatter
  handling" note and IMPLEMENTATION-NOTES for the honesty write-up.
- **No live resolution of `url`/`mcp`/`qmd` sources.** Gate A rule 5 only verifies `file`/`cellar`
  refs locally; live source types are steward-side per TICKET-CONTRACT's own rule-5 note.
- **No pass-shelf pointer.** Per the founder's 2026-07-03 scan-only simplification, `ack()` files a
  terminal ticket to its subject and nothing else — no `<rail>/pass/<id>.done` pointer is written.
  `find_unclosed()` is the entire discovery mechanism for the steward's close-out sweep.
- **No Gate B (phase-0 sufficiency).** That's a judgment call an LLM makes reading the Order +
  eager sources (TICKET-CONTRACT.md) — outside a deterministic, stdlib-only module's scope by
  design.

## Supersedes

This canon replaces the rail-adapter portions (enqueue / pull-with-lease / append / ack /
file-to-subject) of:

| implementation | brigade | what it hand-rolled |
|---|---|---|
| `brigade/rail_walk.py` | Company Research (`company-research-workspace`) | `RailClient` — enqueue/pull/ack/release/append/list + a mechanical Gate-B floor, on top of PyYAML (`yaml.safe_dump`) |
| `brigade/rail_walk.py` (+ `brigade/batch.py`) | Sales-Collateral (`sales-collateral-workspace`) | An explicit fork-with-two-departures of the Company Research copy (per-artifact `refire_rounds`, an `ack(artifact_refs=...)` enhancement) — its own docstring calls out the shared-lib debt directly |
| `brigade/pass_driver.py` (+ rail helpers) | Assessment (`assessment-workspace`) | Multi-phase pass choreography riding the same `RailClient`/`Ticket` shape, plus its own `_pull_or_continue`/`_gate_a_recheck`/`_dispatch_and_close` primitives |
| `skills/service/rail-walk.run.js`'s inline `rail` object + `ticketLint()` | this factory (`skill-agent-brigade`) | The JS reference walk's own frontmatter-regex rail ops and Gate-A lint — the two documented drift bugs (2-space-only context-entry parsing, hardcoded artifact enum) live here |

None of the four are deleted by this doc — the retrofit pass (swap each brigade's hand-rolled rail
code for a vendored copy of this canon, all four suites green) is a separate, sequenced build ticket
(BRIGADE-INTERFACE.md "Adapter distribution," status note). This spec is what that retrofit vendors
*from*.

## Cross-references

- [RAIL-SPEC.md](../RAIL-SPEC.md) — the port this implements
- [TICKET-CONTRACT.md](../TICKET-CONTRACT.md) — the envelope, Gate A's 8 rules, the five exits
- [CELLAR-SPEC.md](../CELLAR-SPEC.md) — the filesystem backend + subject-filing convention
- [BRIGADE-INTERFACE.md](../BRIGADE-INTERFACE.md) — "Adapter distribution — vendored from canon"
- [skills/mise/mise.py](../skills/mise/mise.py) — the `vendor_stamp`/`menu_freshness` check types this
  stamp format is designed to be checked by
- [IMPLEMENTATION-NOTES-2026-07-03-rail-adapter-canon.md](./IMPLEMENTATION-NOTES-2026-07-03-rail-adapter-canon.md) — full design rationale, deviations, open questions
