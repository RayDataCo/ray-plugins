---
name: pipeline-failure-triage
description: Diagnose and triage data pipeline failures - classify into seven evidence-based classes (schema drift, credential expiry, volume anomaly, semantic drift, infra/transient, logic regression, upstream dependency delay) via an evidence ladder (logs, run-history diff, data diff, deploy history); trace blast radius across a DAG via topology plus timing; decide stop-the-line vs. quarantine-and-continue vs. silent-fix, consumption-override checked first; compute the minimal reprocessing window and idempotent-vs-naive row math for a backfill; recommend (not author) the preventive control class. Use for a failed-run alert, anomalous row count, wrong-looking metric, or incident narrative on an EXISTING pipeline needing classification, blast-radius, backfill-window math, or a stop/quarantine/silent-fix call. Do NOT use for incremental-model-design (lookback/write-strategy/partitioning choices), sql-query-optimization (speeding up an already-correct query), or root-cause-analysis (ops-domain Pareto/5-Whys/fishbone).
iteration: 0
---

# Pipeline Failure Triage

Diagnoses and responds to an EXISTING data pipeline that broke. Not a design-time tool, not a query tuner, not the ops-domain root-cause method — see Step 1 and `references/scope-boundary.md`.

## The job

Given an incident narrative plus evidence (logs, run history, data snapshots, deploy/change history, and — for blast-radius/backfill — DAG structure, node schedules, lookback/write-strategy facts), run one or more of: **classify** the failure into exactly one of seven classes, **trace blast radius** across the DAG, **decide a response tier**, **compute backfill correctness**, and **hand off** a postmortem-to-prevention recommendation. Triage is a fast disciplined first pass that runs *before* root cause is nailed down — do not treat it as merely "step one of root-causing."

## Procedure

**1. Confirm scope; decline the three neighbors.** Is this diagnosing/responding to an EXISTING pipeline's failure? If the ask is actually "what lookback/write-strategy/partitioning should this new or redesigned model use" → redirect to incremental-model-design. If it's "this query is slow but returns correct results" → redirect to sql-query-optimization. If it's a manufacturing/ops-process defect investigation → redirect to root-cause-analysis. Otherwise, state which sub-capability(ies) are wanted before running any of them. See `references/scope-boundary.md`.

**2. Work the evidence ladder in strict order; never stop at an early clean rung.** Rung 1 logs → rung 2 run-history diff (row count/duration/resource vs. baseline — the ONLY rung that surfaces volume anomaly) → rung 3 data diff (value distributions vs. a prior snapshot — the ONLY rung that surfaces semantic drift) → rung 4 recent deploys (the pipeline's OWN change history plus explicitly-checked upstream/connector operational-trigger history — never "any company-wide action"). A clean rung 1 or 2 is never "nothing is wrong." Full detail: `references/taxonomy-and-evidence.md`.

**3. Classify into exactly one of seven classes by evidence signature**, never by narrative feel:
- **Schema drift** — fails AFTER a successful connect/read, during parsing/casting/column reference; row counts normal.
- **Credential/permission expiry** — fails BEFORE any row is read, explicit auth error, recurs every run until rotated (does not self-resolve on retry).
- **Volume anomaly** — SUCCESS status, normal runtime, no error, but row count is a floor/ceiling baseline violation — visible only via rung 2.
- **Semantic drift** — schema/types/tests all green, row counts/runtime normal, but a value's MEANING shifted — visible only via rung 3.
- **Infra/transient** — explicit resource-exhaustion/network error that resolves IDENTICALLY on a bare retry with zero other change, correlating with a load/concurrency spike.
- **Logic regression from a deploy** — onset lines up with a specific commit/deploy in the pipeline's OWN history; reverting it resolves the failure.
- **Upstream dependency delay** — not a defect in the job itself; a dependency-sensor timeout or upstream job's late-completion history.
Full signatures and traps: `references/taxonomy-and-evidence.md`.

**4. Blast radius: traverse the DAG, then cross topology with timing.** Compute the descendant set by forward graph traversal. Every non-descendant (and not the origin) is **safe — never downstream**, regardless of timing. For each descendant, compare its scheduled/actual run time to the containment timestamp: before containment → **ran on bad data**; at/after containment → **safe — blocked in time** (even though topologically a true descendant). Guard two traps: a co-parent that merely shares a join with a tainted node is not itself tainted; the node whose run surfaced the incident is bucketed by its own scheduled-time-vs-containment comparison like any other node, not assumed safe for having raised the alarm. Cross-foot the buckets against total node count. Full rule: `references/blast-radius.md`.

**5. Response tier: apply the consumption override, THEN the grid.** (1) If any consumer already acted on the bad data before detection, silent-fix is off the table — escalate to at least quarantine-and-continue regardless of the grid. (2) Otherwise classify criticality HIGH/LOW and impact SEVERE/BOUNDED. (3) HIGH+SEVERE → **stop-the-line**; HIGH+BOUNDED → **quarantine-and-continue**; LOW+(SEVERE or BOUNDED)+no prior consumption → **silent-fix**. Silent-fix requires all three conditions simultaneously — never just one or two. Full framework: `references/response-framework.md`.

**6. Trace to the actual root before declaring the fix complete.** Confirm the fix targets the node the evidence ladder (Step 2) actually located as the cause — not merely the node where the failure was loudest or most visible. A DAG failure is almost always diagnosed several hops downstream of where it originated; patching the visible symptom node leaves the real upstream defect corrupting every consumer that doesn't happen to break as loudly. See `references/pitfalls.md`.

**7. Backfill correctness: window, then verify on a sample, then row math.** (a) Minimal reprocessing window = the UNION of every broken run's own lookback span, not simply the calendar days the job failed — an early broken run's lookback can reach backward past the first failed run-date, and those earlier dates never self-heal on their own. (b) Before a full-window backfill, verify the FIXED model against a single day/partition first — confirm correctness AND idempotency (no duplication on a repeat run) — only then backfill at scale. (c) When a write pattern is stated: for each date compute touch count (how many broken runs' lookback spans include it); naive re-run gross rows = Σ(touch × rows); duplicate rows = Σ((touch − 1) × rows); idempotent (MERGE on natural key) end-state rows = Σ(rows per date). Cross-check: gross − idempotent = duplicates. Full derivation method: `references/backfill-math.md`.

**8. Postmortem-to-prevention: name the control class, don't author it.** Route data-test-shaped classes (schema drift, volume anomaly, semantic drift, logic regression) to `audit-model`/`generate-tests`. Mark credential expiry, infra/transient, and upstream dependency delay as operational/reliability controls — NOT data-test candidates. A flat, non-seasonal volume threshold trains alert fatigue; use a same-day-of-week seasonal baseline instead. See `references/pitfalls.md`.

**9. Emit the auditable deliverable.** Show evidence for every step, never just the final answer — see Output contract below.

## Output contract

In order (include sections for whichever sub-capability(ies) were run):
1. Scope line — sub-capability(ies), incident, confirmation it isn't one of the three neighbors.
2. Evidence-ladder trace (if classifying) — every rung's finding, including clean ones, ending in classification + discriminating signature.
3. Blast-radius table (if applicable) — every node bucketed, topology-then-timing shown, cross-footed against total node count.
4. Backfill correctness (if applicable) — window + derivation, explicit verify-on-sample step, naive-vs-idempotent row math if a write pattern was given.
5. Response-tier decision (if applicable) — override check first, then grid, then tier + rationale.
6. Root-cause confirmation — one line confirming the fix targets the evidence-ladder-located cause, not the loudest node.
7. Postmortem-to-prevention recommendation (if applicable) — control class, and whether it's a data-test candidate or an operational control.
8. Caveats — any assumed or missing inputs (containment timestamp, write pattern, prior-consumption fact) named explicitly, never silently assumed.

## Reference files

- `references/taxonomy-and-evidence.md` — full seven-class signatures + four-rung evidence ladder. Read when classifying.
- `references/blast-radius.md` — full traversal-plus-timing rule, bucket definitions, co-parent/detecting-node traps. Read when tracing a DAG incident.
- `references/response-framework.md` — full override-then-grid framework, criticality/impact definitions, decision table. Read when deciding a response tier.
- `references/backfill-math.md` — full window derivation, verify-before-scale rule, touch-count formulas with generalizable derivation method. Read when computing a backfill.
- `references/pitfalls.md` — the four named pitfalls in full (symptom-node patching, backfill-before-verify, alert fatigue, transient-vs-semantic). Read when Steps 2, 3, 6, 7, or 8 feel ambiguous.
- `references/scope-boundary.md` — full three-way neighbor fence with reciprocal quotes. Read at Step 1 when scope is unclear.
- `references/worked-examples.md` — four fixtures with boxed answers and named traps. Pattern-match against these before answering a multi-part incident; use their exact numbers/classifications as the deterministic oracle.

## When NOT to use

Redirect rather than attempt: **incremental-model-design** (choosing a lookback/write-strategy/partitioning scheme for a model that hasn't been built or is being redesigned), **sql-query-optimization** (a query that completes and returns a correct result but is slow), **root-cause-analysis** (the ops-domain Pareto/5-Whys/fishbone method for manufacturing/process defects). A request with no incident, no evidence, no DAG, and no lookback/write-pattern facts at all — nothing concrete to run — is also out of scope.
