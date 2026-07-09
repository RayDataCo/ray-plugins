---
name: station-code-author
description: Brigade station 3 of 4. Reads the spec and tests artifacts and produces the actual artifact under build (code, markdown, structured doc, etc.) in the per-run scratch dir. Domain-agnostic utility station.
---

# Station Code Author

Utility station 3 of 4 in the ab-skill-factory. Reads the spec and the tests, then writes the actual artifact under build (which despite the station name may be code, markdown, a structured doc, a config file, etc. - the term "code" follows the founder's brigade-architecture naming and means "the thing being built").

## Purpose

Produce the artifact specified by the spec, conforming to the success criteria in the tests. Per the architecture doc's rubber-stamp-prevention principle, this station sees ONLY the spec and the tests - it never sees the canonical reference exemplars directly (those are the critic's job) and it never sees prior-iteration code (each iteration is a fresh-write so the station cannot incrementally smooth over flaws that would otherwise be visible to the critic).

## When invoked

Dispatched by the domain workflow command via Agent tool with `subagent_type: general-purpose` after both `station-spec-author` and `station-test-author` have returned. Parameters:

- `domain` - the slug
- `spec_path` - absolute path to `<run_dir>/spec.md`
- `tests_path` - absolute path to `<run_dir>/tests.md`
- `run_dir` - per-run scratch dir
- `iteration` - integer; on iteration > 0 the station receives the critic's diagnostic so it knows which axes failed last time

The code-author MUST NOT receive `canonical_set_path` or `reference_artifacts_path` as input. Reference exemplars are a critic-only resource; if the code-author saw them, the station would over-fit to those specific exemplars rather than satisfying the spec. Filesystem isolation per architecture doc section 3.2A.

## Process

1. **Read the spec** at `spec_path`. Internalize every requirement and tension.
2. **Read the tests** at `tests_path`. Each test is a success condition; the code MUST satisfy every one.
3. **Read prior critic feedback** at `run_dir/critic-feedback-iter-<N-1>.md` if iteration > 0. The feedback names which axes failed and why; the re-write addresses those specifically without abandoning the parts of the spec the prior iteration handled correctly.
4. **Plan briefly** in a `## Plan` scratch section internal to the station's reasoning. Do not write this scratch to disk; it is for the station's own decomposition.
5. **Write the artifact** to `run_dir/code/` (or the per-domain config's override path). Multiple files are allowed - structure them per the spec's expected-artifacts list. Every file MUST have a header comment or frontmatter naming `iteration: <N>` so audit trails are clean.
6. **Self-check against the tests checklist**. Walk down the list, mark mentally which conditions the current artifact satisfies. If any condition is clearly unmet, fix in-place before returning - the critic will catch it anyway and burn an iteration unnecessarily.
7. **Return** the structured handoff line.

## Reads

- `<spec_path>` - the spec
- `<tests_path>` - the success-criteria checklist
- `run_dir/critic-feedback-iter-<N-1>.md` - on iteration > 0

The code-author NEVER reads:
- The canonical reference set or `reference_artifacts_path`
- Prior-iteration `code/` directories (each iteration is a fresh-write; the only persistent state across iterations is the critic feedback)
- The per-domain config directly (the structural_checks and critic_axes are reflected in the tests artifact; the code-author works against the tests, not the config)

## Writes

- `<run_dir>/code/` - one or more artifact files, per the spec's expected-artifacts list

## Returns

```
path: <run_dir>/code/ | summary: <one-line description of what was built> | confidence: high|medium|low
```

`confidence: low` indicates the station had to make tradeoffs between conflicting test criteria, or the spec was ambiguous on a load-bearing point. The parent workflow surfaces low-confidence builds to the critic with the confidence flag attached so the critic knows to weigh those iterations more carefully.

## Related

- [[../../rdco-vault/01-projects/skill-pipelines/2026-05-12-multi-agent-pipeline-architecture]] - architecture doc
- [[../../rdco-vault/02-sops/2026-05-12-multi-agent-pipeline-config-schema]] - schemas
- [[../../rdco-vault/06-reference/concepts/2026-05-12-rdco-pipeline-rlhf-shaped]] - RLHF framing; this station is the "policy" in the RLHF mapping that gets iterated by critic feedback
- [[station-spec-author]] - upstream
- [[station-test-author]] - upstream
- [[station-critic]] - downstream
