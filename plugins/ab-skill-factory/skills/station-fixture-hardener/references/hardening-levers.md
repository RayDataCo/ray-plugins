# Hardening levers — reference catalog

<!--
Provenance note (non-load-bearing): this catalog is adapted from house eval-engineering
competency knowledge on fixture hardening. It is copied and expanded into this skill's own
packaged copy specifically so the skill functions standalone on any install — it does not read
or depend on any cellar path resolving at runtime. The worked example below is a self-contained
illustrative rebuild, not a live read of any specific fixture file.
-->

Seven levers, fixed set — do not improvise new lever types. `station-fixture-hardener`'s Process
Step 3 selects 2+ of these per fixture, matched to the Step-2 ceiling diagnosis. Not every lever
applies to every fixture; picking levers that don't address the diagnosed ceiling cause produces
diffuse difficulty (harder in general) rather than a diagnostic trap (harder for the specific
lazy method the skill under test is supposed to avoid).

## The seven levers

**1. Trap fingerprints**
A *named* failure mode with a *predicted* wrong value. Grading asserts the trap value must not
appear in the model's answer (`traps[].must_not_equal`). The trap must correspond to a real,
diagnosable lazy method (Step 2) — not an arbitrary wrong number. Use when the ceiling cause is
"the model has no easy wrong path to fall into," i.e. the original fixture doesn't punish a
specific bad shortcut.

**2. Messier inputs**
Mixed units, an irrelevant column, a footnote that modifies a headline number, inputs split
across two locations that must be joined, a stated policy the data partially violates. Use when
the ceiling cause is "the input table is too clean" — nothing forces the model to actually read
carefully rather than pattern-match the obvious number.

**3. Multi-step dependency chains**
Chain 2-3 dependent computations where step 2 consumes step 1's output, and grade the chain's
END (the final field), not the intermediate values. Use when the ceiling cause is
"single-formula, single-step" — there's no opportunity for an error to compound or for a shortcut
to skip a required intermediate step.

**4. Distractor data**
A value that pattern-matches to the wrong method — the input the lazy method would grab instead
of the correct one (e.g. a prior-period actual that looks like it could be this period's base).
Use when the ceiling cause is "no distractor the lazy method would grab" — the model has nothing
tempting it away from the correct path.

**5. Judgment-as-multiple-choice with a defensible key**
The key must be derivable from a rule STATED in the fixture's own prompt — never from taste,
never from an external convention the prompt doesn't state. Use when the ceiling cause is "a
judgment call resolvable by taste rather than a stated rule" — without a stated rule, two graders
(or two models) could defensibly disagree, which is ambiguity, not difficulty (Step 10 anti-
pattern), so this lever is only safe to apply together with an explicit rule written into the
prompt.

**6. Realistic volume**
More line items, degrading attention-dependent accuracy without changing the method. Use when the
ceiling cause is a model correctly executing a short/small version of the task every time and the
skill under test is meant to hold up at realistic scale — this lever tests durability of the
method under load, not knowledge of a harder method.

**7. Weaker-tier arms**
When hardening can't move the stated deployment tier off ceiling (i.e. even a maximally-hardened
version of the fixture is still trivial for that tier), recommend running the fixture at the next
tier down instead. This is not a fixture edit — it's a distinct recommendation (Process Step 8 /
SKILL.md Writes item 3) naming the weaker tier and which fixture(s) belong there, because a
tier-floor lift is real product value even when the deployment tier itself is at ceiling.

## Worked example: seasonal-index revenue forecast

Illustrative only — this shape generalizes; the procedure does not depend on this specific
fixture. (Loosely inspired by the shape of a real non-discriminating rolling-forecast-update
fixture observed in house eval work: a single seasonal-index re-forecast with one clean growth
factor, no distractor lines, no footnote, no chained bridge — exactly the "before" shape below.)

### Before (non-discriminating, base pass rate 1.0)

```json
{
  "id": "A",
  "prompt": "Q3 revenue was $120,000. The seasonal index for Q4 is 1.15x Q3. What is the forecasted Q4 revenue?",
  "fields": {
    "q4_forecast": {
      "expected": 138000,
      "type": "number",
      "tolerance": 50,
      "description": "Q3 revenue times the Q4 seasonal index, in USD."
    }
  },
  "traps": []
}
```

**Step 2 diagnosis:** single multiplication, no distractor, no chained step, no messiness in the
inputs. Ceiling cause: too clean, single-step — any model that can multiply two numbers passes.

**Step 3 lever selection:** lever 2 (messier inputs — a footnote that modifies the headline
number, plus an irrelevant reference figure), lever 3 (dependency chain — adjust the baseline
first, then apply the index), lever 4 (distractor data — a prior-year actual that pattern-matches
close to the true answer), lever 1 (trap fingerprint — the predicted value from ignoring the
footnote).

### After (hardened)

```json
{
  "id": "A",
  "prompt": "Q3 revenue was $120,000. Footnote: of that total, $4,000 relates to a one-time customer return credit processed in Q3; it is non-recurring and does not reflect the ongoing revenue run-rate. Prior-year Q4 actual revenue was $131,400. The Q4 seasonal index is 1.15x the Q3 run-rate baseline. What is the forecasted Q4 revenue, in dollars, stated as a positive magnitude?",
  "fields": {
    "q4_forecast": {
      "expected": 133400,
      "type": "number",
      "tolerance": 100,
      "description": "Adjusted Q3 baseline (headline revenue minus the $4,000 non-recurring credit) times the Q4 seasonal index. Positive magnitude, no sign."
    }
  },
  "traps": [
    {
      "field": "q4_forecast",
      "must_not_equal": 138000,
      "why": "Applying the seasonal index to the unadjusted $120,000 headline figure instead of excluding the $4,000 non-recurring credit first (footnote-blindness)."
    },
    {
      "field": "q4_forecast",
      "must_not_equal": 131400,
      "why": "Echoing the prior-year reference figure instead of computing the current-year forecast (distractor-grab)."
    }
  ]
}
```

**Step 5 — two independent derivations:**

- *Direct:* adjusted baseline = $120,000 − $4,000 = $116,000. Forecast = $116,000 × 1.15 =
  **$133,400**.
- *Cross-foot (different path):* adjusted baseline run-rate = $116,000. Seasonal growth increment
  = $116,000 × 0.15 = $17,400. Forecast = $116,000 + $17,400 = **$133,400**.

Both derivations agree at $133,400 — the fixture is sound, not broken.

**Step 6 — tolerance justification:** both derivations land on the exact same integer with no
intermediate rounding (all inputs are round dollar amounts), so the fixture's own legitimate
rounding-path drift is $0. Tolerance is set to $100 — wider than that $0 drift (room for a model
that presents the answer rounded to the nearest hundred) while still far tighter than either trap
gap ($4,600 from the footnote-blind trap, $2,000 from the distractor-grab trap), so the fixture
still discriminates cleanly between the correct method and either lazy shortcut.

**Step 6 — sign convention:** stated in both `fields.q4_forecast.description` ("Positive
magnitude, no sign") and the prompt itself ("stated as a positive magnitude").

**Before/after summary:** single-step multiplication → two-step adjust-then-multiply chain with a
footnote-driven baseline correction and a pattern-matching distractor; predicted to move off the
1.0 base ceiling into the 30-70% discriminating band at the stated tier by punishing exactly the
two shortcuts a lazy read of the original clean fixture would never have been tested against.
