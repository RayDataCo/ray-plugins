# Implementation notes — Brigade vocabulary rename + deterministic lint axis

Date: 2026-06-30
Branch: `add-skill-dev-pipeline-and-variance-analysis` (PR #6)
Scope: `plugins/skill-dev-pipeline/` → `plugins/skill-agent-brigade/` + repo-root `marketplace.json`.

Canonical vocab source: the 2026-06-28 agent-brigade editor's-pass note (private house doc, outside this repo)
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

## Seat→station skill rename (follow-up)

Date: 2026-06-30. Resolves the OPEN QUESTION flagged above (lines 58-66): the founder
decided to rename the four EXTERNAL seat-skills from `pipeline-*` → `station-*`, closing the
documented residual seam. These four skills live in `~/.claude/skills/` (NOT in this repo, NOT
in any git repo) — each is a loose `SKILL.md` with NO `name:` frontmatter, so the directory name
IS the skill name; renaming the dir renames the skill.

### Final rename map
- `~/.claude/skills/pipeline-spec-author/` → `station-spec-author/`
- `~/.claude/skills/pipeline-test-author/` → `station-test-author/`
- `~/.claude/skills/pipeline-code-author/` → `station-code-author/`
- `~/.claude/skills/pipeline-critic/`      → `station-critic/`

### Inventory (pre-edit grep over the live surfaces)
Patterns `pipeline-spec-author|pipeline-test-author|pipeline-code-author|pipeline-critic`:
- **`~/.claude/skills/` (the 4 SKILL.md bodies):** cross-link `[[...]]` references between the
  four skills — spec-author:64-66, test-author:67-69, code-author:63-65, critic:84. Plus prose
  references "after `pipeline-spec-author` returns" (test-author:17), "after both
  `pipeline-spec-author` and `pipeline-test-author`" (code-author:15), "after `pipeline-code-author`"
  (critic:17). Plus the `description:` frontmatter "Pipeline seat N of 4 ..." and the H1 titles.
- **repo `plugins/skill-agent-brigade/`:** `workflow/brigade-variance-analysis.run.js` 4 path refs
  (lines 188/200/216/227); `examples/variance-analysis/spec.md:8` (`station: pipeline-spec-author
  (station 1 of 4)`); `examples/variance-analysis/tests.md:2` (`station: pipeline-test-author
  (station 2 of 4)`). The `IMPLEMENTATION-NOTES-*.md` matches (lines 58, 65 + this section) are
  historical/documentary and are EXCLUDED from acceptance check #4 by the `grep -v IMPLEMENTATION-NOTES`.
- **vault:** `CAPABILITIES.md` lines 122, 124, 164; `01-projects/skill-pipelines/2026-05-29-v-model-build-workflow-spec.md`
  lines 18, 24, 25, 26, 27 (lines 37/39/41/43 use bare `pipeline-*-author`/`pipeline-critic` in
  backticks too — all updated).
- **NOT touched (per spec):** `~/.claude/state/rdco-doctor-*.json` snapshots (historical diagnostics)
  and `~/.claude/state/ray-handoff.md` (parent updates that).

### Edits made (after the `mv` renames above)

**Dirs renamed** (plain `mv`, NOT git mv — `~/.claude/skills/` is not a git repo):
all four `pipeline-*` → `station-*`. Confirmed `ls -d ~/.claude/skills/station-*` shows 4,
`ls -d ~/.claude/skills/pipeline-*` shows none.

**`~/.claude/skills/station-*/SKILL.md` (4 files), per the rename map:**
- `description:` — "Pipeline seat N of 4" → "Brigade station N of 4"; "...multi-agent skill
  build-out pipeline" → "...skill-agent-brigade"; trailing "Domain-agnostic utility seat" →
  "...utility station".
- H1 title — "# Pipeline {Spec,Test,Code} Author" / "# Pipeline Critic" → "# Station ...".
- body prose — "seat"→"station" throughout (unit vocab); "multi-agent skill build-out pipeline"
  → "skill-agent-brigade"; the four cross-link wikilinks `[[pipeline-*]]` → `[[station-*]]`;
  prose skill refs ("after `pipeline-spec-author` returns" etc.) → `station-*`.
- station-test-author body: "same per-run scratch dir as the rest of the pipeline" → "...the
  rest of the pass" (orchestrator-layer sense).
- station-code-author body: "follows the founder's pipeline-architecture naming" → "...brigade-
  architecture naming".

**Tool used:** the Edit tool was NOT denied on `~/.claude/**`, but its read-tracking guard
required re-Reading each renamed path; given the volume of order-sensitive replacements per file
(and the need to preserve file-path "pipeline" tokens) I used a verified Python one-off
(`scratchpad/rename_skills.py`, literal `str.replace` with an ordered list + per-file leftover
audit) for the 4 SKILL.md bodies, and a second one (`rename_refs.py`, four exact-string swaps)
for the repo + vault refs. Each script printed post-edit verification; final grep confirms zero
stale strings.

**Repo refs (`plugins/skill-agent-brigade/`):**
- `workflow/brigade-variance-analysis.run.js` — 4 station-method path refs `~/.claude/skills/
  pipeline-*/SKILL.md` → `station-*/SKILL.md` (lines 188/200/216/227).
- `examples/variance-analysis/spec.md:8` `station: pipeline-spec-author` → `station-spec-author`.
- `examples/variance-analysis/tests.md:2` `station: pipeline-test-author` → `station-test-author`.

**Vault refs (surgical — skill-name strings only, no restructuring):**
- `CAPABILITIES.md` — lines 122 (`pipeline-critic`→`station-critic`), 124 (all four names),
  164 (`pipeline-critic`→`station-critic`).
- `01-projects/skill-pipelines/2026-05-29-v-model-build-workflow-spec.md` — lines 18, 24-27,
  37, 39, 41, 43 (all backticked skill-name occurrences) → `station-*`.

**Judgment calls / kept-as-is:**
- **File-path "pipeline" tokens preserved** in all SKILL.md `Related` wikilinks and config/template/
  runs/axes paths: `skill-pipelines/`, `multi-agent-pipeline-architecture`, `multi-agent-pipeline-
  config-schema`, `rdco-pipeline-rlhf-shaped`. These point at REAL vault files/folders that were
  NOT renamed in this pass — changing them would break the links. The replacement logic targeted
  product-vocab strings only, never these paths (verified by per-line leftover audit).
- **Vault surrounding vocab left intact per the "surgical, skill-name strings only" instruction:**
  `CAPABILITIES.md` still reads "**Pipeline seats (the 4-seat utility set):**" (header) and
  "gate for pipeline-stage outputs" (line 164 prose); the v-model spec still reads "(seat 1/4)"…
  "(seat 4/4)". Only the skill-name strings were swapped. Flagging these as a possible future
  consistency follow-up if the founder wants the prose vocab aligned too.
- **`station-code-author` description** keeps "(code, markdown, structured doc, etc.)" and the
  body keeps the "the term 'code' follows..." caveat — these are functional explanation, not the
  seat/pipeline vocab, so untouched.

**Acceptance checks:** (1) PASS — 4 dirs renamed, no `pipeline-*` of the four remain.
(2) PASS — each description begins "Brigade station N of 4". (3) PASS — `node --check
plugins/skill-agent-brigade/workflow/brigade-variance-analysis.run.js` → OK. (4) PASS — stale-ref
grep (with `grep -v IMPLEMENTATION-NOTES`) returns ZERO across all live surfaces.

**Commit SHA (rename content commit):** `277a1d90e9911006fb5e7cb9c74a55506b7281de`
on branch `add-skill-dev-pipeline-and-variance-analysis` (this notes-only SHA line is a
trailing doc commit on top). NOT merged.
