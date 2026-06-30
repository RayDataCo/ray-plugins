---
station: station-test-author (station 2 of 4)
domain: variance-analysis
spec_consumed: spec.md (iteration 0)
target_artifact: Claude Code SKILL (variance-analysis/SKILL.md + references/)
critic_axes: [triggering-precision, domain-fidelity, procedure-not-knowledge-dump, progressive-disclosure-hygiene, no-slop]
confidence: high
---

# ACCEPTANCE CONTRACT — `variance-analysis` skill

This is the success-criteria checklist the code-author (station 3) must satisfy and the
critic (station 4) verifies against. It was written from the spec ONLY — the test-author
never saw the skill that will be built.

**Axis tags:** `[STRUCT]` deterministic file/grep/line-count check (runs before any critic
fires) · `[TRIGGER]` axis 1 triggering-precision · `[FIDELITY]` axis 2 domain-fidelity ·
`[PROCEDURE]` axis 3 procedure-not-knowledge-dump · `[DISCLOSURE]` axis 4
progressive-disclosure-hygiene · `[NOSLOP]` axis 5 no-slop.

Each line is a single testable assertion. PASS requires ALL `[STRUCT]` checks green AND
every critic axis PASS@high.

---

## 0. CANONICAL ORACLE SET (ground truth, computed independently of the build)

Per the Lloyd verify-then-build discipline, these reference answers were generated
separately from any code so the oracle is uncontaminated. The skill's worked examples
AND the procedure-when-applied must reproduce these numbers. Sign rule under test:
cost variance is **U if actual > standard, F if actual < standard** (operating-income effect).

### Oracle A — DM price + quantity, AQ purchased ≠ AQ used  (the trap)
Inputs: SP=$4.00/lb, std 2 lb/unit, actual output 5,000 units, AQ **purchased**=12,000 lb @ AP=$4.10, AQ **used**=10,200 lb.
- SQ allowed = 2 × 5,000 = **10,000 lb**
- DM price = (4.10−4.00) × **12,000 (purchased)** = **$1,200 U**
- DM quantity = (10,200 **used** − 10,000) × 4.00 = **$800 U**
- TRAP (wrong) answer if price computed on AQ used: $1,020 — must NOT appear as the price.
- Reconciliation note: price + quantity = $2,000 U does **not** form a single clean
  flexible-budget variance because purchased ≠ used; the skill must state the inventory-timing
  difference rather than force a tie-out.

### Oracle B — FOH budget(spending) vs production-volume
Inputs: budgeted FOH=$100,000; denominator capacity=20,000 std hrs ⇒ std FOH rate=$5.00/hr; std 2 hr/unit; actual output 9,000 units; actual FOH=$104,000.
- SH allowed = 18,000 hr; Applied FOH = 18,000 × 5.00 = **$90,000**
- FOH spending = 104,000 − 100,000 = **$4,000 U**
- FOH production-volume = 100,000(budgeted) − 90,000(applied) = **$10,000 U** → **CAPACITY ARTIFACT, non-controllable**
- Total under/over-applied = 104,000 − 90,000 = **$14,000 underapplied (U)**
- Reconcile: 4,000 + 10,000 = 14,000 ✓
- TRAP: computing production-volume as actual−applied ($14,000) or using applied in the
  spending line is wrong — must use budgeted vs applied.

### Oracle C — multi-input materials mix + yield
Inputs: Material X 60% @ $3.00, Material Y 40% @ $5.00 (std weighted price=$3.80); std total input for actual output=10,000 lb; actual total input=10,500 lb; actual X=7,000, actual Y=3,500.
- Std-mix at actual total: X=6,300, Y=4,200
- MIX = (7,000−6,300)×3 + (3,500−4,200)×5 = +2,100 − 3,500 = **$1,400 F**
- YIELD = (10,500−10,000) × 3.80 = **$1,900 U**
- Total usage = mix + yield = −1,400 + 1,900 = **$500 U**
- Cross-check (direct): X(7,000−6,000)×3 + Y(3,500−4,000)×5 = 3,000U − 2,500F = $500 U ✓

### Oracle D — management-by-exception ranking (materiality × controllability)
Variance set for the month (materiality threshold = ≥$1,000 absolute AND ≥2% of that element's standard cost base):

| variance | $ | F/U | owner | % of base | material? | exception action |
|---|---|---|---|---|---|---|
| DL efficiency | 9,500 | U | production | 11.9% | YES | **#1 investigate** |
| DM quantity | 8,000 | U | production | 4.0% | YES | **#2 investigate** + link to DM price |
| FOH production-volume | 10,000 | U | capacity artifact | n/a | NO (non-controllable) | **excluded from action list, labeled artifact** |
| DM price | 1,200 | F | purchasing | 0.6% | NO on its own | surfaced only via gaming-linkage to DM quantity |
| DL rate | 300 | F | labor market | 0.4% | NO | drop (noise) |
| VOH spending | 500 | U | production | 1.2% | NO | drop (noise) |

Correct interpretation behaviors under test:
- Largest absolute number ($10,000 FOH production-volume) is **NOT** ranked #1 and is
  **not** assigned to a controllable owner — the controllability filter demotes it. A
  ranking purely by absolute dollars is a FAIL.
- DM price F + DM quantity U is flagged as the **cheap-material-drives-waste** gaming
  signature (purchasing's cheap buy may have caused production's overusage) — the two are
  cross-linked even though DM price alone is immaterial.
- DL rate $300 F and VOH spending $500 U fall below the absolute threshold ⇒ dropped as noise.

---

## 1. STRUCTURAL CHECKS (deterministic; gate before critic)

- S1 `[STRUCT]` Directory `variance-analysis/` exists and contains `SKILL.md`.
- S2 `[STRUCT]` `SKILL.md` opens with YAML frontmatter containing `name: variance-analysis` and a non-empty `description:`.
- S3 `[STRUCT]` `references/` contains all five files: `formulas.md`, `budget-hierarchy.md`, `mix-yield.md`, `interpretation.md`, `worked-examples.md`.
- S4 `[STRUCT]` `SKILL.md` body is ≤ ~200 lines (spec 9G ceiling; hard cap 500 from skill-creator).
- S5 `[STRUCT]` `description` field contains positive trigger lexicon — at minimum the tokens: `price`, `quantity`/`usage`, `rate`, `efficiency`, `flexible budget` (or `flex`), `favorable`/`unfavorable`, `standard`.
- S6 `[STRUCT]` `description` field contains the negative carve-outs — at minimum tokens covering: statistical variance (`σ²`/`ANOVA`/`standard deviation`/`dataset`), mean-variance/portfolio, EVM/earned-value, and ETL/data-diff/reconciliation. (Spec 9A requires at least the statistical + mean-variance carve-outs; full four expected.)
- S7 `[STRUCT]` `SKILL.md` body contains a numbered procedure of ≥8 steps mirroring Section-3 Steps 1–8 (scope → input inventory → flex → compute → label F/U → reconcile → interpret → emit).
- S8 `[STRUCT]` `SKILL.md` states the single Step-5 sign rule in terms of **operating-income effect** (favorable = increases operating income), inline.
- S9 `[STRUCT]` `SKILL.md` lists the four reconciliation identities inline: DM price+quantity, DL rate+efficiency (and VOH), FOH spending+production-volume = total over/under-applied, sales-volume+flexible-budget = static-budget.
- S10 `[STRUCT]` `SKILL.md` contains the output-contract bullets: formula+inputs shown per line, F/U per line, reconciliation block present, FOH production-volume labeled artifact, DM price=purchased / DM quantity=used.
- S11 `[STRUCT]` `references/formulas.md` literally states DM price uses **AQ purchased** and DM quantity uses **AQ used** (both phrases present and distinct).
- S12 `[STRUCT]` `references/formulas.md` states FOH production-volume = budgeted FOH − applied FOH (applied = SH allowed × std FOH rate) AND FOH budget = actual FOH − budgeted FOH.
- S13 `[STRUCT]` `references/formulas.md` includes the three-column layout method (`AQ×AP | AQ×SP | SQ×SP`, price = col1−col2, quantity = col2−col3).
- S14 `[STRUCT]` `references/worked-examples.md` contains ≥1 example where AQ purchased ≠ AQ used AND ≥1 example computing FOH production-volume, each shown inputs→formula→value→F/U→reconciliation.
- S15 `[STRUCT]` `references/mix-yield.md` contains both the mix formula and the yield formula and is pointed to ONLY for >1 input or >1 product.
- S16 `[STRUCT]` `references/interpretation.md` contains the production-volume-is-non-controllable rule and ≥2 named gaming/linkage signatures.
- S17 `[STRUCT]` No worked multi-line numeric example or full per-element formula derivation appears inside `SKILL.md` (depth lives in references). Grep: SKILL.md must not contain a reconciled numeric example block.

---

## 2. SCENARIO ACCEPTANCE (procedure must reproduce the oracle)

The skill is a procedure; "applied" means an agent following SKILL.md (or the optional
`scripts/variance.py`) on the scenario inputs. The reference `worked-examples.md` must
ALSO contain at least Scenarios A and B with these exact numbers.

- T-A1 `[FIDELITY]` Scenario A yields DM price = **$1,200 U** (computed on 12,000 purchased), DM quantity = **$800 U** (10,200 used vs 10,000 allowed).
- T-A2 `[FIDELITY][NOSLOP]` Scenario A does NOT report price = $1,020 (the AQ-used trap); the inputs-used column shows 12,000 for price and 10,200 for quantity.
- T-A3 `[FIDELITY]` Scenario A explicitly notes price+quantity don't form one clean FB variance because purchased ≠ used (inventory-timing caveat), rather than fabricating a tie-out.
- T-B1 `[FIDELITY]` Scenario B yields FOH spending = **$4,000 U** and FOH production-volume = **$10,000 U**, with applied FOH = $90,000 shown.
- T-B2 `[FIDELITY]` Scenario B reconciles spending + production-volume = **$14,000** total underapplied.
- T-B3 `[FIDELITY][NOSLOP]` Scenario B labels the $10,000 production-volume variance a denominator/capacity artifact and assigns it NO controllable spending owner.
- T-C1 `[FIDELITY]` Scenario C yields MIX = **$1,400 F**, YIELD = **$1,900 U**, total usage = **$500 U**, with std weighted price $3.80 shown.
- T-C2 `[FIDELITY]` Scenario C mix + yield reconciles to the total materials usage variance ($500 U), matching the direct method.
- T-C3 `[DISCLOSURE]` Scenario C math lives in `references/mix-yield.md`, reached only via the SKILL.md mix/yield branch pointer (not inlined in SKILL.md, not loaded for single-input problems).
- T-D1 `[FIDELITY]` Scenario D ranks DL efficiency ($9,500 U) and DM quantity ($8,000 U) as the top controllable exceptions.
- T-D2 `[FIDELITY][NOSLOP]` Scenario D does NOT rank the $10,000 FOH production-volume #1 and does NOT put it on a controllable owner — controllability demotes it despite the largest absolute dollar.
- T-D3 `[FIDELITY][NOSLOP]` Scenario D flags DM price F + DM quantity U as the cheap-material-drives-waste linkage and cross-references the two owners (purchasing ↔ production).
- T-D4 `[FIDELITY]` Scenario D drops DL rate ($300) and VOH spending ($500) as below the materiality threshold (applies BOTH absolute-$ and %-of-standard, not just one).
- T-D5 `[FIDELITY]` Every Scenario-D variance is framed as a signal to investigate, not a verdict (no "this proves the manager failed" language).

---

## 3. TRIGGER ACCURACY (labeled set — axis 1 simulates routing on each)

The critic routes each prompt against the produced `description` and checks the verdict.
PASS requires all SHOULD-FIRE → FIRE and all SHOULD-NOT-FIRE → NO-FIRE, with the
discriminating feature being the reason.

### SHOULD FIRE
- TR-P1 `[TRIGGER]` "Compute the DM price and quantity variance — bought 10,000 lbs at $4.10, standard 9,500 lbs at $4.00 for units made." → FIRE (actual vs standard price+qty).
- TR-P2 `[TRIGGER]` "Break our budget-to-actual gap into a volume variance and a rate/efficiency variance." → FIRE (decomposition request).
- TR-P3 `[TRIGGER]` "Why is our direct-labor efficiency variance unfavorable this month?" → FIRE (interpretation, not just compute).
- TR-P4 `[TRIGGER]` "Build a flexible budget at actual output and give me the flexible-budget variance." → FIRE.
- TR-P5 `[TRIGGER]` "FOH was under-applied by $20k — split it into spending and production-volume." → FIRE.
- TR-P6 `[TRIGGER]` "Sales-mix and sales-quantity variance across our three products." → FIRE (multi-product mix/yield).
- TR-P7 `[TRIGGER]` "CMA practice problem: here are standards and actuals, compute all variances." → FIRE.
- TR-P8 `[TRIGGER]` "We have actual vs standard hours and rates for labor — assign the labor variances to responsibility centers." → FIRE.

### SHOULD NOT FIRE (deceptively similar — precision failures if they fire)
- TR-N1 `[TRIGGER]` "What's the variance and standard deviation of this column of numbers?" → NO-FIRE (statistical σ²). Discriminator: dataset/dispersion, no actual-vs-standard cost.
- TR-N2 `[TRIGGER]` "Run an ANOVA on these treatment groups." → NO-FIRE (statistics).
- TR-N3 `[TRIGGER]` "What's the mean-variance optimal portfolio / return volatility for these assets?" → NO-FIRE (portfolio mean-variance).
- TR-N4 `[TRIGGER]` "Compute the earned-value cost variance (CV) and schedule variance (SV) for the project." → NO-FIRE (EVM, not standard costing).
- TR-N5 `[TRIGGER]` "Why don't these two tables reconcile — there's row-count drift between datasets?" → NO-FIRE (ETL data-diff).
- TR-N6 `[TRIGGER]` "Explain the difference between accounting profit and economic profit." → NO-FIRE (managerial-econ definition; no actual-vs-standard data, no variance decomposition). *(expo-named negative)*
- TR-N7 `[TRIGGER]` "Analyze this budget" / "explain why marketing came in over budget" with one line-item delta and no standards. → NO-FIRE (generic FP&A commentary, no standard-costing structure). *(expo-named negative)*

### DISCRIMINATING BOUNDARY PAIR (the hard case — tests the Section-12 tension)
- TR-B1 `[TRIGGER]` "Analyze this budget against actuals — here are our **standard costs and the units we produced**." → FIRE. This is deceptively close to TR-N7 ("analyze this budget"); the presence of standards + actual output volume is the discriminator that flips it to FIRE. The skill must fire here but NOT on bare TR-N7. A skill that fires on both, or neither, FAILS this pair.

---

## 4. FAT-CONTENT CHECK (procedure-not-knowledge-dump, real workflow not generic advice)

- FC-1 `[PROCEDURE]` SKILL.md body reads as imperative steps (lines begin with verbs: Confirm/Build/Flex/Compute/Label/Reconcile/Rank/Emit), NOT as definitions ("The price variance is defined as…"). Heuristic: imperative-step lines outnumber definition lines in the body.
- FC-2 `[PROCEDURE]` Each of the ≥8 steps states an ACTION the agent performs plus the pitfall it kills (e.g. Step 3 flex → kills static-vs-flex; Step 4 → kills AQ purchased/used swap & budgeted/applied FOH; Step 5 → kills sign flips; Step 7 → production-volume-not-controllable).
- FC-3 `[PROCEDURE][DISCLOSURE]` SKILL.md routes depth out via ≥5 lazy "read references/X.md when…" pointers (one per reference file), each with a concrete trigger condition (e.g. "only when >1 input or >1 product").
- FC-4 `[PROCEDURE]` The four named pitfalls each have an explicit in-procedure guard (spec 9H): AQ purchased-vs-used, budgeted-vs-applied FOH, sign flips, production-volume treated as controllable. Each guard is checkable as a distinct sentence.
- FC-5 `[NOSLOP]` Body contains domain-specific load-bearing specifics, not plausible-generic prose: the operating-income sign test, the AQ purchased/used split, the three-column computation layout, named gaming signatures, the four reconciliation identities. A reviewer cannot replace these with generic "analyze the budget carefully" advice without losing meaning.
- FC-6 `[PROCEDURE]` Output is an auditable deliverable spec (scope line → variance table with formula+inputs columns → reconciliation proof → ranked investigation list → interpretation narrative → caveats), not a free-form essay.
- FC-7 `[NOSLOP]` No filler sections that restate the syllabus (e.g. a "History of standard costing" or "Why variance analysis matters" block). Every section is operative.

---

## 5. COVERAGE GAPS (advisory, non-blocking)

- CG-1 No per-domain `configs/variance-analysis.yaml` exists; structural checks S1–S17 are
  declared here from spec Sections 6 & 9. If the workflow expects a config-driven
  `structural_checks` list, generate it from S1–S17 before the deterministic gate runs.
- CG-2 Triggering cannot be executed by a live router in this station; TR-* cases are verified
  by critic axis-1 simulation against the `description` plus the S5/S6 token greps. This is
  inherently fuzzier than a deterministic check — treat a TR-* miss as ITERATE, not hard-fail,
  unless an S5/S6 token check also fails.
- CG-3 The optional `scripts/variance.py` is not mandated by the spec. If present, T-A/T-B/T-C
  oracle numbers can be checked deterministically by executing it; if absent, those become
  reference-comparison checks against `worked-examples.md`. Either path satisfies the contract.
- CG-4 Materiality threshold in Oracle D ($1,000 abs AND 2%) is the test-author's concrete
  instance; the skill need not hardcode these exact numbers but MUST apply both an absolute
  and a percentage gate and reach the same ranked/dropped partition.
