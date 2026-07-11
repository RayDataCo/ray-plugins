---
name: service
description: 'Put the AB Legal brigade in service — the on/off switch over both halves of the surface. "service start" (default) runs the mise readiness gate and, if it passes, opens the brigade: fire path (requests straight to the expo — the default where no rail/cellar is wired) or rail path (house deployments — walk the rail via the vendored canon driver). "service status" reports readiness and walker state. "service end" stands it down via the stop flag. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Legal)

Discipline-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs,
mise gate, stop-flag teardown) is identical across every brigade; only the walk differs.
Per the symmetry guarantee (AGENT-BRIGADE-STANDARD), this brigade ships **both halves**:
fireable expo, queueable walk. Everything served on either path stays **structural, not
advisory** — the stations check documents against explicit enumerated standards and report
coverage/gaps; the brigade never gives legal advice, opines on fairness/lawfulness, or
makes a compliance determination.

## Verbs

- **start** (default) — run the mise gate ([../mise/](../mise/)). Any FAIL → refuse to
  serve, report the remedy. Clean → open the brigade on whichever path the deployment
  supports (below). If already in service, say so and do nothing.
- **status** — re-run mise and report readiness; on the rail path, also report walker
  state (current ticket, processed count, stop flag pending?).
- **end** — stand down cleanly. On the rail path: write the stop flag at
  `{rail_dir}/.service/ab-legal.stop`; the walker honors it **between tickets, never
  mid-ticket** — the current Order is finished or its lease released before stand-down.
  Then remove the lock + stop flag — never leave the lock behind.

## The two paths

- **Fire path** (always available; the default where no rail/cellar is wired — a public
  install): requests go straight to the [expo](../expo/), which composes the stations and
  answers in-session. `service start` here just gates readiness and declares the brigade
  open.
- **Rail path** (house deployments): `service start` takes the service lock
  (`{rail_dir}/.service/ab-legal.lock` — held by a live walker → say "already in service",
  stop), then invokes the harness **Workflow tool**
  on [discipline-rail-walk.run.js](./discipline-rail-walk.run.js) — the vendored canon
  driver — with args:

  | arg | value |
  |---|---|
  | `brigade` | `ab-legal` |
  | `plugin_dir` | absolute installed plugin root (the directory containing `MENU.md`) |
  | `cellar_root` | the cellar root path |
  | `rail_dir` | the rail directory |

  The driver pulls-with-lease scoped to the menu's live artifact types, hands each Order
  to the expo, lands the answer at `{cellar_root}/{subject}/artifacts/`, and acks on the
  discipline exit mapping:

  | expo exit | rail ack |
  |---|---|
  | `answered` | `advance` |
  | `partial-with-gaps` | `advance` (gaps recorded in the work log + answer) |
  | `needs-clarification` | `reroute-to-steward` |
  | `out-of-scope` | `kill` (work log names why + the right brigade if known) |

**Walk port (2026-07-11 convergence — factory WALK-SPEC.md):** pass `allowed_artifacts`
(the MENU's live artifact-type strings) in the driver args — the invoking session reads
MENU.md anyway to gate service; without the arg the driver spends one agent call deriving
it. This Workflow driver is the walk port's HARNESS-NATIVE adapter (agents execute the
vendored adapter CLI and report its output verbatim; the script owns every judgment). The
port's Python REFERENCE adapter is vendored at [vendor/walk.py](./vendor/walk.py) — a
deployment with a Python process should prefer it (`Walk(WalkConfig)` +
`make_expo_dispatcher(run_agent, ...)` per its module docstring); mise checks both copies'
stamps.

  Where the rail/cellar ports are unwired, mise reports them as unconfigured-with-remedy
  and fire-only is the honest mode — a deployment posture, not a packaging gap.

## Declared runtime dependencies (the manifest `mise` and the serving session check)

| dependency | why | check |
|---|---|---|
| `python3` on PATH | the driver's rail reads/mutations shell to the vendored adapter CLI ([vendor/rail_adapter.py](./vendor/rail_adapter.py)); the mise engine itself runs on it | `command -v python3` — verified by the serving session at `start` |
| harness **Workflow tool** | `discipline-rail-walk.run.js` is a Workflow script, executed by the harness — not by `node` | verified by the serving session at `start` (rail path only) |
| vendored copies match canon | both the adapter and the driver are byte-identical stamped copies of ab-skill-factory canon — build artifacts, never hand-edited | `vendor_stamp` checks in [../mise/mise.toml](../mise/mise.toml) |

## The precondition

`service start` is mise-gated. A brigade with a missing station, drifted vendor copy, or
broken manifest must not pretend to serve. Mise is the gate; service is the switch it
guards.
