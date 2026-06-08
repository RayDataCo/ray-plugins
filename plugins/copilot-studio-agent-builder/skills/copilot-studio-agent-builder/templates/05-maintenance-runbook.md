# Agent Maintenance Runbook — `<AGENT NAME>` (per agent)

> Deliverable #5. How to keep the agent healthy, current, and on-budget after launch.

## Monitoring
- **Which analytics surface:** conversational **effectiveness** for assistant-style agents; **agent health** for agents with autonomous (event/scheduled) triggers.
- Track knowledge-source use and **themes** (recurring real-usage clusters) to spot gaps.
- Ref: `analytics-summary`, `analytics-improve-agent-effectiveness`, `analytics-improve-agent-health`, `analytics-themes`.

## Evaluation cadence & regression policy
- Run the eval suite (deliverable #3) on schedule and before/after any material change.
- Define the regression bar (which pass-thresholds must hold to ship a change).
- Export results before the **89-day** retention window drops them.

## Knowledge refresh
- Schedule for re-crawling/re-uploading sources; owner; how staleness is detected.

## Model / version review
- Periodically check whether a newer Claude Sonnet is offered in the picker; decide whether to move; re-run evals after any model change.

## Cost watch
- Monitor Copilot Credits / Work IQ consumption (consumption billing from **2026-06-16**). Flag if any Work IQ feature was enabled.

## Preview-feature watch
- For each preview feature in use: has it graduated to GA, changed billing, or been deprecated? Adjust accordingly.

## Incident handling
- Triage path for "agent gives wrong/ungrounded answers", auth failures, broken connectors/flows. Use the status-review discipline (enumerate warning → classify → resolve).

## Re-publish procedure
- After ANY change: **Publish** in-environment (new content reaches users only on a new session). For prod, follow the ALM promotion path (managed-solution export/import). **[OPEN]** confirm the ALM path.

## Access review
- Cadence for reviewing who can use/edit the agent (security roles, sharing, auth mode), and DLP policy drift.
