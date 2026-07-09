<!-- iteration: 0 -->
# Worked Examples (Golden Fixtures)

Pattern-match against these before answering a multi-part incident. Use their exact numbers/classifications as the deterministic oracle. All four fixtures are set at **Cobalt Metrics, Inc.**, a fictional B2B SaaS analytics company running a Fivetran/Kafka ingestion layer into Snowflake, transformed with dbt, and orchestrated on Airflow. Each fixture stands alone.

---

## Fixture A: classify six failure narratives against the seven-class taxonomy

**Stated taxonomy (the seven allowed answers):** Classify each narrative into exactly one of: Schema Drift, Credential/Permission Expiry, Volume Anomaly, Semantic Drift, Infra/Transient, Logic Regression From a Deploy, Upstream Dependency Delay.

**Narrative 1.** Cobalt's `stg_accounts` model, built nightly at 01:00 UTC from the raw `raw_accounts` table (synced by Fivetran from the company's CRM), has failed for three consecutive nights. The Airflow task log for the 01:00 run shows:
```
dbt run --select stg_accounts
Compilation Error in model stg_accounts
  Database Error
    invalid identifier 'PLAN_TIER'
```
The CRM vendor's public changelog, checked by the on-call engineer, shows that on the day the failures began, the vendor renamed the `plan_tier` field to `subscription_tier` in their export schema with no prior notice. Cobalt's own dbt-project git log shows no merges in the two weeks prior to the failures. Row counts for `raw_accounts` are normal — within 2% of the 3-day rolling average.

**Narrative 2.** The nightly extract job for `raw_salesforce_opportunities`, run via a scheduled service-account OAuth token, has failed every run since 02:00 UTC Tuesday. The connector log shows:
```
[02:00:03] Starting extract: salesforce_opportunities
[02:00:04] AuthenticationError: INVALID_SESSION_ID: Session expired or invalid
[02:00:04] Extract aborted before any rows were read.
```
The identity-provider's audit log confirms the service account's OAuth refresh token, provisioned 90 days earlier, expired at 01:58 UTC Tuesday under the connected app's 90-day token-lifetime policy — no renewal reminder had been set. Salesforce's admin confirms the object layout is unchanged. No rows were ever read in any of the failed runs.

**Narrative 3.** The hourly job loading `raw_web_events` from a Kafka clickstream topic into Snowflake completed with SUCCESS status at 14:00 UTC, in a normal runtime (4m12s, within the usual 3-5 minute band), with no error anywhere in the log. The row count loaded was **0**, against a rolling 7-day average of roughly 1.2M rows for that hour. Downstream, `stg_web_events` (a left join against `raw_web_events`) also completed with SUCCESS and 0 new rows, because there was nothing to join. Checked afterward, Kafka consumer-lag metrics show 1.4M unconsumed messages sitting in the topic during that hour — the extract job's consumer group had silently rebalanced onto zero active partitions after a consumer-pod restart 45 minutes earlier, and the connector does not treat a zero-row load as an error condition by default.

**Narrative 4.** `fct_page_views` normally lands between 8.5M and 9.5M rows per day (7-day rolling average: 9.05M). Monday's run landed **91.2M rows** — roughly 10x normal — with SUCCESS status and a normal runtime (38 minutes, within the usual 35-40 minute band). A run-history diff shows the upstream `raw_page_views` ingestion connector (a Fivetran sync from a Kinesis firehose) ran **twice** that day: a teammate manually triggered a Fivetran "resync" at 09:14 UTC intending to test a schema change against a sandbox connector, but triggered it against the production connector ID by mistake. A resync re-loads the connector's full historical backfill window (the trailing 10 days), and the raw layer enforces no dedup key, so the backfilled data landed on top of the existing data.

**Narrative 5.** `fct_subscription_status` (schema unchanged — same columns, same types, all dbt schema tests green) feeds the churn-rate metric on the exec dashboard. The churn rate, historically stable in a 2.1%-2.6% weekly band, jumped to **9.8%** for the week of June 15, with no test failing (the table's existing suite is schema- and null-completeness-focused only; nothing checks value content). A diff of the `status` column's value distribution against the prior week's snapshot shows a new categorical value, `paused`, appearing for the first time — 6,200 of that week's 9,100 status changes. Product's change log confirms a self-serve "pause my subscription" feature shipped June 14; the upstream billing system began emitting `paused` as a legitimate status alongside `active`, `canceled`, and `trialing`. The churn-rate CASE statement in `fct_subscription_status`, written before this feature existed, treats any status other than `active`/`trialing` as churned — so all 6,200 paused accounts are being counted as churn.

**Narrative 6.** The nightly `int_order_items` dbt run — a large join across three ~40M-row staging tables — failed twice in the past week (Tuesday and Friday) but succeeded every other night, including nights with equal or higher row volume. Both failures show the identical error:
```
Snowflake Error: SQL execution error: Local disk space exceeded.
Query used more disk than allotted. Consider increasing warehouse size.
```
Both incidents self-resolved on a manual retry roughly 20 minutes later, with zero code, config, or data change of any kind. Warehouse-utilization metrics show both failure windows overlapped with an unrelated BI team's ad-hoc query workload spiking concurrent usage on the same shared warehouse to 3-4x its typical level for that hour. No deploys to `int_order_items` or its dependencies occurred in the two weeks prior to either incident.

### Known answers (boxed)

| # | Narrative | Classification | Discriminator applied |
|---|---|---|---|
| 1 | `stg_accounts` compile failure | **Schema Drift** | Fails after connection/read succeeds, during column reference; corroborated by vendor changelog; normal row count rules out volume; no Cobalt deploy rules out logic regression |
| 2 | Salesforce extract auth failure | **Credential/Permission Expiry** | Fails before any row is read; explicit session-expired error; corroborated by IdP token-expiry log; recurs every run (does not self-resolve like a transient) |
| 3 | Zero-row hourly web-events load | **Volume Anomaly** (zero rows) | SUCCESS status, normal runtime, but count is a hard floor violation (0 vs. ~1.2M baseline) visible only via run-history comparison |
| 4 | 10x `fct_page_views` spike | **Volume Anomaly** (10x rows) | SUCCESS status, normal runtime, count is a ceiling-violation multiple of baseline; traced via the connector's own operational trigger history, not a code deploy |
| 5 | Churn-rate jump via new `paused` status | **Semantic Drift** | Schema and completeness tests green, volume/runtime normal; surfaces only via a value-distribution diff; traced to a legitimate new value in an unchanged column |
| 6 | `int_order_items` disk-spill failures | **Infra/Transient** | Explicit resource-exhaustion signature; resolves on bare retry with zero change; correlates with a concurrency spike, not a deploy or data condition |

### Traps (must-not-equal)

- Narrative 3 must NOT equal **Infra/Transient** — a silently-empty load can read as "a system hiccup," but there is no resource-exhaustion signature anywhere in this narrative, and the job reports SUCCESS rather than an error that would resolve on retry. The only anomaly is a count that violates the historical baseline — that is the volume-anomaly signature, not the infra/transient one.
- Narrative 5 must NOT equal **Schema Drift** — a new value appearing in a column tempts a "the schema changed" read, but the narrative states explicitly that columns, types, and all schema tests are unchanged and green. Schema drift is a structural change to columns/types; this is a change in what an unchanged column's values mean — the defining case of semantic drift.
- Narrative 4 must NOT equal **Logic Regression From a Deploy** — a person did trigger the event that caused this, which can read as "a deploy," but "recent deploys" in the evidence-ladder sense means the pipeline's OWN code/config change history — Cobalt's dbt/orchestration git log shows nothing. The actual evidence trail is the ingestion connector's own operational trigger history (a manual resync), and the signature (SUCCESS status, count anomaly vs. baseline, no code change) is volume anomaly, not logic regression.
- Narrative 2 must NOT equal **Schema Drift** — both classes can surface as a "connection-ish" sounding failure, but the discriminator is WHERE in execution the failure lands: narrative 2's error fires before a single row is read (pure authentication failure), while schema drift fires only after a successful connection and read, during parsing or casting. Narrative 2 also has zero rows read across every failed attempt, which schema drift does not produce.
- Narrative 6 must NOT equal **Volume Anomaly** — row volume on the failure nights was equal to or lower than other nights that succeeded — the narrative states this explicitly. The anomaly here is a resource-exhaustion error tied to concurrent warehouse load, not a row-count deviation from baseline.

---

## Fixture B: blast radius across a twelve-node DAG

**The DAG** — Cobalt's nightly warehouse DAG, 12 nodes:

| Node | Model | Upstream of (feeds) | Scheduled run time |
|---|---|---|---|
| 1 | `raw_orders` (source ingest) | 4 | 01:00 |
| 2 | `raw_customers` (source ingest) | 5 | 01:00 |
| 3 | `raw_products` (source ingest) | 6 | 01:00 |
| 4 | `stg_orders` (staging) | 7, 8 | 01:30 |
| 5 | `stg_customers` (staging) | 8 | 01:30 |
| 6 | `stg_products` (staging) | 7 | 01:30 |
| 7 | `int_order_items` (intermediate) | 9 | 02:00 |
| 8 | `int_customer_orders` (intermediate) | 10 | 02:00 |
| 9 | `fct_revenue` (mart) | 11 | 02:30 |
| 10 | `dim_customer_ltv` (mart) | 12 | 02:30 |
| 11 | `rpt_daily_revenue_dashboard` (BI report) | — | 03:00 |
| 12 | `ml_churn_features` (feature pipeline) | — | 04:00 |

**The incident.** Node 4 (`stg_orders`) — due to a source schema drift in `raw_orders` (a vendor field rename cast silently to NULL rather than throwing) — completes its 01:30 run with bad data at **01:42**. No error is thrown; the failure is only discovered when the revenue dashboard (node 11) shows $0 at its 03:00 refresh, triggering an investigation that identifies `stg_orders` as the source and **quarantines it (blocking any node from consuming it) at 03:20**.

**Question.** Using the DAG's edges and each node's scheduled run time against the 01:42 failure and the 03:20 quarantine, classify every node into exactly one of: the failed/origin node, ran on bad data (consumed node 4's output, directly or transitively, before quarantine took effect), safe — never downstream of node 4, or safe — downstream of node 4 but blocked before its scheduled run.

**Solution.** Step 1 — descendant set by graph traversal: node 4 feeds 7 and 8; node 7 feeds 9; node 8 feeds 10; node 9 feeds 11; node 10 feeds 12. Descendants of node 4: {7, 8, 9, 10, 11, 12}. Step 2 — every node NOT in that set, and not node 4 itself, is safe regardless of timing: {1, 2, 3, 5, 6}. Step 3 — for each descendant, compare scheduled time to 03:20 quarantine:

| Node | Scheduled | vs. 03:20 quarantine | Result |
|---|---|---|---|
| 7 | 02:00 | before | ran on bad data |
| 8 | 02:00 | before | ran on bad data |
| 9 | 02:30 | before | ran on bad data |
| 10 | 02:30 | before | ran on bad data |
| 11 | 03:00 | before | ran on bad data |
| 12 | 04:00 | after | safe — blocked in time |

Step 4 — cross-foot: origin (1) + safe non-descendant (5: nodes 1,2,3,5,6) + ran on bad data (5: nodes 7,8,9,10,11) + safe-blocked (1: node 12) = 1 + 5 + 5 + 1 = 12, matching the DAG's node count.

### Known answers (boxed)

- Failed/origin node: **{4}**
- Ran on bad data: **{7, 8, 9, 10, 11}**
- Safe — never downstream of node 4: **{1, 2, 3, 5, 6}**
- Safe — downstream of node 4, blocked before its scheduled run: **{12}**

### Traps (must-not-equal)

- Node 12 must NOT be bucketed **"ran on bad data"** — node 12 IS a descendant of node 4 (via node 10) and it is tempting to put every descendant into the "ran on bad data" bucket by topology alone. But node 12's scheduled run (04:00) falls AFTER the 03:20 quarantine — it never executed against the tainted input. Blast radius is topology multiplied by timing, not topology alone.
- Node 6 must NOT be bucketed **"ran on bad data"** — node 6 (`stg_products`) feeds node 7, which DID run on bad data — but node 6 itself is built from `raw_products` (node 3), a completely independent lineage from node 4 (`stg_orders`). Node 6's own output was never touched by the failure; it is node 7, which joins node 6's clean output against node 4's tainted output, that becomes tainted. Being a co-parent of a tainted node does not make a node itself tainted.
- Node 11 must NOT be bucketed **"safe"** — node 11 is the node that surfaced the incident (the $0 dashboard at its 03:00 refresh) — a natural instinct is to treat the detecting node as "caught in time" since it's the one that raised the alarm. But detection happening AT node 11's own scheduled run means node 11 already executed on the bad data before anyone knew to stop it; the alarm firing is a consequence of having already run on bad data, not a sign of having been protected from it.

---

## Fixture C: backfill correctness for an incremental model with a 2-day lookback

**The model.** `fct_daily_sessions` is an incremental dbt model with a stated **2-day lookback**: each daily run for date X reprocesses event-dates [X-2, X-1, X] to catch late-arriving session events, merged (upserted) on `(session_id, event_date)`.

**The failure.** A logic regression (deployed May 31 evening, reverted June 6 morning) broke `fct_daily_sessions`'s output for every scheduled run from **June 1 through June 5 inclusive** (5 run-days). Daily event-date row volumes (the true row count that belongs to each event_date, regardless of which run's lookback touches it):

| Event date | Row count |
|---|---|
| May 30 | 48,000 |
| May 31 | 51,000 |
| Jun 1 | 53,000 |
| Jun 2 | 49,500 |
| Jun 3 | 52,250 |
| Jun 4 | 47,800 |
| Jun 5 | 50,900 |

**Question.** (1) What is the minimal correct reprocessing window needed to fully repair `fct_daily_sessions`? (2) If the repair is executed as five naive re-runs (plain INSERT, no dedup key) of the June 1–June 5 jobs, how many total rows are written, and how many of those are duplicate ("double-processed") rows caused by overlapping lookback windows? (3) If the same five re-runs are executed idempotently (MERGE on `(session_id, event_date)`), what is the correct end-state row count?

**Solution.** Step 1 — minimal reprocessing window: each broken run for date X touches event-dates [X-2, X]. Union of every broken run's window (Jun1: May30,May31,Jun1; Jun2: May31,Jun1,Jun2; Jun3: Jun1,Jun2,Jun3; Jun4: Jun2,Jun3,Jun4; Jun5: Jun3,Jun4,Jun5) = **May 30 through June 5**, 7 calendar days. Step 2 — touch count per date:

| Event date | Row count | Touched by runs | Touch count |
|---|---|---|---|
| May 30 | 48,000 | Jun1 | 1 |
| May 31 | 51,000 | Jun1, Jun2 | 2 |
| Jun 1 | 53,000 | Jun1, Jun2, Jun3 | 3 |
| Jun 2 | 49,500 | Jun2, Jun3, Jun4 | 3 |
| Jun 3 | 52,250 | Jun3, Jun4, Jun5 | 3 |
| Jun 4 | 47,800 | Jun4, Jun5 | 2 |
| Jun 5 | 50,900 | Jun5 | 1 |

Cross-check: total touches = 1+2+3+3+3+2+1 = 15 = 5 runs × 3 dates per run's lookback. Matches.

Step 3 — naive re-run gross rows written = Σ(touch count × row count): May30 1×48,000=48,000; May31 2×51,000=102,000; Jun1 3×53,000=159,000; Jun2 3×49,500=148,500; Jun3 3×52,250=156,750; Jun4 2×47,800=95,600; Jun5 1×50,900=50,900. **Total gross rows written: 760,750.**

Step 4 — idempotent end state (each date written exactly once): 48,000+51,000+53,000+49,500+52,250+47,800+50,900 = **352,450.**

Step 5 — duplicate rows under naive re-run = Σ((touch count − 1) × row count): May30 0; May31 (2-1)×51,000=51,000; Jun1 (3-1)×53,000=106,000; Jun2 (3-1)×49,500=99,000; Jun3 (3-1)×52,250=104,500; Jun4 (2-1)×47,800=47,800; Jun5 0. **Total duplicate rows: 408,300.** Cross-check: 760,750 − 352,450 = 408,300, matching.

### Known answers (boxed)

- Minimal correct reprocessing window: **May 30 – June 5 (7 calendar days)**
- Naive re-run gross rows written: **760,750**
- Naive re-run duplicate (double-processed) rows: **408,300**
- Idempotent re-run correct end-state row count: **352,450**

### Traps (must-not-equal)

- Reprocessing window must NOT equal **"June 1 - June 5 (5 days, the days the job failed)"** — this is the reprocessing window a naive reading of "the job failed on these 5 days" produces, but it ignores that Jun1's own lookback reaches back to May 30 and Jun2's reaches back to May 31 — those two earlier dates may have received a corrupted upsert from the broken runs even though the job didn't "fail" ON May 30 or May 31 themselves. The window has to be widened backward by the full lookback amount from the FIRST broken run-date.
- Naive re-run row count must NOT equal **"352,450 (same as idempotent)"** — it is tempting to assume a re-run "just fixes" the data regardless of write pattern, but a naive re-run without a MERGE key does not overwrite prior writes — it appends on top of them. Every date touched by more than one of the five overlapping lookback windows gets written multiple times, inflating the true row count of 352,450 up to a gross 760,750.
- Most-duplicated date must NOT equal **"May 30 or June 5"** — the endpoints of the reprocessing window (May 30 and Jun 5) are each touched by only ONE of the five re-runs and carry zero duplication. The dates in the MIDDLE of the window (Jun 1, Jun 2, Jun 3) are touched by all three overlapping lookback spans that can reach them and carry the heaviest duplication (106,000 / 99,000 / 104,500 rows respectively) — overlap concentrates in the interior of the window, not at its edges.

---

## Fixture D: judgment — stop-the-line vs. quarantine-and-continue vs. silent-fix

**Stated decision rule.** Apply in order: (1) If any downstream consumer has already acted on the bad data before detection (a report was sent, an automated decision fired, a number was already relied on), silent-fix is not available — escalate to at least QUARANTINE-AND-CONTINUE regardless of how the criticality/impact grid below would otherwise classify it. (2) Otherwise, classify consumer criticality as HIGH (financial reporting, regulatory/external delivery, production ML training or serving, customer-facing billing/compliance) or LOW (internal exploratory use, unshipped/unlaunched surfaces, dev/staging). (3) Classify data-correctness impact as SEVERE (wrong in a way that cannot be cheaply isolated or filtered, risks being silently trusted) or BOUNDED (isolable to an identifiable subset/partition, or degrades gracefully). (4) Decision: HIGH + SEVERE → STOP-THE-LINE. HIGH + BOUNDED → QUARANTINE-AND-CONTINUE. LOW + (SEVERE or BOUNDED), no prior consumption → SILENT-FIX.

**Incident 1.** A logic regression from yesterday's deploy causes `fct_revenue` — which feeds both the daily executive P&L dashboard and an automated 6:00 AM revenue-recognition journal-entry feed into the ERP — to double-count refunds as negative revenue, understating revenue by roughly 8% with no bound on which rows are affected (the double-count is embedded in an aggregate, not isolable to specific transactions). This morning's 6:00 AM automated journal-entry feed already posted the understated figures to the ERP before the 9:00 AM detection.

**Incident 2.** A source schema drift (a vendor renamed a currency field) leaves 40 of 50,000 rows in an internal prototype table NULL on currency. The table is used only by two data scientists experimenting with a not-yet-launched churn model; nothing downstream is wired to it, and nothing has consumed it since the drift occurred.

**Incident 3.** A volume anomaly (an upstream API silently dropped a filter, returning 3x the expected order rows with duplicate `order_id`s) hits `int_order_items`, which feeds the executive revenue dashboard. An automated volume-anomaly monitor catches the spike and pauses the pipeline before the dashboard's scheduled refresh runs — no consumer has seen the bad data. The duplicates are exact-duplicate `order_id`s from a mechanical replay, cleanly identifiable and removable via a dedup pass.

**Incident 4.** An upstream dependency delay causes a marketing-spend join to silently fall back to a 5-day-stale cached snapshot (a fallback-on-stale-data misconfiguration) instead of blocking, feeding a low-stakes internal marketing-efficiency dashboard used only by the marketing team. Normally low-criticality and bounded — except the dashboard auto-emails a weekly summary to the marketing director every Monday 8:00 AM, and that email already went out this morning using the stale numbers, before anyone caught the delay.

**Solution.** Incident 1: rule step 1 fires first (journal-entry feed already posted); independently, grid also lands HIGH+SEVERE. Both paths converge. Incident 2: no prior consumption, LOW criticality, BOUNDED impact. Incident 3: no prior consumption (monitor paused before scheduled refresh), HIGH criticality, but BOUNDED impact (mechanically dedupeable exact-duplicate keys). Incident 4: this is the case built to test the override in isolation — on the grid alone this looks LOW+BOUNDED (silent-fix), but rule step 1 fires first (the weekly email already went out using stale numbers) — override applies regardless of how low-stakes the rest of the picture looks.

### Known answers (boxed)

- Incident 1 (revenue double-count, already posted to ERP): **STOP-THE-LINE**
- Incident 2 (prototype table, unlaunched, no consumers): **SILENT-FIX**
- Incident 3 (order duplication, caught before dashboard refresh): **QUARANTINE-AND-CONTINUE**
- Incident 4 (stale marketing dashboard, email already sent): **QUARANTINE-AND-CONTINUE**

### Traps (must-not-equal)

- Incident 4 decision must NOT equal **SILENT-FIX** — every surface fact about incident 4 (low criticality, an internal-only dashboard, a bounded one-week discrepancy) points toward silent-fix if the criticality/impact grid is applied without first checking rule step 1. But the weekly summary email already went out using the stale numbers: a consumer has already acted on the bad data. The consumption override applies BEFORE the grid is even consulted, and it overrides what the grid alone would suggest.
- Incident 1 decision must NOT equal **QUARANTINE-AND-CONTINUE** — quarantine-and-continue is the right call when the bad data is boundable and can be isolated while good data keeps flowing. Incident 1's error is baked into an aggregate revenue figure with no isolable subset of "the wrong rows" — the entire feed is untrustworthy, criticality is at its highest tier (an ERP journal entry, not just a dashboard), and the bad number has already been posted. Both the severity and the prior-consumption override point to the more aggressive response.
- Incident 3 decision must NOT equal **STOP-THE-LINE** — executive-dashboard criticality alone can read as an automatic stop-the-line trigger, but the rule weighs criticality AND impact together, and a mechanically deduplicable exact-duplicate-key problem, caught before any consumer saw it, is a bounded-impact case — the correct response contains the specific bad partition while letting the rest of the pipeline and its unaffected consumers keep running, not a full halt.
- Incident 2 decision must NOT equal **QUARANTINE-AND-CONTINUE** — it is tempting to default to quarantine-and-flag as the "safe middle choice" for any incident involving bad data, even a low-stakes one. But the stated rule reserves quarantine for cases where criticality is high OR consumption already occurred. Neither applies here — no consumer exists yet, and the table is explicitly unlaunched — so the ceremony of a formal quarantine is unwarranted; patch and rerun.
