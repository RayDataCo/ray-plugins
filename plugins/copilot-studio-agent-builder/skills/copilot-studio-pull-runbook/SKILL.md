---
name: copilot-studio-pull-runbook
description: Pull the Copilot Studio generic runbook reference into the current project for clear visibility and tweaking — a markdown file in Claude Code, or a project asset in Claude Web/Desktop. Use when the user wants to pull, copy, add, bring, or drop the Copilot Studio runbook into their project or workspace.
---

# Pull the Copilot Studio runbook into the project

Pull the Copilot Studio **generic runbook** into the user's current working project so they have clear visibility and can tweak it as a living plan. (Part of the `copilot-studio-agent-builder` plugin.)

**Source** (bundled in this plugin): `${CLAUDE_PLUGIN_ROOT}/skills/copilot-studio-agent-builder/reference/generic-runbook.md`. If that variable doesn't resolve in this environment, locate the `copilot-studio-agent-builder` plugin's `skills/copilot-studio-agent-builder/reference/generic-runbook.md` and use its contents.

Steps:
1. Read the bundled generic runbook.
2. **Detect the target environment and emit accordingly:**
   - **Claude Code (local filesystem):** write it as a markdown file in the current working directory — default `./copilot-studio-generic-runbook.md`, or a destination the user names. Confirm the path written.
   - **Claude Web / Desktop (no local filesystem):** emit it as a **project asset**. If the user is NOT already in a Project, first nudge them: "Create a project so this runbook and the per-agent deliverables stay bundled and easy to update as you tweak the plans." Then add the runbook as an asset in that project.
3. Remind the user this is a **living doc**: ask to re-ground it (the **copilot-studio-ground-runbook** skill) to refresh against the latest Microsoft Learn docs before relying on it.

If the user names a destination path/filename, honor it.
