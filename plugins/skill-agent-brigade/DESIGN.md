# skill-agent-brigade — Working Design (v2)

> **Status: living doc, co-developed.** PR #6 shipped v1 (the working pass + the variance-analysis worked example). This captures the v2 architecture as it's being designed. Open questions are at the bottom — edit freely.

## Naming (canonical)

The settled brigade vocabulary — one place, one definition each. Use these exact terms in code and prose; this block is the single source of truth.

- **brigade** — the whole system: the multi-agent assembly line that builds skills (this plugin, `skill-agent-brigade`).
- **station** — one atomic skill / one phase (spec, test, author, critic). Does its single job in isolation; hands off via a file artifact.
- **the pass** — the layer that runs one ticket through the stations: sequencing, phase state, the convergence (rework) loop.
- **expo** — the deciding agent *at* the pass. Routes each ticket using the exit set, holding the phase/ticket state and cross-station context a single-shot critic lacks. (The pass is the layer; the expo is the role inside it.)
- **steward** — the front-of-house role: pairs a request to the menu (use-case catalog), gathers + curates context from the cellar (vault-first, careful-external second), writes a contract-valid ticket, and enqueues it. Also repairs `needs-context` tickets. (See skills/steward/.)
- **rail** — the queue/batch layer: the pluggable mutable ticket store with lease/ack semantics plus the loop that fans the pass over a backlog of tickets (see RAIL-SPEC.md).
- **ticket** — the unit of work flowing through the brigade, defined once in **TICKET-CONTRACT.md** (the FOH↔brigade port): inline context manifest + Order + snapshot + work log + artifacts; it *is* the context bundle (payload schema: BUNDLE-SPEC.md), marked up at each station hop.
- **menu** — a brigade's published input contract: artifact types offered + per-type payload requirements. Per-brigade asset, expo-authored via a discovery ticket (`artifact: menu`), published beside the rail, read by stewards (see MENU-SPEC.md). The envelope (TICKET-CONTRACT) is universal; the menu is what's kitchen-specific.
- **cellar** — the house knowledge store, its own port (CELLAR-SPEC.md): brigades `land` provenance-stamped outputs, stewards `search`/`list` to gather. Filesystem/vault v1; Drive, S3, Snowflake Stage as driven adapters.
- **exit set** — the expo's closed disposition vocabulary, used verbatim: `advance · refire-to-author · reroute-to-spec · reroute-to-steward · kill`.

## 1. The composition pattern

Three layers, each a clean abstraction boundary. This is the **house pattern** — it is *not* skill-specific; the same shape drives any multi-phase production line.

| Tier | Role | Owns |
|---|---|---|
| **Station** | an atomic skill — one phase / one concern | doing its one job well, in isolation |
| **The pass** | runs one ticket through the stations; the **expo** is the deciding agent | sequencing, phase state, the convergence (rework) loop, the exit-set routing decision |
| **Rail** | the queue layer — fans the pass over a backlog of tickets | parallelism, the backlog walk, shared run state, the ticket store |

Naming is settled (see the **Naming (canonical)** block above) — `steward / station / the pass (expo) / rail`, with the whole = the **brigade** and the unit of work = a **ticket**. The expo routes each ticket via the closed exit set `advance · refire-to-author · reroute-to-spec · reroute-to-steward · kill`.

**The hexagonal frame (2026-07-01, cellar added 2026-07-02):** the brigade core (stations + the pass) talks only to four **ports** — the ticket contract (FOH↔brigade), the rail (storage/queue), the resolver (context bytes by source type), and the cellar (durable knowledge: brigades land outputs, stewards gather — [CELLAR-SPEC.md](./CELLAR-SPEC.md)). The steward is a driving adapter; vault/Snowflake rails, the per-type resolvers, and the filesystem/Drive/S3/Stage cellar backends are driven adapters. Contracts are enforced on both sides of the ticket port (steward at enqueue, expo at pull). Full port table + schema: [TICKET-CONTRACT.md](./TICKET-CONTRACT.md).

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

## 4. Context bundles and the steward

The brigade's input is **the ticket itself** — one canonical shape, defined in [TICKET-CONTRACT.md](./TICKET-CONTRACT.md): identity + inline typed-source context manifest + `## Order`. (Earlier iterations here — `{name, dept, competency_excerpt}`, then `{name, context_bundle_ref}` — are both retired; the contract's Supersedes table records them.) The **steward** (skills/steward/) builds the payload. This keeps the brigade domain-agnostic and makes context-acquisition its own reusable capability.

**The symmetry:** the steward (acquire + distill the depth source, front of house) → the brigade (build the artifact, back of house). The front step is a general "learn the domain / gather the inputs" move that recurs across artifact types, not just skills — and phase-0's `reroute-to-steward` closes the front-end loop the way `refire-to-author` closes the back-end one.

**Backend is pluggable — bind to the bundle *interface*, not a retrieval tech:**

- **Internal / dev / demo:** a markdown corpus + local lexical+vector search (Obsidian + QMD-style). Cheap, versioned, no per-query cost, sufficient for building skills. Validated by the broader "context-as-files" movement (markdown corpora + `llms.txt`-style packaging; Shopify is showing it has legs).
- **Enterprise / client production:** a governed store co-located with the data (e.g. Snowflake Cortex Search where the client already lives in Snowflake). The premium buys **governance (RBAC), scale, freshness, and data-gravity** — retrieval living where the data already is — *not* merely better relevance. Reserve it for where those actually matter; **default to the cheap local approach.**

## 5. Evaluation: static critics + the execution-eval station

Three evaluation surfaces, deliberately different shapes:

- **Deterministic lint axis (shipped):** a single programmatic check (no model call) that reads the authored `SKILL.md` and returns pass/fail per hard rule from Anthropic's skill guide. Unlike the LLM axes below it does not *judge* — it *verifies* mechanical conformance, so it is a hard gate, not a vote. See §5.0.
- **Static critics (shipped):** N adversarial *LLM* axes read the authored skill + spec + tests and judge structure/fidelity/specificity. Cheap, fast, read-only, fan out in parallel, vote PASS/FAIL. They answer *"is this well-built?"* and run on **every author revision** — the fast inner loop.
- **Execution-eval station (§5.1+):** actually *runs* the authored skill and measures whether it beats the base model. It answers a different question — *"does this skill earn its place?"* — and is expensive (multi-sample, two arms), so it runs as a **gate at the end of the build**, not every revision.

### 5.0 The deterministic lint axis (mechanical conformance, not a judgment vote)

The LLM critic axes are *judgments* — each is a model call that votes PASS/FAIL with a confidence. The lint axis is the opposite: a **pure function** over the `SKILL.md` file, every rule objectively pass/fail with zero model variance. It runs in the critic phase alongside the LLM axes, but its result is a **hard gate** (any rule FAIL fails the axis) rather than a weighted vote. It is wired in the reference workflow as `skillLint()` (see [`workflow/brigade-variance-analysis.run.js`](./workflow/brigade-variance-analysis.run.js)). The eight hard rules, sourced from Anthropic's skill-authoring guide:

1. **Filename** is exactly `SKILL.md`.
2. **`name` is kebab-case** (lowercase, digits, hyphens only — no spaces, underscores, or capitals) **and matches the folder name**.
3. **No `README.md`** inside the skill folder.
4. **`name` contains neither "claude" nor "anthropic".**
5. **`description` present and ≤ 1024 characters.**
6. **No XML angle brackets** (`<` or `>`) anywhere in the frontmatter.
7. **Body < 5000 words** (everything after the closing frontmatter `---`).
8. **`allowed-tools`, if present, is well-formed** (a comma-separated list or a YAML list of non-empty tool tokens).

Because it is deterministic and cheap it can also run standalone (pre-commit, CI) — but in the brigade it sits in the critic aggregation so a draft that violates a hard rule cannot pass the round on the strength of good LLM votes.

### 5.1 It's a controlled comparison, not a correctness check

The point of a skill is to make the model do something it *can't reliably do on its own*. So execution-eval is not "did the skill produce the right answer" — it's an **A/B ablation** on the same fixture:

- **Arm A (baseline):** base model, the fixture input, **no skill**.
- **Arm B (treatment):** base model + the skill, same input.
- Both graded against the fixture's known-answer. **Lift = score(B) − score(A).**

**Lift ≈ 0 means the skill is dead weight** — the base model already does the job — and the expo should **kill** the ticket rather than ship a skill that adds nothing. This turns the gate from a rubber stamp into a justification: a skill only advances if it demonstrably moves the needle, and the lift number *quantifies how much*.

Because model output is **non-deterministic**, a single run is noise. Each arm runs **N samples**; we report **pass-rate ± stddev** per arm and the **delta**, not a single pass/fail. Lift has to clear the noise band to count.

### 5.2 Reuse skill-creator — don't reinvent the harness

`skill-creator` already ships most of this machinery. We **orchestrate it**, we don't rebuild it:

| Need | skill-creator gives us | What the station adds |
|---|---|---|
| Two-arm runs | spawns with-skill **and** baseline subagents in the same turn | the arms are driven by the **ticket's** fixtures, not an ad-hoc `evals.json` |
| Grading | `agents/grader.md` → per-assertion pass/fail + evidence + execution metrics | assertions derive from the acceptance contract's oracle answers (incl. trap-answer-must-not-appear) |
| Lift number | `scripts/aggregate_benchmark.py` → pass-rate/time/tokens per config, **mean ± stddev + delta** | the delta *is* the lift; the expo consumes it as the advance/kill signal |
| Lift *attribution* | `agents/analyzer.md` benchmark mode: flags "passes with skill but fails without" (skill adds value), "fails with skill but passes without" (**regression**), high-variance/flaky evals | scoped to the targeted-improvement areas so we can confirm lift landed *where we aimed it* |
| Regression over time | `--previous-workspace` diffs this iteration vs the last | we persist the baseline to the **rail**, keyed to skill version (below) |

### 5.3 Where the fixtures live — already in the acceptance contract

The test author already emits the golden fixtures: in `variance-analysis` they're the **canonical oracle set** in `tests.md` — `{inputs, expected numbers, AND the trap answer the base model falls for}` (Oracle A: the AQ-purchased-vs-used DM trap; Oracle B: the FOH production-volume trap; etc.). That's exactly an execution-eval fixture, so the *same* contract artifact drives static review **and** the ablation. For corpus skills the fixture is a sample document + expected extraction; for generative skills, a rubric. **Fixture shape is set by the skill type** (§3) — computational → synthetic-known-answers, which is why `variance-analysis` is the clean first case.

### 5.4 Regression as a first-class, re-runnable gate

This is why execution-eval is its **own station, not a 6th critic axis**: a station can be **invoked standalone, decoupled from a build**, and a regression check is exactly that — re-run the fixture suite against a changed skill and compare to the stored baseline. We persist `{skill version, fixture, arm, score}` to the rail; on any change, **target areas must improve, everything else must not regress** (the analyzer's "fails with skill but passes without" flag is the regression tripwire). The fixture suite becomes the skill's **permanent benchmark** — the same machinery that justifies v1 guards v2…vN.

## 6. Production-wiring expectation (toy → system-of-record)

A skill ships with toy/golden examples to **prove the capability**. It must also document **how to wire into production**: the inputs the skill needs, sourced in production from the customer's *system of record*.

> Example (`variance-analysis`): the toy fixtures prove the procedure. In production you hook the inputs into the observability / revenue-reporting / cost-accounting system that holds the actual-vs-standard data for the assets you're monitoring.

The principle, stated in every skill:

> We demonstrate the skill working on toy examples. Realizing the full agentic benefit is **your** integration: wire the skill's inputs into your system of record / data plane.

This separates **capability** (the skill — the procedure) from **integration** (the plumbing to your systems) and sets honest expectations about the last mile.

## Open questions (for discussion)

- **Naming** — **RESOLVED: `steward / station / the pass (expo) / rail`**, whole = **brigade**, unit = **ticket**, exit set `advance · refire-to-author · reroute-to-spec · reroute-to-steward · kill` (5th exit added 2026-07-01 with the steward role). Canonical definitions in the **Naming (canonical)** block at the top.
- **Context vault** — is QMD/Obsidian the standing internal backend, with an enterprise backend (Cortex Search / etc.) only behind the interface for governed client contexts? Cost vs governance tradeoff.
- **Skill types** — is the 5-type taxonomy complete, or are there others (interactive/elicitation? multi-skill/composite?)?
- **Context-prep skill** — build it next as its own station, against the bundle interface?
- **Execution-eval** — ~~6th critic axis, or separate gate?~~ **RESOLVED: its own station** (§5). It's expensive (N-sample, two-arm), produces a *measurement* not a PASS/FAIL vote, and must be re-runnable standalone for regression — none of which fits inside the fast per-revision critic round. Built on `skill-creator`'s benchmark machinery. *Remaining sub-questions:* (a) N per arm — start at 3 (skill-creator's triggering default) and raise for high-variance fixtures; (b) the lift threshold below which the expo auto-kills — provisional ≥ +0.15 pass-rate over baseline AND outside the noise band, tune empirically once we have the first real variance-analysis lift number.
