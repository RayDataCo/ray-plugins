# Critic report — variance-analysis

Verdict aggregate from the pipeline run that produced this skill.

- **Result:** PASS
- **Rounds:** 1 (cleared on the first author draft; no revision needed)
- **Axes:** 5/5 PASS
- **Critic design:** static adversarial (each axis judged by an isolated sub-agent defaulting to FAIL unless clearly met). Execution-eval is a planned addition — see the plugin README.

| Axis | Verdict | Confidence |
|---|---|---|
| triggering-precision | PASS | 0.78 |
| domain-fidelity | PASS | 0.95 |
| procedure-not-knowledge-dump | PASS | 0.92 |
| progressive-disclosure-hygiene | PASS | 0.93 |
| no-slop | PASS | 0.90 |

## Notes by axis

### triggering-precision (0.78)
Description is a well-tuned routing surface: leads with "standard-costing cost and revenue variances," enumerates every named sub-variance, and uses a conjunctive positive gate (actual-vs-standard data AND a variance verb) rather than a bare "variance" keyword. All should-fire cases map to named variance types; all hard negatives (statistical σ²/ANOVA, portfolio mean-variance, EVM CV/SV, ETL/data-diff) are explicitly carved out.

**One actionable weakness (ITERATE-grade, the reason this is 0.78 not higher):** the generic-FP&A near-miss ("explain why marketing came in over budget," single line-item delta, no standards) is carved out only in the `SKILL.md` body, **not** in the description frontmatter — the actual routing surface. The interpret clause in the description is a near-lexical match and creates mild overtrigger risk on bare budget commentary. Fix: add the generic-FP&A-without-standards carve-out to the description's do-NOT-use list, or scope the interpret clause to "interpret the *computed* variances." Preserved here rather than silently patched — this is exactly the feedback the convergence loop would route to the author on a revision round.

### domain-fidelity (0.95)
Every load-bearing formula matches standard CMA managerial-accounting truth, including all five verification points: DM price uses AQ **purchased**; DM quantity uses AQ **used**; FOH production-volume = budgeted − applied (applied = SH allowed × std FOH rate); flexible budget flexed to **actual** output; sales-volume = (actual − budgeted units) × budgeted CM/unit. DL, VOH, and mix/yield formulas all canonical. Worked-example arithmetic independently recomputed and ties out (incl. the AQ-purchased≠used trap correctly handled as an inventory-timing difference rather than a forced tie-out, and FOH production-volume correctly labeled a non-controllable capacity artifact). No formula errors, sign flips, AQ swaps, or budgeted/applied confusion.

### procedure-not-knowledge-dump (0.92)
Clean 8-step imperative procedure; every step opens with an action verb (Confirm/Build/Flex/Compute/Label/Reconcile/Interpret/Emit) and names the pitfall it kills. Depth genuinely deferred to reference files via lazy pointers; no inline formula card. The only inline "knowledge" (operating-income sign rule, reconciliation identities, output contract) is load-bearing decision logic applied every run — correct procedure-first design.

### progressive-disclosure-hygiene (0.93)
`SKILL.md` lean at 59 lines / 8.5KB (target <200). Layout matches the spec plan: `SKILL.md` + `references/{formulas, budget-hierarchy, mix-yield, interpretation, worked-examples}.md`, all five substantial, none a stub. Strong lazy pointers (step-level + a dedicated load-on-demand block with one conditioned pointer per file). Depth externalized (no worked numeric examples or full derivations inlined). Minor non-blocking nit: a couple of `SKILL.md` lines are very dense; bulleting would improve scannability.

### no-slop (0.90)
Specificity is dense and load-bearing throughout; no plausible-generic filler. Concrete, irreplaceable tells include: the single operating-income sign rule (not case-by-case sign guessing); the AQ-purchased-vs-used split carried as two distinct numbers (the #1 DM pitfall, reinforced across spec/output-contract/reference/worked-example); the three-column computation scaffold; named gaming/linkage signatures with mechanism; explicit reconciliation identities; and the FOH production-volume capacity-artifact treatment.
