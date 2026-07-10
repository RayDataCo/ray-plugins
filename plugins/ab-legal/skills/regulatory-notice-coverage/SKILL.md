---
name: regulatory-notice-coverage
description: Structural disclosure-coverage check of a privacy notice/policy against a named data-protection regime's enumerated mandatory elements. Given notice text plus a regime (GDPR or CCPA/CPRA), classify every enumerated element PRESENT / ABSENT / DEFICIENT and emit a machine-gradable JSON block, a human-readable table, and a fixed disclaimer. Use when asked to audit or review a privacy policy for GDPR Article 13/14 or CCPA/CPRA (Cal. Civ. Code §1798.100 et seq.) disclosure completeness, "which required notice elements are missing", "does this privacy policy cover what GDPR/CCPA requires", or "run a notice coverage check". Reports disclosure gaps only; it is not legal advice and makes no lawfulness or compliance determination.
---

# Regulatory Notice Coverage

Check a privacy notice / privacy policy against the *published, enumerable* mandatory
disclosure elements of a named regime. Each element is a checkable fact ("does the notice
state X?"), not a legal opinion — so the output is deterministic and machine-gradable.

The skill classifies **every** enumerated element for the chosen regime/scope as
`PRESENT` / `ABSENT` / `DEFICIENT`, then emits two synchronized artifacts plus a fixed
disclaimer, in this order: (1) the JSON block (the graded surface), (2) the human table,
(3) the disclaimer (verbatim, always last).

## Inputs

- **notice_text** (required): the full privacy-notice text to check.
- **regime** (required): `"GDPR"` or `"CCPA/CPRA"`. If unstated, infer from the text
  (EEA/controller/Art. 6 language → GDPR; California/consumer/"sell or share" → CCPA/CPRA).
  If genuinely ambiguous, state the assumption you made rather than guessing silently.
- **collection_context** (GDPR only): `from_subject` | `not_from_subject` | `both` |
  `unspecified`. Determines which GDPR elements are in scope (see Scope). For CCPA/CPRA
  this field is always `null`.
- **as_of_date** (`YYYY-MM-DD`): the date the check is run. Default to today — run `date`
  via Bash; never infer it. Used only for CCPA/CPRA element C10 (12-month recency).

## Procedure

1. **Resolve regime and scope.** Pick the element set and total per *Scope* below.
2. **Load the enumerated standard.** Read the matching reference file — it holds every
   element's id, citation, label, conditional trigger, required sub-parts, and the exact
   PRESENT/ABSENT/DEFICIENT rule. Apply those rules; do not improvise element definitions.
   - GDPR → `references/gdpr-elements.md`
   - CCPA/CPRA → `references/ccpa-cpra-elements.md`
3. **Set as_of_date** (default today; run `date`).
4. **Classify each in-scope element** against `notice_text` using the general rules below
   plus the per-element rule from the reference. Capture a verbatim evidence span.
5. **Derive** absent_ids, deficient_ids, present_ids, counts, coverage_verdict.
6. **Emit** the JSON block, then the human table, then the disclaimer.
7. **Self-check the invariants** (below) before finalizing. Fix any violation and re-derive.

## Scope (element set and total)

| regime / collection_context | element ids | total |
|---|---|---|
| GDPR · `from_subject` | G1–G12 | 12 |
| GDPR · `not_from_subject` \| `both` \| `unspecified` | G1–G14 | 14 |
| CCPA/CPRA (collection_context = null) | C1–C10 | 10 |

`from_subject` is Art. 13 only. Art. 14 (`not_from_subject`) is the Art. 13 element list
**plus** the two Art. 14 additions (G13 categories of data, G14 source), so it and `both`
and `unspecified` all use the full 14. When collection context is not clearly stated in the
notice, use `unspecified` → the full 14-element set (never under-scope).

## Classification standard (general)

Apply these three definitions, then the element-specific rule in the reference file.

- **PRESENT** — the element is disclosed with the required specificity (all required
  sub-parts stated). `evidence` = a verbatim span from the notice; `missing_subparts` = `[]`.
- **DEFICIENT** — the element's topic *is* addressed but a required sub-part is missing or
  too vague to satisfy the requirement. `evidence` = the verbatim span that shows the topic
  is addressed (non-null); `missing_subparts` = the specific missing sub-part(s).
  Canonical DEFICIENT cases: purposes stated with **no legal basis** (GDPR's most-missed
  element → G3 DEFICIENT, not present); "we may share your data" with **no recipient
  categories**; retention given only as "as long as necessary" with **no criteria**; a
  rights list **missing one or more** of the enumerated rights.
- **ABSENT** — the element is not addressed at all. `evidence` = `null`;
  `missing_subparts` = the specific undisclosed requirement (a short phrase, non-empty).

**Conditional elements.** Some elements are required only when a trigger appears (e.g.
"where processing is based on consent", "any intention to transfer to a third country",
"where applicable"). The reference marks each conditional element and its trigger. Rule:
- If the trigger **is** evident in the notice → evaluate the required sub-part normally
  (PRESENT / DEFICIENT / ABSENT).
- If the trigger is **not** evident anywhere in the notice → the requirement is not
  activated → status `PRESENT`, `missing_subparts` `[]`, and `evidence` = a short bracketed
  note, e.g. `"[not triggered: no consent-based processing disclosed]"`. (This bracketed
  note is the one permitted non-span value for `evidence`; it applies only to a
  not-triggered conditional and never to a genuinely disclosed element.)

**Determinism rules** (so repeated runs agree):
- Evidence for PRESENT (non-vacuous) and DEFICIENT MUST be a verbatim substring copied from
  `notice_text` — do not paraphrase.
- Judge only what the text says. Do not credit an element because the org "probably" does it.
- An explicit negative disclosure satisfies an element where the regulation asks *whether*
  something happens (e.g. "we do not sell or share your personal information" → C5 PRESENT;
  "we do not share data with third parties" → G5/C4 PRESENT).
- "Last updated" recency (C10): DEFICIENT if a date is present but more than 12 months
  before `as_of_date`; ABSENT if no date at all; PRESENT if dated within 12 months.

## Output

### 1. JSON block (the graded surface)

Emit exactly this shape in a fenced ```json block. Types and keys are fixed.

```json
{
  "regime": "GDPR" | "CCPA/CPRA",
  "collection_context": "from_subject" | "not_from_subject" | "both" | "unspecified" | null,
  "as_of_date": "YYYY-MM-DD",
  "elements": [
    {
      "id": "G3",
      "citation": "Art. 13(1)(c)",
      "label": "Purposes of processing + legal basis for each",
      "status": "PRESENT" | "ABSENT" | "DEFICIENT",
      "evidence": "<verbatim span from notice>" | null,
      "missing_subparts": ["legal basis under Art. 6(1) for each stated purpose"]
    }
  ],
  "absent_ids":    ["G10"],
  "deficient_ids": ["G3", "G7"],
  "present_ids":   ["G1", "G2"],
  "counts": { "present": 0, "absent": 0, "deficient": 0, "total": 0 },
  "coverage_verdict": "COMPLETE_DISCLOSURE" | "GAPS_FOUND"
}
```

Construction rules:
- `elements` holds **exactly one entry per in-scope element**, in ascending id order (sort
  by the numeric suffix: G1, G2, … G10, G11 — not lexical, so G2 precedes G10). No
  duplicates, none omitted. Count == the scope total (14 / 12 / 10).
- `evidence` is non-null for `PRESENT` and `DEFICIENT`; `null` for `ABSENT`.
- `missing_subparts` is `[]` for `PRESENT`; the missing sub-part(s) for `DEFICIENT`; the
  undisclosed requirement for `ABSENT`.
- `absent_ids` = every id with status `ABSENT`; `deficient_ids` = every `DEFICIENT`;
  `present_ids` = every `PRESENT`. Each list sorted ascending by numeric suffix.
- `counts.total` = scope total; `present`/`absent`/`deficient` are the list lengths.
- `coverage_verdict` = `COMPLETE_DISCLOSURE` **iff** `absent_ids` and `deficient_ids` are
  **both** empty; otherwise `GAPS_FOUND`. It is a pure function of the two gap sets — never
  compute it any other way, and never phrase it (or the prose) as "compliant" /
  "non-compliant" / "in violation". Say "complete disclosure" or "disclosure gaps found".

### Invariants (self-check before emitting; the eval relies on these)

- **(a)** `present_ids ∪ absent_ids ∪ deficient_ids` == the full id set for the scope, and
  the three sets are pairwise disjoint (every element appears in exactly one).
- **(b)** `present + absent + deficient == total`, and `total` == the scope's element count.
- **(c)** `coverage_verdict` is exactly `COMPLETE_DISCLOSURE` when both gap sets are empty,
  else `GAPS_FOUND`.
- **(d)** `absent_ids` and `deficient_ids` are the primary graded sets — get their
  membership right; each id's status in `elements` must agree with which list it is in.

If any invariant fails, correct the classification and re-derive all three lists and counts.

### 2. Human table

After the JSON, render a markdown table, one row per element in the same ascending id order:

`id | citation | label | status | gap | evidence`

- `gap` = the `missing_subparts` joined (or `—` when `PRESENT`).
- `evidence` = the verbatim span (or `—` when `ABSENT`; the bracketed note for
  not-triggered conditionals). Truncate long spans with an ellipsis for readability only —
  the JSON keeps the full span.

### 3. Disclaimer (fixed, verbatim, always last)

Output this exact sentence, unmodified, as the final line of the response:

> This is a structural disclosure-coverage check against the regulation's enumerated mandatory elements. It is not legal advice and makes no determination of lawfulness, fairness, or compliance.

## Notes

- Do not add, merge, split, or renumber elements. The id set is fixed per the reference
  files so oracle grading can compare gap sets by exact id.
- The reference files are the authority for each element's required sub-parts and its
  conditional trigger. Read the relevant one every run rather than working from memory.