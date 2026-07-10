# The Agent Brigade Standard — what "agent brigade" means

*(Founder-ratified 2026-07-10: "We should have a standard of what an agent brigade means.
These should definitely be symmetric. Our standard has this hexagonal architecture. You have
a cellar, a registrar brigade, and any number of back of house brigades. A rail connects the
front of house and back of house. We should guarantee that these pieces exist, but allow for
different adapters that match the spec. We have the mise command in every brigade. The mise
command is what will tell us what parts of the agent brigade infrastructure are available and
which need to be configured still.")*

This is the definitional layer. It sits above [BRIGADE-INTERFACE.md](./BRIGADE-INTERFACE.md)
(the command surface of one brigade) and above the port specs
([PORTS.md](./PORTS.md) · [RAIL-SPEC.md](./RAIL-SPEC.md) · [CELLAR-SPEC.md](./CELLAR-SPEC.md)
· [TICKET-CONTRACT.md](./TICKET-CONTRACT.md) · [MENU-SPEC.md](./MENU-SPEC.md) ·
[EVAL-SPEC.md](./EVAL-SPEC.md)). Those documents say *how*; this one says *what must exist*.

## The four guaranteed pieces

An **agent brigade house** is these four pieces. A deployment without one of them is not a
house yet — and mise will say so (see "Mise is the instrument").

| piece | what it is | spec | today's adapter |
|---|---|---|---|
| **the cellar** | the durable knowledge store — everything a brigade lands, provenance-stamped; outputs compound into the next ticket's context | [CELLAR-SPEC.md](./CELLAR-SPEC.md) | filesystem/vault (Drive · S3 · Snowflake Stage are legal adapters) |
| **the rail** | the queue connecting front of house and back of house — enqueue · pull-with-lease · ack · append · file-to-subject | [RAIL-SPEC.md](./RAIL-SPEC.md) | filesystem (Jira · Snowflake are legal adapters) |
| **the registrar** | the front of house — a *house role*, not a kitchen: steward (intake, rework, close-out sweep), registry (menu catalog), orders (open-orders report) | [../ab-registrar/](../ab-registrar/README.md) | the ab-registrar plugin |
| **back-of-house brigades** | any number of kitchens, each interface-complete and **symmetric** (below) | [BRIGADE-INTERFACE.md](./BRIGADE-INTERFACE.md) | the ab-* kitchen plugins |

**Pieces are guaranteed; adapters vary.** Every piece is reached through a port with a spec
(the seam map is [PORTS.md](./PORTS.md)); any adapter that matches the port spec is legal, and
swapping adapters must never require touching a brigade's core. This is the hexagonal
(ports-and-adapters) rule, and it is the standard's one architectural law.

## The symmetry guarantee

**Every kitchen brigade ships BOTH halves of the surface:**

- **The expo half — fireable.** An addressable expo skill matching the brigade's kind
  (composing coordinator for discipline kind; build/phase router for build kind — see
  BRIGADE-INTERFACE "Kind-specific checks"). `fire` and `tasting` are invocation modes of
  this expo; a brigade without an addressable expo cannot be fired or tasted.
- **The rail half — queueable.** A `service` walk: the stamped vendored canon rail adapter
  plus a walk driver (the factory's Workflow-script pattern, or a per-brigade equivalent)
  that pulls-with-lease, hands the ticket to the expo/stations, and acks with the brigade's
  exit set. A brigade without a walk cannot participate in autonomous operation — the
  steward can't route it work and the close-out sweep has nothing to sweep.

A kitchen brigade with only one half is **interface-incomplete**. *(This ruling supersedes
the 2026-07-10 audit's "two designed generations" framing: Gen-A shipped rail-without-expo,
Gen-B shipped expo-without-rail — two half-implementations of one standard, converging via
the symmetric build. Status below.)*

**House roles are exempt by design** (BRIGADE-INTERFACE, 2026-07-06 amendment): a house role
ships `mise` + its role verbs and nothing kitchen-shaped. Symmetry is a kitchen guarantee.

## Mise is the instrument

Every install unit — kitchen or house role — ships `mise`, and mise is how you interrogate
the hexagon from wherever you stand:

1. **One check per port the brigade touches.** Every `mise.toml` declares checks for the
   cellar port (reachable, writable), the rail port (dir exists, a lease can be taken and
   released), station/roster presence, declared tooling, menu freshness, and model access —
   per the BRIGADE-INTERFACE `mise` contract.
2. **Unconfigured ≠ broken.** A port that is not wired in this deployment reports with a
   remedy that names the adapter to configure ("set `CELLAR_ROOT`", "connect MCP server X"),
   so the report reads as a **configuration report** — *what's available, what needs
   configuring still* — not a bare pass/fail. FAIL is reserved for "this brigade cannot
   honestly serve in its current mode."
3. **Deployment progression is legible in mise.** A fresh public-pack install shows the
   rail/cellar ports unconfigured (fire-only mode, honest); a house install shows every port
   wired. The distance between those two reports IS the onboarding checklist.

## Deployment modes — one standard, two defaults

| mode | what's present | surface |
|---|---|---|
| **public pack** (marketplace install, no house) | the plugin only — no cellar, no rail, no registrar | **fire-only**: requests go straight to the expo; tasting runs from the packaged set; mise reports the unwired ports with remedies |
| **house deployment** (cellar + rail + registrar configured) | all four pieces | **full surface**: brigades go in service on the rail, the steward routes orders, close-out sweeps deliver, menus publish to the cellar |

Same plugin, same code, both modes — mise tells you which one you're standing in.

## What varies and what doesn't

| | |
|---|---|
| **guaranteed (never varies)** | the four pieces · the port specs · the symmetric kitchen surface · mise everywhere · ticket contract + Gate A/B · close-out signature semantics · only eval-passers ship (EVAL-SPEC) |
| **varies by adapter** | rail backend · cellar backend · notification channels behind the steward · resolver source types |
| **varies by brigade** | station roster, gates, critic axes (published via `menu`) · walk implementation (Workflow script / Python driver) · exit set per kind |

## Status, honestly (2026-07-10)

- Cellar, rail, registrar, ticket contract, menus, evals: live in the house on filesystem
  adapters; canon `rail_adapter.py` vendored + stamped where walks exist.
- Symmetry: **in flight.** Gen-A (ab-assessment, ab-company-research, ab-sales-collateral)
  has walks, needs expos. Gen-B (ab-data-engineering, ab-domain-research, ab-legal,
  ab-managerial-accounting, ab-marketing) has expos, needs walks + vendored adapters. The
  factory itself is already symmetric and is the reference implementation for both halves.
- Mise: engines live everywhere; declarations are being upgraded to the full
  port-report shape as part of the symmetric build.
