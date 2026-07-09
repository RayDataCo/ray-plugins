---
name: service
description: 'Put the AB Managerial Accounting brigade in service — the on/off switch. "service start" (default) runs the mise readiness gate and, if it passes, declares the brigade ready to take requests (which the expo then composes across the finance stations). "service status" reports readiness. "service end" stands it down. Use when the user says "put the brigade in service", "start the brigade", "is the brigade in service", or "stop the brigade". Start is mise-gated: a FAIL means the brigade refuses to serve.'
---

# service — the brigade's serving lifecycle (AB Managerial Accounting)

This is the discipline-brigade implementation of the standard `service` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/)). The contract (verbs, mise gate) is
identical across every brigade; only what happens between start and end differs by
brigade kind.

For the **factory** brigade, service attaches to a rail and walks a backlog of build
tickets. For a **discipline** brigade, the primary path is `fire` — an ad-hoc request
handed straight to the [expo](../expo/), which composes the stations. So service here is
thin: it gates readiness and declares the brigade open, rather than walking a persistent
queue.

## Verbs

- **start** (default) — run the mise gate ([../mise/](../mise/)). If mise returns any
  FAIL, refuse to serve and report the remedy. If clean, declare the brigade in service:
  requests can now be fired at the expo.
- **status** — report whether the brigade is ready (re-run mise) and, if deployed against
  a cellar, where the walker is.
- **end** — stand the brigade down cleanly.

## The precondition

`service start` is mise-gated. This is the non-negotiable: a brigade with a missing
station or a broken manifest must not pretend to serve. Mise is the gate; service is the
switch it guards.

## Batch mode (when deployed against a cellar)

The common consumption path is `fire` (one request → expo → composed answer), which needs
no rail. When this brigade is deployed against a cellar with a rail, `service start` can
instead walk a backlog of fired requests the same way the factory walks build tickets —
same lock-and-lease discipline. That path is available but not the default for a public
pack, which has no cellar.
