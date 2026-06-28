# skill-dev-pipeline — Working Design (v2)

> **Status: living doc, co-developed.** PR #6 shipped v1 (the working pipeline + the variance-analysis worked example). This captures the v2 architecture as it's being designed. Open questions are at the bottom — edit freely.

## 1. The composition pattern (and what to name it)

Three layers, each a clean abstraction boundary. This is the **house pattern** — it is *not* skill-specific; the same shape drives any multi-phase production line.

| Tier | Role | Owns |
|---|---|---|
| **Seat** | an atomic skill — one phase / one concern | doing its one job well, in isolation |
| **Pipeline** | the orchestrator — runs one item through the seats | sequencing, phase state, the convergence (rework) loop, approve/escalate |
| **Fleet** | the batch driver — fans the pipeline over a queue | parallelism, the backlog walk, shared run state |

Naming is an aesthetic call (override if it doesn't sing). `seat` and `pipeline` are already in use; the only new name is the batch tier — proposed **`fleet`** (swap to `floor` / `batch` if `fleet` collides with other RDCO usage). The reusable whole = "the pipeline stack."

## 2. The skill interface contract

Every skill declares three things (its "type signature"):

1. **Input parameters** — the structured arguments the skill takes.
2. **Accessible context** — the depth/reference material it can pull from (formulas, a corpus, policy, exemplars). Distinct from inputs: context is *what it knows*, inputs are *what it's given this run*.
3. **Expected output** — the artifact/effect it produces, and in what shape.

The skill *type* (below) determines what each of these looks like and how the skill is evaluated.

## 3. Skill type taxonomy

`computational` vs `corpus` was the start; the fuller set:

| Type | What it does | Input | Accessible context | Output | Eval method |
|---|---|---|---|---|---|
| **Computational** | deterministic procedure over structured data | structured params/data | rules/formulas (small) | computed result | **synthetic golden fixtures** (known answers) |
| **Corpus / analytical** | reason over documents | document(s) / corpus ref | the corpus | extraction / synthesis | sample docs + expected extraction; rubric for synthesis |
| **Generative / authoring** | produce an artifact | brief + style/context | templates, exemplars, brand | a document / asset | rubric / judge panel (quality) |
| **Operational / tool-using** | run a workflow against systems | params + system access | live system state / APIs | an effect + report | state-change check in a sandbox |
| **Advisory / judgment** | recommend / classify / route | a case / situation | policy / criteria | a verdict + rationale | labeled decisions / held-out cases |

The taxonomy isn't cosmetic — **type drives the input contract and the eval harness.** `variance-analysis` is computational, which is exactly why synthetic-with-known-answers fixtures work for it.

## 4. Context bundles and context-prep

The pipeline's input generalizes from `{name, dept, competency_excerpt}` to **`{name, context_bundle_ref}`**. The bundle is any depth source; a separate **context-prep skill** builds it. This keeps the pipeline domain-agnostic and makes context-acquisition its own reusable capability.

**The symmetry:** context-prep (acquire + distill the depth source) → pipeline (build the artifact). The front step is a general "learn the domain / gather the inputs" move that recurs across artifact types, not just skills.

**Backend is pluggable — bind to the bundle *interface*, not a retrieval tech:**

- **Internal / dev / demo:** a markdown corpus + local lexical+vector search (Obsidian + QMD-style). Cheap, versioned, no per-query cost, sufficient for building skills. Validated by the broader "context-as-files" movement (markdown corpora + `llms.txt`-style packaging; Shopify is showing it has legs).
- **Enterprise / client production:** a governed store co-located with the data (e.g. Snowflake Cortex Search where the client already lives in Snowflake). The premium buys **governance (RBAC), scale, freshness, and data-gravity** — retrieval living where the data already is — *not* merely better relevance. Reserve it for where those actually matter; **default to the cheap local approach.**

## 5. Evaluation: static + execution

- **Static critic (shipped):** N adversarial axes read the authored skill + spec + tests and judge structure/fidelity/specificity. Catches *structural* problems.
- **Execution-eval critic (planned):** actually *runs* the authored skill on the acceptance scenarios and grades output vs expected. Catches *behavioral* problems.

**Where the sample data lives:** in the acceptance contract. The test author already writes scenarios — extend it to emit **golden fixtures = `{input data, expected output}`.** For computational skills, fixtures are synthetic-with-known-answers (you own the ground truth). For corpus skills, package a representative sample document + expected extraction. The fixture is part of the contract, so the *same* artifact drives both static review and execution eval.

## 6. Production-wiring expectation (toy → system-of-record)

A skill ships with toy/golden examples to **prove the capability**. It must also document **how to wire into production**: the inputs the skill needs, sourced in production from the customer's *system of record*.

> Example (`variance-analysis`): the toy fixtures prove the procedure. In production you hook the inputs into the observability / revenue-reporting / cost-accounting system that holds the actual-vs-standard data for the assets you're monitoring.

The principle, stated in every skill:

> We demonstrate the skill working on toy examples. Realizing the full agentic benefit is **your** integration: wire the skill's inputs into your system of record / data plane.

This separates **capability** (the skill — the procedure) from **integration** (the plumbing to your systems) and sets honest expectations about the last mile.

## Open questions (for discussion)

- **Naming** — confirm `seat / pipeline / fleet` (or the alternative).
- **Context vault** — is QMD/Obsidian the standing internal backend, with an enterprise backend (Cortex Search / etc.) only behind the interface for governed client contexts? Cost vs governance tradeoff.
- **Skill types** — is the 5-type taxonomy complete, or are there others (interactive/elicitation? multi-skill/composite?)?
- **Context-prep skill** — build it next as its own seat, against the bundle interface?
- **Execution-eval** — wire it as a 6th critic axis, or a separate gate after the static critic passes?
