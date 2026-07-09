---
name: mise
description: >-
  Readiness check for the ab-registrar — "is front of house ready?" (mise en
  place, before intake). Runs the vendored static engine (mise.py against
  mise.toml) plus the agent-executor checks it can't do itself (env-root
  agreement, published menus readable), and merges both into one
  PASS/WARN/FAIL/UNCHECKED report. Use when the founder says "run the
  registrar's mise", "is the registrar ready", or before a steward intake
  session. A FAIL anywhere means front of house must refuse intake — no
  ticket gets hung against an unreachable rail or a mispointed cellar.
---

# mise — the registrar's readiness check

The registrar is a **house role** (BRIGADE-INTERFACE.md, house-role amendment 2026-07-06):
no walk, no stations, no service lock. Its readiness question is narrower than a kitchen's —
*can front of house reach the rail and cellar, is the vendored canon undrifted, and is there
at least one menu to serve from?* — and this skill answers exactly that, nothing more.

## Procedure

1. **Static engine:** run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/mise/mise.py"` — reads
   [mise.toml](./mise.toml) (the single source of truth for the check list; this prose is
   documentation of it, not an independent source). `mise.py` is the vendored canon engine —
   stamped via `mise.py.stamp.json`, never hand-edited.
2. **Agent checks** (the static engine reports these `UNCHECKED (agent)`; verify each
   yourself and merge into the report):
   - `cellar-env-agrees` — read `$CELLAR_ROOT` from the session env; compare (after `~`
     expansion) to `[roots].cellar`. Disagreement = FAIL with both values shown.
   - `published-menus-readable` — glob `{cellar}/brigades/*/menu.md`; parse each
     frontmatter (`menu_of`, `version`, `source_hash` present). Zero menus or all
     defective = WARN with the registry verb's discovery-ticket remedy.
3. **One merged report**, engine rows + agent rows, same PASS/WARN/FAIL vocabulary.
   Any FAIL → front of house refuses intake; print the remedy lines.
