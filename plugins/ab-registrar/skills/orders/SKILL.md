---
name: orders
description: >-
  The open-orders report — answers "what's in flight" across the house. Walks
  the rail for open tickets (queued, leased, in-build, needs-context,
  escalated) with ages and holders, checks service locks, and sweeps recent
  cellar filings for terminal tickets missing a close-out signature (feeding
  the steward's sweep). Use when the founder asks "what's on the rail",
  "where can I see hung tickets", "what's blocked", "anything aging", or at
  the start of a front-of-house session. Read-only — takes no lock, works no
  ticket, never mutates rail or cellar.
---

# orders — the house's open-orders report

The rail's v1 UI is `ls` plus frontmatter; this verb is that, productized. It reports; it
never acts — every remedy it surfaces is a pointer to the role that owns the action (the
steward for context repairs and close-outs, the founder for escalations, a brigade's
`service` for workable backlog).

## Procedure

1. **Resolve the rail** — `$CELLAR_ROOT` (fail loudly if unset); rail at `<cellar>/rail/`.
2. **Open tickets** — every `*.ticket.md` on the rail, grouped by frontmatter `status`
   ([TICKET-CONTRACT](../../vendor/specs/TICKET-CONTRACT.md) lifecycle):
   - `queued` — workable; report age since enqueue (first work-log line) and target `menu:`.
     Aging unworked tickets are the "no one has put that brigade in service" signal.
   - `leased` / `in-build` — report the holder (`lease.worker`), lease age vs `ttl_min`.
     An expired lease is flagged: the advisory-lease honesty note (RAIL-SPEC) means a dead
     walker leaves exactly this residue.
   - `needs-context` — parked for the steward; surface the phase-0 notes verbatim (the
     itemized questions/missing-list is the repair spec).
   - `escalated` — waiting on a human; report who escalated, when, and age. **Escalations
     age silently by design — this report is what makes them loud.**
3. **Service state** — list `<rail>/.service/*.lock` (which brigades are in service, held by
   whom, since when) and note the journal's last entry.
4. **Delivery debt** — the canon adapter's `find_unclosed(cellar_root, since_days)`:
   terminal tickets filed in the cellar without a `- close-out:` signature. These belong to
   the steward's sweep ([../steward/SKILL.md](../steward/SKILL.md) § close-out); this report
   only counts and points.
5. **Publish debt** (the reconciliation half of the 2026-07-06 publish wiring — see
   [../steward/SKILL.md](../steward/SKILL.md) § publish wiring). For each subject under
   `<cellar>/assessments/*/`:
   - a `manifest-commit` record, or a filed terminal `sales-collateral` ticket, **newer than
     the subject's newest `assessments/<assessment-id>/publish/` record** (or with no publish record
     at all), **and** no open `assessment-publish` ticket for that subject on the rail
     → report as publish debt. Next action: the steward hangs the publish ticket (a missed
     trigger, not an error — this scan existing is why a miss is safe).
   - Timestamps come from landed `landed:` meta and ticket work logs — never guessed.
6. **Render**: one section per status (skip empty ones), then service state, then delivery
   debt, then publish debt. Every row: ticket id · target menu · age · the one next action
   and whose it is.

## Honest defaults

- An empty rail is reported as exactly that — "rail clear, no open orders" — not silence.
- A ticket whose frontmatter fails to parse is listed as **defective** with its path; a
  broken ticket invisible to the queue is the worst failure mode this report exists to catch.
- Ages are computed from timestamps in the ticket itself (work log / lease), never guessed.
