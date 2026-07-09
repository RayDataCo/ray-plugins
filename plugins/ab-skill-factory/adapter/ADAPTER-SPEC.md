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
   the rail) copies `plugins/ab-skill-factory/adapter/rail_adapter.py` verbatim into the new
   brigade's own tree (its `brigade/` dir, next to its stations — matching where the three prior
   hand-rolled copies already lived: `brigade/rail_walk.py`).
2. **Write the stamp.** Immediately after copying, call `stamp(path, stamped_at=<build timestamp>)`
   on the vendored copy. This writes `<path>.stamp.json` beside it — see "Stamp format" below.
   Both the `.py` file and its `.stamp.json` are committed together; the stamp is a build artifact,
   never hand-edited (same discipline as the frontend's embedded-schema test/vocab.json).
3. **The brigade imports it as a plain local module.** `from brigade.rail_adapter import enqueue,
   pull, ack, ...` (or `import rail_adapter` if it sits at the brigade's own top level) — an
   ordinary same-repo import, not a package dependency. Nothing about the module requires
   `ab-skill-factory` to be installed or on `PYTHONPATH`.
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
  "canon": "ab-skill-factory/adapter/rail_adapter.py",
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

## Walker scope on a shared rail (v1.1.0, 2026-07-06)

`pull(..., allowed_artifacts=None, brigade=None)` and `walker_scope_ok(text, allowed_artifacts,
brigade)` scope a walker's scan to its own brigade's tickets. Demonstrated failure this closes:
on the shared house rail, an unscoped oldest-mtime `pull()` leased ANOTHER brigade's queued
ticket, and the pulling brigade's Gate A (correctly strict against its OWN menu) then parked
that perfectly valid ticket as `needs-context`. The filter skips out-of-scope tickets entirely
— never leased, never judged, no work-log residue. `allowed_artifacts` is the walker's own
menu-derived live set (the same source its Gate A uses); `brigade` handles the one artifact
that set cannot scope — `menu` is universally valid, so a menu ticket is matched by its
`subject: brigades/<name>` instead. Both default to None (historical scan-everything behavior)
so single-brigade rails and existing callers are untouched; the CLI exposes them as repeatable
`--allowed-artifact` flags plus `--brigade`.

## Claim model (v1.2.0, 2026-07-08) — rename IS the lock

`pull()` no longer leases a ticket in place. It **claims** the chosen ticket by `os.rename()`-ing it
from the rail root (or a stale claim dir — see "Expired-lease reclaim" below) into
`<rail_dir>/.claimed/<worker>/<same filename>`, and only writes the `status: leased` + `lease:
{...}` block AFTER that rename has succeeded. This replaces the prior check-then-write advisory
lease (read `lease: null` → write a lease block — two separate steps a second walker could land
between) with a single indivisible filesystem operation:

- **Rename is the lock.** POSIX `rename(2)` is atomic: a source path can only ever be consumed by
  one rename call, no matter how many different processes attempt to rename it to different
  destinations at the same instant. If walker A's rename (`ticket.md` → `.claimed/A/ticket.md`)
  completes first, the source no longer exists — walker B's rename attempt (`ticket.md` →
  `.claimed/B/ticket.md`) then fails with `FileNotFoundError`, deterministically, every time. This is
  the check-and-claim in one step: there is no window between "is this ticket free" and "I now own
  this ticket" for a second process to land in.
- **The worker id is the name on the lock.** `worker` (caller-supplied, may embed a session UUID —
  the house convention is a walker instance id, not just a brigade name, precisely so two
  simultaneous walkers of the same brigade get distinct claim dirs) names the claim directory
  directly: `.claimed/<worker>/`. Attribution is structural, not just a frontmatter field — you can
  tell who holds a ticket from its path alone.
- **A lost race is contention, not an error.** `pull()` catches the `FileNotFoundError` from a
  losing rename and moves on to the next oldest-mtime candidate, exactly as it already skips a
  ticket outside the walker's scope or a ticket with a still-live lease. It never raises for this
  case. The candidate that was lost to another walker is left byte-for-byte untouched — no lease, no
  work-log residue — because the losing process's rename never touched it (rename either fully
  succeeds or has no effect on the source).
- **Expired-lease reclaim now also scans claim dirs.** A ticket sitting in ANY `.claimed/<worker>/`
  whose lease has expired (`now > at + ttl_min`) is an equally valid pull candidate — reclaimed via
  the exact same rename mechanism, moving it from the stale worker's claim dir into the new worker's
  (`rail: lease-reclaimed` is still appended, same as before, so the abandonment stays visible in the
  ticket's own history).
- **`ack()`/`release()` follow the file wherever it is.** Non-terminal `ack()` exits
  (`needs-context`/`escalated`) and `release()` both resolve a claimed ticket back to the rail-dir
  root as part of the same call (`os.rename`, same filesystem, safe). Terminal `ack()` exits
  (`done`/`killed`) are unchanged — still copy the bytes to `<cellar_root>/<subject>/tickets/` and
  `unlink()` the source, never `os.rename`, because `cellar_root` can be an entirely different
  top-level directory or mount, and a cross-device `rename(2)` raises `OSError`. A ticket that was
  never claimed in the first place (at rail-dir root already) is left in place by both — the
  claim-return logic is a no-op for it, which is what keeps brigades whose own `pull()`/`ack()`
  never touch `.claimed/` (e.g. `ab-assessment`'s hand-rolled multi-phase driver) fully compatible
  without any change on their side.
- **`list_tickets()` surfaces claimed (in-flight) tickets too**, alongside unclaimed ones at rail-dir
  root. There's no separate "holder" return field — the holding worker IS the
  `.claimed/<worker>/` path segment (or readable straight off the ticket's own `lease.worker`),
  which keeps the return type `list[Path]` and every existing caller's delegation untouched.

**UUID attribution guidance:** since the claim directory name becomes part of the ticket's live
path, pick `worker` values that are unique per *walker process/instance*, not just per brigade —
e.g. `<brigade>-<short-session-uuid>` — so two simultaneous walkers of the same brigade (a real
scenario: a manual dispatch running alongside the scheduled service loop) get distinct claim dirs
and never contend with each other over destination naming. Reusing the exact same `worker` string
across two truly concurrent processes doesn't break claim safety (the RACE is still resolved
correctly by rename atomicity on the SOURCE path), but it does make `.claimed/<worker>/` briefly
ambiguous about which live process a ticket belongs to if you need to debug/kill one of them.

**Honesty, carried forward and narrowed:** this is a genuine atomicity guarantee, not an advisory
one — for **local filesystems**. It does NOT extend to sync-drive-backed rails
(Dropbox/iCloud/OneDrive and similar): those clients reconcile against a remote copy
*asynchronously*, so two machines can each perform a perfectly atomic local rename against their own
stale local view of the directory and both "win" from their own vantage point before the sync client
ever reconciles the conflict — sync-drive rails remain forbidden for this reason, unchanged from the
house's standing filesystem-adapter guidance. Real atomicity *across machines* is still a backend
property this filesystem adapter can't retrofit; it arrives with a transactional backend (RAIL-SPEC
names a Snowflake Stage row-level `UPDATE ... WHERE status='queued' LIMIT 1` as the reference
shape). What DOES change from the prior "v1 honesty" note: **same-brigade multi-walker is now safe
on a local filesystem** — the failure mode that note used to document (two concurrent `pull()` calls
racing between scan and write) no longer exists on local disk. The house's standing
one-service-lock-per-brigade convention (`<rail>/.service/<brigade>.lock`) remains in force as the
FLEET gate (only one scheduled service loop per brigade), but it is no longer the only thing
standing between two walkers and a double-pull — the rename itself now is.

## What's parameterized vs what's fixed

Per TICKET-CONTRACT.md's SF-1 amendment ("a ab-company-research ticket like `artifact:
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
| `skills/service/rail-walk.run.js`'s inline `rail` object + `ticketLint()` | this factory (`ab-skill-factory`) | The JS reference walk's own frontmatter-regex rail ops and Gate-A lint — the two documented drift bugs (2-space-only context-entry parsing, hardcoded artifact enum) live here |

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
