---
name: service
description: 'Put the AB Domain Research brigade in service — the on/off switch. "service start" (default) runs the mise readiness gate and, if it passes, declares the brigade ready to take fill orders (which the expo composes across the sourcing stations). "service status" reports readiness. "service end" stands it down. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Domain Research)

Fill-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)). The contract (verbs,
mise gate) is identical across every brigade; only what happens between start and end
differs by kind. In a public pack this brigade's primary path is `fire` (a fill order
straight to the [expo](../expo/)), so service here is thin: it gates readiness and declares
the brigade open.

## Verbs

- **start** (default) — run the mise gate ([../mise/](../mise/)). Any FAIL → refuse to
  serve, report the remedy. Clean (WARNs allowed, stated) → declare in service; fill orders
  can be fired at the expo. If the cellar WARN is active, say fills will return in-answer.
- **status** — re-run mise and report readiness.
- **end** — stand down cleanly.

## The precondition

`service start` is mise-gated. A brigade with a missing station or broken manifest must
not pretend to serve. Mise is the gate; service is the switch it guards.

## Batch mode (when deployed against a cellar + rail)

Deployed in a house, fill orders ride tickets on a rail and `service start` walks the
backlog with the same lock-and-lease discipline the factory uses (ab-company-research is
the live precedent for a fill brigade on a rail). Not the default for a public pack.
