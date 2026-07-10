---
name: service
description: 'Put the AB Marketing brigade in service — the on/off switch. "service start" (default) runs the mise readiness gate and, if it passes, declares the brigade ready to take requests (which the expo composes across the marketing stations). "service status" reports readiness. "service end" stands it down. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Marketing)

Discipline-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs,
mise gate) is identical across every brigade; only what happens between start and end
differs by kind. A discipline brigade's primary path is `fire` (an ad-hoc request straight
to the [expo](../expo/)), so service here is thin: it gates readiness and declares the
brigade open.

## Verbs

- **start** (default) — run the mise gate ([../mise/](../mise/)). Any FAIL → refuse to
  serve, report the remedy. Clean → declare in service; requests can be fired at the expo.
- **status** — re-run mise and report readiness.
- **end** — stand down cleanly.

## The precondition

`service start` is mise-gated. A brigade with a missing station or broken manifest must
not pretend to serve. Mise is the gate; service is the switch it guards.

## Batch mode (when deployed against a cellar)

The common path is `fire` (one request → expo → composed answer), no rail needed. Deployed
against a cellar, `service start` can walk a backlog of fired requests with the same
lock-and-lease discipline the factory uses. Not the default for a public pack.
