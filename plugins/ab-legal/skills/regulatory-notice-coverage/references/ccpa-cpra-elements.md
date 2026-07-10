# CCPA/CPRA mandatory privacy-policy elements (Cal. Civ. Code §1798.100 et seq.)

Enumerated, stable id set C1–C10 (total 10). `collection_context` is always `null` for this
regime. Citations are to the California Civil Code as amended by the CPRA.

Legend: **Type** = Unconditional (always required; silence → ABSENT) or Conditional (with
its trigger; if the trigger is not evident in the notice → PRESENT / not-triggered, per the
SKILL.md conditional rule). DEFICIENT = topic addressed but a required sub-part missing/too
vague; PRESENT = all required sub-parts stated.

---

### C1 — §1798.110(c) / §1798.130(a)(5)(B) — Categories of personal information collected
- Type: Unconditional.
- Required sub-part: the categories of PI collected, expressed by the §1798.140 category
  list (identifiers, commercial info, biometric, internet activity, geolocation, etc.).
- PRESENT: categories enumerated. DEFICIENT: collection described generically ("information
  about you", "the data you give us") without the statutory categories. ABSENT: categories
  not addressed.

### C2 — §1798.130(a)(5)(B) — Categories of sources from which PI is collected
- Type: Unconditional.
- Required sub-part: the categories of sources.
- PRESENT: source categories stated. DEFICIENT: sources alluded to but not categorized.
  ABSENT: sources not addressed.

### C3 — §1798.130(a)(5)(B) — Business or commercial purposes for collecting, selling, or sharing PI
- Type: Unconditional.
- Required sub-part: the business/commercial purposes for collection, sale, and sharing.
- PRESENT: purposes stated. DEFICIENT: purposes stated so vaguely they do not cover the
  disclosed processing. ABSENT: purposes not addressed.

### C4 — §1798.130(a)(5)(C) — Categories of third parties to whom PI is disclosed, sold, or shared
- Type: Unconditional.
- Required sub-part: the categories of third parties (an explicit "we do not disclose PI to
  third parties" satisfies it).
- PRESENT: third-party categories stated, or an explicit no-disclosure statement.
  DEFICIENT: disclosure/sharing mentioned but no third-party categories given. ABSENT: the
  third-party disclosure question is not addressed.

### C5 — §1798.130(a)(5)(C) / §1798.135 — Whether the business sells or shares PI (and the categories if so)
- Type: Unconditional.
- Required sub-parts: (i) whether the business sells or shares PI; (ii) the categories sold
  or shared, if it does.
- PRESENT: a clear sells/shares statement — including an explicit "we do not sell or share
  your personal information". DEFICIENT: it acknowledges selling/sharing but omits the
  categories sold/shared. ABSENT: the sale/share question is not addressed.

### C6 — §1798.130(a)(5)(A) — Consumer rights: know/access, delete, correct, opt-out of sale/sharing, limit use of sensitive PI, non-discrimination
- Type: Unconditional.
- Required sub-parts: all six enumerated consumer rights above.
- PRESENT: all six disclosed. DEFICIENT: rights addressed but one or more omitted
  (missing_subpart: name the omitted right(s)). ABSENT: no consumer rights disclosed.

### C7 — §1798.130(a)(1) — Methods for submitting requests (at least two)
- Type: Unconditional.
- Required sub-part: at least two designated methods (must include a toll-free number,
  unless the business operates exclusively online and has a direct relationship with the
  consumer — then a single email/web-form method suffices).
- PRESENT: two or more methods given, or the valid online-only single method. DEFICIENT:
  only one method disclosed where two are required (i.e., not online-only). ABSENT: no
  request method disclosed.

### C8 — §1798.121 — Right to limit use/disclosure of sensitive PI + how to exercise it
- Type: Conditional. Trigger: the notice indicates the business collects or uses sensitive
  personal information.
- Required sub-parts: (i) the right to limit use/disclosure of sensitive PI; (ii) the method
  to exercise it (e.g., a "Limit the Use of My Sensitive Personal Information" link).
- PRESENT: sensitive PI handled and the limit right + method disclosed, OR no sensitive PI
  collected (not triggered). DEFICIENT: sensitive PI collected and the limit right mentioned
  but no method (or method without the right). Note: C6 lists this right among the six; C8
  is the specific limit-right + mechanism disclosure.

### C9 — §1798.100(a)(3) — Retention period or criteria, per category of PI (CPRA)
- Type: Unconditional.
- Required sub-part: the retention period, or the criteria used to determine it, for each
  category of PI (per-category ideal; a single stated period/criteria set is acceptable).
- PRESENT: a period or determinable criteria given. DEFICIENT: retention addressed only as
  "as long as necessary" with no criteria. ABSENT: retention not addressed.

### C10 — §1798.130(a)(5) — Date the policy was last updated (must be within the last 12 months)
- Type: Unconditional.
- Required sub-part: a "last updated" date within 12 months of `as_of_date`.
- PRESENT: a date present and within 12 months before `as_of_date`. DEFICIENT: a date is
  present but more than 12 months before `as_of_date` (an update-currency defect in itself).
  ABSENT: no last-updated date at all.
