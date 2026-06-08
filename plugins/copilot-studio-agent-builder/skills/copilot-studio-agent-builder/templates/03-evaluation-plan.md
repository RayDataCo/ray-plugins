# Agent Evaluation Plan — `<AGENT NAME>` (per agent)

> Deliverable #3. Driven by §4.14. Evals must **mirror the Topics/intents** in the Implementation Plan (#2). All agents are generative → use **Knowledge-based** test-case generation; validate Topics via the **Tool / Capability use** method.

## 1. In-scope intents / topics
List every intent/topic the agent must handle (mirror deliverable #2, field 13). For each, name what behavior the eval protects.

| Intent / Topic | What it must do | Test-set type (single-response / conversational) | Method(s) + pass threshold |
|---|---|---|---|
| | | | |

## 2. Method selection (pick per what you're protecting)
| Method | Scoring | Use when |
|---|---|---|
| General quality | 0–100% (relevance/groundedness/completeness/abstention) | No single expected answer; default. |
| Compare meaning | 0–100%, pass score, expected answer | Many correct phrasings, intent must come through. |
| Tool / Capability use | Pass/fail, expected capabilities | Verify the right tool/topic fired — couples evals to Topics. |
| Keyword match | Pass/fail, any/all keywords | Specific terms must (or must not) appear. |
| Text similarity | 0–1 cosine, pass score, expected answer | Wording + meaning should be close. |
| Exact match | Pass/fail | Codes, numbers, fixed phrases. |
| Custom | Pass/fail via labels + instructions | Policy/compliance checks. |

## 3. Test-case inventory
- Up to **100** test cases. Generation: **Full question set from Knowledge** (our path). Optionally seed from test-chat, import, or Theme (preview, from production analytics).
- **CSV import format** (single-turn) — header row exactly:
  ```
  Question, Expected response, Testing method
  ```
  ≤100 questions; ≤1,000 chars each. File-accepted methods: General quality / Compare meaning / Similarity / Exact match / Keyword match. (Download the CSV template under **Data source** after **New evaluation**.)
- **Multi-turn (conversational)** test sets are created differently — document that path separately; don't try to express it in the single-turn CSV.

## 4. Topic/guardrail validation
For each Topic that must deterministically fire, add a **Tool / Capability use** test asserting the correct topic/tool was invoked for the intent. This is how Topics stay aligned with Evals without the retired classic "Topics-based generation" path.

## 5. Operations
- Evaluation account / auth: ____________
- Cadence + owner: ____________
- **Results retention = 89 days** → export policy: ____________
- Note: evaluation docs are prerelease/subject to change — re-verify at build time.

Ref: `analytics-agent-evaluation-overview`, `analytics-agent-evaluation-create`, `analytics-agent-evaluation-multi-turn`, `analytics-agent-evaluation-results`.
