---
name: mise
description: 'Readiness check for the AB Marketing brigade — "is the brigade ready?" (mise en place, before service). Runs the vendored engine (mise.py against mise.toml) and reports PASS/WARN/FAIL: is the live station installed, the expo and menu present, the manifest valid. Use when the user says "run mise", "is the brigade ready", "readiness check", or as the precondition gate before serving. A FAIL means fix the named remedy before serving.'
---

# mise — readiness check (AB Marketing)

"Mise en place — everything in its place before service." Before this brigade serves, mise
answers "are you ready?" deterministically. Discipline-brigade implementation of the
standard `mise` command (canon [BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)).

For this brigade the checks are pack integrity (the live station, expo, menu, manifest).
As each held-for-refire station lands, it brings its own station-present check with it —
the roster and the gate grow together.

## Source of truth

[mise.toml](./mise.toml) is the single source of truth. Edit checks there.

## Running it

```
python3 skills/mise/mise.py skills/mise/mise.toml
```

Relative targets resolve against `skills/mise/`, so the pack is portable — no absolute paths.

## Severity contract

- **FAIL** — cannot serve reliably (the live station, expo, menu, or manifest missing/broken).
- **WARN** — runs, but degraded.
- **PASS** — ready.

Exit codes: 0 clean, 1 any FAIL, 2 malformed declaration.
