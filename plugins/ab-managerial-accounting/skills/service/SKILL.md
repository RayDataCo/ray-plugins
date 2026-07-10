---
name: service
description: 'Put the AB Managerial Accounting brigade in service — the on/off switch over both halves of the brigade surface. "service start" (default) runs the mise readiness gate and, if it passes, opens the brigade: fire path (requests straight to the expo, which composes across the finance stations) always; rail path (walk a queue of tickets) where a rail and cellar are wired. "service status" reports readiness and walker state. "service end" stands it down via the stop flag. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Managerial Accounting)

This is the discipline-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs, mise
gate, stop-flag teardown) is identical across every brigade; only the walk between start and end
differs by brigade kind. Per the symmetry guarantee (AGENT-BRIGADE-STANDARD), this brigade ships
**both halves**: the fireable expo and the queueable rail walk.

## Verbs

Invoked as `service [start|end|status]`. **No argument → `start`** — unless already in service,
in which case say so and do nothing.

- **start** (default) — run the mise gate ([../mise/](../mise/)). Any FAIL → refuse to serve and
  report the remedy. If clean, open the brigade on whichever path the deployment supports (below).
- **status** — re-run mise and report readiness; when walking a rail, also report the current
  ticket, tickets served, and whether a stop is pending.
- **end** — stand down cleanly. On the rail path: write the stop flag
  (`{rail_dir}/.service/ab-managerial-accounting.stop`); the walker honors it **between tickets,
  never mid-ticket** — the in-flight ticket is finished or its lease released with a work-log note
  of where it stopped. Then remove the lock + stop flag — never leave the lock behind. On the fire
  path there is nothing to drain; just declare the brigade closed.

## The precondition

`service start` is mise-gated. This is the non-negotiable: a brigade with a missing station or a
broken manifest must not pretend to serve. Mise is the gate; service is the switch it guards.

## Two paths, one surface

- **Fire path (the default where no rail/cellar is wired).** Requests go straight to the
  [expo](../expo/), which decomposes each request and composes across the finance stations —
  including compound asks (a full due-diligence picture) that fire several stations plus a
  finishing synthesis. A public-pack install serves this way; mise reports the unwired rail/cellar
  ports with configure-remedies, and fire-only is the honest mode, not a failure.
- **Rail path (house deployments).** Where a rail and cellar are wired, `service start` takes the
  service lock (`{rail_dir}/.service/ab-managerial-accounting.lock` — held by a live walker → say
  "already in service" and stop), then walks the
  queue: invoke the harness **Workflow tool** on
  [discipline-rail-walk.run.js](./discipline-rail-walk.run.js) (vendored canon driver, stamped)
  with args:

  ```
  brigade:     "ab-managerial-accounting"
  plugin_dir:  {absolute path of this installed plugin's root}
  cellar_root: {cellar root}
  rail_dir:    {rail directory}
  ```

  The driver pulls-with-lease scoped to the menu's live artifact types, hands each Order to the
  expo, lands the composed answer at `{cellar_root}/{subject}/artifacts/`, and acks per the exit
  mapping below. Every rail mutation shells to the vendored adapter
  ([vendor/rail_adapter.py](./vendor/rail_adapter.py)) — the driver itself never touches the rail.

## Discipline exit mapping (expo exit → rail ack)

| expo exit | ack | meaning |
|---|---|---|
| `answered` | `advance` | done; ticket files to its subject |
| `partial-with-gaps` | `advance` | terminal answer with declared gaps — recorded in the work log and the artifact, not rework |
| `needs-clarification` | `reroute-to-steward` | needs context; stays on the rail for the steward |
| `out-of-scope` | `kill` | work log names why, and the right brigade if known |

## Declared runtime dependencies (what `mise` checks for THIS brigade)

The source of truth is [../mise/mise.toml](../mise/mise.toml); this table is its human-readable
mirror.

| dependency | why | check |
|---|---|---|
| the five finance stations + expo + MENU.md | what the expo composes; the roster it reads | `path_exists` per station (FAIL) |
| Claude Code session with the **Workflow tool** | the rail walk is a Workflow script, executed by the harness — **not** by `node` | agent-verified at `start` (rail path only) |
| `python3` on PATH | the walk's `agent()` calls run the vendored adapter CLI for every rail read/mutation | stdlib engine runs on it |
| `node` on PATH | lint-time only — `node --check` on the walk driver | `command_on_path` (WARN) |
| vendored driver + adapter match their stamps | no drift from canon, no hand-edits | `vendor_stamp` (WARN) |
| rail dir reachable + writable | pull/lease/ack | `path_*` (WARN + configure-remedy) |
| cellar root reachable + writable | answer artifacts land there | `path_*` (WARN + configure-remedy) |

Credentials: none — these are pure-computation finance stations.
