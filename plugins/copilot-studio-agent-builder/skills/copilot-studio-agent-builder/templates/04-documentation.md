# Agent Documentation — `<AGENT NAME>` (per agent)

> Deliverable #4. The reference record for the built agent. Keep it current as the agent changes.

## Purpose & scope
- What the agent is for; who uses it; what's explicitly out of scope.

## Owners & sign-offs
- Business owner / maker / reviewer; sign-off dates.

## Key design decisions + rationale
Pull from the Implementation Plan (#2). Call out especially:
- **Auth mode** (and why).
- **Knowledge sources + tools** chosen (and what was deliberately excluded).
- **Work IQ OFF by default** — both the semantic index (#7) and MCP tools (#9); note any deliberate exception + its licensing.
- **Model version actually selected** (the newest Sonnet at build time) — record the exact version.
- Orchestration = generative (baseline).

## Known limitations / rough edges
- Behaviors that are weak, unsupported, or channel-specific (e.g. Teams ≤6 suggested actions, attachments generally unsupported).

## Dependencies
- Connectors, agent flows, child agents, knowledge sources, licenses (incl. M365 Copilot if any Work IQ feature is on).

## Preview-feature exposure
- List any preview features in use (e.g. Work IQ MCP, Theme-based eval generation) and the risk that they change/graduate/deprecate. Re-check at each review.

## Change log
| Date | Change | By |
|---|---|---|
| | | |
