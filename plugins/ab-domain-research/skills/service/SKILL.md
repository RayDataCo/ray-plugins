---
name: service
description: 'Put the AB Domain Research brigade in service — the on/off switch, both halves of the symmetric surface. "service start" (default) runs the mise readiness gate and, if it passes, opens the brigade: the fire path (fill orders straight to the expo — the default wherever no rail/cellar is wired) or the rail path (house deployments — walk the rail via the vendored discipline-rail-walk driver, ack on the discipline exit set). "service status" reports readiness. "service end" stands it down via the stop flag. Use when the user says "put the brigade in service", "start the brigade", "walk the rail", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Domain Research)

Fill-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs,
mise gate, stop-flag teardown) is identical across every brigade; only what happens between
start and end differs by kind. **Both halves ship** (the symmetry guarantee,
[AGENT-BRIGADE-STANDARD](../../../ab-skill-factory/AGENT-BRIGADE-STANDARD.md)): the fire
path is always available; the rail path sits vendored and stamped, waiting for a house
deployment. Mise tells you which mode you're standing in.

## Declared runtime dependencies (what `mise` checks for THIS brigade)

| dependency | why | mise check |
|---|---|---|
| stations + expo + MENU.md present | the expo composes the sourcing stations on every fill | one `path_exists` per roster station + expo/menu/manifest checks |
| walk driver + vendored adapter, unmodified | the rail half: [discipline-rail-walk.run.js](./discipline-rail-walk.run.js) + [vendor/rail_adapter.py](./vendor/rail_adapter.py) — byte-identical copies of factory canon, never hand-edited | `walk-driver-present` (FAIL) + `vendor_stamp` on both (drift = FAIL) |
| Claude Code session with the **Workflow tool** | the driver is a Workflow script, not a node script — no fs/env access; every rail mutation happens inside an `agent()` call | agent-verified at `start` (rail path only) |
| `python3` on PATH | the walk's `agent()` calls shell to the vendored rail-port CLI (`vendor/rail_adapter.py {pull,append,ack,release}`) for every rail read/mutation | implied — mise's own engine runs on it |
| `node` on PATH | lint-time only: `node --check` on the driver; the walk runtime does not need it | `walk-driver-syntax` (WARN; node absent = same WARN) |
| `CELLAR_ROOT` set + writable | where fills land | `cellar-root-writable` (WARN — unset = in-answer fills, honest) |
| rail dir reachable + writable | pull/lease/ack (house deployments only) | `rail-root-writable` (WARN — unwired = fire-only mode, honest) |

## Verbs

Invoked as `service [start|status|end]`. **No argument → `start`.**

### `start` (default)

1. **Mise gate** ([../mise/](../mise/)): any FAIL → refuse to serve, report the remedy.
   Clean (WARNs allowed, stated) → open the brigade. If the cellar WARN is active, say
   fills will return in-answer.
2. **Fire path** — the default wherever the rail/cellar ports are unwired (mise reports
   them unconfigured-with-remedy): declare in service; fill orders go straight to the
   [expo](../expo/).
3. **Rail path** (house deployments, rail + cellar wired): take the service lock
   (`{rail_dir}/.service/ab-domain-research.lock` — held by a live walker → say "already
   in service", stop), then invoke the harness Workflow
   tool on [discipline-rail-walk.run.js](./discipline-rail-walk.run.js) with args
   `{"brigade": "ab-domain-research", "plugin_dir": {absolute installed plugin root},
   "cellar_root": {cellar root}, "rail_dir": {rail dir}}`. The driver pulls-with-lease
   scoped to the menu's live artifact types, hands each Order to the expo, lands the
   result, and acks per the exit mapping below. One honest note on kind: this is a fill
   brigade — a rail Order here is usually "stock the cellar for domain X", so the serve
   step lands fill artifacts per the stations' own landing conventions
   (`$CELLAR_ROOT/competencies/{domain}/` + the `SOURCING-DECISIONS-{date}.md` sheet —
   see [MENU.md](../../MENU.md) "Where fills land"); the driver's generic
   `{cellar}/{subject}/artifacts/{ticket-id}-answer.md` path is the fallback for
   question-shaped tickets.

### Exit mapping (discipline exit set → rail ack)

| expo exit | rail ack | meaning |
|---|---|---|
| `answered` | `advance` | fill complete; ticket files to its subject |
| `partial-with-gaps` | `advance` | terminal with declared gaps (work log + artifact name them) — not rework |
| `needs-clarification` | `reroute-to-steward` | itemized questions on the work log; stays on the rail |
| `out-of-scope` | `kill` | work log names why + the right brigade if known |

### `status`

Re-run mise and report readiness; on a rail, add walk state (stop flag pending? current
lease?).

### `end`

Stand down via the **stop flag** (`{rail dir}/.service/ab-domain-research.stop`), issuable
from any session. The walker honors it **between tickets, never mid-ticket**: the current
ticket is finished or its lease is released with a work-log notation of exactly where it
stopped — the append-only work-log is the resume state. Then remove the lock + flag —
never leave the lock behind. In fire-only mode there is no walker; `end` simply stands
the brigade down.

## The precondition

`service start` is mise-gated. A brigade with a missing station, a drifted vendor copy, or
a broken manifest must not pretend to serve. Mise is the gate; service is the switch it
guards.
