---
description: Pull the Copilot Studio generic runbook reference into the current project for clear visibility and tweaking.
---

Pull the Copilot Studio **generic runbook** into the user's current working project so they have clear visibility and can tweak it as a living plan.

**Source** (bundled in this plugin): `${CLAUDE_PLUGIN_ROOT}/skills/copilot-studio-agent-builder/reference/generic-runbook.md`. If that variable doesn't resolve in this environment, locate the `copilot-studio-agent-builder` plugin's `reference/generic-runbook.md` and use its contents.

Steps:
1. Read the bundled generic runbook.
2. **Detect the target environment and emit accordingly:**
   - **Claude Code (local filesystem):** write it as a markdown file in the current working directory — default `./copilot-studio-generic-runbook.md`, or the path named in `$ARGUMENTS`. Confirm the path written.
   - **Claude Web / Desktop (no local filesystem):** emit it as a **project asset**. If the user is NOT already in a Project, first nudge them: "Create a project so this runbook and the per-agent deliverables stay bundled and easy to update as you tweak the plans." Then add the runbook as an asset in that project.
3. Remind the user this is a **living doc**: run `/copilot-studio-ground-runbook` to refresh it against the latest Microsoft Learn docs before relying on it.

If `$ARGUMENTS` names a destination path/filename, honor it.
