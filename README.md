# ray-plugins — Ray Data Co's example Claude Code plugin marketplace

A minimal, working example of a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces). Add it and install the example plugin in two commands.

## Use it

```
/plugin marketplace add RayDataCo/ray-plugins
/plugin install rdco-example@ray-plugins
```

Then say hello to it, or ask for a Ray Data Co greeting — both are skills.

## What's inside

```
.claude-plugin/marketplace.json      # marketplace manifest (lists plugins)
plugins/rdco-example/                 # minimal copy-me template (skills-only)
  .claude-plugin/plugin.json          # plugin manifest
  skills/rdco-greeting/SKILL.md       # a skill (explains plugin structure)
  skills/rdco-hello/SKILL.md          # a skill (say hello, by name)
plugins/copilot-studio-agent-builder/ # real plugin: build Microsoft Copilot Studio agents (skills-only)
  .claude-plugin/plugin.json
  skills/copilot-studio-agent-builder/  # lifecycle orchestrator (plan->build->test->publish->maintain)
    SKILL.md
    reference/                        # generic runbook (living) + verified facts + doc-endpoint index
    templates/                        # the 4 per-agent deliverable templates (#2-#5)
  skills/copilot-studio-pull-runbook/   # skill: pull the runbook into the current project
  skills/copilot-studio-ground-runbook/ # skill: re-ground the runbook in the latest MS docs
plugins/ab-skill-factory/          # real plugin: the agent brigade that manufactures skills
  .claude-plugin/plugin.json
  README.md + DESIGN.md + BUNDLE-SPEC.md + RAIL-SPEC.md  # pattern docs + interface specs
  skills/expo/                        # the deciding role at the pass (routing + exit set)
  skills/execution-eval-station/      # lift-over-base-model value gate (per-fixture, per-tier)
  workflow/*.run.js                   # reference workflow runs (as-executed)
  examples/                           # worked examples w/ real run reports (variance-analysis, generate-tests)
plugins/ab-managerial-accounting/     # discipline brigade: eval-proven finance skills + menu/router
  .claude-plugin/plugin.json
  MENU.md                             # the routing table (situation -> skill / base-model-covered)
  skills/managerial-accounting/       # router skill (front of house for the brigade)
  skills/variance-analysis/           # + 4 more eval-proven skills
  base-model-covered/                 # tasks the base model covers (exemplar prompts + evidence)
plugins/ab-data-engineering/          # discipline brigade: eval-proven DE skills + menu/router
  .claude-plugin/plugin.json
  MENU.md
  skills/pipeline-failure-triage/     # first eval-proven DE skill
```

## Plugins

- **`rdco-example`** — minimal template: two example skills (`rdco-greeting` + `rdco-hello`), skills-only. Copy it to start your own.
- **`copilot-studio-agent-builder`** — guides the full lifecycle of building a Microsoft Copilot Studio agent and emits five standard deliverables (generic runbook + per-agent implementation / evaluation / documentation / maintenance docs). Generative-orchestration baseline; Work-IQ-off + grounded-internal defaults; built from a verified Microsoft Learn walkthrough. Works in **Claude Code** (deliverables as markdown files) and **Claude Web/Desktop** (deliverables as project assets). Skills-only (no slash commands) — ships two companion skills: `copilot-studio-pull-runbook` (pull the runbook into your project) and `copilot-studio-ground-runbook` (refresh it against the latest Microsoft docs — the field moves fast).
  ```
  /plugin install copilot-studio-agent-builder@ray-plugins
  ```
- **`ab-skill-factory`** — the agent brigade that manufactures Claude skills: stations (spec → tests → author → critic) coordinated at **the pass** by an **expo** that decides routing via a closed exit set (`advance · refire-to-author · reroute-to-spec · kill`), pulling mutable **tickets** off a **rail**. Includes the `execution-eval-station` (measures a produced skill's lift over the base model, per-fixture and per-tier), a deterministic skill-lint gate, full pattern docs (README/DESIGN/BUNDLE-SPEC/RAIL-SPEC), reference workflow runs, and two worked examples with real measured-lift reports.
- **`ab-managerial-accounting`** — managerial-accounting discipline brigade (né `discipline-skills`): 5 eval-proven finance skills (`variance-analysis`, `annual-budget-build`, `close-management`, `treasury-liquidity-analysis`, `debt-schedule`), the `managerial-accounting` router skill + `MENU.md` (situation -> skill pairing), and the `base-model-covered/` registry (5 tasks with eval-verified base-model coverage). Only eval-passers ship.
- **`ab-data-engineering`** — data-engineering discipline brigade: first eval-proven skill `pipeline-failure-triage` (+1.00 lift on silent zero-row failure classification) + the `data-engineering` router skill + `MENU.md` with honest per-task status (held-for-refire / weak-evidence / base-model-covered-pending). Only eval-passers ship.

## Copy it

`plugins/rdco-example/` is a template. Copy the folder, rename it, edit `plugin.json`, add your own `skills/`, `agents/`, hooks, or MCP servers, then add an entry to `.claude-plugin/marketplace.json`. (RDCO standardizes on **skills** over slash commands — build capabilities as skills.)

## Other sources

- **Private GitHub repos** work — Claude Code uses your existing `gh`/git credentials (anyone with repo access can add it). For background auto-updates, set `GITHUB_TOKEN`.
- **Bitbucket / GitLab / self-hosted** work via a full git-URL source, e.g. `/plugin marketplace add https://bitbucket.org/team/plugins.git`.

Built by [Ray Data Co](https://raydata.co).
