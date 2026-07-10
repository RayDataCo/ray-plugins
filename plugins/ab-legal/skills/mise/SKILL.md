---
name: mise
description: 'Readiness check for the AB Legal brigade — "is the brigade ready?" (mise en place, before service). Runs the vendored engine (mise.py against mise.toml) and reports PASS/WARN/FAIL: are the two live stations installed, the expo and menu present, the manifest valid. Use when the user says "run mise", "is the brigade ready", "readiness check", or as the precondition gate before serving. A FAIL means fix the named remedy before serving.'
---

# mise — readiness check (AB Legal)

"Mise en place — everything in its place before service." Before this brigade serves, mise
answers "are you ready?" deterministically. Discipline-brigade implementation of the
standard `mise` command (canon [BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)).

This is the onboarding gate. For this brigade the checks are pack integrity (the two live
stations, expo, menu, manifest). A legal brigade that later gained a connector (a contract
repository, an e-signature platform) would grow an `executor="agent"` reachability check
and become the load-bearing "does this work in YOUR environment" gate.

## Source of truth

[mise.toml](./mise.toml) is the single source of truth. Edit checks there.

## Running it

```
python3 skills/mise/mise.py skills/mise/mise.toml
```

Relative targets resolve against `skills/mise/`, so the pack is portable — no absolute paths.

## Severity contract

- **FAIL** — cannot serve reliably (a live station, expo, menu, or manifest missing/broken).
- **WARN** — runs, but degraded.
- **PASS** — ready.

Exit codes: 0 clean, 1 any FAIL, 2 malformed declaration.
