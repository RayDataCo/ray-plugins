/* ============================================================================
 * EXECUTION-EVAL STATION — reference run for variance-analysis.
 *
 * Measures LIFT: does the authored skill beat the base model? Two arms on the
 * SAME fixture (identical prompt) — base model alone vs base model + skill —
 * N samples each, graded deterministically against the acceptance contract's
 * oracle answers. Lift = with-skill pass-rate minus baseline pass-rate.
 *
 * Fixtures are the canonical oracle set from examples/variance-analysis/tests.md
 * (A: DM price/qty AQ-purchased-vs-used trap; B: FOH spending vs production-volume
 * trap; C: mix+yield; D: management-by-exception controllability trap). Grading is
 * scripted (exact numeric/categorical match) per skill-creator's guidance to script
 * programmatically-checkable assertions rather than use an LLM grader.
 *
 * Built on the design in DESIGN.md §5 and the contract in
 * skills/execution-eval-station/SKILL.md.
 * ============================================================================ */

export const meta = {
  name: 'execution-eval-variance-analysis',
  description: 'Execution-eval station: two-arm ablation (base vs base+skill) on the variance-analysis oracle fixtures; reports lift with variance',
  phases: [
    { title: 'Run arms' },
    { title: 'Report' },
  ],
}

/* DEFENSIVE ARGS PARSE (verified live 2026-07-03): the harness delivers `args`
 * to workflow scripts as a JSON-encoded string even when the tool call passes
 * an object. Accept both forms. */
let A = {}
if (typeof args === 'string') { try { A = JSON.parse(args) } catch (e) { A = {} } }
else if (args && typeof args === 'object') { A = args }

const SKILL_PATH = A.skill_path
if (!SKILL_PATH) throw new Error('args.skill_path is required: absolute path to the skill directory under test, e.g. {plugins-root}/ab-managerial-accounting/skills/variance-analysis. No baked-in default: install locations differ per machine.')
const N = A.samples_per_arm || 3 // samples per arm (skill-creator default; raise for high-variance fixtures)

// Each fixture: a prompt (identical to both arms) + the gradeable answer keys.
// `expect` values are normalized (uppercase, alphanumerics only) before compare.
const FIXTURES = [
  {
    id: 'A-dm-price-qty-trap',
    prompt: `Standard costing, direct materials. Standard price SP = $4.00/lb; standard 2 lb per unit. Actual output = 5,000 units. Materials PURCHASED = 12,000 lb at actual price $4.10/lb. Materials USED = 10,200 lb.
Compute the direct materials PRICE variance and the direct materials QUANTITY (usage) variance. Express each as a dollar amount labeled F (favorable) or U (unfavorable).`,
    keys: [
      { name: 'DM price variance', tokens: ['PRICE'], expect: '1200 U' },
      { name: 'DM quantity variance', tokens: ['QUANTITY', 'USAGE'], expect: '800 U' },
    ],
  },
  {
    id: 'B-foh-volume-trap',
    prompt: `Fixed overhead analysis. Budgeted fixed overhead = $100,000. Denominator capacity = 20,000 standard hours (so standard FOH rate = $5.00/hr). Standard 2 hours per unit. Actual output = 9,000 units. Actual fixed overhead = $104,000.
Compute the FOH spending (budget) variance, the FOH production-volume variance, and applied FOH. Label each variance F or U.`,
    keys: [
      { name: 'FOH spending variance', tokens: ['SPENDING', 'BUDGET'], expect: '4000 U' },
      { name: 'FOH production-volume variance', tokens: ['VOLUME'], expect: '10000 U' },
      { name: 'Applied FOH', tokens: ['APPLIED'], expect: '90000' },
    ],
  },
  {
    id: 'C-mix-yield',
    prompt: `Materials mix and yield. Two inputs: Material X standard 60% at $3.00/lb; Material Y standard 40% at $5.00/lb (standard weighted price $3.80/lb). Standard total input for the actual output = 10,000 lb. Actual total input = 10,500 lb (actual X = 7,000 lb, actual Y = 3,500 lb).
Compute the materials MIX variance, the materials YIELD variance, and the total materials usage variance. Label each F or U.`,
    keys: [
      { name: 'Mix variance', tokens: ['MIX'], expect: '1400 F' },
      { name: 'Yield variance', tokens: ['YIELD'], expect: '1900 U' },
      { name: 'Total usage variance', tokens: ['TOTAL'], expect: '500 U' },
    ],
  },
  {
    id: 'D-mgmt-by-exception',
    prompt: `Management by exception. The month's variances: Direct labor EFFICIENCY 9,500 U (production); DM QUANTITY 8,000 U (production); FOH PRODUCTION-VOLUME 10,000 U (capacity); DM PRICE 1,200 F (purchasing); DL RATE 300 F; VOH SPENDING 500 U. Materiality threshold = at least $1,000 absolute AND at least 2% of that element's standard cost base.
Answer with these exact figure names:
- "FOH production-volume is the single #1 priority" → yes or no
- "FOH production-volume is a controllable spending issue" → yes or no
- "DM price (F) and DM quantity (U) form a cheap-material-causes-overusage gaming linkage" → yes or no`,
    keys: [
      { name: 'FOH production-volume is the single #1 priority', tokens: ['PRIORITY'], expect: 'NO', yesno: true },
      { name: 'FOH production-volume is a controllable spending issue', tokens: ['CONTROLLABLE'], expect: 'NO', yesno: true },
      { name: 'DM price (F) and DM quantity (U) form a cheap-material-causes-overusage gaming linkage', tokens: ['GAMING', 'LINKAGE'], expect: 'YES', yesno: true },
    ],
  },
]

const norm = (s) => String(s == null ? '' : s).toUpperCase().replace(/[^A-Z0-9]/g, '')

const EXEC_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    figures: {
      type: 'array',
      description: 'one entry per requested figure, using EXACTLY the requested figure names',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          name: { type: 'string' },
          value: { type: 'string', description: 'the answer, e.g. "$1,200 U" or "yes"' },
        },
        required: ['name', 'value'],
      },
    },
    reasoning: { type: 'string', description: 'brief working' },
  },
  required: ['figures', 'reasoning'],
}

// Grade one executor result against a fixture's keys. Returns pass-rate 0..1.
// Match a key to a figure by its IDENTIFYING TOKENS, not by exact name — the
// with-skill arm legitimately paraphrases names ("direct materials price
// variance" vs "DM price variance"); penalizing that is an eval bug, not a skill
// failure. Consume each matched figure so two keys can't claim the same one.
function grade(fixture, result) {
  const figures = [...((result && result.figures) || [])]
  let passed = 0
  for (const k of fixture.keys) {
    const want = norm(k.expect)
    const idx = figures.findIndex(f => k.tokens.some(t => norm(f.name).includes(norm(t))))
    if (idx < 0) continue
    const got = norm(figures[idx].value)
    figures.splice(idx, 1) // consume the matched figure
    // yes/no answers: match the leading token (handles "no, capacity artifact").
    // numeric answers: substring (handles "1200U" inside "1200UUNFAVORABLE").
    const ok = k.yesno ? got.startsWith(want) : got.includes(want)
    if (ok) passed++
  }
  return passed / fixture.keys.length
}

function arrPrompt(fixture, arm, k) {
  const head = arm === 'with_skill'
    ? `You have a skill available. FIRST read the skill at ${SKILL_PATH}/SKILL.md and any reference files it points to, then FOLLOW its procedure to solve the problem below.`
    : `Solve the problem below using your own managerial-accounting knowledge.`
  return `${head}

PROBLEM (independent attempt #${k + 1}):
${fixture.prompt}

Return your final answer as the requested figures (name/value pairs), using EXACTLY the figure names requested. Numeric figures: give the dollar amount and an F or U label. Keep reasoning brief.`
}

// Model matrix. The fair ablation holds the MODEL constant and toggles the skill
// (base-M vs M+skill); lift = how much the skill lifts model M. Pass
// args = { models: ['haiku','sonnet'] } to sweep tiers; default = session model.
// A weaker model has headroom, so that's where a procedure skill should show lift.
const MODELS = (Array.isArray(A.models) && A.models.length) ? A.models : ['haiku', 'sonnet']
const arms = ['with_skill', 'without_skill']

// ---- Phase: run both arms, N samples each, for every fixture, per model ----
phase('Run arms')
const jobs = []
for (const model of MODELS)
  for (const fx of FIXTURES)
    for (const arm of arms)
      for (let k = 0; k < N; k++)
        jobs.push({ model, fx, arm, k })

const results = await parallel(jobs.map(j => () => {
  const opts = {
    phase: 'Run arms',
    label: `${j.model || 'session'}/${j.arm === 'with_skill' ? 'skill' : 'base'}:${j.fx.id}#${j.k + 1}`,
    schema: EXEC_SCHEMA,
  }
  if (j.model) opts.model = j.model
  return agent(arrPrompt(j.fx, j.arm, j.k), opts)
    .then(r => ({ ...j, passRate: grade(j.fx, r) }))
    .catch(() => ({ ...j, passRate: null }))
}))

// ---- Phase: aggregate lift per model tier ----
phase('Report')
const stats = (xs) => {
  const v = xs.filter(x => x != null)
  if (!v.length) return { mean: 0, stddev: 0, n: 0 }
  const mean = v.reduce((a, b) => a + b, 0) / v.length
  const variance = v.length > 1 ? v.reduce((a, b) => a + (b - mean) ** 2, 0) / (v.length - 1) : 0
  return { mean: +mean.toFixed(4), stddev: +Math.sqrt(variance).toFixed(4), n: v.length }
}

// Per-fixture decision thresholds. The expo reads PER-FIXTURE lift, not the
// aggregate mean — a skill that fixes one real failure mode must not be washed
// out by easy (ceilinged) fixtures diluting the average.
const TH = 0.15   // a fixture's lift must clear this (and its own noise band) to count as a win
const CEIL = 0.95 // base ≥ this on a fixture = non-discriminating (no headroom to show lift)

function classify(f) {
  if (f.lift < -Math.max(0.1, f.band)) return 'regression'      // skill made this worse
  if (f.baseline >= CEIL) return 'non-discriminating'            // base already at ceiling
  if (f.lift >= TH && f.lift > f.band) return 'win'              // skill lifts a fixture with headroom
  return 'flat'                                                  // had headroom, skill didn't help
}

const byModel = MODELS.map(model => {
  const mr = results.filter(r => r.model === model)
  const w = stats(mr.filter(r => r.arm === 'with_skill').map(r => r.passRate))
  const b = stats(mr.filter(r => r.arm === 'without_skill').map(r => r.passRate))
  const perFixture = FIXTURES.map(fx => {
    const fw = stats(mr.filter(r => r.fx.id === fx.id && r.arm === 'with_skill').map(r => r.passRate))
    const fb = stats(mr.filter(r => r.fx.id === fx.id && r.arm === 'without_skill').map(r => r.passRate))
    const f = {
      fixture: fx.id,
      with_skill: fw.mean,
      baseline: fb.mean,
      lift: +(fw.mean - fb.mean).toFixed(4),
      band: +Math.sqrt(fw.stddev ** 2 + fb.stddev ** 2).toFixed(4),
    }
    f.class = classify(f)
    return f
  })
  // Decide from the per-fixture classes, not the aggregate mean.
  const classes = perFixture.map(f => f.class)
  const action = classes.includes('regression') ? 'refire-to-author'
    : classes.includes('win') ? 'advance'
      : classes.every(c => c === 'non-discriminating') ? 'inconclusive-fixtures-dont-discriminate'
        : 'kill' // had headroom on at least one fixture and didn't lift it
  const wins = perFixture.filter(f => f.class === 'win')
  return {
    model: model || 'session',
    aggregate_lift: +(w.mean - b.mean).toFixed(4), // kept for reference; NOT the decision basis
    with_skill: w, baseline: b, action,
    decision_basis: wins.length ? `win on ${wins.map(f => f.fixture).join(', ')}` : `no discriminating win (classes: ${classes.join(', ')})`,
    per_fixture: perFixture,
  }
})

for (const m of byModel) {
  log(`[${m.model}] base ${(m.baseline.mean * 100).toFixed(0)}% → +skill ${(m.with_skill.mean * 100).toFixed(0)}% (agg ${m.aggregate_lift >= 0 ? '+' : ''}${(m.aggregate_lift * 100).toFixed(0)}pp) → ${m.action} [${m.decision_basis}]`)
  for (const f of m.per_fixture) log(`    ${f.fixture}: skill ${(f.with_skill * 100).toFixed(0)}% vs base ${(f.baseline * 100).toFixed(0)}% (Δ ${f.lift >= 0 ? '+' : ''}${(f.lift * 100).toFixed(0)}pp) — ${f.class}`)
}

return { skill: 'variance-analysis', n_per_arm: N, by_model: byModel }
