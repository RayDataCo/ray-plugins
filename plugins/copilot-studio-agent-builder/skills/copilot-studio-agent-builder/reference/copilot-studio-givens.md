# Copilot Studio — verified givens (corrected facts)

The building agent draws on these so it doesn't re-derive. All grounded in the Microsoft Learn walkthrough; **re-verify preview/pricing/model claims at build time** (see `doc-endpoints.md`). Snapshots are illustrative, not current truth.

## 1. Always-generative — downstream givens

Classic agent creation appears retired; generative is the default and the fixed baseline. Encode:
- Web Search, "Allow ungrounded responses", and the "Turn on Work IQ" semantic index are available (generative-only features).
- The model routes per turn by reading descriptions of knowledge sources / tools / child agents. **Every one needs a clear, accurate description.**
- Topics are optional guardrails, not the primary driver.
- Generous knowledge limits (see §4.6/4.7 below).
- Eval test-case generation = Knowledge-based path; Topics validated via Tool/Capability-use method (keeps Topics + Evals coupled).
- The old docs describing "classic orchestration" are out of date — read past them.

Ref: `advanced-generative-actions`, `knowledge-copilot-studio`.

## 2. Mental model — Knowledge vs Tools vs Topics vs Entities

- **Knowledge** = passive grounding (RAG-style) the agent reads to answer. "What do I know?" Sources: public website (Bing-restricted), uploaded documents (Dataverse), SharePoint, Dataverse, enterprise data via connectors.
- **Tools** = actions to *do* something or fetch live/transactional data on demand. "What can I do / fetch?" Connectors, agent flows (Power Automate-style; the matrix calls these "Copilot Flows"), prompt tools, code interpreter, computer use, MCP servers, other agents.
- **Topics** = authored conversational units (trigger → nodes → responses) — rails for the conversation. In a generative agent, optional-but-useful guardrails over orchestration.
- **Entities + slot filling** = NLU layer that extracts structured values into variables so the agent skips questions it already has answers to.

## 4.4. Model selection + Instructions

- **Model:** select the **latest-generation Claude Sonnet** in the tenant's model picker at build time. **Do not hardcode a version** — Copilot Studio's available models lag direct-Claude availability and turn over quickly. Illustrative snapshot (mid-2026): Copilot Studio exposed Sonnet 4.6 while Sonnet 4.7 was GA via direct Claude subscription; newer versions reach Copilot Studio on a lag. Record the actual version chosen in the Implementation Plan + Documentation.
- **Instructions (system prompt)** = the agent's core behavior contract. State role + scope, what to do when out of scope (defer to a topic / fallback), tone, and — since generative — *when to use which tool/knowledge source* (the model reads this to route). Keep **deterministic guarantees in Topics, not prose.** Ref: `nlu-gpt-overview`.

## 4.5. Entities & slot filling (was missing from the draft)

- An **entity** is a unit of real-world info (email, date/time, person, phone, color, country, city, number, money…). Copilot Studio ships **prebuilt** entities and supports **custom**: **closed list** (small enumerations + synonyms) and **regex** (pattern extraction).
- **Slot filling** = placing an extracted entity value into a variable, typically via a Question node. **Proactive slot filling** harvests entities from the trigger phrase / earlier turns and skips questions it can already answer.
- Synonyms on closed-list values also raise trigger-phrase weight (better topic triggering).
- Per topic that collects input, define: (a) entities to capture, (b) required vs optional, (c) the variable each fills, (d) disambiguation when NLU can't decide. Configure under **Settings → Entities**.
- Ref: `advanced-entities-slot-filling`, `guidance/slot-filling-best-practices`, `guidance/topic-authoring-best-practices`.

## 4.6 / 4.7. Knowledge config + sources (generative-mode limits)

| Source | Internal/External | Generative-mode notes / limit |
|---|---|---|
| Public website | External | Bing-restricted to listed sites. Up to **25**. |
| Documents (Dataverse upload) | Internal | Uploaded docs **don't count** toward the 25-source search limit. |
| SharePoint | Internal | Entra ID auth (per-user trimming). Up to **25**. |
| Dataverse | Internal | RAG over Dataverse. **Unlimited**. |
| Enterprise data via connectors | Internal | Indexed by Microsoft Search. **Unlimited**. |

- If >25 search sources are configured, the agent filters them with an internal model using each source's **description** (another reason descriptions matter).
- **Related toggles & defaults:**
  - **Web Search** (Bing grounding interleaved with public-site sources) — **default OFF** for internal agents.
  - **Allow ungrounded responses** — **default OFF** for grounded internal agents (off = block any turn that used neither knowledge nor tool → fallback fires).
  - **Turn on Work IQ semantic index** — **default: turn OFF** (ships ON; see §4.8).
- "Official source" marking isn't available with generative orchestration — out of scope.
- Ref: `knowledge-copilot-studio`, `knowledge-add-public-website`, `knowledge-add-sharepoint`, `knowledge-add-file-upload`.

## 4.8. Work IQ — disambiguation (two different features, both OFF by default)

1. **"Turn on Work IQ" semantic index** — toggle on the Generative AI settings page. Improves knowledge retrieval (esp. SharePoint). Requires an M365 Copilot license + auth = Authenticate with Microsoft. **Ships ON by default** → the builder must *explicitly disable it* (make it a checklist line). Retrieval-quality setting, **not** the Office-search tool.
2. **Work IQ MCP tools (preview)** — added on the **Tools** tab via Add tool → Model Context Protocol (Mail, Calendar, Teams…). Grounds the agent in M365 work context. **Preview**, requires M365 Copilot license, moves to **consumption billing via Copilot Credits on 2026-06-16**. This is what the draft's "search Word/PPT/Excel/Outlook, default disable, extra cost, preview" actually meant.

Default: **both off** unless deliberately chosen + documented (and the M365 Copilot licensing confirmed). The MCP one lives on the Tools tab — don't place it on Overview. Ref: `use-work-iq`, `knowledge-copilot-studio`.

## 4.9. Tools / connectors

Add as needed. Families: standard/custom connectors, **agent flows** (Power Automate-style automation invoked by/with the agent), **prompt tools** (incl. code interpreter for Python), **MCP servers**, **computer use**, **other agents** (§6). Every tool gets a clear description — in generative mode the description is how the orchestrator decides to call it. Ref: `add-tools-custom-agent`, `advanced-connectors`, `flow-agent`, `agent-extend-action-mcp`.

## 4.12. Variables & state

Distinguish **system** variables, **topic (local)** variables, and **global** variables (persist across topics). Decide what must survive topic transitions — this underpins slot filling + multi-turn context. Ref: `authoring-variables`, `authoring-using-conditions`.

## 5. Triggers (two distinct concepts — ask which apply)

- **Conversational triggers** — topic trigger phrases / intent; NLU matches utterances (even unlisted phrasings) to a topic. The everyday "how a topic starts" mechanism. Use for assistant-style agents.
- **Autonomous triggers** — **event** (push: "when a record is created / a message arrives") or **scheduled** (pull/cron: recurrence). Adding one makes the agent (partly) autonomous, which changes monitoring (you analyze **agent health**, not just conversational effectiveness). Use event triggers to react to a system change; scheduled for periodic batch work.

Ref: `authoring-triggers`, `analytics-improve-agent-health`.

## 6. Multi-agent (Agents tab)

Two ways to bring in other agents: **add a child agent** (built/owned here) or **connect to an existing** Copilot Studio agent. Use multi-agent when:
- the problem decomposes into distinct domains/skills with different knowledge or permission scopes;
- you want to reuse a specialized agent across several parents;
- an orchestrator + specialists pattern keeps each agent's instructions/tools focused (better routing, easier evals);
- you need to isolate a high-risk capability behind its own auth/governance boundary.

Avoid it when a single agent with a few tools/topics suffices (multi-agent adds routing complexity + eval surface). Ref: `authoring-add-other-agents`, `add-agent-child-agent`, `add-agent-copilot-studio-agent`.

## 4.3. Agent status review

Copilot Studio surfaces warnings/errors on the **Overview** page and the **Publish** page. Discipline: enumerate each warning verbatim, classify it (config / missing dependency / auth / unpublished-change), record the resolution. The publish-time troubleshooting checklist (verify configs → check missing dependencies → read error logs/codes) is the same discipline applied later. Ref: `publication-fundamentals-publish-channels` (Troubleshoot section).

## 4.14. Evaluations (feeds the Evaluation Plan)

- **Two eval types:** **single-response** (one unconnected question at a time — good for capability calls, exact wording, per-question quality) and **conversational** (multi-turn behavior). Choose per what you're protecting.
- **Test set:** up to **100** test cases. Build via Quick question set (auto 10), **Full question set (from Knowledge — our path, since all agents are generative)**, Use test-chat conversation, Import CSV/TXT, manual, or **Theme** (from real production analytics, preview).
- **Seven test methods:**

| Method | Scoring | Use when |
|---|---|---|
| General quality | 0–100% (relevance/groundedness/completeness/abstention) | No single expected answer; default; needs no expected answer. |
| Compare meaning | 0–100%, pass score, expected answer | Many correct phrasings but intent must come through. |
| Tool / Capability use | Pass/fail, expected capabilities | Verify the agent invoked the right tool/topic — ties evals to Tools/Topics design. |
| Keyword match | Pass/fail, any/all keywords | Specific terms must (or must not) appear. |
| Text similarity | 0–1 cosine, pass score, expected answer | Wording + meaning should be close. |
| Exact match | Pass/fail | Codes, numbers, fixed phrases. |
| Custom | Pass/fail via labels + instructions | Policy/compliance checks (e.g. HR-compliant vs not). |

- **CSV import format:** header row `Question, Expected response, Testing method`; ≤100 questions; ≤1,000 chars each. Methods accepted in file: General quality / Compare meaning / Similarity / Exact match / Keyword match. A CSV template is downloadable under **Data source** after **New evaluation**. Ship a single-turn template; document the multi-turn (conversational) path separately (conversational sets are created differently).
- **Coupling to Topics:** since all agents are generative, use **Knowledge-based** generation. Topics still act as guardrails → validate them with the **Tool / Capability use** method (assert the right topic/tool fired for a given intent). The retired classic "Topics-based generation" path no longer applies.
- Docs are prerelease/subject to change; results retained **89 days** (export to keep). Ref: `analytics-agent-evaluation-overview`, `analytics-agent-evaluation-create`, `analytics-agent-evaluation-multi-turn`, `analytics-agent-evaluation-results`.
