# Generic Copilot Studio Runbook (reusable, agent-agnostic)

> Deliverable #1. The master process doc spanning **plan → build → test → publish → maintain**. Agent-agnostic — copy it once, reuse across agents. Per-agent decisions go in deliverables #2–#5, never here.

## 0. Build-time discipline (every time)
- Prefer `learn.microsoft.com` over blogs/videos. Copilot Studio = formerly Power Virtual Agents; ignore old-UI / classic-mode content.
- Re-verify every preview/pricing/model claim at build time (Work IQ MCP = preview; Copilot Credits billing from 2026-06-16).
- All agents are **generative** — orchestration is not a choice.
- Descriptions are functional: the orchestrator routes on them.

## A. Power Platform environment setup (one-time)
- [ ] Licensing/capacity confirmed. Ref: `requirements-licensing`, `copilot-credits-overview`.
- [ ] **Dev** and **prod** environments exist (or planned). Ref: `environments-first-run-experience`.
- [ ] Maker has the correct security role.
- [ ] (Per-agent check at build time, not an assumption) Managed environments / DLP data policies — which connectors are allowed? Ref: `admin-data-loss-prevention`, `security-and-governance`.

## B. Solution setup (one-time per agent)
- [ ] Agent built inside a **Power Platform solution** (NOT the default solution).
- [ ] Publisher + prefix set.
- [ ] This enables clean export/import for dev→prod ALM later.

## C. Create the agent (drive deliverable #2 — the mad-libs form)
Order ≈ build order. All agents generative (no mode field).
- [ ] **Overview:** name, description (functional), agent-status-review (enumerate warnings + resolutions), primary model (= newest Sonnet in the picker; record version), instructions (system prompt), Web Search (default OFF internal), Allow ungrounded responses (default OFF), **Turn on Work IQ semantic index → DISABLE (it ships ON)**.
- [ ] **Knowledge:** sources + type + why (limits: ~25 web/SharePoint; Dataverse unlimited; uploads free).
- [ ] **Tools:** Work IQ MCP → do NOT add (preview, credits). Connectors / agent flows / prompt tools / MCP / computer use as needed, each with a clear description.
- [ ] **Triggers:** conversational and/or autonomous (event / scheduled).
- [ ] **Agents:** child / connected agents only if decomposition is warranted.
- [ ] **Topics:** conversational rails + entities + slot filling + variable/state design.
- [ ] **Overview polish:** suggested starter prompts (late step).
- [ ] **Evaluations:** test sets + methods mirroring Topics/intents (drive deliverable #3).

## D. Publish (keep the two senses separate)
- [ ] **In-environment Publish** (the Publish button) — required before use; re-publish after every change; new content reaches users on a new session.
- [ ] **dev → prod (ALM)** — export managed solution from dev → import to prod; rebind connection refs / env variables. **[OPEN] confirm ALM path** (manual vs pipelines).
- [ ] **Connect channels** — Teams/M365, SharePoint, web, etc. Record channel-specific UX adaptations (e.g. Teams ≤6 suggested actions).
- [ ] **Security/access** — auth mode (default Authenticate with Microsoft), sharing, security roles, DLP.

## E. Maintain (drive deliverable #5)
- [ ] Monitoring surface chosen (conversational effectiveness vs agent health for autonomous agents).
- [ ] Eval cadence + regression policy; results export (89-day retention).
- [ ] Knowledge-refresh schedule; model/version review; cost watch (Copilot Credits / Work IQ).
- [ ] Preview-feature watch (graduation/deprecation); access-review cadence; re-publish procedure.

## References
See `../reference/doc-endpoints.md` for the full Microsoft Learn endpoint index and `../reference/copilot-studio-givens.md` for the verified facts/limits/defaults.
