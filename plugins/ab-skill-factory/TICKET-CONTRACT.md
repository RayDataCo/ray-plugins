# The Ticket Contract — the FOH ↔ Brigade Port

> **This document is the single source of truth for what a ticket is.** Every prior partial definition — `{ bundle_ref }` in BUNDLE-SPEC, the 4-field input record in the expo skill, the inline-pointer sketch in RAIL-SPEC — is superseded by the schema below. BUNDLE-SPEC.md remains the spec for the *context payload's source entries*; RAIL-SPEC.md remains the spec for the *store the ticket lives in*. The ticket itself is defined here, once.

## Why a contract (the hexagonal frame)

The brigade is a hexagonal (ports-and-adapters) system. The core — the stations and the pass — never talks to a technology; it talks to four **ports** (seam-by-seam handoff map: [PORTS.md](./PORTS.md)):

| port | what crosses it | driving/driven adapters |
|---|---|---|
| **ticket contract** (this doc) | the unit of work, front-of-house → brigade | **steward** (driving: writes + enqueues tickets) · human hand-authoring (driving) |
| **rail** ([RAIL-SPEC.md](./RAIL-SPEC.md)) | ticket storage + queue semantics | Obsidian vault (driven, v1) · Snowflake Stage · Cortex Search |
| **resolver** ([BUNDLE-SPEC.md](./BUNDLE-SPEC.md)) | context bytes, on demand, by source type | `file` · `url` · `mcp` · `qmd` · `cellar` (· `graph` future) |
| **cellar** ([CELLAR-SPEC.md](./CELLAR-SPEC.md)) | durable knowledge: brigades land outputs, the steward gathers context | filesystem/vault (driven, v1) · Google Drive · S3 · Snowflake Stage |

The dividend: the core is testable with no adapter at all — hand a synthetic contract-valid ticket to the pass and the brigade runs (the variance-analysis fire-through did exactly this). Swapping the vault rail for a Snowflake Stage, or the steward for a human writing a ticket by hand, changes an adapter, never the core.

**The contract is enforced on both sides of the port:** the steward validates before `enqueue`; the expo validates at `pull`. Same deterministic check, two checkpoints — a ticket that passes one and fails the other means an adapter mutated it in transit, which is itself a caught defect.

## The one ticket shape

A ticket is **one mutable, append-only markdown file**: YAML frontmatter (identity + state + context manifest) over four fixed body sections. It starts as the order, travels the stations, and ends as the full build record. There is no separate "bundle" artifact and no `bundle_ref` indirection — the manifest is inline; the pointers point OUT to where context already lives.

```yaml
---
ticket: variance-analysis        # id — kebab-case, unique on the rail
artifact: skill                  # a type from the target brigade's menu (this brigade: skill | brigade | menu)
status: queued                   # rail status — see lifecycle below
requested_by: founder            # who placed the order
menu: fpna/variance-analysis     # optional — use-case catalog entry this order was paired to
subject: companies/acme          # optional — canonical cellar subject key; where a closed ticket FILES, and the default subject for station kwargs. Fallback when absent: derived from the first cellar-typed context source. (Added 2026-07-02 with the filing rule.)
type_hint: computational         # optional — computational | corpus | generative | operational | advisory
lease: null                      # null, or { worker, at, ttl_min } while a pass works it
context:                         # the payload — typed pointer sources (schema: BUNDLE-SPEC.md)
  - id: core-competency
    type: file
    ref: "10-source-material/competencies/variance-analysis/core.md"
    when: "always — the competency knowledge the spec translates into procedure"
  - id: worked-examples
    type: file
    ref: "10-source-material/competencies/variance-analysis/worked-examples.md"
    when: "always — golden fixtures with known answers; the test station's oracle source"
  - id: current-standard
    type: url
    ref: "https://example.org/standard"
    when: "if the spec needs the authoritative external definition"
---
```

```markdown
## Order
<intent + scope, written by the steward: what to build, for whom, what done looks like>

## Resolved-context snapshot
<append-only — at build time the resolver records the exact content/version each
 source resolved to, so the build is auditable and re-runnable against known inputs>

## Work log
<append-only — one timestamped entry per event: enqueue, lease, phase-0 verdict,
 each station hop, each expo decision with its rationale, terminal close>

## Artifacts
<refs to produced outputs: spec.md, tests.md, the skill, eval reports>
```

### Rail status vs build phase (two lifecycles, deliberately separate)

- **Rail status** (frontmatter `status`) is what the *queue* cares about: `queued → leased → in-build → done | killed`, with two parking states: `needs-context` (routed to the steward) and `escalated` (waiting on a human). This is the only field an adapter reads to decide workability.
- **Build phase** (`phase-0 → spec → tests → author → critic → eval`) is what the *pass* cares about, and it lives in the work log, not the frontmatter. The rail never needs to know which station a ticket is at.

Conflating these was a v1 bug (RAIL-SPEC's old lifecycle mixed them); they are now layered.

## Gate A — contract validity (deterministic)

`ticketLint()` — pure pass/fail mechanics, the same move as the critic's `skillLint()` axis. No LLM judgment. Runs at **enqueue** (steward-side) and again at **pull** (expo-side).

1. `ticket` id present, kebab-case, unique on the rail.
2. `artifact` is a type the **target brigade's menu** offers (`menu` itself is universal — every brigade answers discovery). *(Amended 2026-07-02, stress-test finding SF-1: the original rule hardcoded this brigade's own enum `{skill, brigade, menu}` into the supposedly-universal envelope — a company-research ticket like `artifact: company-jobs-snapshot` failed a contract it should satisfy. Artifact vocabularies belong to menus; the envelope only checks the pairing.)*
3. `status` ∈ { `queued`, `leased`, `in-build`, `needs-context`, `escalated`, `done`, `killed` }; `lease` is null unless status is `leased`/`in-build`, and well-formed (`worker`, `at`, `ttl_min`) when set.
4. `context` has ≥ 1 source; every source has `id`, `type`, `ref`, `when`; every `type` is a registered resolver type.
5. Every **eager** source (`when` starts with "always") resolves at enqueue-time — the steward must verify the pointers aren't dead before hanging the ticket.
6. `## Order` section present and non-empty.
7. The four body sections exist under their canonical H2 names, in order.
8. No inline content copies in `context` — pointers only. (Resolved content belongs in the snapshot section, written at build time by the resolver, never pre-pasted by the steward.)
9. The resolved `subject` is a **cellar-contained relative path** — no `..` segment, not absolute, no drive letter. `ack()` files a terminal ticket to `<cellar>/<subject>/tickets/`, so an unvalidated subject (`../…`, `/etc/…`) turns a routine ack into an arbitrary file write *outside* the cellar. Validated here so a malicious ticket never enqueues, and again at the ack write site as defense in depth. Subject may be absent (derived from a cellar context ref, or genuinely unfileable) — only a *present-and-unsafe* subject fails. *(Added 2026-07-10, adversarial-review finding C1: reproduced live — `subject: ../../outside` passed the then-8-rule Gate A 8/8 and escaped the cellar on ack.)*

A Gate-A failure at enqueue bounces the ticket back to the steward with the failing rule numbers. A Gate-A failure at pull is logged and the ticket is parked `needs-context` — it should have been impossible, so it is also flagged as an adapter defect.

## Gate B — sufficiency (judgment)

The expo's **phase-0** call, made only after Gate A passes. The expo reads the Order + eager sources and renders one of three verdicts — criteria written, not vibes:

- **Clear** — the intent is derivable without guessing: one skill (or one brigade roster), one scope; `artifact` and `type_hint` are consistent with what the sources actually contain; and the sources carry enough domain substance to build from — for `computational`/`corpus` skills that means worked examples with known answers exist (the test station's oracle source), for `generative`/`advisory` it means exemplars of acceptable output exist. → **advance into the stations.**
- **Ambiguous** — the Order plausibly describes more than one skill or slice, or the sources contradict the stated scope. The expo appends the specific question(s) to the work log. → **reroute-to-steward.**
- **Thin** — intent is clear but named context is missing (e.g. a computational skill with no worked examples; a generative skill with no exemplars). The expo appends an itemized specify-missing list — *what* is missing and *how it would sharpen the build*. → **reroute-to-steward.**

Two gates, deliberately not one: Gate A is schema truth a script can check; Gate B is a judgment call an agent must make. Folding them together either turns judgment into checkbox theater or buries mechanical failures in prose.

**Menu tickets** (`artifact: menu`) are the discovery special case ([MENU-SPEC.md](./MENU-SPEC.md)): same envelope, same Gate A, but they never enter the stations — the expo answers one by introspecting its own brigade and publishing the menu beside the rail. Gate B for a menu ticket reduces to "does the pointer reach a brigade home?"; the sufficiency-by-type table above applies to build tickets, whose payload requirements come from the *target brigade's menu*.

## The exit set (amended: five exits)

The canonical closed exit set is now:

`advance · refire-to-author · reroute-to-spec · reroute-to-steward · kill`

**`reroute-to-steward`** (the amendment, 2026-07-01) — the ticket's context is the problem, not the build: phase-0 returned Ambiguous/Thin, or a station discovered mid-build that the context can't support the acceptance contract (e.g. the spec station finds the competency source contradicts the Order). Sets rail status `needs-context`; the steward reads the expo's work-log notes, repairs the payload, and re-enqueues. This closes the front-end loop the same way `refire-to-author` closes the back-end one.

(`escalate` remains what it always was: a budget stop on `max_rounds`, pausing for a human's exit call — a pause, not a sixth exit.)

## Supersedes

| old definition | where it lived | disposition |
|---|---|---|
| `Ticket = { bundle_ref }` | BUNDLE-SPEC.md | retired — the manifest is inline; no indirection |
| 4-field record `{ name, purpose, context, competency_excerpt }` | expo SKILL.md (v1) | retired — `name` → `ticket`, `purpose` → `## Order`, `context`/`competency_excerpt` → `context:` sources |
| inline-pointer sketch + fused lifecycle | RAIL-SPEC.md | formalized here; rail status and build phase separated |

## Worked example

The live `variance-analysis` ticket on a private house rail (outside this repo) conforms to this contract and carries a complete build record (queued → phase-0 `clear` → spec → tests → author ×2 rounds → critic 5/5 → advance) — the ticket-is-the-build-record model, demonstrated.
