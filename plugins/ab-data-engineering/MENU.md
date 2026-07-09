# ab-data-engineering — Menu

**Status:** live · 1 skill shipped (eval-proven) · rest of the vertical tracked below
with honest status

This is the packaged menu (source of truth, versioned with the plugin). It is the
**station roster** the [expo](skills/expo/) reads to route and compose a request. Only
eval-passers ship as stations (see `evals/`); everything else on the menu carries its
measured status, and the expo reports that status honestly rather than faking a station.

Brigade surface: `mise` (readiness gate) → `service` (on/off) → `expo` (composes the
stations below).

## Route to a skill (live, eval-proven)

| When the situation is… | Route to | Eval headline |
|---|---|---|
| A failed-run alert, anomalous row count, wrong-looking metric, or incident narrative on an EXISTING pipeline — classify the failure, trace blast radius, size the backfill, call stop/quarantine/silent-fix | `pipeline-failure-triage` | win +1.00 — base misclassified a silent zero-row SUCCESS (0 rows loaded, consumer group rebalanced to zero partitions) as Infra/Transient in every sample; skill classified Volume Anomaly 3/3 |

## Held for refire (real measured gaps — do not ship yet)

- `incremental-model-design` — two named gaps, both arms failed both: (1) delete+insert
  duplicate semantics (a delta-internal duplicate key survives the insert step), (2)
  lookback windows are bounds, not completeness guarantees (rows later than the window
  stay dropped). Ships after a refire encodes both.

## Weak evidence (not yet judged)

- `warehouse-cost-optimization` — one +0.33 win on n=3 single-sample evidence
  (break-even inter-arrival-gap convention). Needs higher n before a ship/covered call.

## Base-model-covered pending registry docs

Sonnet base at ceiling on all fixtures; registry entries (exemplar prompts + evidence,
per the ab-managerial-accounting `base-model-covered/` pattern) queued:

- `dbt-model-design` · `dimensional-modeling` · `data-contract-design` ·
  `semantic-layer-modeling`
- `sql-query-optimization` — same status, pending one fixture-key correction first
  (adjudicated: models answered a 91-day inclusive window correctly at 364 partitions;
  the key said 360).

## Disambiguation quick rules

- Choosing a lookback/write-strategy/partitioning scheme for a model being (re)designed
  → that's `incremental-model-design` territory (held) — say so honestly; do the best
  base-model work and flag the held status.
- A query that completes correctly but is slow → base-model-covered-pending
  `sql-query-optimization`, not `pipeline-failure-triage`.
- Manufacturing/process defect root-cause (Pareto/5-Whys/fishbone) → the operations
  brigade (`root-cause-analysis`), not this one.
