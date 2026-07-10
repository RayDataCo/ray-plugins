/* ============================================================================
 * DISCIPLINE RAIL WALK — canon driver for discipline-kind brigades.
 *
 * The rail half of the symmetry guarantee (AGENT-BRIGADE-STANDARD.md): pulls
 * tickets with a lease, hands each Order to the brigade's EXPO (the composing
 * coordinator), lands the answer in the cellar, and acks on the discipline
 * exit set mapped to the rail's dispositions:
 *
 *   answered            -> ack advance             (done; ticket files to subject)
 *   partial-with-gaps   -> ack advance             (done; gaps recorded in the
 *                                                   work log + answer artifact —
 *                                                   a terminal answer with
 *                                                   declared gaps, not rework)
 *   needs-clarification -> ack reroute-to-steward  (needs-context; stays on rail)
 *   out-of-scope        -> ack kill                (killed; work log names why +
 *                                                   the right brigade if known)
 *
 * CANON LIVES IN ab-skill-factory (skills/service/discipline-rail-walk.run.js).
 * Discipline brigades receive a VENDORED, byte-identical copy (stamped via the
 * adapter's `stamp` subcommand) — copies are build artifacts, never hand-edited.
 * All per-brigade variance arrives via args; the file itself never changes.
 *
 * Executed by the harness Workflow tool (not node). No fs/env access here —
 * every rail mutation happens inside an agent() call shelling to the vendored
 * rail_adapter.py. Same constraints as the factory's rail-walk.run.js:
 * defensive args parse (harness may deliver args as a JSON string), no
 * Date.now()/Math.random(), {curly} placeholders in prompts (never angle
 * brackets — they corrupt StructuredOutput parses).
 * ============================================================================ */

export const meta = {
  name: 'discipline-rail-walk',
  description: 'Walk the rail for a discipline brigade: pull-with-lease, hand the Order to the expo, land the answer, ack on the discipline exit set',
  phases: [
    { title: 'Walk' },
  ],
}

let A = {}
if (typeof args === 'string') { try { A = JSON.parse(args) } catch (e) { A = {} } }
else if (args && typeof args === 'object') { A = args }

const BRIGADE = A.brigade
const PLUGIN_DIR = A.plugin_dir
const CELLAR_ROOT = A.cellar_root
const RAIL_DIR = A.rail_dir
for (const [k, v] of [['brigade', BRIGADE], ['plugin_dir', PLUGIN_DIR], ['cellar_root', CELLAR_ROOT], ['rail_dir', RAIL_DIR]]) {
  if (!v) throw new Error('args.' + k + ' is required. The invoking service session supplies: brigade (plugin name, e.g. ab-marketing), plugin_dir (absolute installed plugin root), cellar_root, rail_dir.')
}
const WORKER = A.worker || (BRIGADE + '-walker')
const MAX_TICKETS = A.max_tickets || 10
const EXPO = A.expo_skill || (PLUGIN_DIR + '/skills/expo/SKILL.md')
const ADAPTER = PLUGIN_DIR + '/skills/service/vendor/rail_adapter.py'
const STOP_FLAG = RAIL_DIR + '/.service/' + BRIGADE + '.stop'
const MODEL = A.model || 'sonnet' // pinned for rail ops; the serve step inherits unless overridden

const PULL_SCHEMA = {
  type: 'object',
  properties: {
    found: { type: 'boolean' },
    ticket_path: { type: 'string' },
    ticket_text: { type: 'string' },
    note: { type: 'string' },
  },
  required: ['found'],
}

const SERVE_SCHEMA = {
  type: 'object',
  properties: {
    exit: { type: 'string', enum: ['answered', 'partial-with-gaps', 'needs-clarification', 'out-of-scope'] },
    summary: { type: 'string' },
    artifact_path: { type: 'string' },
    gaps: { type: 'string' },
  },
  required: ['exit', 'summary'],
}

const EXIT_TO_ACK = {
  'answered': 'advance',
  'partial-with-gaps': 'advance',
  'needs-clarification': 'reroute-to-steward',
  'out-of-scope': 'kill',
}

const results = []
let served = 0

for (let i = 0; i < MAX_TICKETS; i++) {
  phase('Walk')

  const pulled = await agent(
    'You operate the rail port for the ' + BRIGADE + ' brigade walk (worker id: ' + WORKER + ').\n' +
    '1. If the stop flag exists at ' + STOP_FLAG + ' return found=false with note "stop flag".\n' +
    '2. Read this brigade\'s MENU at ' + PLUGIN_DIR + '/MENU.md and collect the artifact types whose Status is live.\n' +
    '3. Run: python3 ' + ADAPTER + ' pull ' + RAIL_DIR + ' --worker ' + WORKER + ' --brigade ' + BRIGADE + ' --allowed-artifact {one flag repetition per live type from step 2, plus menu}\n' +
    '4. If a ticket is leased: return found=true, ticket_path = the leased ticket file path exactly as the CLI reports it, ticket_text = the full file contents read AFTER the lease was taken.\n' +
    '5. If the rail has nothing workable: found=false, note = the CLI output.\n' +
    'Never edit the ticket yourself; the adapter owns all mutations.',
    { label: 'pull:' + (i + 1), phase: 'Walk', schema: PULL_SCHEMA, model: MODEL }
  )

  if (!pulled || !pulled.found) { log('walk: rail dry after ' + served + ' ticket(s)' + (pulled && pulled.note ? ' (' + pulled.note + ')' : '')); break }

  let serve = null
  try {
    serve = await agent(
      'You are the ' + BRIGADE + ' expo, serving ONE rail ticket end to end.\n' +
      'Read the expo procedure at ' + EXPO + ' and follow it exactly — decompose the Order, select stations from ' + PLUGIN_DIR + '/skills/, compose, finishing touch. Honest statuses: a held station presents as held.\n' +
      'The ticket (leased to ' + WORKER + ') is at ' + pulled.ticket_path + ' — its full text:\n---\n' + pulled.ticket_text + '\n---\n' +
      'Rules of the rail (origin: this ticket rode the queue; gates still apply):\n' +
      '- If the Order is ambiguous or the context is thin, do NOT guess: exit needs-clarification with the itemized questions appended to the work log.\n' +
      '- If the Order is outside this brigade\'s menu, exit out-of-scope and name the right brigade if you can.\n' +
      '- Otherwise produce the composed answer. Write it as a markdown artifact to ' + CELLAR_ROOT + '/{subject}/artifacts/{ticket-id}-answer.md where {subject} is the ticket\'s subject field and {ticket-id} its id — create dirs as needed, and include provenance frontmatter: produced_by brigade ' + BRIGADE + ', the ticket id, and the stations used.\n' +
      '- Append ONE work-log line via: python3 ' + ADAPTER + ' append ' + pulled.ticket_path + ' {your one-line summary, quoted as a single shell argument}\n' +
      '- If the answer is complete: exit answered. If real gaps remain that more context would not fix cheaply, exit partial-with-gaps and state the gaps in both the artifact and the gaps field.\n' +
      'Return exit, a one-line summary, artifact_path when you wrote one, gaps when partial.',
      { label: 'serve:' + (i + 1), phase: 'Walk', schema: SERVE_SCHEMA }
    )
  } catch (e) {
    serve = null
  }

  if (!serve) {
    await agent(
      'Release the lease so the ticket is workable again: python3 ' + ADAPTER + ' release ' + pulled.ticket_path + '\n' +
      'Then append a work-log line: python3 ' + ADAPTER + ' append ' + pulled.ticket_path + ' {a one-line note that the serve step failed mid-flight for worker ' + WORKER + ' and the lease was released}',
      { label: 'release:' + (i + 1), phase: 'Walk', model: MODEL }
    )
    results.push({ ticket: pulled.ticket_path, exit: 'released-after-failure' })
    continue
  }

  const ackExit = EXIT_TO_ACK[serve.exit] || 'reroute-to-steward'
  await agent(
    'First append one final work-log line: python3 ' + ADAPTER + ' append ' + pulled.ticket_path + ' {one line recording: expo exit ' + serve.exit + ' — ' + serve.summary + (serve.gaps ? ' — gaps: ' + serve.gaps : '') + ', quoted as a single shell argument}\n' +
    'Then close out the lease: python3 ' + ADAPTER + ' ack ' + pulled.ticket_path + ' ' + ackExit + ' ' + CELLAR_ROOT + '\n' +
    'Report the adapter output verbatim.',
    { label: 'ack:' + (i + 1), phase: 'Walk', model: MODEL }
  )

  served++
  results.push({ ticket: pulled.ticket_path, expo_exit: serve.exit, ack: ackExit, summary: serve.summary, artifact: serve.artifact_path || null })
  log('walk: ' + served + ' served — last exit ' + serve.exit)
}

return { brigade: BRIGADE, worker: WORKER, served, results }
