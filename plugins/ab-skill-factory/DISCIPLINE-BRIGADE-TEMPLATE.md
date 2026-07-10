# Discipline-brigade emission template

What the factory stamps out when an `artifact: brigade` ticket asks for a **discipline
brigade**. This is the reference shape + parameterized skeletons the assembling expo
follows, so a discipline brigade's surface can be **generated instead of hand-built**.
Status: **designed, not yet exercised** — no discipline brigade has been produced by the
assembling process yet. The one worked exemplar on disk,
[`../ab-managerial-accounting/`](../ab-managerial-accounting/), was **built by hand**
(2026-07-09); this template generalizes it, and the next `artifact: brigade` discipline
build is the live test that it emits generated-not-hand-built.

## Two brigade kinds

The expo is the same general role in every brigade — the per-brigade **station
coordinator** that knows its roster and decides which stations a ticket needs, sequences
them, and adds a finishing touch. What differs by kind is **what the stations are** and
**what the exit set means**:

| | **build brigade** | **discipline brigade** |
|---|---|---|
| stations | build stations that TRANSFORM an unfinished artifact (spec → tests → author → critic), or domain phases that produce a deliverable | **finished, eval-proven skills** — the stations are the capability, already built |
| what a ticket is | an order to BUILD something (a skill, an assessment, a collateral piece) | a REQUEST to be answered by composing finished skills |
| expo exit set | `advance · refire-to-author · reroute-to-spec · reroute-to-steward · kill` (build convergence) | `answered · needs-clarification · partial-with-gaps · out-of-scope` (composition completeness) |
| primary path | `service` walks a rail of build tickets | `fire` — an ad-hoc request straight to the expo (no rail needed) |
| examples | this factory; ab-assessment / ab-company-research / ab-sales-collateral / ab-website *(house brigades, not in this public repo)* | ab-managerial-accounting, ab-data-engineering |

Both kinds hold the **same surface: `mise + expo + service + menu`**. The factory must be
able to emit either; before this template it could only emit the build kind.

## What gets stamped (discipline kind)

Given a ticket that names a **station roster** (the finished skills this brigade serves)
and a **domain**, the assembling expo produces:

1. `skills/expo/SKILL.md` — the composing coordinator, parameterized by the roster (§ Expo skeleton).
2. `skills/mise/SKILL.md` + `skills/mise/mise.toml` + vendored `skills/mise/mise.py` — the readiness gate, with **checks derived from the roster** (one station-present check per station; § Mise skeleton).
3. `skills/service/SKILL.md` — the mise-gated on/off switch (§ Service skeleton).
4. `MENU.md` — the station roster the expo reads (§ Menu skeleton).
5. `.claude-plugin/plugin.json` — `name: ab-<domain>`, `displayName: AB <Domain>`, description naming the mise+expo+service surface over the stations.

Placeholders: `{{DOMAIN}}` (e.g. "Managerial Accounting"), `{{domain}}` (e.g. "managerial-accounting"), `{{STATIONS}}` (the roster: each station's slug + one-line "when the situation is…" trigger), `{{COMPOUND_EXAMPLE}}` (a domain compound request that fires several stations — the DD-picture equivalent).

## Expo skeleton (discipline kind)

```
---
name: expo
description: 'The deciding agent for the AB {{DOMAIN}} brigade — the composing
  coordinator over its stations. Use for any {{domain}} request not already aimed
  at one named skill: reads the request, decomposes it, selects the station(s) it
  needs, runs them, and synthesizes one answer — including compound requests like
  "{{COMPOUND_EXAMPLE}}" that need several stations plus a finishing synthesis.
  Also decides when the base model covers a task directly, or when a request is out
  of this brigade''s scope. Do NOT use when the user already named one station
  (invoke it directly).'
---
```
Body procedure (fixed across discipline brigades — only the roster examples change):
1. **Read the Order and the menu** ([MENU.md](../../MENU.md) = the roster).
2. **Phase-0 sufficiency gate:** Clear (proceed) / Ambiguous (ask one focused question, stop) / Thin (name required inputs, stop). Fire means "now", not "ungated".
3. **Decompose + select:** single-station → route to one; compound → select every station the Order touches (cite `{{COMPOUND_EXAMPLE}}`); base-model-covered sub-task → do directly; out-of-scope → name where it belongs.
4. **Sequence** (only when one station feeds another; usually independent).
5. **Run each selected station** on its slice of the Order; trust each station's own "Do NOT use for" boundaries.
6. **Finishing touch — compose** into ONE answer to the original Order, surfacing the cross-station observations no single station sees.
7. **Decision surface:** `answered · needs-clarification · partial-with-gaps · out-of-scope` (NOT the build exit-set).
8. **Record (fire contract):** every invocation is a `fire` — note which stations fired and why (in-answer trace for a public pack; a closed `origin: fire` ticket when deployed against a cellar).

## Mise skeleton (discipline kind)

`mise.toml` = one `path_exists` check per station in the roster + `expo-present` +
`menu-present` + `manifest-parses` (all FAIL severity) + any registry check (WARN). The
**checks are derived from the roster** — the factory emits one station-present check per
station it stamped, so a missing station FAILs the gate. `mise.py` is a stamped vendored
copy of canon (zero pip deps, relative targets resolve against the brigade's own
`skills/mise/`). **Known drift (2026-07-09): the two hand-built exemplars vendored their
`mise.py` from the private house factory (sha `6a680f2…`), which differs from THIS public
factory's own `skills/mise/mise.py` (sha `291612b…`) — the public↔house factory is not yet
reconciled. When the reconciliation lands, "canon" is one file and the stamp is
unambiguous; until then, treat the house version as newer.** Credentials: none for a
pure-computation brigade; a brigade with a
**connector** adds an `executor = "agent"` reachability check here — that is where mise
stops being a pack-integrity check and becomes the load-bearing "does this work in YOUR
environment" onboarding gate.

## Service skeleton (discipline kind)

`start` (default) runs the mise gate and, if clean, opens the brigade; `status` re-runs
mise; `end` stands down (stop flag, honored between tickets). `start` is **mise-gated** —
any FAIL refuses service. **Both halves ship** (symmetry guarantee, 2026-07-10 —
AGENT-BRIGADE-STANDARD.md, superseding this section's earlier "no rail walk is required"):

- **fire path** (always available): requests go straight to the expo — the primary path in
  a public-pack install where no rail/cellar is wired.
- **rail path** (house deployments): `service start` walks the rail via the vendored canon
  driver `skills/service/discipline-rail-walk.run.js` (byte-identical copy of the factory's
  canon, stamped) + the vendored `skills/service/vendor/rail_adapter.py`. The driver
  pulls-with-lease scoped to the menu's live artifact types, hands each Order to the expo,
  lands the answer at `{cellar}/{subject}/artifacts/`, and acks on the discipline exit
  mapping (answered/partial-with-gaps -> advance · needs-clarification ->
  reroute-to-steward · out-of-scope -> kill). Where the rail/cellar ports are unwired,
  mise reports them as unconfigured-with-remedy and fire-only is the honest mode.

## Menu skeleton (discipline kind)

The station roster with each station's "when the situation is…" trigger + disambiguation
rules + any base-model-covered list + honest gap status. This is what the expo reads to
route and compose. Same `MENU-SPEC` source-vs-publication + `source_hash` stamp rules as
any brigade menu.

## Acceptance (what makes an emitted discipline brigade interface-complete)

- All four surface skills present: `mise`, `expo`, `service`, and a published `MENU.md`.
- `expo` is a **composing** coordinator (decompose → select → compose → finish) with the
  **consumption exit surface** (`answered · needs-clarification · partial-with-gaps ·
  out-of-scope`), NOT the build exit-set.
- `mise.toml` has one station-present check **per station in the roster** (derived, not
  hand-listed), plus expo/menu/manifest checks AND the rail-half checks (vendored driver +
  adapter present with fresh stamps; rail/cellar port checks at WARN severity with
  configure-remedies so an unwired deployment reads as fire-only, not broken); `mise.py`
  is a stamped vendored copy.
- `service start` is mise-gated (refuses on any FAIL) — verified by a live run returning
  exit 1 when a station is hidden.
- The rail half is present: `skills/service/discipline-rail-walk.run.js` +
  `skills/service/vendor/rail_adapter.py`, both byte-identical to canon and stamped
  (symmetry guarantee — a discipline brigade without its walk is interface-incomplete).
- `plugin.json` carries `name: ab-<domain>` + `displayName: AB <Domain>`.
