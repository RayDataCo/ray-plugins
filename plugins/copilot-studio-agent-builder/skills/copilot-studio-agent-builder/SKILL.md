---
name: copilot-studio-agent-builder
description: Guide a human (and the assisting agent) through the full lifecycle of building a Microsoft Copilot Studio agent — plan, build, test, publish, and maintain — and emit five standard deliverables (generic runbook + per-agent implementation, evaluation, documentation, and maintenance docs). Use when the user wants to build, configure, test, publish, or document a Copilot Studio agent; prepare a client runbook for Copilot Studio; or learn the Copilot Studio build process. Also triggers on "Power Virtual Agents" (the product's former name).
---

# Microsoft Copilot Studio — Agent-Building Skill

Guides building a Microsoft Copilot Studio agent end to end and produces five standard deliverables (§ Deliverables). The skill separates **generic, reusable process** (the runbook) from **per-agent decisions** (the implementation/eval/docs/maintenance set) so it is reusable across many agents.

This skill bakes in a **verified-and-corrected** version of a field engineer's draft workflow. Corrections are grounded in the Microsoft Learn docs (see `reference/doc-endpoints.md` for the full endpoint list the building agent should read in full at build time). Unresolved decisions are tagged **[OPEN]**.

## ⚠️ Non-negotiable build-time discipline (read first)

1. **Prefer `learn.microsoft.com` over blogs/videos/third-party content.** Copilot Studio was formerly **Power Virtual Agents** — a lot of public content (and screenshots) still shows the old UI and the retired "classic" mode. Read past it.
2. **Several cited features are preview and/or have changing billing** — notably **Work IQ MCP tools** (preview) and **Copilot Credits** (consumption billing effective **2026-06-16**). **Re-verify every preview/pricing/model-availability claim at build time.** Do not trust the snapshots in this skill as current; they are illustrative.
3. **All agents are generative.** Orchestration mode is a fixed baseline, not a per-agent decision (see § Always generative). Do not author a mode-selection step.
4. **Descriptions are functional, not cosmetic.** In generative orchestration the model routes per turn by reading the descriptions of knowledge sources, tools, and child agents. Every one needs a clear, accurate description.

## Always generative (the fixed baseline)

Agent creation no longer prompts for "Generative vs Classic" (classic creation appears retired; generative is the default, confirmed against the June 2026 UI). Treat generative as a given. Only fall back to classic behavior if a future tenant unexpectedly surfaces the option — re-verify then.

What "always generative" means downstream (encode as givens — detail in `reference/copilot-studio-givens.md`):
- Web Search, "Allow ungrounded responses", and the "Turn on Work IQ" semantic index are all available (they were the generative-only features). Defaults are set in the implementation template.
- The model decides per turn which knowledge / tools / child agents to call from their descriptions. **Topics are optional guardrails, not the primary driver.**
- Knowledge limits are the generous generative-mode limits (~25 search sources; Dataverse unlimited; uploaded files don't count toward the 25).
- Eval test-case generation uses the **Knowledge-based** path (generative). Topics are still validated, via the **Tool / Capability use** eval method — which is why Topics and Evaluations stay coupled.

Ref: `advanced-generative-actions`, `knowledge-copilot-studio`.

## The mental model the user must carry

Four things that are routinely confused — make the distinction explicit (full version in `reference/copilot-studio-givens.md` §2):
- **Knowledge** = passive grounding the agent reads from (RAG). "What do I know?" Sources: public website (Bing-restricted), uploaded docs (Dataverse), SharePoint, Dataverse, enterprise data via connectors.
- **Tools** = actions the agent invokes to *do* something or fetch live/transactional data. "What can I do / fetch on demand?" Connectors, agent flows, prompt tools, code interpreter, computer use, MCP servers, other agents.
- **Topics** = authored conversational units (trigger → nodes → responses) — optional-but-useful rails layered over orchestration.
- **Entities + slot filling** = the NLU layer that extracts structured values from input into variables, so the agent skips questions it already has answers to.

## Lifecycle — the four phases

Full corrected detail lives in `reference/copilot-studio-givens.md`. Summary:

- **Phase A — Power Platform environment setup (one-time).** Confirm licensing/capacity; ensure a **dev** and **prod** environment exist; maker has the right security role. **Build-time per-agent check (not a runbook assumption):** managed environments / DLP data policies constrain which connectors an agent may use. Ref: `environments-first-run-experience`, `requirements-licensing`, `admin-data-loss-prevention`.
- **Phase B — Solution setup (one-time per agent).** Build the agent inside a **Power Platform solution** (not the default solution), with a publisher + prefix, so it can be exported/imported for ALM. This is what makes dev→prod promotion clean.
- **Phase C — Create the agent (the centerpiece).** Drive the fill-in template `templates/02-implementation-plan.md` (the "mad-libs" form). Order ≈ build order: Overview → Knowledge → Tools → Triggers → Agents → Topics → polish (suggested prompts) → Evaluations.
- **Phase D — Publish the agent.** See § Publish (two distinct senses).

## Publish — two senses (keep them separate)

1. **Promote dev → prod (ALM):** export the **managed solution** from dev, import into prod; plan connection-reference / environment-variable rebinding. This is solution ALM, **not** the in-app Publish button. **[OPEN]** confirm the org's ALM path (manual export/import vs Power Platform pipelines).
2. **Publish (in-environment):** the **Publish button** pushes latest content to all connected channels. You must publish before anyone can use the agent, and **re-publish after every change**. New content reaches users only on a new session (~30 min inactivity; in Teams/Omnichannel type "start over", else up to ~1 hr).
3. **Connect output channels** (after at least one publish): Teams & M365 Copilot, SharePoint, WhatsApp, Demo website (stakeholder review only — not production), Custom website, mobile/custom app, Azure Bot Service channels (Slack, Telegram, Twilio, Email…). Channels differ in supported UX (e.g. Teams renders ≤6 suggested actions; attachments generally unsupported) — record adaptations.
4. **Security & access:** authentication mode (default **Authenticate with Microsoft** for any internal/org agent), sharing/distribution, environment security roles, DLP policies.

Ref: `publication-fundamentals-publish-channels`, `configuration-end-user-authentication`, `security-and-governance`.

## Work IQ — both features OFF by default

There are **two different things called "Work IQ"** — the draft conflated them. Default policy: **turn both off** unless deliberately chosen and documented.
1. **"Turn on Work IQ" semantic index** — a toggle on the Generative AI settings page (retrieval quality, esp. SharePoint). **Ships ON** — the builder must *explicitly disable it*; make it a checklist line item. Requires an M365 Copilot license + auth = Authenticate with Microsoft.
2. **Work IQ MCP tools (preview)** — added on the **Tools** tab via Add tool → Model Context Protocol (Mail, Calendar, Teams…). Preview; M365 Copilot license; **consumption billing via Copilot Credits from 2026-06-16**. Don't add it; it lives on the Tools tab (not Overview).

Ref: `use-work-iq`, `knowledge-copilot-studio` (Turn on Work IQ section).

## Deliverables — the five documents

The skill produces five docs. Generic/reusable = #1; per-agent = #2–#5. Each has a bundled template.

1. **Generic Copilot Studio Runbook** (reusable, agent-agnostic) → `templates/01-generic-runbook.md`
2. **Agent Implementation Plan** (per agent — the §4 mad-libs, filled in) → `templates/02-implementation-plan.md`
3. **Agent Evaluation Plan** (per agent) → `templates/03-evaluation-plan.md`
4. **Agent Documentation** (per agent) → `templates/04-documentation.md`
5. **Agent Maintenance Runbook** (per agent) → `templates/05-maintenance-runbook.md`

## Workflow order (how to run this skill)

1. **Draft the generic Runbook (#1) first** — it's agent-agnostic and validates the process before any specific agent.
2. **Then request the engineer's example agent** to validate the per-agent templates (#2–#5). The example was deliberately withheld to avoid over-anchoring — **do not ask for it before the generic runbook exists.**
3. For each new agent: fill #2 → derive #3 (evals must mirror the Topics/intents in #2) → write #4 → set up #5.
4. At every step, **re-verify preview/pricing/model claims against `learn.microsoft.com`** and record the actual values chosen (esp. the model version — pick the **newest Claude Sonnet** the tenant's picker offers; do not hardcode a version).

## Open questions to resolve at build time

- **[OPEN] ALM path** — manual managed-solution export/import, or Power Platform pipelines? Affects Phase B and dev→prod promotion.
- **[OPEN] Licensing for previews** — is there an M365 Copilot license in-tenant (required if either Work IQ feature is ever re-enabled), and is Copilot Credits billing set up (2026-06-16)? Not blocking while both Work IQ features stay off.
- **Example agent** — request after the generic runbook is drafted (see Workflow order).

Resolved already (do not re-litigate): orchestration mode = generative; Work IQ = both off; model = version-agnostic "newest Sonnet"; DLP/governance = per-agent build-time check.

## Bundled files

- `reference/copilot-studio-givens.md` — the verified facts the building agent draws on (knowledge-source limits, entities/slot filling, variables, triggers, multi-agent, full mental model, Work IQ disambiguation, eval methods table).
- `reference/doc-endpoints.md` — the `learn.microsoft.com` endpoint index to read in full, grouped by topic.
- `templates/01-generic-runbook.md` … `templates/05-maintenance-runbook.md` — the five deliverable templates.

## Provenance

Built from a verified-and-corrected handoff spec (Ray Data Co, 2026-06-08) grounded in a Microsoft Learn walkthrough. Distributed via the `ray-plugins` marketplace; designed to be portable into an internal (e.g. Bitbucket) plugin repo — it references only public Microsoft Learn docs and its own bundled templates, no org-internal paths.
