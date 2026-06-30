/* ============================================================================
 * REFERENCE IMPLEMENTATION — the exact workflow run that produced the
 * variance-analysis worked example (examples/variance-analysis/ + the installed
 * skill at plugins/discipline-skills/skills/variance-analysis/).
 *
 * Runs the 4-seat skill pipeline (spec -> tests -> author -> critic) with a
 * convergence loop, via the Claude Code Workflow tool. Result on this run:
 * passed=true, rounds=1, 5/5 critic axes PASS.
 *
 * NOTE (portability): as-run, each seat agent reads its canonical seat skill
 * from the local RDCO harness (~/.claude/skills/pipeline-*) and writes to a
 * per-run scratch dir. The seat ROLES + contracts are documented in README.md.
 * To adapt for another environment, point the seat-read paths at your own seat
 * skills and set your own run dir. The cert-competency seed + per-domain config
 * are inlined below as the depth source for this domain.
 * ============================================================================ */

export const meta = {
  name: 'skill-pipeline-pilot-variance-analysis',
  description: 'Pilot the 4-seat skill pipeline (spec -> tests -> author -> critic + convergence loop) on Finance/variance-analysis; output a Claude skill for ray-plugins',
  phases: [
    { title: 'Spec' },
    { title: 'Tests' },
    { title: 'Author' },
    { title: 'Critic' },
  ],
}

const SCRATCH = '/private/tmp/claude-501/-Users-ray/9dc2c717-3170-4bb7-9002-c8c126306f3f/scratchpad/variance-analysis-pilot'

const CERT_SEED = `CERT-COMPETENCY SEED -- Variance Analysis (CMA Part 1 / managerial accounting; this is the depth source the skill must ENCODE AS A PROCEDURE, not restate as theory):
- Standard costing: standard cost = standard price (SP) x standard quantity (SQ) per cost element (direct materials DM, direct labor DL, variable overhead VOH, fixed overhead FOH).
- Budget hierarchy: static (master) budget vs flexible budget (flexed to ACTUAL output) vs actual results.
  * Static-budget variance = actual - static budget; decomposes into sales-volume variance + flexible-budget variance.
  * Sales-volume variance = (actual units - budgeted units) x budgeted contribution margin/unit (isolates volume).
  * Flexible-budget variance = actual - flexible budget at actual volume (isolates price/efficiency).
- Direct materials: Price variance = (AP - SP) x AQ PURCHASED [owner: purchasing]; Quantity/usage variance = (AQ USED - SQ allowed) x SP [owner: production]. SQ allowed = std qty/unit x actual output.
- Direct labor: Rate variance = (AR - SR) x AH; Efficiency variance = (AH - SH allowed) x SR.
- Variable OH: Spending variance = actual VOH - (AH x std VOH rate); Efficiency variance = (AH - SH) x std VOH rate.
- Fixed OH: Budget/spending variance = actual FOH - budgeted FOH; Production-volume variance = budgeted FOH - applied FOH (SH x std FOH rate) -- a denominator-capacity artifact, NOT a controllable spending issue.
- Mix & yield (multiple inputs / products): materials mix variance = (actual mix% - std mix%) x total actual qty x std price; yield variance = (actual total input - std input for actual output) x std weighted price; sales-mix & sales-quantity variances decompose the sales-volume variance for multi-product.
- Interpretation/management use: Favorable (F) vs Unfavorable (U) are SIGNALS not verdicts; investigate by materiality + controllability (management by exception); tie each variance to a responsibility center; watch gaming (cheap low-quality material -> favorable price BUT unfavorable usage + downstream quality); standards must be current (ideal vs currently-attainable).
- Pitfalls the skill must guard against: budgeted-vs-flexed FOH confusion; AQ-purchased vs AQ-used (materials PRICE uses purchased, QUANTITY uses used); sign errors; treating production-volume variance as controllable.`

const DOMAIN_CONFIG = `PER-DOMAIN CONFIG -- target artifact = a Claude Code SKILL (a SKILL.md with YAML frontmatter {name, description} + optional progressive-disclosure reference files). Follow skill-creator conventions: a trigger-tuned description (when to use / when NOT to use), progressive disclosure (keep SKILL.md lean, push depth to reference files), procedure-first (workflow steps the agent executes), NOT a knowledge dump. The skill must encode the cert competency as an executable PROCEDURE.
Critic axes (Phase 7 / Quality Gates): (1) triggering-precision -- fires on the right asks, not the wrong ones; (2) domain-fidelity -- the procedure is actually CORRECT vs the cert competency; (3) procedure-not-knowledge-dump -- workflow steps not a syllabus restatement; (4) progressive-disclosure-hygiene -- size/file layout/lazy pointers; (5) no-slop -- specificity over plausible-generic.`

const VERDICT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    axis: { type: 'string' },
    verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
    confidence: { type: 'number', description: '0..1 confidence in this verdict' },
    notes: { type: 'string', description: 'specific and actionable; for FAIL, exactly what to fix' },
  },
  required: ['axis', 'verdict', 'confidence', 'notes'],
}

// Seat 1 -- Spec
phase('Spec')
await agent(
  `You are SEAT 1 of the skill-build pipeline (spec author). First read your seat method at ~/.claude/skills/pipeline-spec-author/SKILL.md and follow it.
FOUNDER ASK: build a Finance skill named "variance-analysis" -- the management-accounting procedure for computing and interpreting cost/revenue variances. Department=Finance, cert anchor=CMA/CFA.
${DOMAIN_CONFIG}
${CERT_SEED}
Produce the BUILD SPEC: the procedure the skill must encode (step by step), its trigger description (when to use / when not), inputs/outputs, and a progressive-disclosure file plan (which depth goes to which reference file). This is where cert KNOWLEDGE becomes agent PROCEDURE.
Write the spec to ${SCRATCH}/spec.md. Return a 4-line summary + the absolute path.`,
  { phase: 'Spec' }
)

// Seat 2 -- Tests / acceptance contract
phase('Tests')
await agent(
  `You are SEAT 2 of the skill-build pipeline (test / acceptance-contract author). First read your seat method at ~/.claude/skills/pipeline-test-author/SKILL.md and follow it.
Read ONLY the spec at ${SCRATCH}/spec.md (you are independent of how it gets implemented).
${DOMAIN_CONFIG}
Produce the ACCEPTANCE CONTRACT for the variance-analysis skill: concrete scenarios it must handle (include at least: a DM price+quantity decomposition that exercises the AQ-purchased-vs-used trap; a FOH budget-vs-production-volume decomposition; a multi-input mix+yield case; and a management-by-exception interpretation that ranks variances by materiality+controllability), trigger-accuracy cases (asks it SHOULD fire on vs deceptively-similar asks it should NOT, e.g. generic "analyze this budget" vs "explain the difference between accounting profit and economic profit"), and a fat-content check (encodes real workflow steps, not generic advice). Make every item objectively checkable.
Write to ${SCRATCH}/tests.md. Return a 4-line summary + the absolute path.`,
  { phase: 'Tests' }
)

// Convergence loop: author -> critic, up to 2 rounds
let round = 0
let priorNotes = ''
let finalVerdicts = []
let passed = false
while (round < 2) {
  phase('Author')
  await agent(
    `You are SEAT 3 of the skill-build pipeline (author). First read your seat method at ~/.claude/skills/pipeline-code-author/SKILL.md and follow it. Also follow skill-creator conventions (a lean, trigger-tuned SKILL.md + progressive-disclosure reference files).
Read the spec at ${SCRATCH}/spec.md and the acceptance contract at ${SCRATCH}/tests.md.
${round > 0 ? 'THIS IS A REVISION ROUND. The critic FAILED the prior draft on these axes -- fix EXACTLY these, and do NOT regress what already passed:\n' + priorNotes + '\n' : ''}Write the ACTUAL SKILL: ${SCRATCH}/skill/SKILL.md (YAML frontmatter with name: variance-analysis and a precise trigger description) plus reference files under ${SCRATCH}/skill/ (e.g. reference/formulas.md, reference/worked-examples.md). Procedure-first: the SKILL.md is the executable workflow the agent runs; formulas/worked-examples/depth go to reference files. Encode the cert competency as STEPS the agent executes, not theory it recites. Create directories as needed with Bash.
Return a 4-line summary of what you wrote + the file list (absolute paths).`,
    { phase: 'Author' }
  )

  phase('Critic')
  const axes = ['triggering-precision', 'domain-fidelity', 'procedure-not-knowledge-dump', 'progressive-disclosure-hygiene', 'no-slop']
  const verdicts = (await parallel(axes.map(ax => () =>
    agent(
      `You are a SEAT 4 critic for the skill-build pipeline, judging ONE axis only: "${ax}". First read ~/.claude/skills/pipeline-critic/SKILL.md for the critic method.
Read the authored skill at ${SCRATCH}/skill/SKILL.md and ALL files under ${SCRATCH}/skill/, plus the spec at ${SCRATCH}/spec.md and the acceptance contract at ${SCRATCH}/tests.md.
${DOMAIN_CONFIG}
Judge ONLY the "${ax}" axis. Be adversarial -- default to FAIL if the axis is not clearly met. For domain-fidelity specifically, verify the formulas/decompositions against standard CMA managerial-accounting truth (materials PRICE variance uses AQ PURCHASED; QUANTITY variance uses AQ USED; production-volume variance = budgeted FOH - applied FOH; flexible budget is flexed to actual output). Return your verdict.`,
      { phase: 'Critic', label: `critic:${ax}`, schema: VERDICT }
    )
  ))).filter(Boolean)

  finalVerdicts = verdicts
  const hardFails = verdicts.filter(v => v.verdict === 'FAIL' && v.confidence >= 0.6)
  log(`Round ${round + 1}: ${verdicts.filter(v => v.verdict === 'PASS').length}/${verdicts.length} pass, ${hardFails.length} hard-fail`)
  if (hardFails.length === 0) { passed = true; break }
  priorNotes = hardFails.map(v => `- [${v.axis}] ${v.notes}`).join('\n')
  round++
}

return {
  passed,
  rounds: round + 1,
  verdicts: finalVerdicts,
  artifacts: {
    spec: `${SCRATCH}/spec.md`,
    tests: `${SCRATCH}/tests.md`,
    skillDir: `${SCRATCH}/skill/`,
  },
}
