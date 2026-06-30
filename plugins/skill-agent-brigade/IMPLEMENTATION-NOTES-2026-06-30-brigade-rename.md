# Implementation notes — Brigade vocabulary rename + deterministic lint axis

Date: 2026-06-30
Branch: `add-skill-dev-pipeline-and-variance-analysis` (PR #6)
Scope: `plugins/skill-dev-pipeline/` → `plugins/skill-agent-brigade/` + repo-root `marketplace.json`.

Canonical vocab source: `~/rdco-vault/08-tooling/2026-06-28-agent-brigade-rough-edges-editor-pass.md`
(items #2 exit set, #3 docs-vs-code split, #4 86→kill, pass-vs-expo note in #5).

## Canonical mapping (final, do not re-debate)

| old | new | layer |
|---|---|---|
| `seat` | **station** | delivery layer — one atomic skill / one phase |
| `pipeline` / `orchestrator` (run one ticket through the stations) | **the pass**; deciding agent = **expo** | control loop |
| `fleet` (batch driver over a queue) | **rail** (the loop / queue layer) | batch |
| plugin `skill-dev-pipeline` | **skill-agent-brigade** | — |
| skill dir `skill-dev-orchestrator` | **expo** (`name: expo`) | the decider role |
| `86` | **kill** (only term; NO prose flavor) | exit primitive |
| whole system | **brigade** | — |
| unit of work | **ticket** | — |

Canonical exit set (verbatim everywhere enumerated): `advance · refire-to-author · reroute-to-spec · kill`.

### MID-FLIGHT SPEC UPDATE (founder, 2026-06-30)
Remove "86" ENTIRELY — do NOT keep it as prose flavor anywhere. The primitive is `kill`
(or `drop`) and that is the only term. Only occurrence in the tree was DESIGN.md §5 line 67
`kill (86) the ticket` → changed to `kill the ticket`. Verified `grep -rnE "\b86\b"` returns
zero after the edit.

## Inventory (pre-edit grep over the tree)

Counts: seat 37, pipeline 34, orchestrator 24, fleet 3, skill-dev-orchestrator 3,
skill-dev-pipeline 3, `\b86\b` 1.

- `fleet`: DESIGN.md only (lines 13, 15, 105) — the Tier-3 table row + naming paragraph + open question.
- `skill-dev-orchestrator`: README.md:125 link, execution-eval-station/SKILL.md:97 link, skill dir + SKILL.md `name:`.
- `skill-dev-pipeline`: README.md:1 title, DESIGN.md:1 title, plugin.json:2 name. (+ marketplace.json x2 at repo root.)
- `skill-pipeline-variance-analysis.run.js`: filename + README.md:115 link + meta.name `skill-pipeline-pilot-variance-analysis`.
- `86`: DESIGN.md:67 only.
- `seat`/`pipeline`/`orchestrator`: spread across DESIGN.md, README.md, both SKILL.md, the
  three .run.js, and examples/ (spec.md, tests.md, critic-report.md, generate-tests-eval-report.md).

### Reference graph (what points at what)
- repo-root `.claude-plugin/marketplace.json` → plugin name `skill-dev-pipeline` + `source: ./plugins/skill-dev-pipeline` (entry) AND discipline-skills description text "produced by the skill-dev-pipeline".
- `.claude-plugin/plugin.json` → `name` + description.
- README.md → links `skills/skill-dev-orchestrator/`, `workflow/skill-pipeline-variance-analysis.run.js`, `skills/execution-eval-station/`, `workflow/execution-eval-*.run.js`, examples/*.
- execution-eval-station/SKILL.md → link `../skill-dev-orchestrator/SKILL.md`.
- examples spec.md/tests.md frontmatter → `seat:` keys + external skill names `pipeline-{spec,test}-author`.

## Rename plan (git mv — must show as renames, not delete+add)
1. `plugins/skill-dev-pipeline/` → `plugins/skill-agent-brigade/`
2. `.../skills/skill-dev-orchestrator/` → `.../skills/expo/`
3. `.../workflow/skill-pipeline-variance-analysis.run.js` → `.../workflow/brigade-variance-analysis.run.js`

## Judgment calls / things kept as-is

- **External seat-skill names kept**: `~/.claude/skills/pipeline-spec-author` (and `-test-`,
  `-code-`, `-critic`) are EXTERNAL harness skills, not in this repo, and acceptance check #3
  does NOT include them in the zero-hit grep. Renaming their paths would break references to
  real skills I cannot rename here. I kept the external paths/names verbatim and only updated
  the surrounding VOCAB prose (`seat method` → `station method`). OPEN QUESTION for founder:
  do you want those external harness skills renamed `station-*` (or `brigade-*`) in a separate
  pass and these paths updated to match? Today they read e.g. "read your station method at
  ~/.claude/skills/pipeline-spec-author/SKILL.md" — a deliberate, documented residual seam
  (README already flags these as pending genericization).
- **"pipeline" was never generic English** in this tree (no "CI pipeline"/"data pipeline"
  usage) — every occurrence is the product/architecture, so all were renamed. Mapping by
  context: whole-system "pipeline" → **brigade**; tier-2 "runs one item through the seats" →
  **the pass**; "orchestrator"-the-agent → **expo**; batch fan-out over the backlog → **rail**.
- **meta.name** `skill-pipeline-pilot-variance-analysis` → `brigade-pilot-variance-analysis`
  (drops "pipeline" for consistency even though it didn't match the check-3 substring).
- **mermaid node IDs** (ORCH, ORCH2, LOOP) kept stable to avoid breaking edge refs; only the
  display labels were changed to expo/the pass.

## Deliverables beyond rename
- A. Canonical "## Naming (canonical)" block added near the top of DESIGN.md.
- B. Deterministic (non-LLM) `skill-lint` axis added to the critic in the reference workflow
  (`brigade-variance-analysis.run.js`): a real programmatic `skillLint()` function checking the
  8 hard rules from Anthropic's skill guide, wired into the Critic-phase aggregation as a
  pass/fail-per-rule axis (distinct from the LLM judgment axes). Documented in DESIGN.md §5.

## Change log (final)

**Renames (all `git mv`, show as R in status):**
- `plugins/skill-dev-pipeline/` → `plugins/skill-agent-brigade/`
- `.../skills/skill-dev-orchestrator/` → `.../skills/expo/`
- `.../workflow/skill-pipeline-variance-analysis.run.js` → `.../workflow/brigade-variance-analysis.run.js`

**Reference/vocab edits (files touched):**
- repo-root `.claude-plugin/marketplace.json` — skill-dev-pipeline entry (name+source+description) → skill-agent-brigade; discipline-skills description ("produced by the skill-agent-brigade").
- `.claude-plugin/plugin.json` — name + description.
- `DESIGN.md` — title; added **Naming (canonical)** block; §1 table (Station/The pass(expo)/Rail); §4 brigade; §5 intro now lists 3 surfaces + new **§5.0 deterministic lint axis** (8 rules); §5 `kill` (86 removed); open questions resolved.
- `README.md` — title/tagline; architecture prose + both mermaid diagrams relabeled to the exit set; phase table header Station; added the **skill-lint** deterministic axis bullet; expo/rail/ticket throughout; workflow link → new filename.
- `skills/expo/SKILL.md` — `name: expo`; full body rewrite to expo/the pass/station/ticket; routing aligned to the exit set; rail fan-out; state diagram adds a `kill` state.
- `skills/execution-eval-station/SKILL.md` — brigade/expo/station; cross-link `../expo/SKILL.md`.
- `workflow/brigade-variance-analysis.run.js` — header/meta/comments/prompts → station/brigade; **added `skillLint()`** (deterministic 8-rule check) and wired it into the Critic aggregation (`verdicts.push(lint)`).
- `examples/variance-analysis/{spec.md,tests.md,critic-report.md}` + `examples/generate-tests-eval-report.md` — seat→station, orchestrator-named→expo-named, pipeline-run→brigade-run, canonical seats→stations. No results fabricated.

**Deliverable B — lint axis validated standalone:** `skillLint()` returns PASS (8/8) on the real installed
skill `plugins/discipline-skills/skills/variance-analysis/` and correctly FAILs a crafted bad skill on
rules 2/3/4/6/8. Folder-name rule (rule 2) is checked against an install `folderName` because the build
dir is a generic scratch `skill/`.

**Note on acceptance check #3:** the literal grep over `plugins/skill-agent-brigade` also matches THIS
notes file and the branch name, which intentionally quote the old identifiers to document the rename.
The functional tree (everything except this notes md) returns ZERO. The external `~/.claude/skills/pipeline-*`
station-skill paths do not match check #3's three patterns and are kept by design.
