# Data-engineering vertical — execution-eval evidence (2026-07-08)

Nine skills (8 data-engineering + one respec riding the same batch) were built by the
skill-agent-brigade (spec → tests → author ⇄ critic → expo, 9/9 tickets `advance`, all
round 1) and measured by the execution-eval station: two-arm ablation (sonnet base vs
sonnet + skill) on the oracle fixtures from each skill's acceptance contract, n=3
samples per arm, fixed per-fixture output schemas graded deterministically in code (no
name-matching). 213 eval agents, 0 errors. Results were recovered verbatim from the
run's workflow journal after a session restart; every anomalous row was re-verified
against fixture source before the verdicts below.

**This plugin ships only the skill whose eval demonstrated lift.** Per-fixture classes
follow the execution-eval station contract: `win` (base had headroom, lift ≥ +0.33 at
n=3) · `non-discriminating` (base at ceiling — proves nothing either way) · `flat` ·
`regression`.

## Shipped (eval evidence)

| skill | deployment-tier evidence | headline |
|---|---|---|
| pipeline-failure-triage | fixture A **win +1.00** (sonnet); B/C/D non-disc | Base misclassified the silent zero-row SUCCESS (0 rows loaded vs 1.2M hourly average, consumer group silently rebalanced onto zero partitions) as Infra/Transient in all 3 samples; skill arm classified Volume Anomaly 3/3. The cleanest lift of the three-vertical eval day — judgment lift on exactly the failure mode the skill exists for. |

## Held back (honest reasons, not failures)

- **incremental-model-design** — two REAL shared gaps, both oracle-verified by hand:
  (A) both arms claimed delete+insert leaves 0 duplicate keys, but the stated
  semantics (delete matching keys, then append the delta verbatim) leave a
  delta-internal duplicate key duplicated in the target; (B) both arms claimed a
  3-day lookback drops 0 rows, but a row 5d+ older than the watermark is outside the
  bound by definition. The skill lifted neither. Two named, fixable gaps → refire
  before shipping.
- **warehouse-cost-optimization** — weak signal, honestly below the ship bar: one
  +0.33 win from a single base miss in three samples (break-even inter-arrival-gap
  convention, 55 vs 60 s). Directionally the convention-lift story, but n=3
  single-sample evidence. Raise n before judging.
- **sql-query-optimization** — apparent "flat" on fixture A is a FIXTURE KEY DEFECT:
  the predicate `>= DATEADD(day,-90,'2025-01-18') AND <= '2025-01-18'` spans 91
  inclusive days → 91×4 = 364 partitions scanned, 95.45% pruned — exactly what both
  arms answered. The key's 360/95.5 assumed 90 days. Models right, key wrong; after
  the key fix the skill is fully at ceiling → base-model-covered candidate.
- **dbt-model-design, dimensional-modeling, data-contract-design,
  semantic-layer-modeling** — INCONCLUSIVE at the skill-shipping bar: sonnet base at
  ceiling on all fixtures (non-discriminating). Per the hardened re-eval finding on
  the finance vertical (difficulty-hardened fixtures stayed non-discriminating —
  hardening does not manufacture headroom vs a 2026 sonnet base), these default to
  base-model-covered registry entries with exemplar prompts, queued.

## Cross-vertical read

Consistent with the two-kinds-of-lift law measured on the finance vertical: the 2026
sonnet base aces textbook DE arithmetic; surviving lift is judgment (incident
classification under misleading surface signals) and convention (definitional
boundaries). Tier-floor sweeps (haiku arms) remain the untried lever for finding
minimum-viable-tier assets in this vertical.
