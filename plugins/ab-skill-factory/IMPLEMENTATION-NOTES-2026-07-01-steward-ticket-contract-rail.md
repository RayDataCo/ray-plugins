# Implementation notes — steward + ticket contract + rail queue (2026-07-01)

Founder-directed evening push (iMessage go ~21:32 ET): make the FOH↔BOH handoff an explicit hexagonal port, define the one canonical ticket shape, give the rail real queue semantics, and spec the front-of-house role (named **steward**, founder's pick over captain/concierge).

## What landed

| artifact | role |
|---|---|
| `TICKET-CONTRACT.md` | NEW — the FOH↔brigade port: one ticket shape, Gate A (`ticketLint`, 8 deterministic rules), Gate B (phase-0 sufficiency criteria, written), the 5-exit amendment, supersedes table |
| `skills/steward/SKILL.md` | NEW — the front-of-house role: menu-pairing, cellar-first gathering, curate-to-type, Gate A self-check, enqueue, the `needs-context` rework loop |
| `RAIL-SPEC.md` | REWRITTEN — lease/ack/release queue semantics, rail-status ≠ build-phase separation, v1 advisory-lease honesty, queue-walk loop spec |
| `workflow/rail-walk.run.js` | NEW — reference queue-walk runner: pull-with-lease → Gate A → phase-0 → stations → expo decision policy (written signals) → ack; models pinned to sonnet |
| `skills/expo/SKILL.md` | UPDATED — phase-0 as loop step 0 (both gates), 5-exit set, contract-shaped ticket input (4-field record retired), mermaid + responsibilities |
| `BUNDLE-SPEC.md` | ALIGNED — payload-only scope, `{bundle_ref}` retired, context-prep → steward |
| `README.md` / `DESIGN.md` / both plugin manifests | swept — steward in the naming block + diagrams, 5-exit set everywhere, hexagonal-ports paragraph, §4 rewritten |
| vault ticket (`brigade-rail/variance-analysis.ticket.md`) | MIGRATED to contract shape — history preserved, migration logged as an append event; execution-eval + artifacts sections added |

## Decisions (and why)

1. **Inline manifest won as the one ticket shape.** Of the three shapes the fresh-eyes review flagged (identity / inline payload / external `bundle_ref`), inline implements the founder's 6/28 unification (bundle IS the ticket) with no indirection to dangle. `bundle_ref` retired in a Supersedes table rather than silently — future readers can trace the history.
2. **Rail status ≠ build phase.** The old lifecycle (`queued → phase-0 → spec → …`) fused queue state with station progress; adapters were being asked to parse build semantics. Now frontmatter `status` is the only thing an adapter reads; the phase lives in the work log.
3. **`reroute-to-steward` = exit #5, `escalate` stays a pause.** The front-end loop needed a formal return route (phase-0 Ambiguous/Thin, mid-build context discoveries). Escalate remains a budget stop awaiting a human's exit call — deliberately NOT an exit, clarified everywhere the set is enumerated.
4. **Two gates at phase-0, not one.** Gate A is deterministic (`ticketLint`, same move as `skillLint`) and runs on BOTH sides of the port (steward at enqueue, expo at pull — a pull-side failure implies an adapter defect). Gate B is judgment with written criteria. Folding them would either turn judgment into checkbox theater or bury mechanical failures in prose.
5. **v1 lease is advisory, and the spec says so.** Markdown files have no compare-and-swap; pretending otherwise would be the exact "slogan" failure the expo review caught. One walker per rail by convention; the lease field detects violations; real atomicity is the Snowflake adapter's job.
6. **Runner models pinned to sonnet.** Rail walks are fan-outs; per the standing commitment (2026-07-01) they must not inherit an expensive session model by accident.

## Deviations / debts

- `rail-walk.run.js` is REFERENCE code: expired-lease reclaim is left to a human sweep (documented), frontmatter access is regex not a YAML parser, and station-skill paths remain harness-coupled (same genericization debt as the other runners).
- The steward SKILL.md specs the procedure but the menu (use-case catalog) doesn't exist yet — `menu: unset` is legal v1.
- Execution-eval is still not sequenced into the expo's loop (known gap from the 7/1 review; not in this push's scope).
- Snapshot storage for live sources (url/mcp/qmd) still lacks a content-addressed home — flagged in the 7/1 review, deferred.

## Open questions for the founder — ANSWERED (iMessage, 2026-07-01 ~22:01 ET)

1. Gate-A rule 5 file-only at pull → **tight enough for v1.** ✓
2. 3-bounce steward rework budget → **fine.** ✓
3. Menu → **founder's design, blended into this PR (~22:10 go):** the menu is a **per-brigade asset** discovered **over the rail itself**.

## Addendum — the menu blend (same evening, founder-designed)

- **`MENU-SPEC.md`** (NEW): envelope-vs-menu two-layer split (envelope = universal TICKET-CONTRACT; menu = per-brigade payload requirements); discovery via an `artifact: menu` ticket the expo answers by introspection; published at `<rail>/menus/<brigade>.menu.md`; versioned by re-answering on brigade change. Precedent: MCP `tools/list` / A2A agent card, re-derived from the kitchen.
- **`MENU.md`** (NEW): this brigade's own menu — skill/brigade/menu artifact types + per-`type_hint` payload requirements. **This is where the curate-to-type table moved**: the steward SKILL.md had hardcoded it (menu content leaked into the FOH role — the founder's decoupling question exposed the coupling within an hour of shipping it); the steward now reads requirements from the target brigade's menu.
- **TICKET-CONTRACT**: `artifact` enum gains `menu` (Gate A rule 2 updated); menu tickets = same envelope + Gate A, never enter stations.
- **Steward**: binds to envelope + rail + menus (explicitly decoupled, N stewards ↔ M brigades); no-menu-published → hang the discovery ticket first.
- **Expo**: new "Menu tickets" section — introspect, publish, bump version, ack advance.
- **rail-walk.run.js**: `artifact: menu` branch (single expo introspection agent, no stations); lint rule 2 enum updated.
- **v1 pragmatism** (agreed): adopt the pattern, no live discovery protocol — one brigade + one steward means run discovery once, persist, re-run on change.
