# ray-plugins — Ray Data Co's example Claude Code plugin marketplace

A minimal, working example of a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces). Add it and install the example plugin in two commands.

## Use it

```
/plugin marketplace add RayDataCo/ray-plugins
/plugin install rdco-example@ray-plugins
```

Then try the `/hello` slash command.

## What's inside

```
.claude-plugin/marketplace.json      # marketplace manifest (lists plugins)
plugins/rdco-example/                 # minimal copy-me template
  .claude-plugin/plugin.json          # plugin manifest
  commands/hello.md                   # a slash command (/hello)
  skills/rdco-greeting/SKILL.md       # a skill
plugins/copilot-studio-agent-builder/ # real plugin: build Microsoft Copilot Studio agents
  .claude-plugin/plugin.json
  skills/copilot-studio-agent-builder/
    SKILL.md                          # lifecycle orchestrator (plan->build->test->publish->maintain)
    reference/                        # verified Microsoft Learn facts + doc-endpoint index
    templates/                        # the 5 deliverable templates
```

## Plugins

- **`rdco-example`** — minimal template (`/hello` + a skill). Copy it to start your own.
- **`copilot-studio-agent-builder`** — guides the full lifecycle of building a Microsoft Copilot Studio agent and emits five standard deliverables (generic runbook + per-agent implementation / evaluation / documentation / maintenance docs). Generative-orchestration baseline; Work-IQ-off + grounded-internal defaults; built from a verified Microsoft Learn walkthrough.
  ```
  /plugin install copilot-studio-agent-builder@ray-plugins
  ```

## Copy it

`plugins/rdco-example/` is a template. Copy the folder, rename it, edit `plugin.json`, add your own `commands/`, `skills/`, `agents/`, hooks, or MCP servers, then add an entry to `.claude-plugin/marketplace.json`.

## Other sources

- **Private GitHub repos** work — Claude Code uses your existing `gh`/git credentials (anyone with repo access can add it). For background auto-updates, set `GITHUB_TOKEN`.
- **Bitbucket / GitLab / self-hosted** work via a full git-URL source, e.g. `/plugin marketplace add https://bitbucket.org/team/plugins.git`.

Built by [Ray Data Co](https://raydata.co).
