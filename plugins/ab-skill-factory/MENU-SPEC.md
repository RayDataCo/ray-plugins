# The Menu — Spec

> A **menu** is a brigade's published input contract: what artifact types it can produce, and what a ticket's context payload must contain for each. It is a **per-brigade asset** — the brigade authors it (the kitchen decides the menu); the steward reads it (front of house serves from it). This spec defines the menu's shape, where it lives, and how a steward discovers it **over the rail itself**.

## Envelope vs menu (the two-layer split)

| layer | owned by | contains | brigade-specific? |
|---|---|---|---|
| **Envelope** — [TICKET-CONTRACT.md](./TICKET-CONTRACT.md) | infrastructure | identity, status, lease, context-manifest shape, Gate A, the exit set | **no** — every ticket on every rail has this shape |
| **Menu** — this spec | each brigade | artifact types offered + per-type payload requirements (oracle sources, exemplars, expected Order shape) | **yes** — one per brigade |

The steward composes the two: envelope says *how* to write a ticket; the target brigade's menu says *what this kitchen needs on it*. This split is what keeps the steward **decoupled** — it binds to the envelope + the rail + menus, never to a brigade. Topology: N stewards ↔ M brigades over shared rails.

## The menu shape

A menu is one markdown file with a small frontmatter header and one section per offered artifact type:

```yaml
---
menu_of: ab-skill-factory      # the brigade this menu describes
version: 1                        # bumped every time the brigade re-answers a discovery ticket
generated_by: expo                # discovery answers are expo-authored (introspection), or hand-maintained
source_hash: <sha256>             # publication copies only — sha256 of the packaged MENU.md at publish time (freshness stamp)
---
```

## Source vs publication *(settled 2026-07-03 — resolves the packaging question)*

The menu has two homes, one role each:

- **SOURCE — the packaged `MENU.md`** in the brigade's plugin: versioned with the code, updated as
  part of the release cycle (the factory obligation enforces it — a capability-changing build that
  doesn't touch the menu isn't done). This is what makes a fresh marketplace install
  self-describing on day one, before any discovery has run.
- **PUBLICATION — the cellar copy** at `<cellar>/brigades/<name>/menu.md`, created/refreshed by a
  discovery ticket (the expo derives it from the packaged source + live introspection). This is the
  copy **stewards read** — reachable across the rail boundary, which packaged plugin files are not
  (in split-runtime deployments the steward may only see the shared store).

**Freshness is checked, not assumed:** at publish time the expo stamps `source_hash` (sha256 of the
packaged `MENU.md` it derived from) into the published frontmatter. The mise engine's
`menu_freshness` check recomputes the packaged hash and compares — mismatch or missing stamp = WARN,
remedy "re-hang a discovery ticket." Stale publications tell on themselves. Menus are never
generated per-read: generation costs a model run and introspection output can vary — the payload
requirements a steward relies on must be stable between publishes.

Each artifact-type section opens with a machine-parseable **`**Status:** live`** (or `planned`) line — stewards and Gate-A lint discover live types by this marker, so it is contract, not decoration (pinned 2026-07-02 after two houses' menus diverged on it). Each section then states: **what you get** (the output artifact + its quality gates), **what the ticket must carry** (payload requirements by `type_hint`), and **what the Order should specify**. See [MENU.md](./MENU.md) — this brigade's own menu — for the worked example.

## Discovery — over the rail, no new machinery

The steward learns a brigade's menu by hanging a ticket, the same way it orders anything else:

1. **Steward enqueues a discovery ticket** — `artifact: menu`, Order = "what can your brigade do? publish your expected ticket input contract", context = a pointer to the brigade's own home (its plugin/docs dir). It's a contract-valid ticket like any other; Gate A applies.
2. **The expo pulls it** and, instead of running the stations, **introspects its own brigade** — stations, per-domain config, critic axes, eval gates — and writes the menu.
3. **The menu is published into the cellar's brigades section** (`<cellar>/brigades/<brigade>/menu.md`) — capability knowledge is house knowledge; any steward serving the house reads it there — and the discovery ticket is acked `advance` with the menu path in its Artifacts section. *(Location amended 2026-07-02 with the one-store centralization; formerly `<rail>/menus/`.)*
4. **Steward reads menus before gathering.** For every subsequent ticket aimed at that brigade, the menu tells the steward exactly what to track down.

**Versioning:** re-hang the discovery ticket whenever the brigade changes (new station, new critic axis, new artifact type) — the expo bumps `version` and rewrites. The old menu is superseded in place; the discovery tickets themselves remain on the rail as the audit trail of when capability changed.

**Precedent, for orientation:** this is capability discovery — the same move as MCP's `tools/list` or an A2A agent card — arrived at via the kitchen: the menu is exactly the artifact that tells front of house what the kitchen can produce.

## Where menus live

- **Runtime (authoritative for stewards):** `<cellar>/brigades/<brigade>/menu.md` — published by discovery into the house store's brigades section, read by stewards. Menus are house knowledge, NOT repo code.
- **In-repo (this plugin only):** [MENU.md](./MENU.md) ships with the ab-skill-factory as its current self-description and the worked example of the format — the expo's discovery answer derives from it plus live introspection.

## v1 pragmatism (adopt the pattern, not a protocol)

With one brigade and one steward, discovery runs **once** and the menu persists; re-run on brigade change. Do not build live control-plane traffic on the rail until there is actual multi-brigade demand — the mechanism is designed so that day requires no new machinery, which is the point.
