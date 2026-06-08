# Agent Implementation Plan — `<AGENT NAME>` (per agent)

> Deliverable #2. The §4 fill-in form, completed. One field per decision with the **chosen value + rationale + doc ref**. Orchestration mode is fixed at generative — not a field.

```
AGENT IMPLEMENTATION — FILL IN
(All agents are generative — orchestration is not a choice; see runbook §C.)

— Overview tab —
1.  Agent name ................ ______________________
2.  Description ............... ______________________
    (Plain-language purpose. FUNCTIONAL, not cosmetic — generative orchestration
     routes on this text.)
3.  Agent status review ....... List each warning Copilot Studio shows + resolution.
    Common causes: missing dependency (topic/flow/connector/knowledge),
    auth misconfig, unpublished changes.
4.  Primary model ............. DEFAULT: newest Claude Sonnet in the tenant's picker.
    Do NOT hardcode a version. RECORD the version actually chosen: ____________
5.  Instructions (system prompt) ... ______________________   ← high-leverage
    (role + scope; out-of-scope behavior; tone; when to use which tool/knowledge
     source. Keep deterministic guarantees in Topics, not prose.)
6.  Knowledge — Web Search ... DEFAULT: DISABLED for internal agents.
    Allow ungrounded responses ... DEFAULT: OFF for grounded internal agents.
7.  Knowledge — "Turn on Work IQ" semantic index ... DEFAULT: TURN OFF.
    (Ships ON — must be explicitly disabled. Requires M365 Copilot license if ever on.)

— Knowledge tab —
8.  Knowledge sources ......... List source + type + why.
    (Limits: web 25 / SharePoint 25 / Dataverse unlimited / connectors unlimited;
     uploaded files don't count toward 25.)

— Tools tab —
9.  Work IQ MCP tools ......... DEFAULT: DISABLED (do not add). Preview; Copilot
    Credits cost from 2026-06-16; needs M365 Copilot license. Separate from #7.
10. Connectors / other tools .. As needed: connectors, agent flows, prompt tools,
    code interpreter, MCP servers, computer use. Each gets a clear description.

— Triggers tab —
11. Triggers ................. Conversational (topic trigger phrases) and/or
    autonomous (event / scheduled). Note: autonomous → monitor agent health.

— Agents tab —
12. Child / connected agents . Only if decomposition is warranted.

— Topics tab —
13. Topics ................... Conversational rails + entities + slots + variables.
    For each input-collecting topic: entities to capture / required vs optional /
    variable filled / disambiguation behavior.

— Overview tab (polish) —
14. Suggested prompts ........ Starter prompts that steer users onto the rails. Late step.

— Evaluation tab —
15. Evaluations ............. Test sets + methods; must mirror Topics/intents (deliverable #3).

— Cross-cutting —
16. Channels ................. Which output channels + any per-channel UX adaptation.
17. Auth / security ......... Auth mode (default Authenticate with Microsoft);
    sharing/distribution; environment security roles; DLP constraints.
```

## Decision log (fill one row per field)
| # | Field | Chosen value | Rationale | Doc ref |
|---|---|---|---|---|
| 1 | Agent name | | | |
| 2 | Description | | | `advanced-generative-actions` |
| 4 | Model | | newest Sonnet at build time | `nlu-gpt-overview` |
| 5 | Instructions | | | `nlu-gpt-overview` |
| 6 | Web Search / ungrounded | OFF / OFF | grounded internal agent | `knowledge-copilot-studio` |
| 7 | Work IQ semantic index | OFF | no Work IQ unless deliberate | `use-work-iq` |
| 8 | Knowledge sources | | | `knowledge-copilot-studio` |
| 9 | Work IQ MCP | not added | preview + credits | `agent-extend-action-mcp` |
| 10 | Tools | | | `add-tools-custom-agent` |
| 11 | Triggers | | | `authoring-triggers` |
| 12 | Child agents | | | `authoring-add-other-agents` |
| 13 | Topics/entities/slots | | | `advanced-entities-slot-filling` |
| 16 | Channels | | | `publication-fundamentals-publish-channels` |
| 17 | Auth/security | Authenticate with Microsoft | internal agent | `configuration-end-user-authentication` |
