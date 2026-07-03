# The Brigade Interface — Spec

> Every Agent Brigade exposes the **same five standard commands**, regardless of domain. This is the
> brigade's public surface — what a steward, an operator, or another agent can rely on being there.
> A brigade that implements these five (plus its stations à la carte) is interface-complete; anything
> else it exposes is house-specific extension.
>
> **Naming status (2026-07-03):** all five **founder-approved** (`mise`/`service`/`fire` "I like
> those names"; `runner` "Runner too - I like that", iMessage 2026-07-03). All five are also now
> SETTLED in implementation terms: three built, two ruled no-build (see the table).

## The five commands

| command | answers | kitchen reading | status today |
|---|---|---|---|
| **`menu`** | "what can you do?" | the kitchen publishes what it serves | **LIVE** — [MENU-SPEC.md](./MENU-SPEC.md), discovery over the rail, `<cellar>/brigades/<name>/menu.md` |
| **`mise`** | "are you ready?" | mise en place — everything in its place before service | **BUILT for this brigade** ([skills/mise/](./skills/mise/SKILL.md): `mise.py` stdlib engine + `mise.toml` declaration — D1 source of truth — merges static + agent-executor checks). Domain brigades: contract defined, wrappers queued |
| **`service`** | "start taking orders" | the brigade goes *in service*: attaches to the rail and polls | **BUILT for this brigade** ([skills/service/](./skills/service/SKILL.md): start/end/status verbs, service lock, mise-gated; walk script packaged inside the skill). Domain brigades: contract defined, wrappers queued |
| **`fire`** | "do this one now" | "fire table 12" — cook immediately, skip the queue | **SETTLED — invocation mode, no build** (founder 7/3): calling the expo directly IS fire; ticket still created, gates still apply |
| **close-out** *(né `runner` — dropped as a role, 7/3)* | "order up — who tells the table?" | the plate goes up on the pass shelf; front of house delivers it | **CONTRACT PINNED, absorbed into the steward**: expo drops a pointer on `<rail>/pass/` at terminal ack (lands free in the retrofit's `ack()`); steward sweep delivers + clears the shelf — sweep builds at P2 intake |

## Command contracts

### `menu` — capability discovery *(live)*

Already specified in [MENU-SPEC.md](./MENU-SPEC.md). Summary: steward hangs an `artifact: menu`
ticket; the expo introspects its own brigade and publishes `<cellar>/brigades/<name>/menu.md` with
machine-parseable `**Status:**` markers per artifact type. Re-hang on any capability change; the
discovery tickets are the audit trail.

### `mise` — readiness check *(built for the factory 2026-07-03; declaration = mise.toml per D1)*

Deterministic-first, judgment-second — same two-gate shape as ticket intake (Gate A then phase-0).
Implementation: [skills/mise/](./skills/mise/SKILL.md) — stdlib `mise.py` engine + per-brigade
`mise.toml` declaration (approved deviation from the plan's yaml: TOML parses with stdlib `tomllib`,
keeping the zero-dependency marketplace constraint). The checks below are the contract the
declaration encodes; script-executor checks run in the engine, agent-executor checks (Workflow tool,
MCP connections, station resolution) are verified by the harness agent and merged into one report.

**Checks (deterministic tier):**
1. **Ports reachable** — cellar root exists + writable; rail dir/store exists + writable; a lease can
   be taken and released on a probe ticket.
2. **Stations present** — every station skill named in the brigade's roster resolves (skill dir
   exists, SKILL.md parses, `skillLint()` passes).
3. **Tooling** — every dependency in the brigade's **declared-deps manifest** is available. The
   manifest lives in the brigade's own `service` skill (see the table in
   [skills/service/SKILL.md](./skills/service/SKILL.md) for the pattern): the walk's runtime (this
   factory: harness Workflow tool; a Python brigade: `python3` + its venv), plus every external
   dependency a station declares (CLI on PATH, MCP server connected, API credential resolvable
   *by name* — never printed). Mise checks the declared list — it doesn't guess.
4. **Menu freshness** — the `menu_freshness` check: packaged `MENU.md` sha256 vs the published
   copy's `source_hash` stamp (MENU-SPEC "Source vs publication"); mismatch or missing stamp = WARN,
   remedy "re-hang a discovery ticket".
5. **Model access** — one minimal model call per configured tier returns.

**Output:** a mise report — one line per check, `PASS` / `FAIL` / `WARN`, and for every non-PASS a
**specific remedy** ("run `uv sync`", "connect MCP server X", "re-hang the discovery ticket"). The
report is written to the ticket work-log when run as part of `service` startup, or returned directly
when run ad hoc. A brigade whose mise has a FAIL must refuse `service` (a kitchen that isn't set up
doesn't open).

### `service` — attach to the rail and poll *(contract settled 2026-07-03; built for the factory)*

**Verbs:** `service [start|end|status]` — **no argument → `start`**, unless the service lock is
already held, in which case say "already in service" and do nothing (founder-specified behavior).

- **`start`** (default): lock check → **mise gate** (any FAIL refuses to start) → take the
  **rail-level service lock** (`<rail>/.service/<brigade>.lock`) → run the walk loop: pull-with-lease
  (filtered to `artifact` types this brigade's menu marks `live`) → Gate A → phase-0 → stations →
  critic advises → expo decides → ack one of the five exits → file closed tickets to their subject.
  The lock is what upgrades the filesystem rail from *one-walker-by-convention* to
  **one-walker-enforced** (still advisory-grade — see the skill's failure-honesty note; real
  atomicity arrives with an atomic rail adapter, [RAIL-SPEC.md](./RAIL-SPEC.md)).
- **`end`**: graceful stand-down, issuable from any session via a stop flag the walker honors
  **between tickets, never mid-ticket**. Current ticket is finished or its lease released **with a
  work-log notation of exactly where it stopped** (phase, round, last station) — the append-only
  work-log is the resume state. Then: drop lock + flag, journal the session (tickets processed).
- **`status`**: read-only — in service? current ticket + phase, processed count, stop pending?

**Service is a CONTRACT, the walk is per-brigade.** The verbs, lock, mise precondition, and
teardown semantics above are identical across every house brigade; the walk *implementation* is the
brigade's own (this factory: [skills/service/rail-walk.run.js](./skills/service/rail-walk.run.js),
a Workflow script — packaged inside the skill; the domain brigades: their Python `rail_walk`/pass
drivers, wrapped by their own `service` skills, queued). Each brigade's service skill **declares its
runtime dependencies** in a manifest table — that manifest is exactly what `mise` checks.
*(Impl-language fork decided in dialogue 2026-07-03: contract-standard / per-brigade-implementation
[option A] recommended over one-canonical-JS-runner [option B]; note — the factory's walk runs via
the harness Workflow tool, not `node`, which is itself the best argument for declared-deps-per-brigade.)*

### `fire` — ad-hoc direct request *(settled 2026-07-03: an INVOCATION MODE of the expo, not a build)*

**Founder ruling: no machinery.** Fire is what happens when you call the expo directly with an
Order in hand — it already exists behaviorally (the 7/2 collateral stress run WAS a fire). The
contract is two lines of discipline in the expo's procedure, not a skill: the **expo performs
minimal steward work** — wraps the Order in a contract-valid ticket (envelope + payload per its own
menu), runs Gate A + phase-0 like any other ticket, then executes immediately, no rail wait. Two
non-negotiables:

- **A ticket is still created.** `fire` skips the *queue*, never the *record* — the decision trace
  lands on the rail as a normal closed ticket, marked `origin: fire`.
- **Gates still apply.** Phase-0 can still return Thin/Ambiguous and bounce the request back to the
  caller. Fire means "now", not "ungated".

### Close-out — the FOH contract *(runner DROPPED as a role, founder 2026-07-03; absorbed into the steward)*

**The full ruling chain:** runner is not a station (stations transform the artifact; this moves
information) → so it sits *outside* the rail, FOH-side → and outside, there is nothing it does that
the steward couldn't → so it is the **steward's close-out procedure**, not a role. The word "runner"
survives at most as that procedure's nickname. What was worth keeping is the CONTRACT — how a
completion crosses the rail boundary, clears the rail, and reaches the requester. Pinned:

**Pull-based shared state — no push, so channel knowledge never enters the kitchen:**

1. **Kitchen side — the pass shelf (one line in `ack()`):** at a terminal ack the expo already
   appends the completion event and files the ticket to its subject. It additionally drops a pointer
   on the **pass shelf** — `<rail>/pass/<ticket-id>.done`, containing the filed ticket's path. The
   finished plate under the heat lamp. This is the expo's last touch; it requires zero FOH knowledge.
   *(Lands nearly free: `ack()` is exactly what the retrofit centralizes into the vendored rail
   adapter — one implementation, every brigade gets the shelf.)*
2. **FOH side — the steward's sweep (deferred until P2 intake exists):** the steward sweeps the
   pass shelf on its own cadence; per pointer: read the filed ticket (`requested_by`) + its own
   intake record (channel) → respond to the requester → append a close-out line to the filed ticket
   (`close-out: requester notified via <channel>`) → **delete the pointer (this is what clears the
   rail — the hot section ends every cycle empty)**. Failed notification → pointer stays → next
   sweep retries. Today's only requester stands at the pass, so this paragraph builds when P2 gives
   it someone to deliver to.
3. **Truth lives on the ticket:** the close-out line completes the order record
   (placed → built → delivered) and makes the sweep idempotent. The pass shelf is a transient
   index, never authoritative — if lost, a scan for terminal-tickets-without-close-out-lines
   rebuilds it.

Notification-channel adapters (iMessage/Slack/email/Jira-comment) are driven adapters behind the
steward, same pattern as the rail itself. A standalone runner *agent* only ever exists if
multi-steward scale demands it — the pass shelf is the seam, so that split costs no redesign.

## Stations à la carte

**Station skills stay individually exposed.** An expert who knows exactly what they want may invoke
a station directly (`station-spec-author`, `station-critic`, a domain brigade's D-gate station, …).
One discipline, stated plainly:

> Direct station output is **un-gated work product**. It bypassed Gate A, phase-0, the critic, and
> the expo — so it must never be filed to the cellar as a brigade-certified artifact or land on a
> ticket as if it rode the line. If it's worth keeping, it enters the house the honest way: as
> *context* on a new ticket (an exemplar, a draft the stations refine), carrying
> `provenance: a-la-carte`.

This is the same two-fidelity honesty rule as everywhere else in the house: the value of a brigade
artifact is the *build record* behind it; à la carte output has none, and pretending otherwise is
how slop gets certified.

## Adapter distribution — vendored from canon *(settled 2026-07-03)*

The walk's *orchestration* is per-brigade (stations, gates, phase chaining — the legitimate
variance). The **rail-adapter code** (enqueue / pull-with-lease / append / ack / file-to-subject
against a backend) is not — today it is hand-implemented 3+ times across the house brigades, which
is drift debt (the 7/2 shakedown's "inherited fix" is the receipt).

The fix respects the distribution constraint the founder set: brigades ship through the Claude
plugin marketplace, so **every brigade must be self-contained** — no shared pip package, no
separately-installed CLI. Therefore:

- **Canon lives here, once:** a single module (`rail_adapter.py`, part of the service-skill
  template in this plugin) owns the rail port implementation, with backends (filesystem today;
  Jira/Snowflake later) *inside* it as options.
- **Vendored at build time:** the factory's `artifact: brigade` build copies the module into the
  new brigade, stamped with canon version + content hash. Copies are **build artifacts, never
  hand-edited** — the same generated-plus-drift-checked move as the frontend's embedded-schema
  test and vocab.json.
- **`mise` closes the loop:** compares the shipped stamp to canon and flags staleness ("adapter
  v3, canon v5 — re-stamp via `iterate-brigade`"). Stale kitchens tell on themselves.
- **The factory's own walk converges too:** its workflow agents call the vendored module (an
  internal script of this plugin, not a separate tool).

*Status, honestly: pattern settled in dialogue; `rail_adapter.py` canon not yet extracted — the
retrofit pass (replace the 3 brigades' hand-rolled adapter code with vendored canon, suites green)
is a queued build ticket, sequenced after the founder's P1 port validates and before P2/multi-walker.*

## Factory obligation — brigades ship interface-complete

**The meta rule (founder, 2026-07-03): the factory must structurally be unable to emit an
interface-incomplete brigade.** An `artifact: brigade` (or `add-station` re-wire) build is not done
until the new brigade ships the five commands: its menu published, a `service` skill wrapping *its*
walk with the standard verbs + declared-deps manifest, and mise/fire/runner at minimum spec'd in its
README with honest status markers. Enforcement lands in two places:

1. **Acceptance contract** — the brigade acceptance checklist gains interface-completeness checks
   (five commands present, service manifest declares the walk runtime, rail adapter is a stamped
   vendor copy of canon — see "Adapter distribution" above). *(Wired into MENU.md's
   `artifact: brigade` entry as of this commit.)*
2. **Lint rule** — a deterministic critic-axis check (brigade artifact missing any of the five →
   FAIL). *Status: documented here, code wiring in the critic queued — do not claim it fires yet.*

## What this spec deliberately does not standardize

- **Station rosters, gates, critic axes** — per-brigade, published via `menu`.
- **Polling cadence / concurrency** — deployment-profile concerns (see the deployment matrix,
  vault: `01-projects/phdata/2026-07-03-hex-deployment-matrix.md`).
- **Requester notification channels** — driven adapters behind `runner`, chosen per deployment.

## Cross-references

- [MENU-SPEC.md](./MENU-SPEC.md) — the `menu` command in full
- [TICKET-CONTRACT.md](./TICKET-CONTRACT.md) — envelope, Gate A, the five exits
- [RAIL-SPEC.md](./RAIL-SPEC.md) — pull/lease/ack semantics `service` rides on
- [CELLAR-SPEC.md](./CELLAR-SPEC.md) / [PORTS.md](./PORTS.md) — the store and the seam map
