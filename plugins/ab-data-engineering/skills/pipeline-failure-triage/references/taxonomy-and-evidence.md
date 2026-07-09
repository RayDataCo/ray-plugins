<!-- iteration: 0 -->
# Taxonomy and Evidence Ladder

Read this when classifying a pipeline failure (SKILL.md Steps 2-3).

## The evidence ladder — work in strict order, never stop at an early clean rung

**Rung 1 — Logs.** Read the failed/suspect run's own log output. Many classes (explicit auth error, explicit resource-exhaustion trace, explicit cast failure naming a column) are identifiable here alone.

**Rung 2 — Run-history diff.** Compare this run's row counts, duration, and resource usage against its own historical baseline (recent successful runs, a rolling average, the same weekday in prior weeks). This is the ONLY rung that surfaces volume anomalies, which produce zero signal on rung 1.

**Rung 3 — Data diff.** When the job succeeded, volume looks normal, and logs are clean, but a downstream number still looks wrong, diff the actual data content (value distributions, categorical domains, row samples) against a prior known-good snapshot. This is the ONLY rung that surfaces semantic drift, which is defined precisely by producing no signal on rungs 1-2.

**Rung 4 — Recent deploys.** Cross-reference the failure's onset timestamp against the pipeline's OWN change history (code commits, config changes, orchestration edits) and, separately, against any known upstream/connector operational-trigger history (a vendor changelog, another team's deploy log, a connector's own manually-triggered-resync log). This is not "any operational action anywhere in the company" — it is specifically the pipeline's own change history plus explicitly-checked upstream-change history.

Work all four rungs in order when the failure isn't already identified by an earlier one. Never conclude "nothing is wrong" or "must have been a blip" from a clean rung 1 or rung 2 alone. Kills: stopping at logs and missing a volume anomaly or semantic drift entirely; defaulting to "it's probably transient" on any anomaly without an error message.

## The seven classes, by discriminating signature

Classify by the DISCRIMINATING SIGNATURE, never by narrative feel or which explanation is most familiar/blameless.

### Source schema drift
Fails AFTER a successful connection/read, during parsing/casting/column reference (an "invalid identifier," "column not found," cast-failure naming a field). Corroborated by the source's own schema/changelog. Row counts normal.

### Credential/permission expiry
Fails BEFORE any row is read, at connection/auth, with an explicit auth-flavored error (session expired, access denied, 401/403). Recurs on EVERY subsequent run until rotated — does NOT self-resolve on a bare retry the way transient does.

### Volume anomaly
Job status SUCCESS, runtime normal, no error anywhere — but row count is a hard floor violation (near-zero) or a ceiling-violation multiple of baseline (commonly ~10x). Visible ONLY via rung-2 comparison, never from the log alone.

### Semantic drift
Schema/columns/types unchanged, all schema tests green, row counts and runtime normal — but the MEANING of a value changed (a new legitimate categorical value, a silent unit/currency change, a redefined status). Visible ONLY via rung-3 content diff, usually triggered by a downstream business metric looking wrong.

### Infra/transient
An explicit resource-exhaustion/network-reset/throttling error, tied to no specific data condition or code change, that resolves IDENTICALLY on a bare retry with ZERO code/config/data change, correlating with a load/concurrency spike rather than a deploy or a particular input.

### Logic regression from a deploy
The failure's onset lines up with a specific commit/deploy in the pipeline's OWN change history, and reverting that specific change resolves the failure.

### Upstream dependency delay
NOT a defect in the job under investigation at all — a dependency-sensor timeout or an upstream job's own late-completion history, with no anomaly in the downstream job's own code/logic. The anti-pattern version is silently falling back to stale/partial data instead of correctly blocking.

## Discriminator traps to guard

- **Volume anomaly vs. infra/transient**: a silently-empty or 10x-inflated load with SUCCESS status and normal runtime has no resource-exhaustion signature and does not resolve on bare retry — it is volume anomaly, not infra/transient, no matter how much a system hiccup "feels" like the more familiar, blameless story.
- **Semantic drift vs. schema drift**: schema drift is a structural change to columns or types, discriminated by a failure that surfaces *after* a successful connection and read, during parsing or casting. Semantic drift leaves schema, types, and every schema test green — the meaning of an unchanged column's values shifts underneath a business-logic assumption written before the shift happened, visible only via a content/value-distribution diff, never from logs or row counts.
- **"Recent deploys" scope**: rung 4 means the pipeline's own change history plus, separately, any known upstream/connector operational-trigger history — never any company-wide operational action collapsed loosely into "a deploy happened." A manually triggered resync of an ingestion connector against the wrong target is a relevant deploy-adjacent event on that connector's own operational log, even though it never shows up in the transformation repo's git log; conflating "a person did something" with "our pipeline's own code changed" misclassifies a volume-anomaly incident as a logic regression.
- **Credential/permission expiry vs. schema drift**: both sound "connection-ish," but the discriminator is *where in execution* the failure lands — credential expiry fires before any row is read, with an explicit auth-flavored error, and recurs on every subsequent run until the credential is rotated (it does not self-resolve on a bare retry the way infra/transient does); schema drift fires only after a successful connection and read, during parsing or column reference.
