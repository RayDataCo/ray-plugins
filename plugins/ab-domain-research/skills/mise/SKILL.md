---
name: mise
description: 'Readiness check for the AB Domain Research brigade — "is the brigade ready?" (mise en place, before service). Runs the vendored engine (mise.py against mise.toml) and reports PASS/WARN/FAIL: are the sourcing stations installed, the expo and menu present, the manifest valid, and CELLAR_ROOT reachable (the fill landing target — WARN if unset, the brigade then serves in-answer only). Use when the user says "run mise", "is the brigade ready", "readiness check", or as the precondition gate before serving. A FAIL means fix the named remedy before serving.'
---

# mise — readiness check (AB Domain Research)

"Mise en place — everything in its place before service." Before this brigade serves, mise
answers "are you ready?" deterministically. Fill-brigade implementation of the standard
`mise` command (canon [BRIGADE-INTERFACE](../../../ab-skill-factory/BRIGADE-INTERFACE.md)).

For this brigade the checks are pack integrity (live stations, expo, menu, manifest) plus
the one environment check a fill brigade needs: **is there a cellar to land in?**
`CELLAR_ROOT` is read from the environment via `[roots]` — unset, the check reports WARN
with its remedy (the brigade still serves, returning fills in-answer). This is the
"does this work in YOUR environment" onboarding gate in its smallest honest form.

## Source of truth

[mise.toml](./mise.toml) is the single source of truth. Edit checks there.

## Running it

```
python3 skills/mise/mise.py skills/mise/mise.toml
```

Relative targets resolve against `skills/mise/`, so the pack is portable — no absolute paths.

## Severity contract

- **FAIL** — cannot serve reliably (a live station, expo, menu, or manifest missing/broken).
- **WARN** — runs, but degraded (no cellar: fills return in-answer instead of landing).
- **PASS** — ready.

Exit codes: 0 clean, 1 any FAIL, 2 malformed declaration.
