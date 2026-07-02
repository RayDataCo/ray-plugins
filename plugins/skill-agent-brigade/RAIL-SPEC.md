# The Rail — Spec

The **rail** is where tickets live and travel. It is a **pluggable mutable ticket store** — bind to the interface, not the backend. Our v1 rail is the Obsidian vault; the same interface is meant to sit on a Snowflake Stage or Cortex Search just as well.

## Ticket = bundle (the unification)

A **ticket** is the brigade's unit of work, and it *is* the context bundle. One mutable artifact:

1. **starts as the order** — context pointers (mostly OUT to where the context already lives) + scope;
2. **travels the stations** — marked up at each hop;
3. **ends as the build record** — phase-0 verdict → spec → tests → critic verdicts → work-log.

(Kitchen ticket: order in, marked up down the line, record out.)

A ticket carries:
- **context payload** — typed-source pointers `{id, type, ref, when}` (see [BUNDLE-SPEC.md](./BUNDLE-SPEC.md)). The pointers reference context where it lives; the ticket does NOT carry child copies.
- **resolved-context snapshot** — append-only; at build-time the resolver records the exact content/version it resolved, so the same ticket replays to the same skill even if the underlying notes later change. **Mutable work-log + snapshot inputs = a living ticket AND replayable builds.**
- **work-log** — append-only markup as the ticket moves.

## The rail interface

A rail backend implements:

| op | meaning |
|---|---|
| `enqueue(ticket)` | put a new ticket on the rail |
| `pull()` | get the next ticket to work (the pass pulls from here) |
| `read(id)` | load a ticket |
| `append(id, entry)` | append work-state (append-only — never overwrite history) |
| `list(filter)` | enumerate tickets by status |

Tickets are **mutable but append-only**. State advances (`queued → phase-0 → spec → tests → author → critic → done | killed`); history is never destroyed.

## Backends

| backend | a ticket is… | `pull` | context co-location |
|---|---|---|---|
| **Obsidian vault** *(v1)* | a markdown file in a rail folder (`08-tooling/brigade-rail/`) | read next un-done ticket file | pointers resolve to vault notes (wikilinks) |
| **Snowflake Stage** | a staged file/object | list-stage + pick next | context pointers resolve via Snowflake (stages, tables) |
| **Cortex Search** | an indexed ticket document | query for next workable ticket | context pointers resolve via Cortex Search retrieval |

The brigade only ever talks to the rail interface; swapping the vault for a Snowflake Stage is a backend change, not a brigade change. This is the same interface-not-tech move as the context resolver — one level up.

## Where the packaging smarts live

`context-prep` (future) **produces** tickets — gathering and curating the context pointers. On the vault rail, **QMD** is the natural packaging aid: semantic/lexical search over the vault to find which notes a ticket should point at. The retrieval smarts live in context-prep, behind the rail/resolver boundary — never in the brigade.

## Worked example

The `variance-analysis` ticket lives on the vault rail at `~/rdco-vault/08-tooling/brigade-rail/variance-analysis.ticket.md`. Its context payload points at three competency notes under `~/rdco-vault/10-source-material/competencies/variance-analysis/` (core competency · worked-example fixtures · interpretation & pitfalls). The brigade pulls it, the expo runs phase-0 over it, the resolver reads the pointed-at notes, and the build marks the ticket up as it goes.
