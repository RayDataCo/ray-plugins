<!-- iteration: 0 -->
# Scope Boundary — The Three Neighbor Fences

Read this at Step 1 when scope is unclear. This skill diagnoses and responds to **an existing pipeline that broke**. It does not do incremental-model-design, sql-query-optimization, or root-cause-analysis. The trigger must actively decline all three neighbors, not just fail to mention them.

## Fence 1 — incremental-model-design (reciprocally corroborated)

**Not this skill's job:** the DESIGN-TIME discipline of choosing a lookback window's length, a merge/upsert vs. append-only vs. insert-overwrite write strategy, a partitioning or SCD-handling approach for a model that hasn't been built yet, or a redesign of an existing one.

**This skill's job:** diagnosing an EXISTING model's break against its already-stated design. It does not choose that design.

**Reciprocal quote** (from `incremental-model-design/interpretation.md`'s own scope-boundary section, stating the identical split from the other side): "It does not cover what happens when the pipeline itself breaks... designing that idempotency is this competency's job, and diagnosing and responding to the failure itself is not."

**Discriminator:** "what lookback window should this NEW model use" (design-time choice) vs. "our incremental model failed last night with a duplicate-key error" (an EXISTING model that broke).

## Fence 2 — sql-query-optimization (reciprocally corroborated)

**Not this skill's job:** rewriting a slow-but-*correctly-completing* query for sargability, join order, clustering keys, or micro-partition pruning.

**This skill's job:** stops at recognizing an infra/transient resource-exhaustion signature and routing the finding (e.g. "this warehouse needs a size bump"); actually rewriting the query is `sql-query-optimization`'s job. A query that fails outright belongs here until it's fixed to the point of successful, correct completion — only then does it become a candidate for `sql-query-optimization`'s analysis.

**Reciprocal quote** (from `sql-query-optimization/interpretation.md`'s own scope-boundary section, stating the identical split): "SQL query optimization assumes the query runs to completion and returns the correct result... A query that fails outright is a pipeline-failure-triage problem until it is fixed to the point of successful, correct completion — only then does it become a candidate for this competency's analysis."

**Discriminator:** "this job keeps failing with a disk-spill error" (fails outright — in scope, infra/transient territory) vs. "this query runs but it's slow, can we add a clustering key" (completes correctly, just slow — out of scope).

## Fence 3 — root-cause-analysis, the ops-domain sibling (one-sided; asymmetric)

**Not this skill's job:** the ops/manufacturing-domain investigation method — Pareto vital-few analysis, branching 5-Whys, evidence-based cause verification, 6M fishbone classification, root-cause-vs-band-aid-vs-unverified-cause countermeasure taxonomy — applied to manufacturing/process defects.

**This skill's job:** shares deep structural DNA with root-cause-analysis (evidence before conclusion, verification discipline, response classified against a stated rule) but has its own vocabulary, evidence ladder, taxonomy, and response framework built specifically for data pipelines.

**Quote, one-sided** (this competency's own `interpretation.md` states the fence directly; `root-cause-analysis`'s own `interpretation.md` does NOT reciprocate — it states a three-way scope fence against `spc-control-charts`, `process-capability-analysis`, and `sop-authoring` only, with no mention of this competency): "this competency can be described as root-cause-analysis's method applied to the data-pipeline domain... authored as its own competency... because the vocabulary, evidence sources, and decision framework are different enough that collapsing them would blur both." Treat this quote as the authoritative statement of the fence, since it is unreciprocated on the other side.

**Discriminator:** "walk me through triage of this pipeline incident using logs, run history, data diff, deploys" (this competency's own evidence-source vocabulary) vs. "run a 5-Whys and build a fishbone diagram on this manufacturing defect" (ops-domain method vocabulary) — despite the structural-DNA overlap, fire on data-pipeline evidence sources and taxonomy, not on ops-domain method vocabulary.

## The empty-ask carve-out

A request with no incident, no evidence, no DAG, and no lookback/write-pattern facts at all — e.g. "explain how blast-radius analysis works" in the abstract, with nothing concrete to classify, trace, or compute — is also out of scope. There is nothing to run without a real incident's data in hand.
