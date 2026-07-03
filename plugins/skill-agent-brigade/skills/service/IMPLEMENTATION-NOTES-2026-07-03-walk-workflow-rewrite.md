# rail-walk.run.js rewrite — Workflow-tool compatibility (2026-07-03)

## What broke, found in live fire

`rail-walk.run.js` had only ever been validated with `node --check` — syntax only. It could not
actually execute under the Claude Code Workflow tool, which runs script bodies with no filesystem
or Node API access at all (no `import`, no `node:fs`/`node:path`, no `process.env`) and requires
`export const meta = {...}` to be the literal first statement in the file. The prior version:

- `import`ed `existsSync`/`readFileSync`/`readdirSync`/`writeFileSync` from `node:fs` and `join`
  from `node:path`
- read `process.env.HOME` for every path default (`RAIL_DIR`, `STATION_SKILLS`, `PLUGIN_DIR`)
- drove the rail with an inline `rail` object (`list`/`pull`/`ack`/`release`/`append`) that read and
  wrote ticket files directly via regex frontmatter surgery
- ran its own `ticketLint()` — a second, drifted copy of Gate A (2-space-only context-entry
  parsing, a hardcoded `['skill', 'brigade', 'menu']` artifact enum) alongside the canon
  `adapter/rail_adapter.py` implementation that already existed to replace exactly this.

None of that is Workflow-tool legal. `node --check` cannot catch it because it only parses syntax —
it doesn't know or care that the Workflow tool's script sandbox has no `fs`/`process` at runtime.

## What changed

The rewrite keeps every phase, gate, and decision **exactly** where it was (Pull → Gate A → menu
branch → Phase-0 Gate B → 4-station pass with the author⇄critic convergence loop → expo decision on
the five-exit set → ack) but moves the *mechanism* entirely:

- The script now does orchestration only: `phase()`/`log()`/`agent()` calls, `if`/`while` branching
  on the plain-JSON objects those `agent()` calls return, and string template-building for prompts.
  Nothing in the script body touches a filesystem path directly.
- **Every** rail read or mutation (`pull`, `lint`, `append`, `ack`) now happens inside a dedicated
  `agent()` call whose prompt instructs a real Claude Code subagent (which *does* have Bash/Read/Edit
  tool access) to run `python3 <plugin>/adapter/rail_adapter.py <subcommand> ...` and report back —
  either a raw stdout transcription, or a small JSON object per an explicit `schema` when the
  orchestrator needs to branch on the result (`pull`'s found/ticket_id/ticket_path/artifact,
  `lint`'s passed/failed_rule_ids).
- Two small pure-JS helper functions, `appendEntry()` and `ackTicket()`, wrap the repeated
  append/ack `agent()` calls (used ~10 times across the walk) so the Bash-command instructions and
  shell-escaping warning aren't re-typed at every call site. They are ordinary functions that
  return an `agent()` promise — they don't touch fs/env themselves.
- The inline `rail` object and `ticketLint()` are gone entirely. Gate A now runs in exactly one
  place (`rail_adapter.py`'s `lint` subcommand) instead of two drifted copies — this was already the
  intent of building the adapter (see `ADAPTER-SPEC.md`'s "Supersedes" table, which explicitly names
  this file's inline rail object + `ticketLint()` as one of the four hand-rolled implementations the
  canon replaces).
- All path configuration comes through `args` with hardcoded literal fallbacks (no
  `process.env.HOME` string interpolation): `rail_dir`, `cellar_root`, `plugin_dir`, `worker`, `now`,
  `max_tickets`, and (new) `station_skills_dir`.

## Simplified / dropped

- **`release()` dropped.** The old `rail` object defined a `release()` op (lease → back to queued,
  untouched) but the walk loop never called it — it was dead code carried over from the adapter's
  public API shape. `service end`'s graceful-stand-down path (SKILL.md) is a separate concern from
  this walk script and isn't affected.
- **Menu/run paths now resolve from `CELLAR_ROOT` directly**, not via `RAIL_DIR/../..` relative
  hops. The old script only had `RAIL_DIR` and derived everything else with `join(RAIL_DIR, '..',
  ...)`; the new script takes `cellar_root` as its own first-class arg (matching the adapter's own
  `--cellar-root` flag), so the menu path is `${CELLAR_ROOT}/brigades/skill-agent-brigade/menu.md`
  and the per-ticket scratch dir is `${CELLAR_ROOT}/brigade-runs/${ticketId}` — no relative-path
  guessing through the rail directory.
- **Station work-log appends now go through the adapter's `append` CLI**, not a vague "append a
  line to the ticket" instruction. The old script's station prompts said this but relied on the
  orchestrator's own (buggy) `rail.append()` to actually do it correctly; now the *station agent
  itself* is told to run `python3 rail_adapter.py append ...` via Bash, which is both correct (the
  canon's timestamp + placement logic) and keeps the "only agents touch files" rule intact even for
  the small per-station log lines.
- **`args.now` is now log-metadata only.** The adapter CLI's `pull`/`append`/`ack` subcommands don't
  expose a `--now` override (confirmed by reading the CLI's `argparse` wiring in `rail_adapter.py`)
  — they always timestamp with the adapter process's own real clock. The old script's `NOW` constant
  was threaded into every hand-rolled mutation; the new script keeps `NOW` around only for the
  startup `log()` line, since there's no CLI hook to actually pass it through, and the script itself
  has no `Date.now()`/clock access to derive one.

## A genuine behavior question resolved, not just simplified

The expo's decision schema still includes `reroute-to-spec` as a possible exit (per
TICKET-CONTRACT's five-exit framing), but `rail_adapter.py`'s `ack` subcommand only accepts
`{advance, escalate, kill, reroute-to-steward}` — it raises `RailError` on anything else, it does
**not** silently fall back the way the old inline JS `rail.ack()` did (`statusFor[exit] ||
'escalated'`). TICKET-CONTRACT's status enum has no distinct status for "needs a new spec" in the
first place, so a `reroute-to-spec` decision was always going to collapse into `escalated` for the
ticket's *status* field — the old JS's fallback-to-escalated behavior wasn't a bug, it's the correct
reading of the contract, just implemented as an implicit `|| 'escalated'` rather than a stated rule.
The rewrite makes this explicit: `ackExit = exit === 'reroute-to-spec' ? 'escalate' : exit` is
computed right before the CLI call, with a comment explaining why, while the human-readable `exit`
value (`'reroute-to-spec'`) is still what's recorded in the expo's own work-log line and in the
returned `summary` — so the distinction the ticket-contract cares about (why it stopped) survives in
the record even though the filesystem `status:` field only has room for `escalated`.

## Open questions

- **Agent-schema fidelity for CLI transcription.** Every mutating `agent()` call in the new script
  trusts a subagent to run a Bash command and transcribe its result faithfully (rather than
  re-deriving the answer itself). This is the same trust model the original script's judgment calls
  (phase-0, critic, expo) already used for LLM verdicts, just extended to mechanical CLI calls too —
  but it does mean a hallucinating or careless subagent could report `{found: true, ...}` without
  having actually run the command. Nothing in the Workflow tool's `agent()` contract (as inferred
  from this codebase's other `.run.js` files) offers a way to force literal tool-call verification
  from the orchestrator side; this is a known trust boundary, not new to this rewrite.
- **`workflow/brigade-variance-analysis.run.js` and its siblings have the identical violation**
  (`import`s from `node:fs`/`node:path` at the top) and were explicitly out of scope for this task.
  They will fail the same way this file did if anyone tries to run them through the actual Workflow
  tool rather than `node --check`. Worth a follow-up ticket.
- **No end-to-end run.** Per the task, the operator live-fires this through the Workflow tool after
  commit — this rewrite is validated structurally (`node --check`, meta-first, banned-pattern greps)
  but has not actually been exercised against a real rail/ticket. The adapter CLI itself has its own
  test suite (`adapter/tests/`) that was not re-run as part of this task.
