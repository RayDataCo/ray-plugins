---
name: mise
description: Readiness check for the ab-skill-factory — "is the brigade ready?" (mise en place, before service). Runs the static engine (mise.py against mise.toml) plus the agent-executor checks it can't do itself (Workflow tool, station skills), and merges both into one PASS/WARN/FAIL/UNCHECKED report. Use when the founder says "run mise", "is the brigade ready", "readiness check", or as the precondition gate before `service start`. A FAIL anywhere means this brigade must refuse service.
---

# mise — readiness check

> Deviation from IMPLEMENTATION-PLAN.md: the plan specifies a `mise.yaml` declaration. This
> brigade instead ships `mise.toml`, parsed with the stdlib `tomllib` (python 3.11+). YAML has
> no parser in the standard library, and `mise.py` must run with **zero pip dependencies** — it
> is meant to be vendored into every brigade this factory builds (same "vendored from canon,
> version+hash stamped" move as `rail_adapter.py`, per BRIGADE-INTERFACE.md's "Adapter
> distribution" section), so it has to work on a bare `python3` with nothing installed. TOML is
> the only stdlib-parseable structured format that fits. Full writeup:
> [IMPLEMENTATION-NOTES-2026-07-03-mise-build.md](./IMPLEMENTATION-NOTES-2026-07-03-mise-build.md).

This is the factory brigade's implementation of the standard `mise` command
([BRIGADE-INTERFACE.md](../../BRIGADE-INTERFACE.md)). "Mise en place — everything in its place
before service": before a brigade goes `service start`, mise answers "are you ready?" with a
deterministic report, not a vibe.

## Source of truth (Decision D1, 2026-07-03)

**[mise.toml](./mise.toml) is the single source of truth for this brigade's readiness checks.**
[skills/service/SKILL.md](../service/SKILL.md)'s declared-deps table is a human-readable summary
of what's declared here — if the two ever disagree, `mise.toml` wins; fix the table, not the
declaration. Adding, removing, or changing a check means editing `mise.toml`, not the prose.

## The two-tier check split

Every check in `mise.toml` has an `executor`:

- **`executor = "script"`** — `mise.py` can verify it deterministically: paths exist/writable,
  a command resolves on PATH, a file parses, a vendored file's hash matches its stamp. Run these
  with `python3 mise.py` (no arguments needed — it defaults to the `mise.toml` sitting next to
  it, i.e. this directory).
- **`executor = "agent"`** — only the calling agent (this skill's procedure) can verify it:
  Workflow-tool callability, a harness skill resolving (`~/.claude/skills/station-*`), model
  access, MCP connectivity. `mise.py` always reports these as `UNCHECKED (agent)` — it never
  guesses at them.

## Procedure

1. **Run the static engine.**
   ```
   python3 mise.py
   ```
   (or `python3 skills/mise/mise.py` from the plugin root, or pass an explicit declaration path
   as the first argument). This is the default, static-only run — no paid or live probes, per
   Decision D3: `service start` gates on this tier alone, because a model outage will surface on
   ticket 1 anyway and gating every start on live probes burns tokens for nothing.

2. **Perform the agent-executor checks yourself.** For each `UNCHECKED (agent)` row in the
   engine's output, verify it directly and record PASS/WARN/FAIL:
   - **`workflow-tool-callable`** — confirm the Workflow tool is present in this session's tool
     config (it's what runs [rail-walk.run.js](../service/rail-walk.run.js)).
   - **`station-*-present`** (`station-spec-author`, `station-test-author`,
     `station-code-author`, `station-critic`) — confirm each harness skill resolves: the
     directory under `~/.claude/skills/<name>/` exists and its `SKILL.md` is readable/parseable.
     These are harness skills, not files in this plugin, so only the agent can see them.

3. **Merge into one report.** Combine the engine's script-check rows with your agent-check
   verdicts into a single table (same PASS/WARN/FAIL/UNCHECKED shape). Print the declared
   `remedy` for every non-PASS row — pull it straight from `mise.toml`, don't paraphrase it.

4. **Apply the FAIL rule.** **Any FAIL anywhere in the merged report — script or agent-executor —
   means this brigade must refuse `service`.** Say so plainly and stop; don't proceed to
   `service start` with a FAIL outstanding. WARN rows don't block service; they're behind or
   degraded but runnable (Decision D2: a stale vendor stamp is a WARN, not a FAIL — a brigade
   running an older vendored copy still runs correctly on its own copy, it's just behind).

5. **Report.** When invoked ad hoc ("run mise", "is the brigade ready"), return the merged report
   directly to the caller. When invoked as part of `service start`'s mise gate
   ([service/SKILL.md](../service/SKILL.md) step 2), append the report to the service journal
   instead.

## `--live` (paid/slow probes)

```
python3 mise.py --live
```

`mise.py` **never performs live probes itself** — no model calls, no MCP round-trips; those are
always `executor = "agent"` entries with `mode = "live"` in the declaration (this brigade's
`mise.toml` currently declares none — the factory's stations make no external calls; see
"Credential checks" below). `--live` just adds a section to the static report listing which
declared checks are tagged `mode = "live"`, so the calling agent knows which ones to go probe
itself and fold into the merged report. Everything else about the run is identical to the
default — `--live` is additive, not a different mode.

## Credential checks

**None needed for this brigade.** The factory's own stations (steward, expo,
spec/test/author/critic) operate entirely on local ticket and cellar state — no external API
calls, no MCP servers, from this brigade's own build line. Domain brigades that DO call external
APIs/MCP servers will declare `executor = "agent"` credential-resolvable-by-name checks in their
own `mise.toml` when they're retrofitted with the standard five-command interface
(BRIGADE-INTERFACE.md) — credentials are checked **by name only, never printed**.

## `--json`

```
python3 mise.py --json
```

Machine-readable form of the same static report — `{declaration, checks[], summary, exit_code}`.
Use this when merging programmatically rather than reading the human table.

## Exit codes (static engine only — the merged report's FAIL rule in step 4 still governs)

- `0` — no FAIL among the script checks.
- `1` — at least one script check is FAIL.
- `2` — engine error: the declaration is missing, isn't valid TOML, or doesn't match the check
  schema (missing field, unknown check type, duplicate id, ...). Fix `mise.toml`, don't retry.

An exit code of `0` from the static engine is **not** the same as "the brigade is ready" — step 2
(agent-executor checks) still has to clear before `service start` proceeds.

## Cross-references

- [BRIGADE-INTERFACE.md](../../BRIGADE-INTERFACE.md) — the standard `mise` contract this
  implements, and the two-gate (deterministic-first, judgment-second) shape it's modeled on.
- [mise.toml](./mise.toml) — this brigade's declaration (D1 source of truth).
- [mise.py](./mise.py) — the check engine (stdlib-only; see the module docstring for the full
  check-type reference).
- [skills/service/SKILL.md](../service/SKILL.md) — `service start` step 2 is this mise gate; its
  declared-deps table summarizes (but does not duplicate the authority of) `mise.toml`.
- [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md) — the founder-approved plan this skill
  implements (D1/D2/D3 decisions, check taxonomy, build sequence).
- [IMPLEMENTATION-NOTES-2026-07-03-mise-build.md](./IMPLEMENTATION-NOTES-2026-07-03-mise-build.md)
  — build decisions, the yaml→toml deviation in full, v1 simplifications, open questions.
