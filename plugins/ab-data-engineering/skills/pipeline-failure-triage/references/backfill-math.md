<!-- iteration: 0 -->
# Backfill Correctness: Window, Verify, Row Math

Read this when computing a backfill (SKILL.md Step 7).

## (a) Minimal correct reprocessing window

For an incremental model with a stated lookback of N days, each broken run for date X touches event-dates [X-N, X]. The minimal correct reprocessing window is the **union of every broken run's own lookback span** — not simply the calendar range of days the job failed.

Why: an early broken run's lookback can reach backward past the first "failed" run-date, and dates that old will never self-heal on their own, because normal forward operation only re-touches the model's own rolling lookback going forward. A date can receive a corrupted upsert from a broken run's lookback touch even though the job never "failed" ON that date itself.

**Derivation method (generalize beyond any one fixture):**
1. List every broken run-date.
2. For each broken run-date X, compute its own touched span [X-N, X].
3. Take the union of all those spans — the earliest date across all spans through the latest date across all spans, inclusive. That union is the reprocessing window, expressed as a contiguous calendar range.

## (b) Verify before backfilling at scale

Before committing to the full-window backfill, re-run the FIXED model against a single day/partition first and confirm BOTH:
- its output is now correct, AND
- the write pattern is genuinely idempotent (re-running that single day's fixed job twice produces no duplication).

Only after that spot-check passes does the full-window backfill run. A backfill executed before the fix is confirmed does not repair anything — it reproduces the same bad data at scale, under cover of an action that looks like remediation, which is worse than doing nothing, because once "the backfill ran," people stop watching for the problem.

## (c) Row-count arithmetic, when a write pattern is stated

**Step 1 — touch count per date.** For each event-date in the reprocessing window, count how many of the broken runs' lookback spans include that date. (Cross-check: total touches across all dates = number of broken runs × lookback span length, e.g. 5 runs × 3 dates each = 15.)

**Step 2 — naive re-run (plain INSERT, no dedup key).**
- Gross rows written = Σ (touch count × that date's true row count), summed over every date in the window.
- Duplicate rows = Σ ((touch count − 1) × that date's true row count), summed over every date in the window.
- A plain INSERT with no dedup key writes a fresh duplicate copy every time an overlapping lookback window touches the same date again.

**Step 3 — idempotent re-run (MERGE/upsert on the natural key).**
- Correct end-state row count = Σ (true row count per date in the window) — each date written exactly once regardless of touch count.

**Cross-check:** gross rows − idempotent end-state = total duplicate rows.

**Duplication concentrates in the window's interior, not its edges.** Dates at the very start or end of the reprocessing window are touched by only one broken run's lookback span and carry zero or minimal duplication. Dates in the middle of the window are reachable by the lookback spans of multiple overlapping broken runs and carry the heaviest duplication.

## Kills

- Reprocessing only "the days the job failed" and leaving earlier corrupted dates unrepaired.
- Assuming a naive re-run "just fixes" the data without inflating the row count — a naive re-run's row count is never asserted equal to the idempotent end-state count.
- Assuming duplication concentrates at the window's edges rather than its interior, where overlapping lookback spans stack.
- Recommending a full-window backfill without first calling for a single-partition/single-day verification of both correctness and idempotency.
