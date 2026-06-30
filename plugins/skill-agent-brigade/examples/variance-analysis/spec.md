---
iteration: 0
domain: variance-analysis
department: Finance
cert_anchor: CMA Part 1 (managerial accounting) / CFA
target_artifact: Claude Code SKILL (SKILL.md + progressive-disclosure reference files)
parent_workflow: skill-build-brigade
station: pipeline-spec-author (station 1 of 4)
confidence: high
---

# BUILD SPEC — `variance-analysis` Finance skill

## 0. What this station is specifying

The downstream code-author (station 3) must produce a **Claude Code skill**, not a memo or a study guide. That means a `variance-analysis/` directory with a `SKILL.md` (YAML frontmatter `{name, description}` + lean markdown body) plus progressive-disclosure reference files. The skill must encode the CMA variance-analysis competency **as an executable procedure the agent runs** — gather inputs → flex the budget → route to the right formula → compute with a fixed sign convention → reconcile → interpret by exception → emit an auditable table. It is NOT a restatement of the syllabus.

This spec is the contract. The test-author (station 2) writes tests against Section 9 (Success Criteria). The critic (station 4) scores against the five axes in Section 10.

---

## 1. The competency, restated as the ONE job the skill does

Given a standard-costing / budget-to-actual situation, the skill turns raw operating data into a **reconciled, signed, responsibility-assigned variance breakdown plus a management-by-exception investigation list**. The differentiator vs a naive answer: (a) it flexes to actual output before computing efficiency/price variances, (b) it never flips a sign, (c) its sub-variances provably sum to the parent, and (d) it reads variances as *signals to investigate*, not verdicts — tied to the right responsibility center, with gaming/linkage patterns surfaced.

---

## 2. Skill identity (frontmatter the code-author must produce)

- **name:** `variance-analysis`
- **description:** trigger-tuned, dual-purpose (what it does + when to use + when NOT). Must combat undertriggering on in-domain phrasings AND carve out the statistical/finance near-misses (Section 8). Draft direction (code-author may refine wording, must preserve the trigger surface):

  > Compute and interpret standard-costing cost and revenue variances — direct materials price/quantity, direct labor rate/efficiency, variable-overhead spending/efficiency, fixed-overhead spending/production-volume, sales-volume and flexible-budget variances, and multi-input/multi-product mix & yield. Use this whenever the user gives actual vs standard (or budgeted) prices, rates, quantities, hours, or output and wants the variances computed, decomposed, reconciled, labeled favorable/unfavorable, assigned to a responsibility center, or interpreted (why is X unfavorable, what should we investigate) — including CMA/CFA exam-style problems and manufacturing/ops cost reviews. Do NOT use for statistical variance (σ², ANOVA, "variance of this dataset"), portfolio mean-variance / return volatility, project earned-value schedule/cost variance (EVM), or generic ETL/data-diff reconciliation between two tables.

---

## 3. THE PROCEDURE (the heart — what the SKILL.md body instructs the agent to execute)

The SKILL.md body is a numbered workflow, not prose. Each step below is mandatory; the parenthetical names the pitfall the step exists to kill.

**Step 1 — Confirm scope and pick the variance set.**
Decide which cost elements / levels are in play from the ask + the data present: direct materials (DM), direct labor (DL), variable overhead (VOH), fixed overhead (FOH), sales-volume/flexible-budget level, mix & yield. If the request is statistical variance or mean-variance volatility, stop and redirect (this is the wrong skill). State which variances you will compute before computing.

**Step 2 — Build the input inventory and flag what's missing.**
For each element collect: standard price/rate (SP/SR), standard quantity or hours per unit, actual price/rate (AP/AR), actual quantity/hours, **actual output units**, budgeted output units, budgeted contribution margin per unit (for sales-volume), actual and budgeted FOH, and the denominator/normal capacity + standard FOH rate (for FOH). **For direct materials, capture AQ PURCHASED and AQ USED as two distinct numbers** — they differ whenever purchases ≠ usage, and the two materials variances use different ones (Step 4). Name any missing input explicitly rather than assuming it.

**Step 3 — Flex the budget: compute standard quantity allowed.**
`SQ allowed = standard quantity per unit × ACTUAL output`. Likewise `SH allowed = standard hours per unit × actual output`. Everything downstream compares against this flexed figure, never the static/master budget. (Kills: comparing efficiency/price against the static budget instead of the flexible budget.)

**Step 4 — Compute each variance with the canonical formula.** Pull the exact formula card from `references/formulas.md`; do not reconstruct formulas from memory. Core set:
- **DM price** = (AP − SP) × **AQ purchased** — owner: purchasing.
- **DM quantity/usage** = (**AQ used** − SQ allowed) × SP — owner: production.
- **DL rate** = (AR − SR) × AH.
- **DL efficiency** = (AH − SH allowed) × SR.
- **VOH spending** = actual VOH − (AH × standard VOH rate).
- **VOH efficiency** = (AH − SH allowed) × standard VOH rate.
- **FOH budget/spending** = actual FOH − budgeted FOH.
- **FOH production-volume** = budgeted FOH − applied FOH, where applied FOH = SH allowed × standard FOH rate.
- **Sales-volume** = (actual units − budgeted units) × budgeted contribution margin per unit.
- **Flexible-budget** = actual result − flexible budget at actual volume.
- **Mix & yield / sales-mix & sales-quantity:** only when multiple inputs or products — load `references/mix-yield.md`.

(Kills: AQ-purchased-vs-used swap; budgeted-vs-applied FOH confusion.)

**Step 5 — Label F/U with ONE unambiguous rule (no sign guessing).**
Compute the dollar amount, then label by effect on operating income: **a variance is Favorable (F) if it increases operating income, Unfavorable (U) if it decreases it.** Operationally — for cost variances, actual > standard ⇒ U, actual < standard ⇒ F; for revenue/contribution variances, actual > budget ⇒ F. Apply this single test to every line so signs never flip element-to-element. (Kills: sign errors.)

**Step 6 — Reconcile (the integrity gate — do not skip).**
The sub-variances must sum to their parent; show the arithmetic:
- DM price + DM quantity = total DM flexible-budget variance (when AQ purchased = AQ used; if not, note the inventory-timing difference explicitly).
- DL rate + DL efficiency = total DL variance; same pattern for VOH.
- FOH spending + FOH production-volume = total over/under-applied FOH.
- Sales-volume variance + flexible-budget variance = static-budget variance.
If a reconciliation does not tie out, a sign or input is wrong — go back to Step 4/5 before reporting. (This self-check is what makes the output trustworthy; it is the procedural backbone, not optional polish.)

**Step 7 — Interpret by exception (signals, not verdicts).**
For each material variance: (a) **materiality** — flag only those large in absolute dollars AND as a % of the standard; small variances are noise. (b) **Controllability / responsibility center** — assign each variance to who owns it; explicitly mark the **FOH production-volume variance as a denominator-capacity artifact, NOT a controllable spending issue.** (c) **Cross-variance linkage / gaming** — look for tradeoff signatures: favorable DM price + unfavorable DM usage ⇒ possibly cheap low-quality material driving waste/rework; favorable DL rate + unfavorable DL efficiency ⇒ lower-skill labor. (d) **Standard currency** — note whether standards look current/attainable vs ideal/stale, since a stale standard manufactures variances. Pull depth from `references/interpretation.md`.

**Step 8 — Emit the auditable deliverable** (Section 6 output contract). Always show formula + inputs per line, not just the answer.

---

## 4. Inputs (what the agent must elicit or read)

- **The ask:** which variances, which decomposition level, whether interpretation is wanted.
- **Per element:** SP/SR, standard qty or hours per unit, AP/AR, actual qty/hours, actual output units.
- **Materials-specific:** AQ purchased AND AQ used (two numbers).
- **Sales/volume level:** budgeted units, actual units, budgeted contribution margin per unit; for multi-product, per-product budgeted CM and budgeted vs actual sales mix.
- **FOH:** actual FOH, budgeted (lump-sum) FOH, denominator/normal capacity, standard FOH rate.
- **Multi-input materials:** standard mix %, actual mix %, total actual input quantity, standard weighted price.

If inputs arrive as a table/CSV/narrative, parse them into this inventory first (Step 2). Missing inputs are named, not silently assumed.

## 5. Outputs

A structured deliverable containing, in order:
1. **Scope line** — which variances were computed and at what level.
2. **Variance table** — columns: `element | variance name | formula | inputs used | computed $ | F/U | responsibility center`.
3. **Reconciliation proof** — sub-variances summing to parent(s), shown as arithmetic.
4. **Investigation list** — material variances ranked by (materiality × controllability), each with the likely driver and the owner to ask.
5. **Interpretation narrative** — gaming/linkage flags, standard-currency caveat, and explicit "this is a signal to investigate, not a verdict" framing where relevant.
6. **Caveats** — any assumed/missing inputs.

## 6. Output contract (non-negotiables the test-author can assert on)

- Every variance line shows its formula and the actual numbers plugged in (auditability).
- Every variance line carries an F/U label produced by the Step-5 operating-income rule.
- A reconciliation block is present and ties out (or the timing/rounding reason it doesn't is stated).
- FOH production-volume variance, whenever computed, is labeled a capacity/denominator artifact and is NOT placed on a controllable spending owner.
- DM price uses AQ purchased; DM quantity uses AQ used — verifiable from the "inputs used" column.

---

## 7. Trigger — WHEN TO USE (positive surface; description must cover these)

- "Compute the direct materials price and quantity variance — we bought 10,000 lbs at $4.10, standard is 9,500 lbs at $4.00 for the units we made."
- "Break our budget-to-actual gap into a volume variance and a rate/efficiency variance." / "Decompose the static-budget variance."
- "Why is our direct-labor efficiency variance unfavorable this month?" (interpretation, not just compute)
- "Build a flexible budget at actual output and give me the flexible-budget variance."
- "FOH was under-applied by $20k — split it into spending and production-volume."
- "Sales-mix and sales-quantity variance across our three products."
- A CMA/CFA practice problem stating standards and actuals and asking for variances.
- A manufacturing/ops cost review that needs variances tied to responsibility centers.

## 8. Trigger — WHEN NOT TO USE (near-misses the description MUST exclude)

These share the word "variance" or "budget" but need a different tool; firing here is a precision failure (critic axis 1):
- **Statistical variance / σ² / standard deviation / ANOVA** — "what's the variance of this column of numbers." (Stats, not management accounting.)
- **Portfolio mean-variance / return volatility / variance-covariance** — investing risk, not cost accounting.
- **Project earned-value (EVM) cost variance / schedule variance (CV/SV)** — project management; not standard-cost variance unless explicitly framed as standard costing.
- **Generic FP&A budget commentary with NO standards and NO price/efficiency decomposition** — "explain why marketing came in over budget" with a single line-item delta and no flexible-budget structure adds nothing here.
- **ETL / data-diff reconciliation** — "why don't these two tables match" / row-count drift between datasets.

The tension between "be pushy to avoid undertriggering" (skill-creator guidance) and "don't fire on the near-misses" (critic axis 1) is resolved by being assertive on the standard-costing phrasings of Section 7 while keeping the hard negative carve-outs above explicit in the description.

---

## 9. Success Criteria (the test-author writes tests against THESE)

A. **Frontmatter present and valid** — `name: variance-analysis`, a `description` containing both the positive trigger surface (Section 7) and at least the statistical-variance + mean-variance negative carve-outs (Section 8).

B. **Procedure-first body** — SKILL.md body is the numbered workflow of Section 3 (steps the agent executes), not a syllabus/definitions dump. Heuristic the test can check: the body reads as imperative steps and routes to reference files, rather than re-deriving every formula inline.

C. **Domain-fidelity (formulas correct)** — the formula card matches Section 3/4 exactly, including:
   - DM price uses **AQ purchased**, DM quantity uses **AQ used**.
   - FOH production-volume = budgeted FOH − applied FOH (applied = SH allowed × std FOH rate); FOH budget = actual − budgeted.
   - SQ allowed = std qty/unit × **actual** output (flex step present).
   - Sales-volume = (actual − budgeted units) × budgeted CM/unit.

D. **Sign discipline encoded** — a single F/U labeling rule (operating-income effect) is stated and applied uniformly.

E. **Reconciliation gate present** — the body instructs sub-variances to sum to the parent and to recheck on mismatch, with the four reconciliation identities of Step 6 available.

F. **Interpretation = signal-not-verdict** — body includes materiality + controllability + responsibility-center assignment + gaming/linkage patterns + standard-currency check, and explicitly flags production-volume variance as non-controllable.

G. **Progressive-disclosure hygiene** — SKILL.md stays lean (target < ~200 lines / well under skill-creator's 500-line ceiling); depth lives in reference files with lazy-load pointers from the body (Section 11). Mix & yield and worked examples are NOT inlined into SKILL.md.

H. **Pitfall guards visible** — the four named pitfalls (AQ purchased vs used, budgeted vs applied FOH, sign flips, treating production-volume as controllable) each have an explicit guard in the procedure.

I. **Worked example with a trap** — at least one fully reconciled numeric example exists in a reference file, including a case where AQ purchased ≠ AQ used and a case computing FOH production-volume, so the agent can pattern-match.

## 10. Critic axes → where each is satisfied (for station 4)

1. **Triggering-precision** → Sections 2, 7, 8 (positive surface + hard negative carve-outs).
2. **Domain-fidelity** → Sections 3, 4, 9C/9D/9E; formulas match CMA exactly, flex step present, sign rule unambiguous.
3. **Procedure-not-knowledge-dump** → Section 3 is imperative workflow steps; Section 9B; depth pushed out of SKILL.md.
4. **Progressive-disclosure-hygiene** → Section 11 file plan, lazy pointers, size targets (9G).
5. **No-slop** → concrete formulas, the AQ purchased/used distinction, the operating-income sign rule, named gaming signatures, reconciliation identities, a trap worked example — specificity over plausible-generic prose.

---

## 11. Progressive-disclosure file plan (which depth goes where)

```
variance-analysis/
├── SKILL.md                      (required; lean)
└── references/
    ├── formulas.md
    ├── budget-hierarchy.md
    ├── mix-yield.md
    ├── interpretation.md
    └── worked-examples.md
```

- **SKILL.md** (target < ~200 lines): frontmatter; the ONE-job framing (Section 1); the 8-step procedure (Section 3) in imperative form; the Step-5 sign rule and Step-6 reconciliation identities inline (small, load-bearing, every run needs them); the output contract (Section 6); and a "When NOT to use" reminder echoing the negative carve-outs. Each reference file is named with a one-line "read this when…" pointer. Do NOT inline full formula derivations, mix/yield math, or examples.

- **references/formulas.md** (the canonical formula card): exact formula per element (DM, DL, VOH, FOH) with precise variable definitions; the AQ-purchased-vs-used callout; the three-column presentation method (`AQ×AP | AQ×SP | SQ×SP`, price = col1−col2, quantity = col2−col3) so the agent can lay out computations consistently. Include a short table of contents (it will exceed ~50 lines). Pointer from SKILL.md Step 4.

- **references/budget-hierarchy.md**: static (master) vs flexible vs actual; the Level 0→1→2→3 decomposition (static-budget variance → sales-volume + flexible-budget → price/efficiency); flexing mechanics and SQ/SH-allowed; sales-volume variance with budgeted CM. Pointer from SKILL.md Steps 3 and 4 (sales-volume / flexible-budget level).

- **references/mix-yield.md** (advanced, lazy-loaded only when multiple inputs/products): materials mix variance = (actual mix% − std mix%) × total actual qty × std price; yield variance = (actual total input − std input for actual output) × std weighted price; sales-mix and sales-quantity decomposition of the sales-volume variance. Pointer from SKILL.md Step 4's mix/yield branch, explicitly "only when >1 input or >1 product."

- **references/interpretation.md**: management-by-exception (materiality thresholds, absolute + %); controllability and responsibility-center mapping; the production-volume-variance-is-not-controllable rule with the why; gaming/linkage signatures (cheap-material, low-skill-labor, and others); ideal vs currently-attainable standards and why stale standards manufacture variances. Pointer from SKILL.md Step 7.

- **references/worked-examples.md**: 2–3 fully worked, fully reconciled numeric examples covering DM+DL+VOH+FOH and the sales-volume/flexible-budget split, including (i) a trap where AQ purchased ≠ AQ used and (ii) an FOH case with a production-volume variance correctly labeled non-controllable. Each example shows inputs → formula → value → F/U → reconciliation. Pointer from SKILL.md as "pattern-match against these before answering a multi-element problem."

- **OPTIONAL — `scripts/variance.py`** (code-author's discretion, not mandated): a deterministic calculator that takes the input inventory and returns each variance value + F/U + a reconciliation check. Rationale: the arithmetic and sign-labeling are deterministic and repetitive (skill-creator's "scripts for deterministic/repetitive tasks"), so a script removes the two most common failure modes (arithmetic slips, sign flips) and auto-verifies the reconciliation gate. Spec'd as optional because the *conceptual* core — scope routing, controllability, interpretation — is the irreducible skill and cannot be scripted; the script is an accelerator, not the artifact. If included, SKILL.md must still teach the procedure (the agent should understand, not just call a black box).

---

## 12. Tensions (flagged for the test-author per station method)

- **Pushy description vs triggering-precision.** Skill-creator says lean pushy to fight undertriggering; critic axis 1 penalizes false fires. Resolution baked into Section 2/8: assertive on standard-costing phrasings, explicit hard carve-outs for statistical variance, mean-variance, EVM, and data-diff. Test-author should test BOTH a should-trigger near-miss (e.g., budget-to-actual *with* standards) and a should-NOT-trigger near-miss (e.g., "variance of this dataset").
- **Completeness vs leanness.** Encoding all four elements + mix/yield + interpretation is a lot of surface, which fights "procedure-not-knowledge-dump" and disclosure hygiene. Resolution: SKILL.md carries only the routing workflow + sign rule + reconciliation identities + output contract; every formula/example/advanced-decomposition body goes to a reference file loaded on demand. The test for 9G should confirm SKILL.md did not absorb the depth.
- **Script vs teach.** A calculator script maximizes arithmetic fidelity but can hollow out the competency into a black-box call. Resolution: script optional and explicitly subordinate to the taught procedure; SKILL.md must still encode the steps so the agent reasons, not just invokes.
