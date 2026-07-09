<!-- iteration: 0 -->
# Named Pitfalls

Read this when Steps 2, 3, 6, 7, or 8 feel ambiguous.

## 1. Fixing the symptom node instead of the root

A DAG failure is almost never diagnosed at the point where it originated — it is diagnosed several hops downstream, at whichever node finally threw a loud error or a consumer finally noticed a number looked wrong. Patching that visible node makes the alarm go quiet while the actual upstream defect keeps corrupting every other consumer that doesn't happen to break as loudly on the same input.

**Concrete illustration:** a node errors on a NULL-join failure. Adding a `COALESCE` to silence the NULL makes the error stop — but if the source is still silently emitting NULLs upstream (say, a source schema drift that casts a renamed field to NULL instead of throwing), every other consumer of that source keeps receiving corrupted data, undetected, because the loudest alarm has been muted rather than the actual defect fixed.

**The tell:** a fix scoped only to the node where the failure was OBSERVED, without tracing back through that node's own upstream dependencies via the evidence ladder, is very often a symptom patch wearing a root-cause fix's confidence. Before declaring a fix complete, confirm it targets the node the evidence ladder (Step 2) actually located as the cause.

## 2. Backfilling before the fix is verified

Re-running a broken window through a pipeline whose fix has not been confirmed to work does not repair anything — it reproduces the same bad data at scale, under cover of an action that looks like remediation, which is worse than doing nothing, because once "the backfill ran," people stop watching for the problem.

**Sequencing rationale:** verify the fix against a single day/partition first (correctness AND idempotency — does a repeat run of that single day produce no duplication) before committing to the full-window backfill. The single-day check is cheap and catches a still-broken fix before it gets amplified across the entire reprocessing window.

## 3. Alert fatigue from a flat volume-anomaly threshold

When recommending a volume/freshness test as the postmortem-to-prevention control for a volume-anomaly class incident, a flat rolling-average threshold fires constantly on ordinary day-of-week, month-end, or campaign seasonality. That trains the on-call rotation to ignore volume alerts as noise — and lets a real anomaly sail through unexamined once everyone has learned to dismiss the alert.

**The fix:** compare against the same day-of-week across trailing weeks (a seasonally-aware baseline) instead of a flat rolling average. This is the single discriminator between a volume-anomaly control that stays useful and one that gets muted within a month.

## 4. Blaming transient when it's actually semantic drift

A clean log plus a normal row count is itself evidence — it points toward semantic drift (or nothing at all being wrong yet), not toward "it must have been a transient blip that already resolved itself." Infra/transient requires an EXPLICIT resource-exhaustion/network error signature that resolves identically on a bare retry with zero other change; it is never inferred from the mere absence of an error combined with a downstream number looking off. When logs are clean, runtime and row count are normal, but a downstream metric still looks wrong, the correct move is rung 3 (data diff against a prior snapshot) — not defaulting to "must have been transient, it's fine now."
