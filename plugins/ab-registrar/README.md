# ab-registrar — the house's coordinator and record-keeper

Front of house as its own install unit. The registrar owns everything that happens **before a
ticket hangs and after a ticket files**: intake and context curation, menu pairing, Gate A at
enqueue, the rework loop, delivery + close-out, and visibility. It never cooks — no expo, no
stations, no rail lock. It is the first **house role** under BRIGADE-INTERFACE.md's
kitchen-brigade / house-role split (amendment 2026-07-06).

Extracted from `ab-skill-factory` 2026-07-06: the steward was always declared
brigade-decoupled ("binds to the envelope + the rail + menus, never to a brigade") — this
plugin makes the packaging match the architecture. One registrar serves every kitchen.

## The three verbs

| verb | question it answers |
|---|---|
| [`steward`](./skills/steward/SKILL.md) | "I need something done" — order → contract-valid ticket on the rail; rework repairs; close-out sweep + delivery |
| [`registry`](./skills/registry/SKILL.md) | "who can do what" — scan-on-demand over published menus; brigade → version → freshness → live artifact types; Gate A's `allowed_artifacts` source |
| [`orders`](./skills/orders/SKILL.md) | "what's in flight" — rail by status with ages, lease health, service locks, escalations made loud, unsigned close-outs |

Plus [`mise`](./skills/mise/SKILL.md) — front-of-house readiness (rail/cellar reachable,
vendored canon undrifted, ≥1 menu published). Deliberately **no `service` verb**: the
registrar takes no lock and works no ticket; monitoring is sweep-on-invocation (founder's
scan-only ruling, 2026-07-03, reaffirmed for the registry 2026-07-06). And **no `fire`
lane** — fire is an invocation mode of a kitchen's expo (skip the rail); it has no
front-of-house meaning (founder, 2026-07-06).

## What's vendored (never hand-edit; stamps are checked by mise)

- `vendor/rail_adapter.py` — `ticket_lint()` (Gate A) + `find_unclosed()` (close-out sweep).
  Stdlib-only. Canon: `ab-skill-factory/adapter/rail_adapter.py`.
- `skills/mise/mise.py` — the readiness engine. Canon: `ab-skill-factory/skills/mise/mise.py`.
- `vendor/specs/` — TICKET-CONTRACT, MENU-SPEC, RAIL-SPEC, CELLAR-SPEC, BUNDLE-SPEC: the five
  contracts front of house binds to. Canon home stays the factory; these are verbatim stamped
  copies so the registrar installs where the factory isn't (split-runtime). Cross-links
  inside them that point at other factory docs (e.g. `PORTS.md`) resolve only at the canon
  home — by design, since vendored copies are never edited.

## Configuration

Two layers, kept in agreement (the `cellar-env-agrees` mise check FAILs when they drift):
`$CELLAR_ROOT` via the workspace `.claude/settings.local.json` env block, and
`skills/mise/mise.toml` `[roots]`. The rail is `<cellar>/rail/` per the house layout.
