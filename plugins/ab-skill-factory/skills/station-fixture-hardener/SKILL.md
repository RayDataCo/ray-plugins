---
name: station-fixture-hardener
description: Harden a set of eval fixtures whose base-model pass rate is at ceiling (non-discriminating - proves nothing about the skill under test) into fixtures landing in the ~30-70% discriminating band at the stated deployment tier, preserving known-answer derivability (every solution re-derived twice) and grading determinism (fixed fields, tolerances wider than legitimate rounding drift, pinned sign conventions, stated-rule judgment option lists). Applies trap fingerprints, messier inputs, dependency chains, distractor data, realistic volume, and weaker-tier-arm recommendations - never ambiguity, trivia, or prompt leakage. Use after execution-eval-station returns inconclusive (expo-routed), or fire directly on a fixture set with eval results in hand. Do NOT use to author acceptance contracts (station-test-author), to measure lift (execution-eval-station), to harden without eval results attached, or to touch win-class fixtures (working measurements) or regression-class fixtures (skill defect - refire-to-author).
---

# Station Fixture Hardener

Eval-engineering utility station in the ab-skill-factory `add-station` family. Given (a) a
fixture set in the execution-eval oracle schema and (b) that same set's execution-eval RESULTS
(per-fixture base/skill pass rates + classes), this station rewrites every **non-discriminating**
fixture (base already at or near ceiling — proves nothing about the skill under test) into a
**hardened** fixture that lands in the **30-70% base-model pass-rate band** at the stated
deployment tier, without breaking two invariants:

- **known-answer derivability** — every hardened fixture's solution is re-derived twice,
  independently, and is script-verifiable.
- **grading determinism** — fixed output fields, tolerances wider than the fixture's own
  legitimate rounding-path drift, sign conventions pinned in both the field description and the
  prompt, judgment answers as fixed option lists tied to a rule stated in the prompt.

It applies only the seven named levers (`references/hardening-levers.md`) and never hardens by
ambiguity, trivia, or prompt leakage. It does not invent new fixtures, does not touch fixtures
that already discriminate (`win`), and does not "fix" `regression` fixtures — that is an author
defect, routed to `refire-to-author`, not a fixture problem.

## When invoked

Three trigger cases:

1. The expo runs execution-eval-station on a fixture set and gets back `inconclusive (fixtures
   don't discriminate)` — every fixture `non-discriminating`. Primary, pipeline-driven trigger.
2. A human or another station directly fires "harden this fixture set" for a set with known eval
   results already in hand.
3. A re-hardening pass (`iteration > 0`): a prior hardening attempt was re-run through
   execution-eval-station and STILL came back non-discriminating for one or more fixtures.

Parameters:

- `fixtures_path` - absolute path to the fixture set file (execution-eval-station's oracle-set
  schema; see Input schemas below).
- `eval_results` - path or reference to the eval results rows for this skill (same schema family
  as `cellar/brigade-runs/EVAL-RESULTS-*.json`'s `rows` array), filtered to the target skill +
  tier.
- `deployment_tier` - the tier the results were measured at; the 30-70% band target applies at
  THIS tier (e.g. `sonnet`).
- `run_dir` - per-run scratch dir for the hardened fixtures file, hardening log, and
  (conditionally) the tier-arm recommendation.
- `iteration` - integer; on `iteration > 0` a prior hardening attempt was re-run through
  execution-eval-station and STILL came back non-discriminating — read the prior hardening log
  and select a different/additional lever combination rather than repeating what already failed.

## When NOT to use

Five hard carve-outs — a triggering-precision failure if any of these fire here instead of at
their real owner:

- **Authoring a skill's acceptance contract from a spec** → `station-test-author`. This station
  never touches a spec and never creates a new oracle set from scratch; it hardens an EXISTING
  one with measured results already in hand.
- **Measuring lift or producing per-fixture classes** → `execution-eval-station`. This station is
  a *consumer* of `non-discriminating`/`flat`/`win`/`regression` classes, never a producer. It
  does not run two-arm ablations, does not grade, does not compute lift.
- **A generic "make this harder" request with no eval results attached** → route to
  `execution-eval-station` first. Hardening must be grounded in an actual measured classification,
  not a guess that a fixture is probably too easy.
- **Fixing a `regression`-class fixture** → route to `refire-to-author`. The fixture isn't the
  defect; the skill's authored behavior is.
- **Fixing a `win`-class fixture** → leave it alone. It already discriminates; touching it risks
  breaking a working measurement for no gain.

## Input schemas

`fixtures_path` — execution-eval-station's oracle-set schema:

```json
{
  "skill": "<skill-name>",
  "type": "computational | generative | ...",
  "fixtures": [
    {
      "id": "A",
      "prompt": "<full fixture prompt text, incl. the named output fields the model must answer>",
      "fields": {
        "<field_name>": {
          "expected": "<value>",
          "type": "number | ...",
          "tolerance": "<number>",
          "description": "<definition, incl. sign convention when relevant>"
        }
      },
      "traps": [
        { "field": "<field_name>", "must_not_equal": "<value>", "why": "<the lazy method this catches>" }
      ]
    }
  ]
}
```

`eval_results` — per-fixture rows for the target skill + tier:

```json
{
  "skill": "<skill-name>", "fixture": "A", "tier": "sonnet",
  "base": 1.0, "withSkill": 1.0, "lift": 0,
  "class": "non-discriminating | win | flat | regression",
  "baseFail": ["<field>: got <val>, want <val>±<tol> | ..."],
  "skillFail": ["..."]
}
```

## Process

1. **Read the fixture set and its eval results; scope to the non-discriminating class.** Filter
   to fixtures whose `class` is `non-discriminating` (base pass rate at or near ceiling — no
   headroom, no signal). `flat` fixtures enter scope ONLY if the invoking party explicitly asks
   for them (they had headroom and the skill still didn't lift them — that may be a real skill
   gap, not a fixture problem; hardening a `flat` fixture without that explicit ask risks papering
   over a genuine miss). `win` and `regression` fixtures are OUT OF SCOPE — a `win` fixture
   already discriminates; a `regression` fixture's problem is the skill's authored behavior, not
   the fixture, and hardening it would mask an author defect instead of surfacing it for
   `refire-to-author`.
2. **Diagnose why each non-discriminating fixture is at ceiling.** Read the fixture's `baseFail`
   evidence (empty, since it passed) alongside its prompt and fields: is the input table too
   clean? Single-formula/single-step? Missing a distractor the lazy method would grab? A judgment
   call resolvable by taste rather than a stated rule? Name the specific ceiling cause before
   picking levers — undiagnosed hardening produces diffuse difficulty, not a diagnostic trap.
3. **Select 2+ levers matched to the diagnosis, from the fixed set of seven** — trap fingerprints,
   messier inputs, multi-step dependency chains, distractor data, judgment-as-multiple-choice with
   a defensible key, realistic volume, weaker-tier arms. Full definitions and a worked before/after
   example live in `references/hardening-levers.md` — read it before selecting; do not improvise
   new lever types. Select levers deliberately, tied to Step 2's diagnosis — not all seven on
   every fixture.
4. **Rewrite the fixture with the selected levers, in the SAME schema.** Same field names, same
   `fields`/`traps` shape — the output must be a drop-in replacement in execution-eval-station's
   fixture consumption. Never remove a field the original graded; add fields only as the levers
   require (e.g., a distractor line the question does NOT ask about).
5. **Re-derive the full solution TWICE, independently, and show both.** Direct computation AND an
   independent cross-foot (a second, different path to the same numbers — e.g., built up from line
   items vs. built down from a total). If the two derivations disagree, the fixture is broken, not
   hard — return to Step 4. This is the known-answer-derivability invariant; it is non-negotiable,
   and both derivations must be visible in the hardening log so the critic can verify they
   reconcile.
6. **Pin grading determinism on every field.** For each `fields` entry: keep a fixed field name,
   no free-form prose fields; set `tolerance` **wider than the fixture's own legitimate
   rounding-path drift** — compute what that drift actually is from the two Step-5 derivations,
   never guess a round number; state the sign convention explicitly in `description` AND make sure
   the fixture's own `prompt` text states the same convention whenever the field could be read
   either way. For any judgment field, the key MUST be one of a fixed option list, and the prompt
   MUST state the rule the key is derived from — never taste, never an unstated external
   convention.
7. **Write the trap block with predicted wrong values.** For every lever-1 (trap fingerprint)
   applied, add a `traps` entry: `{field, must_not_equal, why}` naming the EXACT wrong value the
   diagnosed lazy method would produce — not a vague "might get this wrong." This becomes
   execution-eval-station's must-not-appear assertion on re-run. The trap and its `why` must
   NEVER appear in the fixture's own `prompt` text — warnings belong in the skill under test, not
   the fixture; leaking one here is the prompt-leakage anti-pattern (Step 10).
8. **When the whole set stays at-ceiling even after hardening headroom is diagnosed as
   unavailable at the stated tier, emit a weaker-tier-arm recommendation** naming the next tier
   down and the specific fixture(s) worth running there, with rationale. This fires ONLY on that
   diagnosed condition — never as a default or fallback action — and is a DISTINCT output (Section
   below), never folded into the fixture rewrite itself.
9. **Assemble the hardened fixtures file.** Same top-level schema as the input (`{skill, type,
   fixtures: [...]}`); non-discriminating fixtures replaced with their hardened versions,
   `win`/`regression` fixtures passed through byte-for-byte unchanged (never touched), and any
   in-scope `flat` fixtures hardened only if Step 1's explicit-ask condition was met.
10. **Self-check against the anti-patterns before returning — reject and redo any fixture where:**
    (a) **ambiguity** — two readings of the question are both defensible (measures luck, not
    difficulty); (b) **trivia** — the added difficulty is an obscure convention no practitioner
    would know (measures memorization); (c) **prompt leakage** — the prompt contains a
    warning/hint about the trap (undermines the measurement of the skill under test); (d)
    **fabrication** — an expected value was asserted without both Step-5 derivations shown. This
    is a gate, not a checklist to note and move past — a fixture that fails any of the four goes
    back to Step 4.
11. **Write the per-fixture hardening log entry and return the structured handoff.** One entry
    per touched fixture (Writes section below); then return the Returns line.

## Reads

- `<fixtures_path>` - the fixture set (Input schemas above).
- `<eval_results>` - the eval results rows for this skill + tier (Input schemas above).
- On `iteration > 0`: the prior iteration's hardening log (the invoking party's `run_dir`
  convention determines the exact path — e.g. `run_dir/hardening-log.md` from the previous pass,
  or a versioned `run_dir/hardening-log-iter-<N-1>.md` if the parent workflow keeps per-iteration
  history) — read it to see which lever combination was already tried and pick a
  different/additional one this pass.

The station never reads a domain pipeline config directly for this build — no
`station-fixture-hardener.yaml` exists in the config directory at time of authoring; its
structural checks and critic-axis roster are reflected in this build's own `tests.md` instead.

## Writes

1. **Hardened fixtures file** — `run_dir/hardened-fixtures.json` (or the invoking party's
   documented override path). Schema-compatible drop-in for the input: exact same
   `{skill, type, fixtures: [{id, prompt, fields, traps}]}` shape, no renamed or dropped fields.
   `win`/`regression` fixtures are byte-identical to the input.
2. **Per-fixture hardening log** — `run_dir/hardening-log.md`. One entry per touched fixture,
   containing: which lever(s) were applied and why (tied to the Step-2 diagnosis, not generic),
   the predicted trap value(s), both Step-5 derivations shown in full, and a before/after summary
   of what changed. The log states the PREDICTED discriminating-band outcome per hardened fixture
   ("predicted to land in the 30-70% band at `<tier>`") — it never claims a measured pass rate;
   that number only exists after execution-eval-station re-runs the hardened set.
3. **Tier-arm recommendation** — inline in the hardening log, or a distinct
   `run_dir/tier-arm-recommendation.md` when non-empty. Present ONLY when Step 8 fired: names the
   recommended tier and which fixture(s) to re-run there, with rationale. Absent entirely (not an
   empty stub) when every fixture found headroom at the stated deployment tier.

## Returns

```
path: <run_dir>/hardened-fixtures.json | summary: <N> non-discriminating fixture(s) hardened via <levers used>; tier-arm: present|absent | confidence: high|medium|low
```

`confidence: low` indicates a ceiling diagnosis (Step 2) was ambiguous between two plausible
causes, or a selected lever combination's effect on headroom can't be confirmed without the live
execution-eval-station re-run. The parent workflow attaches the confidence flag when routing the
hardened set to that re-run so a low-confidence pass gets closer scrutiny if it comes back
non-discriminating again.

## Related

- `../station-test-author/SKILL.md` - authors the acceptance contract this station never touches.
- `../execution-eval-station/SKILL.md` - upstream producer of the classes this station consumes;
  downstream consumer of this station's hardened fixtures on re-run (the `inconclusive` verdict
  that routes here, and the eventual measured-band confirmation, both live there).
- `references/hardening-levers.md` - the seven-lever catalog and worked example, lazy-loaded from
  Process Step 3.

Lever catalog and worked example adapted from house eval-engineering competency knowledge into
this skill's own packaged copy (see `references/hardening-levers.md` for provenance note) so the
skill does not depend on any cellar path resolving at runtime on another install.
