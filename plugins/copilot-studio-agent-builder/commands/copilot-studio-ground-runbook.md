---
description: Re-ground the Copilot Studio generic runbook in the latest Microsoft Learn docs (this field changes fast — refresh instead of trusting a frozen asset).
---

Re-ground the Copilot Studio **generic runbook** against the LATEST Microsoft Learn documentation. The product changes fast (preview features, Copilot Credits pricing, model availability, UI), so refresh before relying on it.

**Source files** (bundled under `${CLAUDE_PLUGIN_ROOT}/skills/copilot-studio-agent-builder/`):
- `reference/generic-runbook.md` — the doc to refresh
- `reference/doc-endpoints.md` — the Microsoft Learn endpoint index to check
- `reference/copilot-studio-givens.md` — verified facts that may need updating

Steps:
1. Read the three reference files above. Note the runbook's current "Last grounded" date.
2. For each endpoint in `doc-endpoints.md` (root `https://learn.microsoft.com/en-us/microsoft-copilot-studio/`), fetch the current page (WebFetch) and look specifically for changes since that date:
   - preview features graduating to GA or being deprecated
   - billing/pricing changes (Copilot Credits; Work IQ consumption)
   - model-picker availability (which is the newest Claude Sonnet offered?)
   - orchestration / UI changes (e.g. lingering classic-mode references)
   - knowledge-source limits, eval methods, channel support
   **Prefer `learn.microsoft.com` over any blog/video.** Treat anything you cannot verify as unchanged and FLAG it rather than guessing.
3. Produce a **diff summary**: what changed, each with its source URL.
4. Apply the verified updates to `generic-runbook.md` (and `copilot-studio-givens.md` where a fact changed) and bump the "Last grounded against Microsoft Learn" date at the bottom of the runbook to today.
   - **Claude Code:** edit the files in place. If a pulled project copy also exists (from `/copilot-studio-pull-runbook`), ask which to update, or update both.
   - **Claude Web / Desktop:** update the runbook asset in the current Project.
5. **Report the diff summary with sources. Do NOT silently rewrite** — show what changed so the engineer can sanity-check a fast-moving field.

If WebFetch / web access is unavailable in this environment, say so and stop — do not fabricate "latest" doc content.
