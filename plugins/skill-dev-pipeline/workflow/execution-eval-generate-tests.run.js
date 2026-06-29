/* ============================================================================
 * EXECUTION-EVAL STATION — second skill: generate-tests.
 *
 * A DIFFERENT skill type than variance-analysis (transform: Scope×Basis matrix
 * → dbt tests). Same station, same two-arm tier ablation.
 *
 * Lift hypothesis: base models know universal dbt conventions (not_null,
 * accepted_values) but NOT this skill's specific rules — severity mapping
 * (absolute/relative→error, temporal→WARN, human→SKIP no code) and coverage-gap
 * flagging. So lift, if any, should land on the skill-specific-rule answers.
 *
 * Grading is deterministic against FIXED per-fixture output schemas. (Earlier
 * free-form "figures" grading was too fragile — models name fields wildly
 * differently, e.g. test_1_severity vs severity_row_level_absolute — so the
 * grader matched values to the wrong slot. Forcing exact field names removes
 * the whole name-matching failure mode.) Oracle answers are grounded in the
 * skill's own rules (~/.claude/skills/generate-tests/SKILL.md).
 * ============================================================================ */

export const meta = {
  name: 'execution-eval-generate-tests',
  description: 'Execution-eval station on a second skill (generate-tests): two-arm tier ablation, fixed-schema deterministic grading, per-fixture lift',
  phases: [{ title: 'Run arms' }, { title: 'Report' }],
}

const SKILL_PATH = '/Users/ray/.claude/skills/generate-tests'
const N = 3
const MODELS = (args && Array.isArray(args.models) && args.models.length) ? args.models : ['haiku', 'sonnet', 'opus']

const sev = { type: 'string', enum: ['error', 'warn'] }
const yn = { type: 'string', enum: ['yes', 'no'] }
const obj = (props) => ({ type: 'object', additionalProperties: false, properties: { ...props, note: { type: 'string' } }, required: Object.keys(props) })

const MATRIX = `Scope × Basis testing matrix for model \`daily_revenue\`:
| scope \\ basis | absolute | relative | temporal | human |
| row-level | amount must be >= 0 | — | — | spot-check 5 rows against the billing UI |
| aggregate-level | — | sum(amount) within 2 std-dev of trailing-30-day mean | daily row count within 20% of prior day | — |
| transformation-level | (empty) | (empty) | (empty) | (empty) |`

// Expected answers per the generate-tests rules: absolute→error, relative→error,
// temporal→WARN, human→SKIP (no executable test); flag any scope with 0 tests.
const FIXTURES = [
  {
    id: 'S1-severity-and-human-skip',
    prompt: `${MATRIX}
Generate dbt data-quality tests from this matrix for model \`daily_revenue\`.`,
    schema: obj({
      amount_check_severity: sev,
      temporal_rowcount_check_severity: sev,
      human_spotcheck_generates_executable_test_code: yn,
    }),
    expected: {
      amount_check_severity: 'error',
      temporal_rowcount_check_severity: 'warn',
      human_spotcheck_generates_executable_test_code: 'no',
    },
  },
  {
    id: 'S2-coverage-gap',
    prompt: `${MATRIX}
Generate the dbt tests and a coverage report for model \`daily_revenue\`.`,
    schema: obj({
      scope_with_zero_automated_tests: { type: 'string' },
      transformation_level_test_count: { type: 'string' },
    }),
    expected: {
      scope_with_zero_automated_tests: 'transformation', // contains-match
      transformation_level_test_count: '0',
    },
  },
  {
    id: 'S3-test-type-and-relative-severity',
    prompt: `Scope × Basis matrix for model \`opportunities\`:
| scope \\ basis | absolute | relative |
| row-level | column \`stage\` must be one of: prospecting, qualified, closed_won, closed_lost | — |
| aggregate-level | — | sum(amount) this month within 2 std-dev of the trailing-12-month average |
Generate dbt tests for model \`opportunities\`.`,
    schema: obj({
      stage_enum_dbt_test_type: { type: 'string' },
      relative_sum_amount_check_severity: sev,
    }),
    expected: {
      stage_enum_dbt_test_type: 'accepted_values', // contains-match
      relative_sum_amount_check_severity: 'error',
    },
  },
]

const norm = (s) => String(s == null ? '' : s).toUpperCase().replace(/[^A-Z0-9]/g, '')

// Grade by EXACT field lookup against the fixture's fixed schema — no name-matching.
function grade(fixture, result) {
  if (!result) return 0
  let passed = 0
  const fields = Object.keys(fixture.expected)
  for (const field of fields) {
    const got = norm(result[field])
    const want = norm(fixture.expected[field])
    if (got === want || got.includes(want)) passed++
  }
  return passed / fields.length
}

function arrPrompt(fixture, arm, k) {
  const head = arm === 'with_skill'
    ? `You have a skill available. FIRST read the skill at ${SKILL_PATH}/SKILL.md and FOLLOW its rules (especially its severity mapping and how it handles human checks and coverage gaps).`
    : `Use your own knowledge of dbt data-quality testing.`
  return `${head}

TASK (independent attempt #${k + 1}):
${fixture.prompt}

Do the work, then fill in EXACTLY the structured fields requested (these capture the specific decisions being checked). Answer concisely.`
}

phase('Run arms')
const arms = ['with_skill', 'without_skill']
const jobs = []
for (const model of MODELS)
  for (const fx of FIXTURES)
    for (const arm of arms)
      for (let k = 0; k < N; k++)
        jobs.push({ model, fx, arm, k })

const results = await parallel(jobs.map(j => () =>
  agent(arrPrompt(j.fx, j.arm, j.k), {
    phase: 'Run arms',
    label: `${j.model}/${j.arm === 'with_skill' ? 'skill' : 'base'}:${j.fx.id}#${j.k + 1}`,
    model: j.model,
    schema: j.fx.schema,
  }).then(r => ({ ...j, passRate: grade(j.fx, r) }))
    .catch(() => ({ ...j, passRate: null }))
))

phase('Report')
const stats = (xs) => {
  const v = xs.filter(x => x != null)
  if (!v.length) return { mean: 0, stddev: 0, n: 0 }
  const mean = v.reduce((a, b) => a + b, 0) / v.length
  const variance = v.length > 1 ? v.reduce((a, b) => a + (b - mean) ** 2, 0) / (v.length - 1) : 0
  return { mean: +mean.toFixed(4), stddev: +Math.sqrt(variance).toFixed(4), n: v.length }
}

const TH = 0.15, CEIL = 0.95
function classify(f) {
  if (f.lift < -Math.max(0.1, f.band)) return 'regression'
  if (f.baseline >= CEIL) return 'non-discriminating'
  if (f.lift >= TH && f.lift > f.band) return 'win'
  return 'flat'
}

const byModel = MODELS.map(model => {
  const mr = results.filter(r => r.model === model)
  const w = stats(mr.filter(r => r.arm === 'with_skill').map(r => r.passRate))
  const b = stats(mr.filter(r => r.arm === 'without_skill').map(r => r.passRate))
  const perFixture = FIXTURES.map(fx => {
    const fw = stats(mr.filter(r => r.fx.id === fx.id && r.arm === 'with_skill').map(r => r.passRate))
    const fb = stats(mr.filter(r => r.fx.id === fx.id && r.arm === 'without_skill').map(r => r.passRate))
    const f = {
      fixture: fx.id, with_skill: fw.mean, baseline: fb.mean,
      lift: +(fw.mean - fb.mean).toFixed(4),
      band: +Math.sqrt(fw.stddev ** 2 + fb.stddev ** 2).toFixed(4),
    }
    f.class = classify(f)
    return f
  })
  const classes = perFixture.map(f => f.class)
  const action = classes.includes('regression') ? 'refire-to-author'
    : classes.includes('win') ? 'advance'
      : classes.every(c => c === 'non-discriminating') ? 'inconclusive-fixtures-dont-discriminate'
        : 'kill'
  const wins = perFixture.filter(f => f.class === 'win')
  return {
    model, aggregate_lift: +(w.mean - b.mean).toFixed(4),
    with_skill: w, baseline: b, action,
    decision_basis: wins.length ? `win on ${wins.map(f => f.fixture).join(', ')}` : `no discriminating win (${classes.join(', ')})`,
    per_fixture: perFixture,
  }
})

for (const m of byModel) {
  log(`[${m.model}] base ${(m.baseline.mean * 100).toFixed(0)}% → +skill ${(m.with_skill.mean * 100).toFixed(0)}% (agg ${m.aggregate_lift >= 0 ? '+' : ''}${(m.aggregate_lift * 100).toFixed(0)}pp) → ${m.action} [${m.decision_basis}]`)
  for (const f of m.per_fixture) log(`    ${f.fixture}: skill ${(f.with_skill * 100).toFixed(0)}% vs base ${(f.baseline * 100).toFixed(0)}% (Δ ${f.lift >= 0 ? '+' : ''}${(f.lift * 100).toFixed(0)}pp) — ${f.class}`)
}

return { skill: 'generate-tests', n_per_arm: N, by_model: byModel }
