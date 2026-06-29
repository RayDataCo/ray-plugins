# dbt Test Coverage Report: daily_revenue Model

## Matrix Coverage Summary

| Scope | Basis | Test Type | Generated | Test Name | Severity |
|-------|-------|-----------|-----------|-----------|----------|
| row-level | absolute | automated | YES | `expression_is_true: amount >= 0` | error |
| row-level | relative | automated | NO | — | — |
| row-level | temporal | automated | NO | — | — |
| row-level | human | manual | NO | spot-check 5 rows vs billing UI | — |
| aggregate-level | absolute | automated | NO | — | — |
| aggregate-level | relative | automated | YES | `test_sum_within_stddev_of_mean` | warn |
| aggregate-level | temporal | automated | YES | `test_daily_count_variance` | warn |
| aggregate-level | human | manual | NO | — | — |
| transformation-level | absolute | automated | NO | — | — |
| transformation-level | relative | automated | NO | — | — |
| transformation-level | temporal | automated | NO | — | — |
| transformation-level | human | manual | NO | — | — |

## Automated Test Count by Scope

| Scope | Count |
|-------|-------|
| **row-level** | 1 |
| **aggregate-level** | 2 |
| **transformation-level** | 0 |

## Test Inventory

### Row-Level Tests (1)
1. **Non-negative amount** (absolute basis)
   - Expression: `amount >= 0`
   - Severity: error
   - Type: data quality
   - File: `/Users/ray/Projects/ray-plugins/scratchpad/daily_revenue_schema.yml`

### Aggregate-Level Tests (2)
1. **Sum within 2σ of 30-day mean** (relative basis)
   - Macro: `test_sum_within_stddev_of_mean`
   - Parameters: days=30, stddev_threshold=2
   - Severity: warn
   - Detection: anomalies >2 standard deviations from mean
   - File: `/Users/ray/Projects/ray-plugins/scratchpad/daily_revenue_aggregate_dbt_tests.yml`

2. **Daily row count variance ≤20%** (temporal basis)
   - Macro: `test_daily_count_variance`
   - Parameters: variance_pct=20
   - Severity: warn
   - Detection: row count swings >20% day-over-day
   - File: `/Users/ray/Projects/ray-plugins/scratchpad/daily_revenue_aggregate_dbt_tests.yml`

## Coverage Gap Analysis

### Zero-Coverage Scope
**Transformation-level** — 0 automated tests generated.

Rationale: Transformation-level tests validate ETL logic, data lineage, and structural contracts (schema, cardinality, foreign keys). The matrix provided no transformation-level test specifications. To add coverage:
- Row count equivalence (source vs model)
- Column presence and type enforcement
- Primary key uniqueness
- Surrogate key generation logic validation

### Additional Gaps (Non-Transformation)
- **Row-level relative basis**: No statistical comparison tests (e.g., amount distribution shift)
- **Row-level temporal basis**: No time-series continuity checks (e.g., date ordering, gaps)
- **Aggregate-level absolute basis**: No cardinality floor (e.g., minimum daily rows)
- **Row-level human basis**: Manual spot-check not automated (5 rows vs billing UI is out-of-band validation)
- **Aggregate-level human basis**: No manual review specified

## Test Execution Command

```bash
dbt test --models daily_revenue
```

## Files Generated
- `/Users/ray/Projects/ray-plugins/scratchpad/daily_revenue_schema.yml` — row-level tests (1)
- `/Users/ray/Projects/ray-plugins/scratchpad/daily_revenue_aggregate_dbt_tests.yml` — aggregate-level test config (2)
- `/Users/ray/Projects/ray-plugins/scratchpad/daily_revenue_aggregate_tests.sql` — custom macro implementations (2)
