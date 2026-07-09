---
name: mise
description: 'Readiness check for the AB Managerial Accounting brigade — "is the brigade ready?" (mise en place, before service). Runs the vendored engine (mise.py against mise.toml) and reports PASS/WARN/FAIL per check: are all five finance stations installed, the expo and menu present, the manifest valid. Use when the user says "run mise", "is the brigade ready", "readiness check", or as the precondition gate before serving requests. A FAIL means the brigade cannot serve reliably — fix the named remedy first.'
---

# mise — readiness check (AB Managerial Accounting)

"Mise en place — everything in its place before service." Before this brigade serves a
request, mise answers "are you ready?" with a deterministic report, not a vibe. This is
the discipline-brigade implementation of the standard `mise` command (canon
[BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)).

This is the onboarding gate — the thing that separates a delivery-grade brigade from a
skill pack thrown over the wall. For this brigade the checks are pack integrity (all
stations present, expo + menu + manifest intact). The moment a discipline pack has a
connector (a warehouse, a ticket system), mise grows a reachability check and becomes the
load-bearing "does this actually work in YOUR environment" gate.

## Source of truth

[mise.toml](./mise.toml) is the single source of truth for this brigade's checks. Edit
checks there; this SKILL.md is documentation of what's there, not a second list.

## Running it

```
python3 skills/mise/mise.py skills/mise/mise.toml
```

The engine (`mise.py`, vendored from ab-skill-factory canon, zero pip deps) runs each
`[[checks]]` entry and prints a PASS/WARN/FAIL line with the declared remedy on any
non-pass. Relative targets resolve against `skills/mise/`, so the pack is portable — no
absolute paths.

## Severity contract

- **FAIL** — the brigade cannot serve reliably (a station missing, the expo or menu gone,
  a malformed manifest). Do not serve until fixed.
- **WARN** — runs, but degraded (e.g. the base-model-covered registry missing — coverage
  claims unavailable, but the stations still work).
- **PASS** — ready.

Exit codes: 0 clean, 1 any FAIL, 2 malformed declaration.
