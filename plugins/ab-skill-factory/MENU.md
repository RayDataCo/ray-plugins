---
menu_of: skill-agent-brigade
version: 3
generated_by: hand-maintained   # v1 — the expo's first discovery answer will derive from this + live introspection
---

# Menu — skill-agent-brigade

What this brigade can do for you, and what your ticket must carry so the kitchen can cook from it. Envelope shape (identity, status, context-manifest, Gate A) is universal — see [TICKET-CONTRACT.md](./TICKET-CONTRACT.md); this menu covers only what is specific to ordering from *this* brigade.

## `artifact: skill` — build a Claude skill

**Status:** live

**What you get:** a trigger-tuned, procedure-first `SKILL.md` (+ progressive-disclosure references), passed through 5 LLM critic axes + deterministic skill-lint, with an optional execution-eval (measured lift over the base model, per-fixture, per-tier).

**What the ticket must carry, by `type_hint`:**

| type_hint | mandatory payload sources | why |
|---|---|---|
| `computational` / `corpus` | worked examples **with known answers** | the test station's oracle source — fixtures are graded deterministically against them |
| `generative` / `advisory` | exemplars of acceptable output, provenance cited | the only honest quality anchor for subjective artifacts |
| all types | the core competency/knowledge source (`when: "always…"`) | the depth the spec station translates from *knows* → *does* |

**What the Order should specify:** the ONE skill (scope-fenced against neighbors — "variance analysis, NOT budgeting"), who it's for, and what done looks like. Optional but sharpening: `menu:` pairing ref, known near-miss asks the trigger must NOT fire on.

## `artifact: brigade` — assemble a domain brigade

**Status:** live

**Two kinds** (2026-07-09, [DISCIPLINE-BRIGADE-TEMPLATE.md](./DISCIPLINE-BRIGADE-TEMPLATE.md)): a ticket names which. The expo is the same general station coordinator in both; what differs is the stations and the exit surface.
- **build brigade** — stations TRANSFORM an unfinished artifact (build stations spec→tests→author→critic, or domain phases producing a deliverable); expo routes on the build exit-set (`advance · refire-to-author · reroute-to-spec · reroute-to-steward · kill`); `service` walks a rail of build tickets. (ab-assessment, ab-company-research, ab-sales-collateral, ab-website — house brigades, not materialized in this public marketplace.)
- **discipline brigade** — stations are **finished, eval-proven skills**; the expo is a **composing** coordinator (decompose → select → compose → finishing touch) that routes on the consumption exit surface (`answered · needs-clarification · partial-with-gaps · out-of-scope`); `fire` is the primary path. (ab-managerial-accounting, ab-data-engineering.) The factory is meant to stamp this shape from the template so it's generated rather than hand-built — **designed, not yet exercised**; the two named brigades were hand-built (2026-07-09) and are what the template generalizes.

**What you get:** a roster of stations, an expo configured for the brigade's kind (build-station convergence policy, or the composing/consumption policy), a rail binding, **and the standard surface** (`mise + expo + service + menu`) — a runnable, interface-complete brigade. For a discipline brigade, `mise`'s checks are **derived from the roster** (one station-present check per station stamped), so a missing station FAILs the gate. *(Build kind exercised live 2026-07-02: assessment + sales-collateral roster tickets rode spec→tests→expo convergence to advance. Discipline kind worked-exemplar on disk: [`../ab-managerial-accounting/`](../ab-managerial-accounting/), built by hand 2026-07-09; this entry + the template generalize it.)*

**What the ticket must carry:** the brigade **kind** (build | discipline); the station roster intent in the Order (for build: which phases + handoffs; for discipline: which finished skills + one `{{COMPOUND_EXAMPLE}}` request that fires several); one context source per station-to-be (same per-type payload rules as above); and the pass-policy constraints (budgets, gates) if they differ from house defaults.

## `artifact: add-station` — add a station to an existing brigade

**Status:** live

**What you get:** a new station built to the full skill rigor (spec → tests → author → critic, incl. deterministic lint) AND wired in: the target brigade's roster updated, its menu re-published with a version bump, its station registry mapping the new artifact kind. A station IS a skill (the russian-doll definition) — this type exists so the WIRING is part of the order, not an afterthought.

**What the ticket must carry:** the target brigade (its menu ref), the station's competency/source material (same per-type payload rules as `artifact: skill`), and the wiring intent in the Order (which artifact kind(s) it serves, where outputs land). Precedent: the sec-filings station (2026-07-02) ran this shape manually — built, then fresh-eyes critic gates retroactively (verdict ITERATE, 5 hardenings applied before acceptance); this artifact type front-loads those same gates.

## `artifact: iterate-skill` — refine an existing skill

**Status:** live

**What you get:** the skill re-authored against the refinement Order, re-gated by the critics, and **eval-gated against the existing baseline**: the execution-eval station re-runs the oracle fixtures two-arm (current skill vs refined skill, per-fixture, per-tier) — the refinement only `advance`s if it improves the targeted axis WITHOUT regressing any other fixture. No eval pass, no ship. (Machinery exists and is demonstrated: the 2026-06-29 variance-analysis and generate-tests eval runs, per-fixture expo.)

**What the ticket must carry:** the existing skill (cellar/plugin ref), the refinement intent (what's underperforming, with evidence), and any NEW oracle fixtures the refinement targets (a refinement without a measurable target is a smell — the steward should push back).

## `artifact: iterate-brigade` — refine an existing brigade

**Status:** planned

**What you get (when live):** a targeted refinement of a brigade — a single station's behavior, or the expo's routing/decision policy between stations. Policy changes are the highest-authority edits a brigade can receive, so the acceptance bar is REPLAY: the brigade's closed tickets are its build records, and a routing/policy change must be replayed against recorded tickets to show the new policy reaches equal-or-better exits before it lands.

**Why planned, honestly:** the replay-based eval for routing changes is designed-in-principle (ticket-as-build-record makes it possible) but not built — and per the house rule that iterations MUST eval against baseline, this type stays off the live menu until that eval exists. Station-scoped iterations that reduce to `iterate-skill` + re-wire can ride the live types today.

## `artifact: menu` — publish this menu

**Status:** live

**What you get:** this document, regenerated — the expo introspects stations, critic axes, and eval config, bumps `version`, publishes to `<cellar>/brigades/skill-agent-brigade/menu.md`.

**What the ticket must carry:** one pointer at this brigade's home (plugin dir). Order = "what can your brigade do?"

## House quality gates (apply to everything ordered)

- Test station is blind to implementation; critics advise, the expo decides on the five-exit set.
- Deterministic gates (skill-lint, ticket Gate A) cannot be outvoted by LLM judgment.
- Execution-eval reports lift per-fixture and per-tier; non-discriminating fixtures are flagged, not counted as wins.
