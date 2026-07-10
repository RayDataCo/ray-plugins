# EVAL-SPEC — the eval suite as a lifecycle asset

*(Settled design 2026-07-10, founder-directed: "update the design docs first, builds
second." This spec pins the contract; the storage migration and the tasting/freshness
builds ride later tickets.)*

An eval suite — oracle fixtures + answer keys + grading rules — is not build-run
scaffolding to be thrown away when a skill ships. It is the brigade's **proof of
competence**, and it has three uses across the life of a skill:

| moment | use | who runs it |
|---|---|---|
| **Build-time** | the ship gate: only eval-passers ship (house law) | the factory (`execution-eval` station inside spec→tests→author→critic) |
| **Run-time** | regression: keep shipped skills sharp as skills, models, and the WORLD change | the factory's `iterate-skill` path (eval-gated vs baseline = law) |
| **Sale-time** | demonstration: SHOW what a brigade can do and why the output is trusted, before setting up shop | the `tasting` invocation mode (see [BRIGADE-INTERFACE](./BRIGADE-INTERFACE.md)) |

One asset, three moments. The single tension that shapes everything below: **oracle
privacy**. Keys must stay out of shipped packs and out of any surface a graded model
could have seen, or every future eval is contaminated. That is why the same asset needs
two mechanisms — regression runs on private live fixtures; the tasting burns retired ones.

## Storage contract (canonical home)

Eval suites live in the **cellar**, as first-class citizens — not scattered across
per-build folders:

```
<cellar>/evals/<brigade>/<station>/
  fixtures.json          # the suite: id, input, oracle, grading, difficulty, status
  provenance.md          # which grounding sources (w/ version_or_date) the oracles
                         # were authored against + build/run lineage
  runs/<date>-<trigger>.json   # every eval run's raw results, append-only
```

- **Fixture status vocabulary** (per fixture, in the suite): `live` (grades; never
  leaves the cellar) · `retired-for-tasting` (deliberately spent: may ship in a pack's
  tasting set with its expected output; never grades again) · `burned` (exposed by
  accident or defect — a key leaked, an oracle proved wrong; never grades, never
  showcases; kept for the record with a dated note).
- **Oracle-privacy rule:** `live` fixtures and their keys never enter a public repo, a
  shipped pack, a demo, or any prompt whose output could circulate. Retiring a fixture
  is a one-way, recorded decision.
- **Versioning:** every oracle records the `version_or_date` of each grounding source it
  was authored against (the provenance frontmatter the sourcing stations already land).
  A grounding source moving past that version is a **freshness trigger** (below).
- The packaged plugin carries only: `evals/*.md` evidence summaries (headline numbers,
  named residuals, honest history) and, once the tasting ships, the retired showcase set.

*(Migration note: as of 2026-07-10 the suites live in dated build folders — vault
`08-tooling/ab-domain-research-build-2026-07-10/` and cellar `brigade-runs/` — private
and safe, but build-record-shaped. First build ticket under this spec migrates them to
the layout above.)*

## Regression triggers (run-time sharpness)

1. **Skill edit** — any change to a shipped SKILL.md or its references goes back through
   the factory's `iterate-skill` path: eval-gated vs the prior baseline, same suite. No
   eval, no merge. *(Already live in the factory MENU.)*
2. **Model upgrade** — when a deployment tier's model changes, re-run the suite per tier.
   Outcomes: hold (lift persists) · **retire** (the base model absorbed the skill —
   move the task to the base-model-covered registry with exemplar prompts) · refire
   (lift degraded — the skill needs re-encoding). *(Designed 2026-07-01; the two kinds
   of lift — judgment vs convention — predict which way each skill moves.)*
3. **World change (the new piece)** — laws amend, standards re-issue, gold exemplars go
   stale. The **freshness watch** (an ab-domain-research duty — see its menu): on a
   cadence, re-verify each landed grounding source against its PRIMARY source; when a
   source has moved past the `version_or_date` the cellar carries, flag every skill and
   every oracle authored against it and enqueue factory refire tickets carrying the
   updated grounding. Both the skill AND its oracles refresh together — an oracle keyed
   to a superseded regulation is itself stale.

## The primary-source gate (hard-won 2026-07-10, non-negotiable)

A fill station's "verified against primary text" self-stamp is a claim, not a fact: the
same day this spec was written, a fabricated CFR element carrying a false "verified: yes"
stamp propagated through a skill author and two independent critics — each of whom
"verified grounding fidelity" against the same tainted cellar intermediate — and was
caught only by a zero-context reviewer reading the actual regulation. Therefore:

- **At least one gate in every verification chain must check the PRIMARY source**, not
  the cellar intermediate. For standards/regulatory-derived skills this is a mandatory
  fresh-eyes dimension before ship.
- Cellar self-verification stamps are spot-checked independently before skills build on
  them; the freshness watch re-walks them on its cadence.
- A disproven oracle or grounding claim is corrected with a **dated note at the source**
  (never silently edited), and its fixtures move to `burned`.

## Fixture supply (who replenishes the suite)

Retiring fixtures for tasting and burning defective ones consumes the suite, so
replenishment is a named responsibility with two hands:

- **New fixtures** are authored by the factory's **tests station** (the same station that
  authors every suite at build time), via a factory ticket carrying the current grounding
  — that keeps new oracles defensible from source, exactly like a build.
- **Calibration of existing fixtures** is the `station-fixture-hardener`'s job — its
  documented scope is difficulty-adjusting fixtures that prior eval RESULTS showed to be
  non-discriminating (it requires those results in hand and does not invent new fixtures).

Neither path is hand-editing keys — key edits without a run and a dated rationale are
indistinguishable from grade-rigging, and the append-only `runs/` history is what keeps
the evidence honest.

## Grading modes (both proven 2026-07-10)

- **Structural** (checkable-standard skills): per-element status match against an
  enumerated oracle. Reported as per-element accuracy (the founder-ruled
  measure-skill-quality bar: pre-registered, e.g. ≥90% accuracy AND ≥+20pts lift over
  base) with strict all-element match kept as a continuity stat.
- **Exemplar-rubric** (generative skills): the tests station derives 8-12 binary
  criteria from gold exemplars (observable structure only); arms pass at a
  pre-registered criteria threshold with no fixture-fact violations. This is what the
  domain-research fill brigade's gold exemplars exist to enable.
- Bars are **pre-registered before a run** — changing the bar mid-evaluation is
  goalpost-moving; a founder-ruled bar change applies prospectively and is recorded.

## Relationship to the rest of the house

- The **factory** owns the eval machinery (execution-eval, hardener) and every gate.
- **ab-domain-research** owns grounding provenance and the freshness watch.
- The **cellar** owns the suites (storage contract above).
- The **packaged brigade** owns only evidence + (once built) its tasting set — see the
  `tasting` contract in [BRIGADE-INTERFACE](./BRIGADE-INTERFACE.md).
