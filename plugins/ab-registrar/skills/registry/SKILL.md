---
name: registry
description: >-
  The menu registry — answers "who can do what" across the house. Scans the
  published menus at <cellar>/brigades/*/menu.md on demand (no materialized
  index) and renders one table: brigade → menu version → freshness → live
  artifact types. This is where the steward gets Gate A's allowed_artifacts
  for a target brigade. Use when the founder asks "what brigades do we have",
  "what can the house do", "is <brigade>'s menu fresh", or before pairing an
  order to a brigade. Flags missing or stale menus and offers the discovery
  ticket that fixes them. Read-only — never writes the cellar or the rail.
---

# registry — the house's capability catalog

The registry **is** the set of published menus; this verb is a lens, not a store. By founder
decision (2026-07-06, same reasoning as the close-out sweep's scan-only ruling): **no
materialized index file** — five menus is a trivial scan, and a cached index is one more thing
to go stale. If a non-agent consumer (e.g. the frontend) ever needs to read the registry, that
is the moment a materialized index earns its place — not before.

## Procedure

1. **Resolve the cellar** — `$CELLAR_ROOT` (fail loudly if unset; same discipline as every
   cellar client). The scan root is `<cellar>/brigades/`.
2. **Scan** every `brigades/<name>/menu.md`. From each publication's frontmatter
   ([MENU-SPEC](../../vendor/specs/MENU-SPEC.md)): `menu_of`, `version`, `source_hash`,
   `landed`, `generated_by`.
3. **Freshness** — where the brigade's packaged source is reachable on this machine (the
   plugin's `MENU.md` / `brigade/MENU.md`), recompute its sha256 and compare to the published
   `source_hash`: `fresh` / `STALE`. Where the home is not reachable (split-runtime install),
   report `unverifiable — remote home`; never guess.
4. **Live artifact types** — parse each menu's artifact-type sections for the
   `**Status:** live` marker (contract per MENU-SPEC, pinned 2026-07-02). The set of live
   types **is** `allowed_artifacts` for Gate A against that brigade (`menu` itself is
   universal — every brigade answers discovery — so it is always allowed even when absent
   from the table).
5. **Render** the table: brigade · version · landed · freshness · live artifact types.
   Below it, flag exceptions:
   - **No menu published** → offer to hang an `artifact: menu` discovery ticket (the steward's
     move; see [../steward/SKILL.md](../steward/SKILL.md)).
   - **Stale stamp** → offer a republish discovery ticket (the mise `menu-freshness` remedy,
     served from front of house).

## Contract with the steward

The steward's step 2 ("pair to the menu") and step 6 (Gate A self-check) both consume this
verb's output: the pairing reads the live-type table; `ticket_lint(allowed_artifacts=...)`
takes the target brigade's live set. That closes the 2026-07-06 stress-test finding that
`allowed_artifacts` had no principled source.

## Honest defaults

- A menu that exists but fails to parse is reported as **defective**, not skipped — a
  half-published menu is worse than none.
- Freshness verdicts state their basis (hash compared vs home unreachable). No silent
  assumptions.
