# The Brigade Interface — Spec

> Every Agent Brigade exposes the **same five standard commands**, regardless of domain. This is the
> brigade's public surface — what a steward, an operator, or another agent can rely on being there.
> A brigade that implements these five (plus its stations à la carte) is interface-complete; anything
> else it exposes is house-specific extension.
>
> **Naming status (2026-07-03):** all five **founder-approved** (`mise`/`service`/`fire` "I like
> those names"; `runner` "Runner too - I like that", iMessage 2026-07-03). Runner's *implementation
> locus* is the open design conversation — see its contract below.

## The five commands

| command | answers | kitchen reading | status today |
|---|---|---|---|
| **`menu`** | "what can you do?" | the kitchen publishes what it serves | **LIVE** — [MENU-SPEC.md](./MENU-SPEC.md), discovery over the rail, `<cellar>/brigades/<name>/menu.md` |
| **`mise`** | "are you ready?" | mise en place — everything in its place before service | ⚠️ **PROPOSED** — not built; contract below |
| **`service`** | "start taking orders" | the brigade goes *in service*: attaches to the rail and polls | **PARTIAL** — reference loop exists ([workflow/rail-walk.run.js](./workflow/rail-walk.run.js): pull-with-lease → Gate A → phase-0 → stations → expo); the named command wrapper does not |
| **`fire`** | "do this one now" | "fire table 12" — cook immediately, skip the queue | ⚠️ **PROPOSED** — today you can hand the reference workflow a single ticket, but the ad-hoc path (Order-in-hand, no pre-written ticket) is unspecified; contract below |
| **`runner`** | "order up — who tells the table?" | the food runner carries the finished plate to the guest | ⚠️ **PROPOSED / known gap** — step 9 of the teaching diagram; the one DESIGN-ONLY step in the Lenovo receipts audit. Nothing closes the loop to the requester today |

## Command contracts

### `menu` — capability discovery *(live)*

Already specified in [MENU-SPEC.md](./MENU-SPEC.md). Summary: steward hangs an `artifact: menu`
ticket; the expo introspects its own brigade and publishes `<cellar>/brigades/<name>/menu.md` with
machine-parseable `**Status:**` markers per artifact type. Re-hang on any capability change; the
discovery tickets are the audit trail.

### `mise` — readiness check *(proposed; founder-named)*

Deterministic-first, judgment-second — same two-gate shape as ticket intake (Gate A then phase-0).

**Checks (deterministic tier):**
1. **Ports reachable** — cellar root exists + writable; rail dir/store exists + writable; a lease can
   be taken and released on a probe ticket.
2. **Stations present** — every station skill named in the brigade's roster resolves (skill dir
   exists, SKILL.md parses, `skillLint()` passes).
3. **Tooling** — every external dependency a station declares (CLI on PATH, MCP server connected,
   API credential resolvable *by name* — never printed) is available.
4. **Menu freshness** — `brigades/<name>/menu.md` exists and its `version` is not older than the
   brigade's last capability-changing commit (staleness = warn, not fail).
5. **Model access** — one minimal model call per configured tier returns.

**Output:** a mise report — one line per check, `PASS` / `FAIL` / `WARN`, and for every non-PASS a
**specific remedy** ("run `uv sync`", "connect MCP server X", "re-hang the discovery ticket"). The
report is written to the ticket work-log when run as part of `service` startup, or returned directly
when run ad hoc. A brigade whose mise has a FAIL must refuse `service` (a kitchen that isn't set up
doesn't open).

### `service` — attach to the rail and poll *(partial; name proposed)*

The standing loop: run `mise` (must be FAIL-free) → then repeatedly: pull-with-lease from the rail
(filtered to tickets whose `artifact` type this brigade's menu marks `live`) → Gate A → phase-0 →
stations → critic advises → expo decides → ack with one of the five exits → file closed tickets to
their subject. The reference implementation is [workflow/rail-walk.run.js](./workflow/rail-walk.run.js);
`service` is that loop given a standard name, a mise precondition, and a polling cadence parameter.
One walker per rail in the v1 filesystem adapter (advisory lease — see [RAIL-SPEC.md](./RAIL-SPEC.md));
real concurrency arrives with an atomic rail adapter.

### `fire` — ad-hoc direct request *(proposed)*

For an operator with an Order in hand and no patience for the queue. `fire` takes an Order (+ optional
context pointers), and the **expo itself performs minimal steward work**: wraps it in a
contract-valid ticket (envelope + payload per its own menu), runs Gate A + phase-0 on it like any
other ticket, then executes immediately — no rail wait. Two non-negotiables:

- **A ticket is still created.** `fire` skips the *queue*, never the *record* — the decision trace
  lands on the rail as a normal closed ticket, marked `origin: fire`.
- **Gates still apply.** Phase-0 can still return Thin/Ambiguous and bounce the request back to the
  caller. Fire means "now", not "ungated".

### `runner` — close-out to the requester *(proposed; fills the known step-9 gap)*

When the expo acks a terminal exit (`advance` or `kill`), the runner carries the outcome back:

1. **Completion event** appended to the ticket (already happens — the work-log is the record).
2. **Notification** to the ticket's `requester` field — the missing machinery. v1: the runner writes
   a completion note to a standing `<cellar>/rail/completed/` feed the steward reads; richer adapters
   (iMessage/Slack/email per requester preference) are driven-adapter territory, same pattern as the
   rail itself.
3. **Steward confirmation** closes the loop: the steward, not the kitchen, tells the guest — which
   keeps the brigade decoupled from requester identity/channels.

The `requester` field and notification preference belong on the ticket envelope —
[TICKET-CONTRACT.md](./TICKET-CONTRACT.md) needs a small amendment (one optional field) when `runner`
is built.

**Implementation locus (settled in the 7/3 dialogue): the runner is NOT a station.** The test:
stations *transform the ticket's artifact*; the runner transforms nothing — it moves information.
Role-class agrees: it needs requester identity + channel (front-of-house knowledge), not build
knowledge. It is the **steward's mirror image** — same role class, opposite direction (order in:
steward; plate out: runner). The kitchen's obligation ends at the pass: expo acks the terminal exit,
writes the completion event, drops the ticket on the completed feed. **v1: runner is the steward
skill's outbound procedure** (the steward already watches the rail for its rework loop; it also
watches for terminal tickets it enqueued and notifies the requester). Factor it into a standalone
runner agent only when scale demands (multi-steward houses, notification-channel fan-out) — the
completed feed *is* the seam, so that split costs no redesign.

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
