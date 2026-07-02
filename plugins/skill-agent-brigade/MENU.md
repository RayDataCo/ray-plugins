---
menu_of: skill-agent-brigade
version: 1
generated_by: hand-maintained   # v1 — the expo's first discovery answer will derive from this + live introspection
---

# Menu — skill-agent-brigade

What this brigade can do for you, and what your ticket must carry so the kitchen can cook from it. Envelope shape (identity, status, context-manifest, Gate A) is universal — see [TICKET-CONTRACT.md](./TICKET-CONTRACT.md); this menu covers only what is specific to ordering from *this* brigade.

## `artifact: skill` — build a Claude skill

**What you get:** a trigger-tuned, procedure-first `SKILL.md` (+ progressive-disclosure references), passed through 5 LLM critic axes + deterministic skill-lint, with an optional execution-eval (measured lift over the base model, per-fixture, per-tier).

**What the ticket must carry, by `type_hint`:**

| type_hint | mandatory payload sources | why |
|---|---|---|
| `computational` / `corpus` | worked examples **with known answers** | the test station's oracle source — fixtures are graded deterministically against them |
| `generative` / `advisory` | exemplars of acceptable output, provenance cited | the only honest quality anchor for subjective artifacts |
| all types | the core competency/knowledge source (`when: "always…"`) | the depth the spec station translates from *knows* → *does* |

**What the Order should specify:** the ONE skill (scope-fenced against neighbors — "variance analysis, NOT budgeting"), who it's for, and what done looks like. Optional but sharpening: `menu:` pairing ref, known near-miss asks the trigger must NOT fire on.

## `artifact: brigade` — assemble a domain brigade

**What you get:** a roster of stations (each an ordered `artifact: skill` build), a pass policy (expo decision config: exit criteria, round budgets), and a rail binding — a runnable brigade. *(Designed — the russian-doll ticket; not yet exercised end-to-end.)*

**What the ticket must carry:** the domain's station roster intent in the Order (which phases, which handoffs), one context source per station-to-be (same per-type payload rules as above, applied per station), and the pass-policy constraints (budgets, gates) if they differ from house defaults.

## `artifact: menu` — publish this menu

**What you get:** this document, regenerated — the expo introspects stations, critic axes, and eval config, bumps `version`, publishes to `<rail>/menus/skill-agent-brigade.menu.md`.

**What the ticket must carry:** one pointer at this brigade's home (plugin dir). Order = "what can your brigade do?"

## House quality gates (apply to everything ordered)

- Test station is blind to implementation; critics advise, the expo decides on the five-exit set.
- Deterministic gates (skill-lint, ticket Gate A) cannot be outvoted by LLM judgment.
- Execution-eval reports lift per-fixture and per-tier; non-discriminating fixtures are flagged, not counted as wins.
