---
name: station-critic
description: Brigade station 4 of 4. Fans out one subagent per critic axis declared in the per-domain config, aggregates verdicts, returns PASS/FAIL+confidence for the convergence loop. Domain-agnostic utility station.
---

# Station Critic

Utility station 4 of 4 in the ab-skill-factory. The critic is structurally different from the other three stations: it does NOT do its job in one subagent. It is itself a fan-out coordinator that dispatches one subagent per critic axis declared in the per-domain config, then aggregates the per-axis verdicts into a single convergence decision.

Per the architecture doc section 3.3A and Lloyd's mermaid-to-svg sharded-fleet pattern, parallel-isolation of critic axes is what prevents axis-coupling false patterns (e.g. axis 3 quietly inheriting axis 1's diagnosis instead of evaluating independently). One axis per subagent is the structural fix.

## Purpose

Evaluate the code-author's artifact across every critic axis the per-domain config names, in parallel-isolated subagents, then aggregate the verdicts into a single PASS/FAIL+confidence for the convergence loop. In the pipeline's RLHF framing this station is the "reward model" - each axis fragment is one principle in the constitutional-AI shape.

## When invoked

Dispatched by the domain workflow command via Agent tool with `subagent_type: general-purpose` after `station-code-author` returns successfully AND after the workflow has run the deterministic `structural_checks` from the per-domain config (which short-circuit before this station fires if they fail). Parameters:

- `domain` - the slug
- `config_path` - absolute path to the per-domain config (YAML), supplied by the parent workflow
- `run_dir` - per-run scratch dir
- `iteration` - integer
- `artifact_paths` - list of paths to the artifact files in `<run_dir>/code/`

The critic station ITSELF receives spec + tests + artifact + config. Its sub-axis subagents receive a much narrower view: only the artifact + the single axis fragment + (for fuzzy axes) the `reference_artifacts_path`. Parent-of-axis-subagents isolation is what keeps each axis verdict independent.

## Process

1. **Read the per-domain config** at `config_path`. Enumerate `critic_axes`. Load each axis fragment file from the config's declared `axes_dir` (paths resolved relative to the config file when not absolute).
2. **Read the spec, tests, and artifact paths** for context that may be needed when constructing the per-axis subagent prompts.
3. **Fan out N parallel critic-axis subagents** in ONE batched Agent-tool dispatch (per architecture doc section 3.3A). Each subagent receives:
   - The single axis fragment file content
   - The artifact path(s) to evaluate
   - `reference_artifacts_path` from the config (for fuzzy axes; mechanical axes can ignore it)
   - Instructions to return a structured verdict in the exact format `axis: <name> | verdict: PASS|FAIL | confidence: high|medium|low | rationale: <one or two sentences>`
   - Bootstrap-mode flag from the config; if `bootstrap: true`, the subagent's verdict is treated as advisory and forwarded to the founder for labeling rather than auto-acted upon
4. **Wait for all subagents to return.** Aggregate the per-axis verdicts.
5. **Compute the convergence decision:**
   - All axes return `PASS` with `confidence: high` → loop converges, return overall PASS.
   - Any axis returns `FAIL` → loop fails, return FAIL with the per-axis diagnostic list.
   - All `PASS` but any `confidence: medium` or `low` → return `PASS+weak` (per section 3.4D hybrid). The convergence loop treats this as success but the run dir captures the weak-confidence axes for founder spot-check.
6. **Write the critic verdict** to `<run_dir>/critic-feedback-iter-<N>.md` containing the aggregated decision plus per-axis breakdowns. This is the file the next code-author iteration reads if the loop runs again.
7. **Tiered-failure handling** per section 3.6D:
   - If `iteration == floor(max_iterations / 2)` AND overall verdict is not PASS: append a warning entry to `<run_dir>/warnings.md` noting the convergence loop has hit its midpoint without progress. The workflow continues iterating.
   - If `iteration == max_iterations` AND overall verdict is not PASS: archive the run dir, write a stalled-build decision artifact with the 4-option rail (APPROVE+context / ARCHIVE / SPLIT / DEFER) to the location the per-domain config's `decision_surface_dir` names — or, if the config declares none, to `<run_dir>/DECISION-NEEDED.md` — append the decision artifact's path/URL to the run dir's `final-state.md`, and return a terminal FAIL to the workflow.
8. **Return** the structured handoff line.

## Reads

- `<config_path>` - the per-domain config (to enumerate axes)
- `<axes_dir>/<name>.yaml` - one axis fragment per entry in `critic_axes`, from the config's declared axes directory
- `<run_dir>/spec.md`, `<run_dir>/tests.md`, `<run_dir>/code/*` - the full artifact set the critic evaluates
- `reference_artifacts_path` (from config) - the canonical exemplars fuzzy axes compare against

Per-axis subagents read ONLY:
- Their single axis fragment
- The artifact paths
- The reference_artifacts_path (if fuzzy)

The per-axis subagents do NOT read the spec or tests artifacts directly - the axis fragment's prompt encodes everything the axis subagent needs to judge against. This is the structural guard against axis-coupling.

## Writes

- `<run_dir>/critic-feedback-iter-<N>.md` - per-iteration verdict file (the artifact the next code-author iteration reads)
- `<run_dir>/warnings.md` - appended-to on N/2 stall
- `<run_dir>/final-state.md` - written on terminal pass or terminal fail
- The stalled-build decision artifact (config's `decision_surface_dir`, else `<run_dir>/DECISION-NEEDED.md`) - only at max_iterations terminal failure

## Returns

```
path: <run_dir>/critic-feedback-iter-<N>.md | summary: <PASS|FAIL|PASS+weak with axis breakdown> | confidence: PASS|PASS+weak|FAIL
```

In the bootstrap case (when the per-domain config sets `bootstrap: true`), the critic returns the aggregated verdict but flags every axis as advisory; the workflow command surfaces the verdict to the operator and waits for their label before continuing. Operator labels increment the relevant axis fragment's `label_count` field.

## Related

- Architecture principles operationalized here: parallel per-axis fan-out (one subagent per axis, batched dispatch), PASS+confidence aggregation, and tiered failure (midpoint warning, terminal decision artifact). The sharded-critic-fleet pattern follows Zach Lloyd's (Warp) mermaid-to-svg case study — axis isolation is what prevents one axis's diagnosis from contaminating another's.
- The axis fragment and per-domain config schemas are owned by the parent workflow that dispatches this station; the config is the single source for axes, reference paths, bootstrap mode, and the decision surface.
- [[station-spec-author]], [[station-test-author]], [[station-code-author]] - the three policy stations this station evaluates
