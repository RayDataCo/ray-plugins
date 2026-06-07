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
plugins/rdco-example/
  .claude-plugin/plugin.json          # plugin manifest
  commands/hello.md                   # a slash command (/hello)
  skills/rdco-greeting/SKILL.md       # a skill
```

## Copy it

`plugins/rdco-example/` is a template. Copy the folder, rename it, edit `plugin.json`, add your own `commands/`, `skills/`, `agents/`, hooks, or MCP servers, then add an entry to `.claude-plugin/marketplace.json`.

## Other sources

- **Private GitHub repos** work — Claude Code uses your existing `gh`/git credentials (anyone with repo access can add it). For background auto-updates, set `GITHUB_TOKEN`.
- **Bitbucket / GitLab / self-hosted** work via a full git-URL source, e.g. `/plugin marketplace add https://bitbucket.org/team/plugins.git`.

Built by [Ray Data Co](https://raydata.co).
