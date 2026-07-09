---
name: station-spec-author
description: Brigade station 1 of 4. Reads a founder ask plus the domain spec template and produces a build spec artifact in the per-run scratch dir. Domain-agnostic utility station for the ab-skill-factory.
---

# Station Spec Author

Utility station 1 of 4 in the ab-skill-factory. This station translates a founder ask (the input) plus the domain's spec template (the structure) into a concrete build spec the downstream test-author and code-author stations consume.

## Purpose

Read the founder's natural-language ask for a new artifact (a haiku, a website-discovery brief, a MAC matrix row, etc.) plus the domain's spec template, and produce a structured `spec.md` artifact that names every load-bearing requirement the artifact must satisfy. The spec is the contract the test-author writes tests against and the code-author writes code against. Per the architecture doc, this station exists separately from test-author and code-author so neither downstream station can rubber-stamp its own work - the spec author has no visibility into how tests or code will be written.

## When invoked

Dispatched by a domain workflow command (e.g. `/build-haiku-generator`, `/build-website-discovery`) via the Agent tool with `subagent_type: general-purpose` and a prompt that names this skill and supplies:

- `domain` - the slug (e.g. `haiku-generator`)
- `founder_ask` - the raw input (topic, brief, constraint)
- `spec_template_path` - absolute path to the markdown template at `~/rdco-vault/01-projects/skill-pipelines/templates/<domain>-spec.md` (or per-domain override from config)
- `run_dir` - absolute path to the per-run scratch dir at `~/rdco-vault/01-projects/skill-pipelines/runs/<domain>-<timestamp>/`
- `iteration` - integer; on iteration 0 this is a fresh spec, on iteration N > 0 the station receives critic feedback and refines the spec

Per architecture doc section 3.1A, dispatch is one parallel-call-able Agent subagent per station, NOT inline Skill chaining. The spec author sees ONLY the founder ask and the template - it never sees test artifacts, code artifacts, or critic diagnostics from prior iterations except as scoped to spec-refinement guidance.

## Process

1. **Read the spec template** at `spec_template_path`. The template lists required spec fields for this domain (constraint shape, success criteria, structural axes, judgment axes, expected artifacts).
2. **Read the founder ask**. If iteration > 0, also read `run_dir/critic-feedback-iter-<N-1>.md` to absorb the diagnostic that triggered the re-spec.
3. **Fill out the template** by translating the ask into the template's structure. Be specific - "a haiku about snow" becomes a spec that names the topic constraint, the 5-7-5 syllable constraint, the image-coherence requirement, and the novelty target. Resist generalizing into a meta-spec; the downstream stations need concrete success conditions.
4. **Sanity-check the spec** for internal consistency. Conflicting requirements (e.g. "concise" + "exhaustive") get flagged in a `## Tensions` section so the test-author can see them rather than silently inheriting the contradiction.
5. **Write the spec** to `run_dir/spec.md`. Frontmatter MUST include `iteration: <N>`, `domain: <slug>`, `parent_workflow: <workflow-skill-name>`. Body uses the headings the template specifies.
6. **Return** the structured handoff line (see "Returns" below) to the parent workflow.

## Spec constraints the downstream isolation imposes (added 2026-07-08, two live incidents)

The code-author station is PERMANENTLY isolated from canonical sources and reference
artifacts (anti-rubber-stamp, architecture doc 3.2A). Two spec-authoring rules follow:

1. **Embed, never reference-verbatim.** If the spec requires content to appear
   "verbatim from" a source (oracle fixtures, exemplar text, canonical tables), the
   spec MUST embed that content in the spec body itself — the spec is the one artifact
   the code-author CAN read. A "carry forward verbatim from the cellar source"
   instruction is architecturally unsatisfiable and forces the author to fabricate a
   parallel version (live incident: sop-authoring reroute-to-spec, 2026-07-08; earlier
   advance-with-flag: annual-budget-build DF-1). If embedding is inappropriate, restate
   the requirement as faithful-in-structure (named traps/sections present) — never
   verbatim.
2. **Respect the deterministic lint gates at spec time.** Any trigger-description
   content the spec proposes must fit the 1,024-char description ceiling and be
   YAML-safe (prose colons require a quoted scalar). Oversized or colon-broken spec
   drafts cascade into hard lint FAILs at the critic (live incidents: sop-authoring
   spec draft at 2,482 chars; root-cause-analysis bare-colon escalate, both 2026-07-08).

## Reads

- `<spec_template_path>` - the domain's spec template (markdown with section scaffolding)
- The founder ask (passed as input parameter, not a file)
- `run_dir/critic-feedback-iter-<N-1>.md` - only on iteration > 0, contains the critic's diagnostic from the prior failed iteration

The spec author NEVER reads:
- Tests from the test-author station (would defeat the rubber-stamp prevention)
- Code from the code-author station
- Prior-iteration spec artifacts (it produces a fresh spec each iteration; the critic feedback is the only persistent state)

## Writes

- `<run_dir>/spec.md` - the structured spec artifact

## Returns

Structured one-line return to the parent workflow command:

```
path: <run_dir>/spec.md | summary: <one-line description of what was specced> | confidence: high|medium|low
```

`confidence: low` signals the founder ask was ambiguous and the spec required guessing; the parent workflow MAY surface this to the founder as a clarifying question before continuing to the test-author station.

## Related

- [[../../rdco-vault/01-projects/skill-pipelines/2026-05-12-multi-agent-pipeline-architecture]] - the architecture doc that defines this station's role
- [[../../rdco-vault/02-sops/2026-05-12-multi-agent-pipeline-config-schema]] - the schemas this station reads from
- [[../../rdco-vault/06-reference/concepts/2026-05-12-rdco-pipeline-rlhf-shaped]] - the RLHF-topology framing; this station is part of the "policy" in the RLHF mapping
- [[station-test-author]] - downstream station consuming this station's output
- [[station-code-author]] - further downstream station
- [[station-critic]] - the critic that evaluates the final artifact against the spec
