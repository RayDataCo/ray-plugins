---
name: service
description: 'Put the AB Marketing brigade in service — the on/off switch over both halves of the surface. "service start" (default) runs the mise readiness gate and, if it passes, opens the brigade: the fire path (requests straight to the expo — the default where no rail/cellar is wired) or the rail path (house deployments — walk the rail via the vendored canon driver). "service status" reports readiness. "service end" stands it down via the stop flag. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Marketing)

Discipline-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs,
mise gate, stop-flag teardown) is identical across every brigade; both halves of the
symmetry guarantee ship here — fireable and queueable.

## Verbs

- **start** (default) — run the mise gate ([../mise/](../mise/)). Any FAIL → refuse to
  serve, report the remedy. Clean → open on whichever path is wired (below). Lock already
  held → say "already in service", do nothing.
- **status** — re-run mise and report readiness: in service? stop pending?
- **end** — stand down: drop the stop flag at `{rail_dir}/.service/ab-marketing.stop`.
  The walker honors it **between tickets, never mid-ticket** — the current ticket finishes
  or its lease is released with a work-log note of exactly where it stopped. Then remove
  the lock + stop flag — never leave the lock behind.

## Two paths, one switch

- **Fire path (default — public install, no rail/cellar wired):** requests go straight to
  the [expo](../expo/), which composes the marketing stations. Mise reports the unwired
  ports with remedies; fire-only is the honest mode, not a defect.
- **Rail path (house deployments):** take the service lock (`{rail_dir}/.service/ab-marketing.lock` — held by a live walker → say "already in service", stop), then invoke the harness Workflow tool on
  [discipline-rail-walk.run.js](./discipline-rail-walk.run.js) with args: `brigade`
  `"ab-marketing"`, `plugin_dir` (absolute installed plugin root), `cellar_root`,
  `rail_dir`. The driver pulls-with-lease scoped to the menu's live artifact types, hands
  each Order to the expo, lands the answer at `{cellar_root}/{subject}/artifacts/`, and
  acks per the mapping below.

## Discipline exit mapping (expo exit → rail ack)

| expo exit | ack |
|---|---|
| answered | advance |
| partial-with-gaps | advance (gaps recorded in work log + answer artifact) |
| needs-clarification | reroute-to-steward |
| out-of-scope | kill |

## Declared deps (what mise checks)

| dependency | used by | check |
|---|---|---|
| `python3` | the vendored rail adapter ([vendor/rail_adapter.py](./vendor/rail_adapter.py)) | on PATH |
| harness Workflow tool | the walk driver (discipline-rail-walk.run.js runs via Workflow, not node) | agent-verified |
| vendored copies match canon | adapter + driver, stamped from ab-skill-factory canon — never hand-edited | vendor_stamp |
