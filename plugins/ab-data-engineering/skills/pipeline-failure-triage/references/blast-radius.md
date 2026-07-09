<!-- iteration: 0 -->
# Blast Radius: Topology Plus Timing

Read this when tracing a DAG incident (SKILL.md Step 4).

## The rule

Blast radius is topology *and* timing together, never topology alone.

**Step 1 — descendant set by graph traversal.** Compute every node reachable forward through the DAG's edges from the failed node, direct or transitive. This is the descendant set.

**Step 2 — non-descendants are safe regardless of timing.** Every node NOT in the descendant set, and not the failed node itself, is bucketed **safe — never downstream**, no matter what time it ran.

**Step 3 — bucket each descendant by scheduled/actual run time vs. containment.** For every descendant, compare its scheduled (or actual) run time against the containment timestamp:
- Scheduled BEFORE containment → it already executed on the tainted input → bucket **ran on bad data**.
- Scheduled AT OR AFTER containment → it never executed against the tainted input → bucket **safe — blocked in time**, even though it is topologically a true descendant.

**Step 4 — cross-foot.** origin + safe-never-downstream + ran-on-bad-data + safe-blocked-in-time must sum to the DAG's total node count. If it doesn't, a node was mis-bucketed or missed.

## The four buckets

1. **Origin** — the failed node itself.
2. **Ran on bad data** — a true descendant whose scheduled/actual run fell before containment.
3. **Safe — never downstream** — not a descendant of the failed node at all, regardless of timing.
4. **Safe — blocked in time** — a true descendant whose scheduled/actual run fell at or after containment.

## Two traps to guard explicitly

**The co-parent trap.** A node that merely CO-PARENTS a tainted node (shares an unrelated, independently-clean upstream lineage that happens to join against the tainted node downstream) is not itself tainted. It is the join/merge node that consumes both parents that becomes tainted, not the clean parent. Example: node X feeds both node Y (tainted) and, together with an independently-clean node Z, into node Y's join — node Z's own output was never touched by the failure. Tainting a clean co-parent by association is bucketing by proximity in the graph rather than by actual data flow.

**The detecting-node trap.** The node whose own scheduled run is what SURFACED the incident (a dashboard going to $0, say) is not automatically "caught in time" merely for having raised the alarm. If its own scheduled run fell before the containment timestamp, it already ran on bad data — detecting the problem and having been protected from it are two different things. Bucket the detecting node by its own scheduled-time-vs-containment comparison exactly like every other node; do not give it a free pass for being the one that surfaced the issue.

## Kills

- Bucketing every topological descendant into "ran on bad data" by graph distance alone, ignoring containment timing.
- Tainting a clean co-parent by association.
- Treating the detecting node as automatically safe.
