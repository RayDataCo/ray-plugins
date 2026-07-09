---
name: execution-eval-station
description: >-
  Measure whether an authored skill actually beats the base model — the lift
  station of the brigade. Use after the static critics pass,
  when you need to prove a skill earns its place: run the skill against its
  acceptance-contract fixtures in a two-arm ablation (base model alone vs base
  model + skill), grade both against the known answers, and report the lift
  (with-skill pass-rate minus baseline) with variance. Also use standalone to
  regression-check an existing skill after a change. Built on skill-creator's
  benchmark machinery. NOT for judging structure/voice/fidelity (that's the
  static critic station) and NOT for authoring skill content (that's the author station).
---

# Execution-Eval Station

The station that answers the one question the static critics can't: **does this skill add something the base model can't already do?** The static critics read the artifact and judge whether it's *well-built*. This station *runs* the skill and measures whether it's *worth shipping*.

It is structurally different from the critic station, which is why it's its own station and not a sixth critic axis:

- It **executes** the skill (multi-step, expensive), where the critics only read it.
- It needs **N samples per arm** because model output is non-deterministic — a single run is noise.
- It produces a **measurement** (a lift number with a confidence band), not a PASS/FAIL vote.
- It must be **re-runnable standalone**, decoupled from a build, so it can serve as a regression gate over a skill's lifetime. A gate buried inside the per-revision critic round can't be invoked later; a station can.

## The core idea — lift, not correctness

A skill exists to make the model do something it can't reliably do alone. So the measurement is an **A/B ablation** on the same fixture, not a bare correctness check:

- **Arm A (baseline):** base model + fixture input, **no skill**.
- **Arm B (treatment):** base model + the skill, same input.
- Both graded against the fixture's known answer. **Lift = pass-rate(B) − pass-rate(A).**

**Lift ≈ 0 means the skill is dead weight** — the base model already does the job — and the expo should **kill the ticket** rather than ship a skill that adds nothing. A positive lift that clears the noise band is the skill justifying its existence, *and the number says how much*.

## Inputs

- **`skill_path`** — the authored skill to evaluate (`SKILL.md` + references).
- **`fixtures`** — the golden `{input, expected_answer, trap_answers}` set. These already exist in the acceptance contract (`tests.md`): the **oracle set**. Each oracle is a fixture: the inputs are the prompt, the expected numbers are the grading target, and any "trap answer the base model falls for" becomes a *must-not-appear* assertion. Do not invent fixtures — extract them from the contract.
- **`n_samples`** — runs per arm (default **3**, skill-creator's triggering default). Raise for fixtures that show high variance.
- **`baseline`** — for a new skill: **no skill**. For a regression run on an existing skill: the **previous version** (snapshot it first).
- **`run_dir`** — scratch dir for transcripts, outputs, and the benchmark.

## Procedure (orchestrate skill-creator — don't reinvent the harness)

`skill-creator` ships the ablation + grading + variance-aware benchmark. This station drives it with contract fixtures and turns the result into an expo decision.

1. **Extract fixtures from the acceptance contract.** Read `tests.md`; turn each oracle into `{prompt, expected assertions, trap-absent assertions}`. The prompt feeds the skill the oracle's raw inputs and asks for the worked result; the expected numbers and trap-absence become the gradeable assertions.

2. **Spawn both arms in the same turn, N samples each.** Per skill-creator step 1: for each fixture, launch with-skill and baseline subagents together (don't run all with-skill first). With-skill gets `skill_path`; baseline gets no skill (or the prior-version snapshot). Save outputs under `run_dir/iteration-<N>/<fixture>/{with_skill,without_skill}/`.

3. **Grade every run.** Spawn a grader per run following `skill-creator/agents/grader.md`. Assertions = the oracle's expected numbers AND the trap-absent checks (e.g. "the DM price variance is **not** computed on AQ used"). Write `grading.json` with the exact `{text, passed, evidence}` fields the aggregator expects. **Constrain the run's output to the exact gradeable fields** — a fixed output schema (enum/named fields graded by direct lookup), not free-form prose matched by name. Models name free-form fields wildly differently (`test_1_severity` vs `severity_row_level_absolute`), so name-matching grades the wrong slot and manufactures fake lift; deterministic grading needs a fixed answer shape. (Learned the hard way — see the generate-tests report.)

4. **Aggregate into the lift number.** Run skill-creator's `scripts/aggregate_benchmark.py` over the iteration dir. It yields pass-rate / time / tokens per arm as **mean ± stddev**, and the **delta** between arms. The delta pass-rate *is the lift*.

5. **Attribute the lift.** Run the analyzer (benchmark mode, `skill-creator/agents/analyzer.md`) to surface what the aggregate hides: which fixtures the skill carries ("passes with skill, fails without" = value added), any **regression** ("fails with skill, passes without"), non-discriminating fixtures (pass in both arms — they don't prove skill value), and high-variance fixtures that need more samples. Scope the read to the targeted-improvement areas so you can confirm the lift landed *where it was aimed*.

6. **Return a measurement + a recommended action — decided PER FIXTURE, not on the aggregate mean.** This is load-bearing: a skill that fixes one important failure mode gets washed out to a false "kill" if you average it against easy fixtures the base model already aces (observed directly on `variance-analysis` — see DESIGN.md §5 / the report). Classify each fixture, then decide:
   - **per-fixture classes:** `regression` (lift < −band, skill made it worse) · `non-discriminating` (base already ≥ ~95%, no headroom to show lift) · `win` (base had headroom AND lift ≥ +0.15 and clears the fixture's own noise band) · `flat` (had headroom, skill didn't lift it).
   - **advance** — at least one `win` and no `regression`. The skill earns its place on a fixture that actually discriminates; record which.
   - **refire-to-author** — any `regression`. Route the analyzer's specifics back to the author.
   - **inconclusive (fixtures don't discriminate)** — every fixture is `non-discriminating`. NOT a kill — the base model is at the ceiling everywhere, so nothing *could* show lift. Action: harden the fixtures (messier inputs, a weaker-model arm) before judging the skill.
   - **kill** — there was headroom on at least one fixture (`flat`) and the skill lifted nothing. Genuine dead weight; surface the per-fixture table for the human to confirm.

## Regression mode (standalone, the reason this is a station)

Re-run the same fixture suite against a changed skill and compare to the stored baseline. Persist `{skill_version, fixture, arm, pass_rate}` to the rail (the brigade's ticket store), keyed to skill version. On a change:

- **Target areas must improve** (or hold, if already at ceiling).
- **Everything else must not regress** — the analyzer's "fails with skill but passes without" flag, applied against the *prior version* as baseline, is the regression tripwire.

Use skill-creator's `--previous-workspace` to diff this iteration against the last. The fixture suite becomes the skill's permanent benchmark: the same machinery that justifies v1 guards v2…vN.

## Owns vs delegates

- **Owns:** sourcing fixtures from the contract, choosing the baseline + N, turning grades into a lift number, the advance/kill/refire recommendation, and persisting the regression baseline to the rail.
- **Delegates:** the two-arm runs, grading, benchmark aggregation, and lift attribution to skill-creator's existing machinery. Don't rebuild what it already does.

## Honest defaults

- One run is noise — never report lift off a single sample per arm.
- A skill that doesn't beat baseline is not a pass — surface lift ≈ 0 as a kill candidate, don't bury it.
- Report the noise band, not just the point estimate; a +0.10 lift with ±0.20 stddev has not been demonstrated.
- Non-discriminating fixtures (pass in both arms) prove nothing about the skill — flag them so the fixture set can be strengthened, exactly as the grader's eval-critique step intends.

## Returns

```
lift: <+delta pass-rate>  band: <±combined stddev>  action: advance|kill|refire-to-author|inconclusive
per-fixture: <fixture → with_skill% vs baseline% (Δ)>
benchmark: <run_dir>/iteration-<N>/benchmark.json
```

## Related

- skill-creator (`agents/grader.md`, `agents/analyzer.md`, `scripts/aggregate_benchmark.py`) — the benchmark machinery this station orchestrates.
- `../expo/SKILL.md` — the pass whose expo consumes this station's lift number for the advance/refire-to-author/reroute-to-spec/reroute-to-steward/kill decision.
- `../../DESIGN.md` §5 — the design rationale (controlled comparison, own-station decision, regression).
