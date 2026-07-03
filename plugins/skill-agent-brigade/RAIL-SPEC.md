# The Rail — Spec

The **rail** is where tickets live and travel: a **pluggable mutable ticket store with queue semantics** — bind to the interface, not the backend. In hexagonal terms the rail is one of the brigade's four ports (see [TICKET-CONTRACT.md](./TICKET-CONTRACT.md)); the backends below are its driven adapters. In v1 the rail's store is the **cellar's hot section** (`<cellar>/rail/` — see [CELLAR-SPEC.md](./CELLAR-SPEC.md) § organization): separate port, one house store. The same interface is meant to sit on a Snowflake Stage or Cortex Search just as well.

**Closed tickets file, the rail stays hot:** on a terminal `ack` (`done`/`killed`), the ticket moves out of `rail/` to its subject's folder (`companies/<id>/tickets/…`) — the build record lands beside the artifacts it produced, and `rail/` only ever holds in-flight work. Wikilinks (name-based, not path-based) are what make this move free.

## The ticket (defined elsewhere, on purpose)

What a ticket *is* — the one canonical shape, its frontmatter, Gate A rules, the status lifecycle — is owned by [TICKET-CONTRACT.md](./TICKET-CONTRACT.md). The rail's concern is narrower: store tickets durably, hand them out safely, and never lose history. Two properties the rail enforces:

- **Mutable but append-only** — rail `status` and `lease` advance; the snapshot, work-log, and artifact sections only ever grow. History is never destroyed.
- **Rail status ≠ build phase** — the rail reads only frontmatter `status` (`queued · leased · in-build · needs-context · escalated · done · killed`) to decide workability. Which *station* a ticket is at lives in the work log; the rail never parses it.

## The rail interface

A rail backend implements:

| op | meaning |
|---|---|
| `enqueue(ticket)` | Gate-A-valid ticket goes on the rail, `status: queued` |
| `pull(worker)` | **lease** the next workable ticket: atomically pick a `queued` (or lease-expired) ticket, set `status: leased` + `lease: {worker, at, ttl_min}`, return it. Returns nothing if the rail is dry. |
| `ack(id, exit)` | close out a lease with the expo's terminal disposition: `advance → done`, `kill → killed`, `reroute-to-steward → needs-context`, escalate-pause → `escalated`. Clears the lease. |
| `release(id)` | give a leased ticket back untouched (`status: queued`, lease cleared) — worker died, budget hit, orderly shutdown |
| `read(id)` | load a ticket |
| `append(id, entry)` | append work-state (append-only — never overwrite history) |
| `list(filter)` | enumerate tickets by status |

### Lease semantics (why `pull` isn't just "read next file")

Without a lease, two passes walking the same rail pull the same ticket and burn double the tokens producing a merge conflict. So:

- A `pull` **owns** the ticket until `ack`, `release`, or lease expiry (`at + ttl_min`).
- Expired leases make the ticket workable again — the next `pull` may reclaim it (and appends a `lease-reclaimed` entry so the abandonment is visible in the record).
- `needs-context` tickets are workable only by the **steward** (who repairs and re-enqueues); `escalated` only by a human. `pull` never returns either.

**v1 honesty:** the vault adapter's lease is *advisory* — markdown files have no compare-and-swap, so v1 runs **one walker per rail by convention**, and the lease field exists to *detect* violations (a second walker sees a live lease and skips), not to prevent them atomically. Real atomicity arrives with the Snowflake backend (transactional update). This is a documented constraint, not a surprise.

## Backends

| backend | a ticket is… | `pull(worker)` | context co-location |
|---|---|---|---|
| **Obsidian vault** *(v1)* | a markdown file in the cellar's hot section (`<cellar>/rail/`; RDCO instance: `08-tooling/brigade-rail/`) | scan for next `queued`/lease-expired file, write lease to frontmatter (advisory — see above) | pointers resolve to vault notes (wikilinks) |
| **Snowflake Stage** | a staged file/object + a row in a ticket table | transactional `UPDATE … WHERE status='queued' LIMIT 1` — a real atomic lease | context pointers resolve via Snowflake (stages, tables) |
| **Cortex Search** | an indexed ticket document | query for next workable ticket, lease via the backing table | context pointers resolve via Cortex Search retrieval |

The brigade only ever talks to the rail interface; swapping the vault for a Snowflake Stage is a backend change, not a brigade change. Same interface-not-tech move as the context resolver — one level up.

## Walking the rail (the queue loop)

The reference queue-walk runner ([workflow/rail-walk.run.js](./workflow/rail-walk.run.js)) is the loop that makes the rail a *queue* rather than a shelf:

```
while budget remains:
  ticket = pull(worker)          — nothing? rail is dry → stop
  Gate A at pull                 — should-be-impossible failure → ack(needs-context) + flag adapter defect
  phase-0 (Gate B)               — Ambiguous/Thin → ack(reroute-to-steward); Clear → continue
  run the stations               — spec → tests → author ⇄ critic (convergence loop)
  expo decides                   — ack(id, exit) per the five-exit set; escalate-pause → ack(escalated)
```

Tickets flow independently — no barrier between tickets, wall-clock is the slowest single ticket. The only shared state is the rail itself, which is exactly what the lease protects.

## Where the packaging smarts live

The **steward** ([skills/steward/](./skills/steward/)) produces tickets — pairing the request to the menu, gathering and curating the context pointers. On the vault rail, **QMD** is the natural packaging aid: semantic/lexical search over the vault to find which notes a ticket should point at. The retrieval smarts live in the steward, behind the ticket-contract port — never in the brigade.

## Worked example

The `variance-analysis` ticket lives on the vault rail at `~/rdco-vault/08-tooling/brigade-rail/variance-analysis.ticket.md`. Its context payload points at three competency notes under `~/rdco-vault/10-source-material/competencies/variance-analysis/` (core competency · worked-example fixtures · interpretation & pitfalls). The brigade pulls it, the expo runs phase-0 over it, the resolver reads the pointed-at notes, and the build marks the ticket up as it goes.
