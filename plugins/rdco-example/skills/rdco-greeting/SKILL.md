---
name: rdco-greeting
description: Example skill bundled in the rdco-example plugin. Use when the user asks for a Ray Data Co greeting or wants to see how a plugin-bundled skill is structured.
---

# RDCO Greeting (example skill)

A minimal example skill shipped inside the `rdco-example` plugin to demonstrate the plugin -> skill structure.

When invoked:
1. Greet the user on behalf of Ray Data Co.
2. Point them at the source: `plugins/rdco-example/` in the `ray-plugins` marketplace repo.
3. Note that a single plugin can bundle skills (`skills/`), slash commands (`commands/`), subagents (`agents/`), hooks, and MCP servers.

Keep it short and friendly.
