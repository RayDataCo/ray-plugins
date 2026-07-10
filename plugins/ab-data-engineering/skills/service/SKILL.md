---
name: service
description: 'Put the AB Data Engineering brigade in service — both halves of the symmetric surface. "service start" (default) runs the mise readiness gate and, if it passes, opens the brigade: fire path (requests straight to the expo — the default where no rail/cellar is wired) or rail path (house deployments — walk the rail via the vendored discipline walk driver). "service status" reports readiness and walker state. "service end" stands down via the stop flag. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Data Engineering)

Discipline-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs, mise
gate, stop-flag teardown) is identical across every brigade; only the walk differs by kind.
Both halves ship (the symmetry guarantee): the **fire path** — a request straight to the
[expo](../expo/) — stays the default wherever no rail/cellar is wired, and the **rail path**
walks a rail in a house deployment via the vendored canon driver packaged in this skill.

## Verbs

Invoked as `service [start|end|status]`. **No argument → `start`** — unless the service lock
is already held, in which case report "already in service" and do nothing.

- **start** (default) — run the mise gate ([../mise/](../mise/)). Any FAIL → refuse to serve,
  report the remedy. Clean → the brigade is open:
  - **fire path** (no rail/cellar wired — the honest public-pack mode, and what mise reports):
    requests go straight to the expo, which composes across the stations.
  - **rail path** (house deployments): take the service lock
    (`{rail_dir}/.service/ab-data-engineering.lock`), then invoke the harness **Workflow
    tool** on [discipline-rail-walk.run.js](./discipline-rail-walk.run.js) with args:
    `brigade: "ab-data-engineering"`, `plugin_dir` (this plugin's installed root, absolute),
    `cellar_root`, `rail_dir`. The driver pulls-with-lease scoped to the menu's **live**
    artifact types (one live station today: `pipeline-failure-triage` — the held /
    weak-evidence / base-model-covered rows on [MENU.md](../../MENU.md) are not leaseable
    work, and the expo reports their status honestly rather than faking a station), hands
    each Order to the expo, lands the answer at `{cellar_root}/{subject}/artifacts/`, and
    acks per the exit mapping below. On any exit, release per `end` — never leave the lock.
- **status** — read-only: re-run mise and report readiness; on a rail, also lock present?
  current ticket (work-log tail), processed count, stop flag pending?
- **end** — stand down cleanly. On a rail: write the stop flag
  (`{rail_dir}/.service/ab-data-engineering.stop`); the walker honors it **between tickets,
  never mid-ticket** — the current ticket is finished or its lease released with a work-log
  notation of where it stopped (the append-only work-log is the resume state). Then drop
  lock + flag.

## The precondition

`service start` is mise-gated. A brigade with a missing station or broken manifest must not
pretend to serve. Mise is the gate; service is the switch it guards. Unwired rail/cellar
ports are WARN, not FAIL — fire-only is an honest mode, not a broken one.

## Discipline exit mapping (what the walker acks)

The expo's decision surface maps to the rail's dispositions:

| expo exit | ack | meaning |
|---|---|---|
| `answered` | `advance` | done; ticket files to its subject |
| `partial-with-gaps` | `advance` | terminal answer with declared gaps — recorded in the work log + answer artifact, not rework |
| `needs-clarification` | `reroute-to-steward` | needs context; stays on the rail for the steward |
| `out-of-scope` | `kill` | work log names why, and the right brigade if known |

## Declared runtime dependencies (what `mise` checks for THIS brigade)

| dependency | why | check |
|---|---|---|
| Claude Code session with the **Workflow tool** | the walk driver is a Workflow script, executed by the harness — **not** by `node` | rail path only; fire path needs no extra runtime |
| `python3` on PATH | the driver's `agent()` calls shell to the vendored adapter CLI ([vendor/rail_adapter.py](./vendor/rail_adapter.py)) for every rail read/mutation | `command -v python3` |
| `node` on PATH | lint-time only, for `node --check` on the driver | `node-on-path` (WARN) |
| walk driver + vendored adapter present, stamps fresh | both are byte-identical vendored copies of factory canon — never hand-edited | `vendor_stamp` checks |
| rail root reachable + writable | pull/lease/ack | WARN + configure remedy |
| cellar root reachable + writable | answer landing + menu publication | WARN + configure remedy |

The source of truth is [../mise/mise.toml](../mise/mise.toml); this table is its
human-readable mirror.
