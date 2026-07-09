# mise v1 build — implementation notes (2026-07-03)

Build against [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md) (founder-approved) and the
declared decisions D1/D2/D3. Deliverables: [mise.py](./mise.py) (engine), [mise.toml](./mise.toml)
(factory declaration), [SKILL.md](./SKILL.md) (procedure), [tests/](./tests/) (pytest suite).

## Deviation from plan: yaml → toml (stdlib-only constraint)

The plan (§ "Shape: one engine, one declaration, per brigade") specifies `mise.yaml`. **This was
overridden per explicit founder-approved build instruction** for one hard reason: `mise.py` has a
zero-pip-dependency requirement — it's meant to be vendored into every brigade this factory
builds, the same "vendored from canon, version+hash stamped" move as `rail_adapter.py`
(BRIGADE-INTERFACE.md, "Adapter distribution" section) — and it must run on a **bare python3**
with nothing installed. Python's standard library has no YAML parser (PyYAML is a third-party
package); it does have `tomllib` as of 3.11. TOML also has a natural `[[array-of-tables]]` shape
for a list of check entries, and a `[roots]` table for the re-pointable path config, so nothing
about the plan's information shape was lost — only the serialization format changed.

Practical consequences of the switch:
- The declaration file is `mise.toml`, not `mise.yaml`, everywhere (this dir, and every future
  vendored copy in domain brigades).
- Parsed via `tomllib.load()` in binary mode (`tomllib` requires `"rb"` file objects) — this is
  the one place the engine is version-gated: **python 3.11+ required**. Verified the sandbox runs
  3.14.4; if a target environment runs an older python3, that's a real prerequisite gap the
  engine can't route around without a pip dependency (which would defeat the point).
- `[roots]` is a flat `key = "path"` table (rail, cellar for this brigade). Check `target` fields
  reference roots via `{name}` placeholder substitution (`resolve_path_target()` in mise.py) —
  plain `str.replace`, no templating library needed. This is also what satisfies the plan's "make
  paths a config section so other installs can re-point" note: re-pointing a brigade to a
  different cellar/rail install is a one-line edit to `[roots]`, no check touched.
- Relative `target` values with no `{root}` placeholder (the one case in this declaration:
  `walk-script-syntax`'s target `../service/rail-walk.run.js`) resolve relative to the `mise.toml`
  file's own directory, per the build instruction. This is handled in the same
  `resolve_path_target()` function so there's one path-resolution codepath, not two.

## Design decisions not spelled out verbatim in the plan

- **Two script check types for "reachable + writable"**, not one. The plan/BRIDGE-INTERFACE text
  describes "rail root reachable + writable" as a single English requirement; I encoded it as
  two separate checks (`*-exists` via `path_exists`, `*-writable` via `path_writable`) per root.
  Reason: they fail for different, actionably-different reasons ("doesn't exist yet, `mkdir -p`"
  vs. "exists but permissions are wrong, `chmod`") and the whole design principle of mise is a
  *specific* remedy per row, not a merged diagnosis.
- **`node_syntax` and `command_on_path` both severity WARN** in this brigade's declaration. The
  factory's walk runs via the harness Workflow tool, not `node` — `service/SKILL.md`'s own
  declared-deps table already documents `node` as "lint-time, not run-time." A missing/broken
  `node` here degrades linting ability, it doesn't stop the walk from running. Domain brigades
  whose walk *is* a node/python process should likely declare their runtime interpreter check as
  FAIL, not WARN — that's a per-brigade judgment call the declaration author makes, not something
  the engine hardcodes.
- **`node_syntax` when node is absent**: read the plan's "skip with WARN if node absent AND
  severity says so" literally — when node can't be found, the check is "broken" (can't verify)
  and maps through the check's own **declared** `severity` field, same as every other broken
  check. I did not hardcode a special "always WARN regardless of declared severity" path — if a
  future brigade declares this check FAIL severity, a missing `node` reports FAIL for that
  brigade, consistent with its own declared risk tolerance. This reads as the more literal
  interpretation of "severity says so" (the severity field is what "says so"), and it keeps the
  engine's status-mapping logic uniform across every check type (one `classify_status()` function,
  no type-specific carve-outs) rather than special-casing one check type.
- **No `vendor_stamp` entry in this brigade's own `mise.toml`.** The vendor-stamp check type exists
  in the engine (implemented + tested) because the plan calls for it as a v1 check type, and
  because domain brigades vendoring `rail_adapter.py` (and eventually `mise.py` itself) from canon
  will need it. But *this* brigade (`skill-agent-brigade`) is canon — it doesn't vendor anything
  from itself. Adding a self-referential vendor-stamp check for `mise.py` is explicitly future
  work (build sequence step 4 in the plan; see "Open questions" below).
- **No "model access" check.** BRIGADE-INTERFACE.md's mise spec lists "one minimal model call per
  configured tier" as a checkable item, but `skills/service/SKILL.md`'s declared-deps table (the
  thing this task said to encode) has no such row, and it is unambiguously a paid/live probe
  (D3 — static-only default). It's absent from this declaration rather than added as a dead
  `mode = "live"` placeholder with no real target; the `--live` mechanism is proven out instead
  with a synthetic example in the test suite (`test_live_flag_lists_live_mode_checks`).
- **Menu freshness is `path_exists` only, not version-vs-commit comparison.** BRIGADE-INTERFACE.md
  describes menu freshness as "exists AND `version` not older than the brigade's last
  capability-changing commit." This build implements only the existence half
  (`menu-published`, WARN severity) — comparing menu version against git history is materially
  more machinery (parsing frontmatter, walking git log, defining what counts as
  "capability-changing") and wasn't in this task's explicit ask. Flagged as an open question below.
- **Four separate station-presence checks**, not one combined "stations present" check — same
  reasoning as the roots split: a missing `station-critic` and a missing `station-spec-author` are
  different, actionable problems, and per-station remedies are more useful than one row saying
  "some station is missing."

## What v1 deliberately keeps simple

- No auto-fix, ever — mise reports and recommends; it never mutates (explicit in the plan's "Out
  of scope").
- No live probing of anything (model calls, MCP, external URLs) inside `mise.py` — those are
  100% `executor = "agent"` entries by construction; the engine has no code path that could
  reach the network. `--live` only *describes* which agent checks to run; it doesn't run them.
- `python_module` uses `importlib.util.find_spec()`, not an actual `import` — this avoids
  executing arbitrary module-level code as a side effect of a *readiness check*, at the cost of
  not catching every possible import-time failure (a module that resolves via `find_spec` but
  raises on actual import would still show PASS). Judged an acceptable v1 tradeoff: readiness
  checks shouldn't have side effects.
- `vendor_stamp`'s stamp file format is a minimal `{"sha256": "...", "canon_version": "..."}` JSON
  sidecar. No signature, no timestamp trust chain — matches "v1, keep it simple," and nothing in
  the plan asks for more.
- The TOML schema requires every field (`id, description, executor, type, target, remedy,
  severity`) explicitly, even for `executor = "agent"` checks where `mise.py` never inspects
  `target`/`type` deeply. This is slightly more verbose than strictly necessary but keeps the
  schema uniform and lets the SKILL.md procedure step (agent-executor verification) read a
  consistent shape regardless of executor.

## Open questions for the founder / next builder

1. **Menu-freshness-vs-commit** (see above) — worth building the fuller check, or is
   `path_exists` + WARN sufficient indefinitely? If the fuller version is wanted, it needs a
   defined "capability-changing commit" heuristic (probably: last commit touching this brigade's
   `skills/*/SKILL.md` or roster files) — that heuristic belongs in the declaration or the engine?
2. **`mise.py`'s own vendor stamp** — once domain brigades start vendoring `mise.py` from this
   canon copy (build sequence step 4), should the *canon* copy (this one) get a self-check too
   (comparing its own hash to a recorded "last published" stamp, to catch canon drifting without
   a version bump), or does that only make sense on the *vendored copies*, checking against canon?
   The plan says "mise checks its own stamp too" but that's clearly written from the perspective
   of a vendored copy, not canon itself — left unresolved here since no vendoring has happened yet.
3. **Severity policy for `node_syntax`/`command_on_path` in node/python-walk brigades** — flagged
   above as a per-brigade judgment call; might be worth a one-line house convention in
   BRIGADE-INTERFACE.md once a second brigade actually declares its own `mise.toml`, so it's not
   re-litigated per brigade.
4. **`python_module` false-positive risk** (via `find_spec` not `import`) — acceptable for v1 per
   above; flagging in case a future brigade hits a module that resolves-but-fails-to-import and
   wants a stricter (import-based) variant.
5. **Whether `mise.toml` needs a `version` field** of its own (mirroring `menu.md`'s `version`) so
   a future "menu freshness"-style staleness check could apply to the declaration itself, not just
   the menu. Not added in v1 — nothing consumes it yet.

## Test suite notes

61 tests across four files (`test_check_types.py`, `test_declaration_loading.py`,
`test_engine_evaluate.py`, `test_cli.py`). All fixtures use pytest's `tmp_path` — no test touches
the real `~/rdco-cellar` tree. Run with:

```
python3 -m pytest skills/mise/tests/ -q      # from the plugin dir (plugins/skill-agent-brigade/)
python3 -m pytest plugins/skill-agent-brigade/skills/mise/tests/ -q   # from the repo root
```

Both invocations verified green (61 passed) before commit. `node_syntax` PASS/FAIL tests are
`skipif`-guarded on `node` being on PATH (it is, in the build environment: v25.9.0), so the suite
still passes green on a `node`-less runner — it just skips the two tests that need it (a third,
`test_node_syntax_node_absent_is_broken_not_ok`, monkeypatches `shutil.which` to simulate node's
absence regardless of the real environment, so the "node absent" codepath is always covered).
