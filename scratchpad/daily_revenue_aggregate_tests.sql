-- Custom dbt macro tests for daily_revenue aggregate-level validation

-- Test 1: sum(amount) within 2 std-dev of trailing-30-day mean
{% macro test_sum_within_stddev_of_mean(model, column='amount', days=30, stddev_threshold=2) %}

SELECT
  current_date as check_date,
  SUM({{ column }}) as current_sum,
  mean as mean_30day,
  stddev as stddev_30day,
  mean + ({{ stddev_threshold }} * stddev) as upper_bound,
  mean - ({{ stddev_threshold }} * stddev) as lower_bound
FROM (
  SELECT
    (SELECT SUM({{ column }}) FROM {{ model }}
     WHERE date >= CURRENT_DATE - INTERVAL '30 days'
       AND date < CURRENT_DATE) as current_sum,
    AVG(daily_sum) as mean,
    STDDEV_POP(daily_sum) as stddev
  FROM (
    SELECT
      date,
      SUM({{ column }}) as daily_sum
    FROM {{ model }}
    WHERE date >= CURRENT_DATE - INTERVAL '60 days'
      AND date < CURRENT_DATE - INTERVAL '30 days'
    GROUP BY date
  ) historic
)
WHERE current_sum < (mean - {{ stddev_threshold }} * stddev)
   OR current_sum > (mean + {{ stddev_threshold }} * stddev)

{% endmacro %}


-- Test 2: daily row count within 20% of prior day
{% macro test_daily_count_variance(model, variance_pct=20) %}

SELECT
  current_date as check_date,
  current_count,
  prior_count,
  ABS(current_count - prior_count)::FLOAT / NULLIF(prior_count, 0) * 100 as variance_pct
FROM (
  SELECT
    (SELECT COUNT(*) FROM {{ model }} WHERE date = CURRENT_DATE) as current_count,
    (SELECT COUNT(*) FROM {{ model }} WHERE date = CURRENT_DATE - INTERVAL '1 day') as prior_count
)
WHERE ABS(current_count - prior_count)::FLOAT / NULLIF(prior_count, 0) > ({{ variance_pct }} / 100.0)

{% endmacro %}
