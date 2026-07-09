# The Cellar — Spec

The **cellar** is the house's shared knowledge store: where every brigade's outputs **land** (provenance-stamped, so all assets track back), and where the steward **gathers** context when writing tickets. It is the fourth port of the hexagonal system — bind to the interface, not the storage tech. Our v1 cellar is the local filesystem (the vault); the same interface is meant to sit on Google Drive, S3, or a Snowflake Stage as the processes harden.

## Rail vs cellar (two PORTS, one store)

| | **rail** ([RAIL-SPEC.md](./RAIL-SPEC.md)) | **cellar** (this doc) |
|---|---|---|
| holds | tickets — work in flight | knowledge — durable artifacts |
| lifecycle | queued → leased → done/killed | landed, append-only, forever |
| written by | steward (enqueue), pass (work log) | any brigade (land), curators |
| read by | the pass (pull) | the steward (gather), resolvers |

The rail and the cellar stay separate **ports** — pull/lease/ack and land/gather are different access patterns — but in v1 they share one **store**: the rail is the cellar's hot section (`<cellar>/rail/`), the same way daily notes and reference notes are different workflows over one Obsidian vault. When a ticket closes, it **files to its subject** (`companies/<id>/tickets/…`) so the build record sits beside the artifacts it produced; `rail/` holds in-flight work only, never an archive. (2026-07-02, founder direction: centralize — everything writes back to the one house store.)

## Organization — sections by kind, keys inside, links across

Top level answers "what kind of thing is this"; the folder inside is the thing's natural key. Cross-cutting connections ride frontmatter + wikilinks, not the directory tree:

```
<cellar-root>/
  companies/<canonical-id>/        # research subjects: identity.md · <kind>/<date>-artifacts · tickets/ (closed)
  assessments/<subject>/           # assessment records — subjects span companies, disciplines/departments, more groups later
  brigades/<brigade>/              # capability knowledge: menu.md, roster notes
  rail/                            # in-flight tickets ONLY — the queue adapter scans just this
  competencies/<domain>/           # source material skills are built from
```

Conventions that make the flat parts navigable:

- **Frontmatter is the query plane.** Every landed artifact already carries `subject / kind / produced_by.{brigade,ticket,station}` — search and graph tooling slice by any of them regardless of which folder won the filing argument.
- **Wikilinks are the connection plane.** Link by stable name (`[[acme — identity]]`), never by path — filing a closed ticket or reorganizing a section breaks nothing.
- **The cellar is an Obsidian vault.** v1 is literally openable in Obsidian; qmd indexes it as a collection for the steward's `search` op. Keep filenames human-stable and markdown-first for exactly this reason.

## The two flows

- **Gather** (steward-side, read): search and pull context when writing a ticket. The steward's "cellar-first, careful-external-second" sourcing rule ([skills/steward/](./skills/steward/)) runs against this port.
- **Land** (brigade-side, write): every artifact a brigade produces — research briefs, scraped snapshots, built skills' eval reports, CAF phase contracts, sales collateral — lands here with provenance. Landing is what makes an output *house knowledge* instead of a file lost in a run directory.

## The cellar interface

A cellar backend implements:

| op | meaning |
|---|---|
| `land(artifact, meta)` | write an artifact with required provenance meta (below), return its **cellar ref**. Append-only: landing never overwrites — a re-land of the same subject/kind lands *beside* the old one (date-stamped) with `supersedes` pointing back. |
| `resolve(ref)` | return the artifact's content |
| `search(query, filter?)` | full-text/semantic search → refs (the steward's gathering op) |
| `list(filter)` | enumerate refs by meta: subject, kind, brigade, date range |

### Landing meta (provenance, required)

Every landed artifact carries frontmatter recording where it came from:

```yaml
---
landed: 2026-07-02T05:40:00-04:00
kind: company-jobs-snapshot        # what this artifact is, per the landing brigade's menu
subject: companies/acme          # canonical subject key (see identity, below)
produced_by:
  brigade: company-research
  ticket: acme-research-2026-07-02   # the build record that produced it
  station: job-scraping
supersedes: null                    # or the ref this replaces (append-only chain)
provenance: <original source — scraped from careers page X on date Y / derived from Z>
---
```

A deterministic `cellarLint()` (same move as `ticketLint()` / `skillLint()`) checks the meta at land-time: required fields present, `subject` matches the canonical-key convention, `supersedes` (when set) resolves. An artifact that fails does not land — it bounces to the producer.

## Cellar refs and the resolver

A **cellar ref** is a backend-relative path (`companies/acme/jobs/2026-07-02-snapshot.md`) — stable across backend moves. Tickets point into the cellar via a registered `cellar` source type ([BUNDLE-SPEC.md](./BUNDLE-SPEC.md)); the resolver dispatches it through the configured cellar adapter.

**v1 equivalence, documented honestly:** on the filesystem backend a `cellar` ref and a `file` ref reach the same bytes, and existing `file`-sourced tickets keep working. Prefer `type: cellar` for anything that lives in the cellar — those tickets survive the move to Drive/S3/Snowflake; `file` refs are for genuinely local, non-cellar files (a repo checkout, a scratch artifact).

## Subject identity (the canonical-key rule)

`subject` is a **canonical key**, minted once per real-world entity — one entity, one key, however many spellings arrive. For company research: `companies/<canonical-id>` where the id is a lowercase slug resolved at intake (the steward owns identity resolution — pairing "Acme", "acme", "Acme Corp" to the one existing key *before* any ticket is written). The cellar keeps the resolution auditable:

```
companies/<canonical-id>/identity.md   — canonical name, known aliases, resolution provenance
companies/<canonical-id>/<kind>/…      — the landed artifacts, date-stamped
```

Duplicate subjects are a steward defect (same class as portfolio collisions in menu-pairing) — the cellar's `list(subject-prefix)` makes them visible; the identity note is where the merge is recorded when one slips through.

## Backends

| backend | an artifact is… | `search` | fit |
|---|---|---|---|
| **filesystem / vault** *(v1)* | a markdown/asset file under the cellar root | qmd (lexical + vector) over the root; plain grep/glob works | internal, dev, single machine — cheapest, Obsidian-browsable |
| **Google Drive** | a Drive file in a mirrored folder tree | Drive search API | teams already living in Drive; human-browsable sharing |
| **S3** | an object (`<root>/<ref>`) + meta in object tags or a sidecar index | external index (no native content search) | scale + durability; pair with a search index |
| **Snowflake Stage** | a staged file + a row in an artifact table | **Cortex Search** over the stage — the search op's enterprise upgrade | governed client contexts: RBAC, data gravity, audit |

The steward and every brigade talk only to the cellar interface; moving the house from vault to Snowflake Stage is an adapter swap, not a brigade change. Same interface-not-tech move as the rail and the resolver.

**v1 honesty:** the filesystem adapter has no locking or atomic land — two stations landing the same ref simultaneously is unguarded (in practice: distinct date-stamped filenames make collisions rare, and `cellarLint()` catches an exact-ref overwrite attempt). Provenance is enforced at land-time by convention, not by the storage layer. Real atomicity and enforced schemas arrive with the Snowflake backend.

## Where this leaves the ports

| port | what crosses it | spec |
|---|---|---|
| ticket contract | the unit of work, FOH → brigade | [TICKET-CONTRACT.md](./TICKET-CONTRACT.md) |
| rail | ticket storage + queue semantics | [RAIL-SPEC.md](./RAIL-SPEC.md) |
| resolver | context bytes, on demand, by source type | [BUNDLE-SPEC.md](./BUNDLE-SPEC.md) |
| **cellar** | durable knowledge: land (write) + gather (read) | this doc |

## Worked example

A Company Research brigade pulls a `acme-research` ticket, its job-scraping station lands `companies/acme/jobs/2026-07-02-snapshot.md` with full provenance meta, and the ticket's Artifacts section records the cellar ref. Next week the steward writes a CAF engagement ticket for the same company: `search("acme hiring signals")` surfaces the snapshot, and the ticket's context points at it with `type: cellar`. The research is now compounding house knowledge — which is the entire point of the cellar.
