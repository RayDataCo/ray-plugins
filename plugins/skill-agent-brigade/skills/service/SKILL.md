---
name: service
description: Put the skill-agent-brigade in service — attach to the rail and walk it (start, default), stand down cleanly (end), or report the walker's state (status). Start is mise-gated and takes the rail service lock; end finishes-or-releases the current ticket, notates resumable state to its work-log, and drops the lock. Use when the founder says "put the brigade in service", "start the rail walk", "stop the brigade", or "is the brigade in service?".
---

# service — the brigade's rail-attachment lifecycle

This skill is the factory brigade's implementation of the standard `service` command
([BRIGADE-INTERFACE.md](../../BRIGADE-INTERFACE.md)). The *contract* (verbs, lock, teardown
semantics) is identical across every house brigade; only the walk implementation differs per
brigade. This brigade's walk is [rail-walk.run.js](./rail-walk.run.js), packaged inside this skill.

## Declared runtime dependencies (what `mise` checks for THIS brigade)

| dependency | why | check |
|---|---|---|
| Claude Code session with the **Workflow tool** | `rail-walk.run.js` is a Workflow script — it is executed by the harness's Workflow tool, **not** by `node` directly | Workflow tool callable |
| `node` on PATH | only for `node --check` syntax validation of the walk script (lint-time, not run-time) | `command -v node` |
| rail root reachable + writable | pull/lease/ack | probe write |
| cellar root reachable + writable | artifact landing + menu | probe write |

*(A Python-walk brigade declares `python3` + its venv here instead — the manifest is per-brigade,
the checking discipline is the standard. This table is the pattern the other brigades copy.)*

## Verbs

Invoked as `service [start|end|status]`. **No argument → `start`** — unless the service lock is
already held, in which case report "already in service" (lock holder, since when) and do nothing.

### `service start` (default)

1. **Lock check:** if `<rail>/.service/skill-agent-brigade.lock` exists and its holder is live →
   report "already in service", stop. This lock is what upgrades the filesystem rail from
   *one-walker-by-convention* to **one-walker-enforced** (see RAIL-SPEC's advisory-lease honesty note).
2. **Mise gate:** run the readiness checks against the declared-dependency table above. Any FAIL →
   refuse to start, print the remedy lines. (Until a standalone `mise` skill ships, this step IS the
   mise check — same table, same discipline.)
3. **Take the lock:** write `{brigade, started_at, session, walker}` JSON to the lock path.
4. **Walk:** invoke the Workflow tool on [rail-walk.run.js](./rail-walk.run.js) in bounded cycles
   (one backlog sweep per invocation). Between cycles, check for the stop flag
   (`<rail>/.service/skill-agent-brigade.stop`); absent → sweep again after the polling interval.
5. **On any exit** (stop flag, error, session end): release per step "end" below — never leave the
   lock behind.

### `service end`

Graceful stand-down — may be issued from the walking session or any other session (it signals via
the stop flag):

1. Write the stop flag. The walker honors it **between tickets, never mid-ticket** — the current
   ticket is finished or its lease is released.
2. If a lease is released un-finished: append a work-log event to the ticket recording exactly where
   it stopped (phase, round, last station) — the append-only work-log is the resume state; the next
   `service start` (or another walker on an atomic rail) picks it up from the notation.
3. Remove the lock + stop flag; append a service-session close line (tickets processed, wall-clock)
   to `<rail>/.service/journal.md`.

### `service status`

Read-only: lock present? (holder, since when) · current ticket + phase (from its work-log tail) ·
tickets processed this session (journal) · stop flag pending?

## Failure honesty

- Two `start`s racing on the *filesystem* rail can still interleave between the lock check and
  write (no atomic mkdir guard yet) — same advisory caveat as the rail lease itself. Real atomicity
  arrives with the Snowflake rail adapter; the lock is a big honesty upgrade, not a distributed-systems
  guarantee.
- `end` from another session requires the walker to *reach* a between-tickets checkpoint; a hung
  station call means waiting or killing the session (which releases nothing — run `service status`
  then clean up per RAIL-SPEC's expired-lease guidance).

## Cross-references

- [BRIGADE-INTERFACE.md](../../BRIGADE-INTERFACE.md) — the standard contract this implements
- [RAIL-SPEC.md](../../RAIL-SPEC.md) — pull/lease/ack the walk rides on
- [rail-walk.run.js](./rail-walk.run.js) — this brigade's walk (Workflow script, moved here from
  `workflow/` 2026-07-03 for skill-contained packaging per founder)
