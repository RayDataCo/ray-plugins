# Context Bundle — Schema Spec

> **The bundle IS the ticket's context payload.** A bundle is not a standalone artifact and does not live in this repo — it is the `context:` section of a mutable **ticket** ([TICKET-CONTRACT.md](./TICKET-CONTRACT.md) owns the ticket's full shape) that lives on the **rail** ([RAIL-SPEC.md](./RAIL-SPEC.md)). This doc specifies the shape of that payload — the typed-source pointer schema and the resolver port. The ticket is the brigade's only real input; everything else (intent, type, fixtures, wiring) derives from it.

## What a bundle is

A bundle is a **progressive-disclosure pointer**, structured like a `SKILL.md`: a thin **manifest** that points at typed sources, each with a *when-to-read* description. Sources are pulled on demand, not all up front. One progressive-disclosure pattern serves both skills and bundles.

Closest existing standard: [llms.txt](https://llmstxt.org/) — a curated markdown index of links-with-descriptions built for LLM context. This schema is llms.txt-flavored, extended two ways: **typed sources** (llms.txt is URL-only) and **when-to-read** semantics.

## The manifest

```yaml
# bundle.yaml
name: <handle>                 # required
scope: <one-line nudge>        # optional — disambiguates which skill/slice when the bundle is broad
provenance: <where it came from>
type_hint: <skill type>        # optional — computational | corpus | generative | operational | advisory; derivable
sources:
  - id: <stable id>
    type: file | url | mcp | qmd | cellar     # extensible
    ref: <type-specific locator>
    when: <when-to-read description>  # "always …" = eager; otherwise lazy
```

### Source types (the resolver dispatches by `type`)

| type | `ref` shape | resolver (v1) | resolver (later) |
|---|---|---|---|
| `file` | a path | read the file | — |
| `url` | a URL | fetch + convert to markdown | — |
| `mcp` | `{ server, resource/tool, args }` | call the MCP (e.g. Atlassian → ticket JIRA-1234) | — |
| `qmd` | a query string | local lexical+vector retrieval | enterprise governed store (RBAC) |
| `cellar` | a cellar ref (backend-relative path) | dispatch through the configured cellar adapter ([CELLAR-SPEC.md](./CELLAR-SPEC.md)) — filesystem v1 | Drive / S3 / Snowflake Stage, same ref |
| `graph` *(future)* | `{ graph, query }` | — | query a materialized graph (e.g. graphify) for big-corpus context |

The bundle binds to the **resolve interface**, not to a retrieval tech:

```
resolve_bundle(ref) -> { manifest, resolved_sources[] }
```

### Reproducibility — snapshot live sources

`file` sources are static. `url` / `mcp` / `qmd` sources are **live** — so at kickoff the resolver **resolves-and-snapshots** them into the versioned bundle. The build then runs against the snapshot, so `same ticket → same skill` even though some sources were fetched live. Want fresh context? Re-resolve = a new snapshot.

## How the brigade consumes it

1. **The manifest is inline in the ticket** — the `context:` frontmatter list, per [TICKET-CONTRACT.md](./TICKET-CONTRACT.md). (The earlier `Ticket = { bundle_ref }` indirection is retired; the contract's Supersedes table records it.)
2. **Expo phase-0 — the two-gate entry** (criteria live in the contract): **Gate A** validates the payload deterministically (`ticketLint()` rules 4–5 + 8: typed sources well-formed, eager pointers live, pointers-not-copies); **Gate B** judges sufficiency — Clear / Ambiguous / Thin, with Ambiguous/Thin exiting `reroute-to-steward`. The front-end gate mirrors the back-end critic loop: the steward builds the payload → expo gates it → insufficient routes back for more.
3. **Spec station** reads sources (eager first, lazy when its `when` fires) to translate competency *knowledge* → agent *procedure*.

## Where bundles come from

The **steward** ([skills/steward/](../ab-registrar/skills/steward/)) — the brigade's front-of-house role — produces the payload: pairing the request to the use-case catalog, gathering + curating from files, URLs, MCP, retrieval (vault-first, careful-external second). All the retrieval smarts live there — **inside** the steward, behind the ticket-contract port — not in the brigade. The brigade only ever reads a resolved payload. That boundary is what keeps the brigade domain-agnostic.

## What this is NOT

- Not a built knowledge graph (e.g. [graphify](https://github.com/safishamsi/graphify)) — that *compresses* a large corpus for cheap navigation; a bundle *curates and points* at the right depth for one build. graphify is a candidate `type: graph` resolver backend, not the bundle format.
- Not a flat folder — sources are typed and live on different planes (vault file, web, MCP, retrieval) by design.

Worked example: the `variance-analysis` ticket lives on a private house rail (a knowledge-vault folder outside this repo), pointing at competency notes stored beside it. It is intentionally NOT in this repo — see [RAIL-SPEC.md](./RAIL-SPEC.md).
