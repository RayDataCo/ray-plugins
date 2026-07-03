/* ============================================================================
 * REFERENCE IMPLEMENTATION — the queue-walk runner: what makes the rail a
 * QUEUE the brigade works through, rather than a shelf holding one ticket.
 *
 * Implements the loop specified in RAIL-SPEC.md §"Walking the rail":
 *   pull(worker) with an advisory lease → Gate A (ticketLint, deterministic)
 *   → phase-0 Gate B (sufficiency judgment) → the 4-station pass with the
 *   author⇄critic convergence loop → expo decision on the FIVE-exit set
 *   (advance / refire-to-author / reroute-to-spec / reroute-to-steward / kill,
 *   escalate-pause on max_rounds) → ack(id, exit) → next ticket, until the
 *   rail is dry or the ticket budget is spent.
 *
 * Rail backend here = the v1 Obsidian-vault adapter (tickets are markdown
 * files in RAIL_DIR conforming to TICKET-CONTRACT.md). The lease is ADVISORY
 * per RAIL-SPEC: one walker per rail by convention; the lease field detects
 * violations, it does not atomically prevent them.
 *
 * NOTE (portability): station agents read their canonical station skills from
 * the local harness (~/.claude/skills/station-*) — same pending-genericization
 * caveat as brigade-variance-analysis.run.js. Timestamps come in via
 * `args.now` (ISO string) because workflow scripts cannot call Date.now().
 * MODEL PINS: stations/judges run pinned to sonnet — a rail walk is a fan-out,
 * and fan-outs should not inherit an expensive session model by accident.
 * ============================================================================ */

import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

export const meta = {
  name: 'rail-walk',
  description: 'Walk the brigade rail: pull tickets with a lease, gate at phase-0, run the 4-station pass, route on the five-exit set, ack, repeat until dry',
  phases: [
    { title: 'Pull' },
    { title: 'Phase-0' },
    { title: 'Stations' },
    { title: 'Decide' },
  ],
}

/* ------------------------------- config ---------------------------------- */

const RAIL_DIR = (args && args.rail_dir) || `${process.env.HOME}/rdco-vault/08-tooling/brigade-rail`
const WORKER = (args && args.worker) || 'rail-walk-reference'
const NOW = (args && args.now) || 'unstamped' // ISO string, supplied by the caller
const LEASE_TTL_MIN = 120
const MAX_TICKETS = (args && args.max_tickets) || 10
const MAX_ROUNDS = 2
const MODEL = { station: 'sonnet', judge: 'sonnet', expo: 'sonnet' } // pinned — never inherit
const STATION_SKILLS = `${process.env.HOME}/.claude/skills`
const PLUGIN_DIR = (args && args.plugin_dir) || `${process.env.HOME}/Projects/ray-plugins/plugins/skill-agent-brigade`
const RESOLVER_TYPES = ['file', 'url', 'mcp', 'qmd']
const SECTIONS = ['## Order', '## Resolved-context snapshot', '## Work log', '## Artifacts']

/* --------------------- vault rail adapter (driven, v1) -------------------- */
/* Minimal frontmatter field access — regex on the leading YAML block. Good
 * enough for the contract's flat fields; a real adapter would use a parser.  */

function fm(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/)
  return m ? m[1] : ''
}
function fmField(text, key) {
  const m = fm(text).match(new RegExp(`^${key}:\\s*(.*)$`, 'm'))
  return m ? m[1].trim() : null
}
function setFmField(text, key, value) {
  const head = fm(text)
  const updated = head.match(new RegExp(`^${key}:`, 'm'))
    ? head.replace(new RegExp(`^${key}:.*$`, 'm'), `${key}: ${value}`)
    : `${head}\n${key}: ${value}`
  return text.replace(/^---\n[\s\S]*?\n---/, `---\n${updated}\n---`)
}
function contextEntries(text) {
  const lines = fm(text).split('\n')
  const start = lines.findIndex(l => /^context:/.test(l))
  if (start === -1) return []
  const block = []
  for (let j = start + 1; j < lines.length && /^\s/.test(lines[j]); j++) block.push(lines[j])
  return block.join('\n').split(/^\s{2}- /m).slice(1).map(chunk => ({
    id: (chunk.match(/id:\s*(.*)/) || [])[1]?.trim(),
    type: (chunk.match(/type:\s*(.*)/) || [])[1]?.trim(),
    ref: (chunk.match(/ref:\s*"?([^"\n]*)"?/) || [])[1]?.trim(),
    when: (chunk.match(/when:\s*"?([^"\n]*)"?/) || [])[1]?.trim(),
    hasInlineContent: /(^|\s)content:/.test(chunk),
  }))
}

const rail = {
  list() {
    return readdirSync(RAIL_DIR).filter(f => f.endsWith('.ticket.md'))
  },
  /** pull(worker): advisory lease — pick next queued (or lease-expired) ticket */
  pull() {
    for (const f of this.list()) {
      const path = join(RAIL_DIR, f)
      const text = readFileSync(path, 'utf8')
      const status = fmField(text, 'status')
      if (status !== 'queued') continue // v1: expired-lease reclaim left to a human sweep
      let leased = setFmField(text, 'status', 'leased')
      leased = setFmField(leased, 'lease', `{ worker: ${WORKER}, at: ${NOW}, ttl_min: ${LEASE_TTL_MIN} }`)
      writeFileSync(path, leased)
      this.append(path, `leased by ${WORKER} at ${NOW} (ttl ${LEASE_TTL_MIN}m)`)
      return { path, id: fmField(text, 'ticket'), text: readFileSync(path, 'utf8') }
    }
    return null // rail is dry
  },
  /** ack(id, exit): terminal disposition per RAIL-SPEC — clears the lease */
  ack(path, exit) {
    const statusFor = { advance: 'done', kill: 'killed', 'reroute-to-steward': 'needs-context', escalate: 'escalated' }
    let text = readFileSync(path, 'utf8')
    text = setFmField(text, 'status', statusFor[exit] || 'escalated')
    text = setFmField(text, 'lease', 'null')
    writeFileSync(path, text)
    this.append(path, `ack: ${exit} → status ${statusFor[exit] || 'escalated'} (${NOW})`)
  },
  release(path) {
    let text = readFileSync(path, 'utf8')
    text = setFmField(text, 'status', 'queued')
    text = setFmField(text, 'lease', 'null')
    writeFileSync(path, text)
    this.append(path, `released untouched by ${WORKER} (${NOW})`)
  },
  /** append(id, entry): append-only — always under ## Work log, never rewrite */
  append(path, entry) {
    const text = readFileSync(path, 'utf8')
    const idx = text.indexOf('## Artifacts')
    const line = `- ${entry}\n`
    writeFileSync(path, idx === -1 ? text + line : text.slice(0, idx) + line + '\n' + text.slice(idx))
  },
}

/* ------------------- Gate A: ticketLint (deterministic) ------------------- */
/* The 8 rules from TICKET-CONTRACT.md — pure pass/fail, no LLM. Runs at pull
 * (the steward runs the same check at enqueue).                              */

function ticketLint(text, railFiles) {
  const rules = []
  const add = (id, rule, passed, detail = '') => rules.push({ id, rule, passed, detail })

  const id = fmField(text, 'ticket')
  add(1, 'ticket id present, kebab-case, unique on rail', !!id && /^[a-z0-9]+(-[a-z0-9]+)*$/.test(id)
    && railFiles.filter(f => f.startsWith(`${id}.`)).length <= 1, `id=${id}`)

  const artifact = fmField(text, 'artifact')
  add(2, 'artifact ∈ {skill, brigade, menu}', ['skill', 'brigade', 'menu'].includes(artifact), `artifact=${artifact}`)

  const status = fmField(text, 'status')
  const lease = fmField(text, 'lease')
  const statusOk = ['queued', 'leased', 'in-build', 'needs-context', 'escalated', 'done', 'killed'].includes(status)
  const leaseOk = ['leased', 'in-build'].includes(status) ? /worker/.test(lease || '') : true
  add(3, 'status in enum; lease shape matches status', statusOk && leaseOk, `status=${status}`)

  const ctx = contextEntries(text)
  const wellFormed = ctx.length >= 1 && ctx.every(s => s.id && s.type && s.ref && s.when && RESOLVER_TYPES.includes(s.type))
  add(4, '≥1 context source, all well-formed, registered types', wellFormed, `sources=${ctx.length}`)

  const eager = ctx.filter(s => /^always/i.test(s.when || ''))
  const resolveRef = ref => { // absolute, ~-prefixed, or vault-root-relative (RAIL_DIR/../..)
    const r = ref.replace(/^~/, process.env.HOME)
    return existsSync(r) || existsSync(join(RAIL_DIR, '..', '..', r))
  }
  const eagerLive = eager.every(s => s.type !== 'file' || resolveRef(s.ref))
  add(5, 'eager sources resolve (file-type checked here; live types are steward-side)', eagerLive)

  const order = text.match(/## Order\n([\s\S]*?)(?=\n## )/)
  add(6, '## Order present and non-empty', !!order && order[1].trim().length > 0)

  let cursor = -1
  const inOrder = SECTIONS.every(h => { const i = text.indexOf(`${h}\n`); const ok = i > cursor; cursor = i; return ok })
  add(7, 'four canonical H2 sections, in order', inOrder)

  add(8, 'pointers only — no inline content in context', ctx.every(s => !s.hasInlineContent))

  const failed = rules.filter(r => !r.passed)
  return { passed: failed.length === 0, rules, failedIds: failed.map(r => r.id) }
}

/* ------------------------------ the walk ---------------------------------- */

const summary = []
let worked = 0

while (worked < MAX_TICKETS) {
  phase('Pull')
  const t = rail.pull()
  if (!t) { log('rail is dry — stopping'); break }
  worked += 1
  log(`pulled ${t.id} (${worked}/${MAX_TICKETS})`)

  // Gate A at pull — should have been impossible past the steward's enqueue check
  const lint = ticketLint(t.text, rail.list())
  if (!lint.passed) {
    rail.append(t.path, `GATE-A FAIL at pull — rules ${lint.failedIds.join(',')} — ADAPTER DEFECT flagged`)
    rail.ack(t.path, 'reroute-to-steward')
    summary.push({ ticket: t.id, exit: 'reroute-to-steward', why: `gate-A rules ${lint.failedIds.join(',')}` })
    continue
  }

  // Menu tickets (artifact: menu) never enter the stations — the expo answers
  // by introspection and publishes the menu beside the rail (MENU-SPEC.md).
  if (fmField(t.text, 'artifact') === 'menu') {
    const menu = await agent(
      `You are the EXPO answering a menu/discovery ticket ("what can your brigade do?"). Read the ticket at ${t.path} and ` +
      `the brigade home its context points at (this brigade: ${PLUGIN_DIR} — read MENU-SPEC.md, MENU.md, the skills/ roster, ` +
      `and the critic/eval config). Write or refresh the menu at ${join(RAIL_DIR, '..', 'brigades', 'skill-agent-brigade')}/menu.md ` +
      `(the cellar brigades section per MENU-SPEC — menus moved there from <rail>/menus/ in the 2026-07-02 one-store centralization; ` +
      `frontmatter menu_of/version/generated_by: expo — bump version if it exists — plus source_hash: the sha256 of the ` +
      `packaged MENU.md you derived from, computed via Bash \`shasum -a 256\` at publish time; it is the freshness stamp ` +
      `mise's menu_freshness check compares against, per MENU-SPEC "Source vs publication"), then append a work-log line to the ` +
      `ticket and add the menu path under ## Artifacts. Return the published path.`,
      { label: `menu:${t.id}`, phase: 'Phase-0', model: MODEL.expo })
    rail.append(t.path, `menu published: ${String(menu).trim()}`)
    rail.ack(t.path, 'advance')
    summary.push({ ticket: t.id, exit: 'advance', why: 'menu ticket — published by introspection' })
    continue
  }

  // Gate B — phase-0 sufficiency (judgment; criteria in TICKET-CONTRACT.md)
  phase('Phase-0')
  const p0 = await agent(
    `You are the expo running phase-0 (Gate B, sufficiency) on a brigade ticket. Read the ticket at ${t.path}, ` +
    `resolve its EAGER context sources (the ones whose "when" starts with "always"), and judge per the Gate-B criteria in ` +
    `${PLUGIN_DIR}/TICKET-CONTRACT.md: ` +
    `Clear = intent unambiguous + artifact/type consistent with sources + oracle-grade substance present (worked ` +
    `examples for computational/corpus, exemplars for generative/advisory). Ambiguous = >1 plausible skill/scope. ` +
    `Thin = intent clear, named context missing (itemize what + why it sharpens the build).`,
    { label: `phase-0:${t.id}`, phase: 'Phase-0', model: MODEL.judge, schema: {
      type: 'object', additionalProperties: false,
      properties: { verdict: { type: 'string', enum: ['clear', 'ambiguous', 'thin'] }, notes: { type: 'string' } },
      required: ['verdict', 'notes'] } }
  )
  rail.append(t.path, `phase-0: ${p0.verdict} — ${p0.notes}`)
  if (p0.verdict !== 'clear') {
    rail.ack(t.path, 'reroute-to-steward')
    summary.push({ ticket: t.id, exit: 'reroute-to-steward', why: `phase-0 ${p0.verdict}` })
    continue
  }

  // Stations — spec → tests → author ⇄ critic (per-ticket convergence loop)
  phase('Stations')
  const run = join(RAIL_DIR, '..', 'brigade-runs', t.id)
  await agent(`Run STATION 1 (spec author). Read your station skill at ${STATION_SKILLS}/station-spec-author/SKILL.md, the ticket at ${t.path} (its ## Order + resolved context sources), and write spec.md to ${run}/. Append one work-log line to the ticket describing the spec produced.`,
    { label: `spec:${t.id}`, phase: 'Stations', model: MODEL.station })
  await agent(`Run STATION 2 (test author). Read your station skill at ${STATION_SKILLS}/station-test-author/SKILL.md and ONLY ${run}/spec.md (never any draft). Write tests.md to ${run}/. Append one work-log line to the ticket.`,
    { label: `tests:${t.id}`, phase: 'Stations', model: MODEL.station })

  let exit = null, round = 0, lastCritic = null
  while (round < MAX_ROUNDS && !exit) {
    round += 1
    await agent(`Run STATION 3 (author), round ${round}. Read ${STATION_SKILLS}/station-code-author/SKILL.md, ${run}/spec.md, ${run}/tests.md${round > 1 ? `, and the prior critic notes in ${run}/critic-r${round - 1}.json` : ''}. Write the skill (SKILL.md + references/) to ${run}/skill/. Append one work-log line to the ticket.`,
      { label: `author:${t.id}:r${round}`, phase: 'Stations', model: MODEL.station })
    lastCritic = await agent(`Run STATION 4 (critic). Read ${STATION_SKILLS}/station-critic/SKILL.md and judge ${run}/skill/ against ${run}/spec.md + ${run}/tests.md on the per-domain axes. Write the full verdicts to ${run}/critic-r${round}.json. CRITIC ADVISES ONLY — return verdicts, not a route.`,
      { label: `critic:${t.id}:r${round}`, phase: 'Stations', model: MODEL.judge, schema: {
        type: 'object', additionalProperties: false,
        properties: { pass: { type: 'boolean' }, failing_axes: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
        required: ['pass', 'failing_axes', 'notes'] } })
    rail.append(t.path, `critic r${round}: ${lastCritic.pass ? 'PASS' : `FAIL (${lastCritic.failing_axes.join(', ')})`}`)

    // Expo decides — the critic advised; the expo holds round budget + history
    phase('Decide')
    const decision = await agent(
      `You are the EXPO deciding a ticket's route. Your information advantage over the single-shot critic: ` +
      `round=${round} of max ${MAX_ROUNDS}; phase-0 said "clear" with notes "${p0.notes}"; the full work log is on the ticket at ${t.path}. ` +
      `Critic verdict this round: pass=${lastCritic.pass}, failing axes=[${lastCritic.failing_axes.join(', ')}], notes="${lastCritic.notes}". ` +
      `Decision policy: advance if no high-confidence FAIL. refire-to-author if the FAIL is fixable in the draft AND budget remains. ` +
      `reroute-to-spec if the SAME axis failed across rounds or the fail contradicts the acceptance contract (the contract is the problem). ` +
      `reroute-to-steward if the fail traces to missing/contradictory CONTEXT the payload can't support. kill only if the skill is ` +
      `unrecoverable dead weight. escalate if you would refire but the budget is exhausted. Weigh refire cost vs remaining budget — ` +
      `do not burn the last round on a cosmetic gap.`,
      { label: `expo:${t.id}:r${round}`, phase: 'Decide', model: MODEL.expo, schema: {
        type: 'object', additionalProperties: false,
        properties: { exit: { type: 'string', enum: ['advance', 'refire-to-author', 'reroute-to-spec', 'reroute-to-steward', 'kill', 'escalate'] }, rationale: { type: 'string' } },
        required: ['exit', 'rationale'] } })
    rail.append(t.path, `expo r${round}: ${decision.exit} — ${decision.rationale}`)
    if (decision.exit === 'refire-to-author') continue
    exit = decision.exit
  }
  exit = exit || 'escalate' // budget exhausted without a terminal decision

  rail.ack(t.path, exit)
  summary.push({ ticket: t.id, exit, rounds: round })
  log(`${t.id}: ${exit} after ${round} round(s)`)
}

return { worker: WORKER, worked, summary }
