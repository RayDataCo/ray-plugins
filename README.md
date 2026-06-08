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
```

## Plugins

- **`rdco-example`** — minimal template: two example skills (`rdco-greeting` + `rdco-hello`), skills-only. Copy it to start your own.
- **`copilot-studio-agent-builder`** — guides the full lifecycle of building a Microsoft Copilot Studio agent and emits five standard deliverables (generic runbook + per-agent implementation / evaluation / documentation / maintenance docs). Generative-orchestration baseline; Work-IQ-off + grounded-internal defaults; built from a verified Microsoft Learn walkthrough. Works in **Claude Code** (deliverables as markdown files) and **Claude Web/Desktop** (deliverables as project assets). Skills-only (no slash commands) — ships two companion skills: `copilot-studio-pull-runbook` (pull the runbook into your project) and `copilot-studio-ground-runbook` (refresh it against the latest Microsoft docs — the field moves fast).
  ```
  /plugin install copilot-studio-agent-builder@ray-plugins
  ```

## Copy it

`plugins/rdco-example/` is a template. Copy the folder, rename it, edit `plugin.json`, add your own `skills/`, `agents/`, hooks, or MCP servers, then add an entry to `.claude-plugin/marketplace.json`. (RDCO standardizes on **skills** over slash commands — build capabilities as skills.)

## Other sources

- **Private GitHub repos** work — Claude Code uses your existing `gh`/git credentials (anyone with repo access can add it). For background auto-updates, set `GITHUB_TOKEN`.
- **Bitbucket / GitLab / self-hosted** work via a full git-URL source, e.g. `/plugin marketplace add https://bitbucket.org/team/plugins.git`.

Built by [Ray Data Co](https://raydata.co).
