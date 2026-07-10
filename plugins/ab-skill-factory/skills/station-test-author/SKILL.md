---
name: station-test-author
description: Brigade station 2 of 4. Reads only the spec artifact and produces a tests artifact describing what success looks like - independent of how the code will be implemented. Domain-agnostic utility station.
---

# Station Test Author

Utility station 2 of 4 in the ab-skill-factory. Reads ONLY the spec (never sees the code that will be written) and produces a tests artifact - the success criteria the downstream code-author station must satisfy and the critic station verifies against.

## Purpose

Translate the spec into testable success criteria. The test-author's job is to prevent the rubber-stamp anti-pattern: when the same station writes spec + tests + code, tests get written to pass the code instead of measuring against ground truth. By isolating this station to see ONLY the spec (never the code), tests are forced to express "what would success look like" from the spec's perspective rather than "what does my code happen to do."

Per Zach Lloyd's (Warp) verify-then-build mermaid-to-svg case study, the canonical reference set must be generated separately from the code under test for the oracle to be uncontaminated. This station is the analog of that canonical-set generator.

## When invoked

Dispatched by the domain workflow command via Agent tool with `subagent_type: general-purpose` after `station-spec-author` returns successfully. Parameters:

- `domain` - the slug
- `spec_path` - absolute path to `<run_dir>/spec.md` written by the spec-author station
- `config_path` - absolute path to the per-domain config (YAML), supplied by the parent workflow; declares the `structural_checks` list and `critic_axes`
- `run_dir` - same per-run scratch dir as the rest of the pass
- `iteration` - integer; on iteration > 0 the station may receive critic feedback indicating tests need to be tightened or expanded

The test-author MUST NOT receive code artifacts as input parameters. Filesystem isolation per architecture doc section 3.2A - the station reads ONLY `spec_path` and (on iterations > 0) the critic feedback file. It does NOT have read access in process to the `run_dir/code/` directory; the workflow dispatch prompt explicitly excludes that path.

## Process

1. **Read the spec** at `spec_path`. Absorb every load-bearing requirement, every constraint, every tension flagged in the spec's `## Tensions` section.
2. **Read the per-domain config's `structural_checks` list** at `config_path`. These are the deterministic checks the workflow runs before any critic fires; the tests artifact MUST cover them explicitly so coverage is auditable, even though their execution is mechanical.
3. **Enumerate success conditions** for each spec requirement. Map every requirement to either:
   - A structural assertion (matches a `structural_checks` entry from the config)
   - A judgment criterion (will be evaluated by a fuzzy critic axis)
   - A reference-comparison check (compare against an exemplar in `reference_artifacts_path`)
4. **Write the tests artifact** at `run_dir/tests.md`. Use a checklist format: each success condition is a single-line testable assertion with a tag indicating which critic axis (or structural check) is responsible for verifying it.
5. **Flag spec gaps**. If the spec has requirements no axis can verify (e.g. spec says "should feel inspirational" but no `inspiration-match` axis exists in the config), surface this in a `## Coverage gaps` section. The critic will treat coverage gaps as advisory, not blocking.
6. **Return** the structured handoff line to the parent workflow.

## Reads

- `<spec_path>` - the spec artifact (this station's only direct input from upstream)
- `<config_path>` - the per-domain config, to know which structural checks and critic axes are in play
- `run_dir/critic-feedback-iter-<N-1>.md` - only on iteration > 0

The test-author NEVER reads:
- `run_dir/code/` - the code artifact directory (excluded by workflow dispatch)
- Any prior-iteration `tests.md` (fresh-write each iteration)
- Reference exemplars directly (those are for the critic, not the test-author)

## Writes

- `<run_dir>/tests.md` - the success-criteria checklist with axis tags

## Returns

```
path: <run_dir>/tests.md | summary: <N criteria across M axes> | confidence: high|medium|low
```

`confidence: low` indicates the spec had ambiguities the test-author had to guess at, or coverage gaps that the available axes can't measure. The parent workflow may surface low-confidence test runs to the founder as a check before proceeding to code-author.

## Related

- Architecture principle: tests are authored blind to the code (spec-only view) so they measure against ground truth, not against what the code happens to do. In the pipeline's RLHF framing, the tests are the labeling target the critic compares against.
- The test-harness-first discipline here follows Zach Lloyd's (Warp) verify-then-build case study: generate the canonical reference set separately from the code under test so the oracle stays uncontaminated.
- [[station-spec-author]] - upstream station
- [[station-code-author]] - downstream station (which does NOT see this station's output directly, only via the spec)
- [[station-critic]] - uses the tests artifact as the verification checklist
