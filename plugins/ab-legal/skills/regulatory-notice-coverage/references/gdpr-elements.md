# GDPR mandatory privacy-notice elements (Articles 13 & 14)

Enumerated, stable id set. **from_subject** scope = G1–G12 (Art. 13). **not_from_subject /
both / unspecified** scope = G1–G14 (Art. 13 list + the two Art. 14 additions G13, G14).

Legend: **Type** = Unconditional (always required; silence → ABSENT) or Conditional (with
its trigger; if the trigger is not evident in the notice → PRESENT / not-triggered, per the
SKILL.md conditional rule). For every element, DEFICIENT = topic addressed but a required
sub-part missing/too vague; PRESENT = all required sub-parts stated.

---

### G1 — Art. 13(1)(a) — Identity and contact details of the controller (and representative, if any)
- Type: Unconditional.
- Required sub-parts: (i) the controller's identity/name; (ii) a contact method.
- PRESENT: name + a contact method given. DEFICIENT: one given without the other (e.g., a
  name but no contact channel). ABSENT: no identifiable controller disclosed.

### G2 — Art. 13(1)(b) — Contact details of the Data Protection Officer (where applicable)
- Type: Conditional. Trigger: the notice references a DPO / designated data-protection or
  privacy officer, or states one is appointed.
- Required sub-part: the DPO's contact details.
- PRESENT: DPO contact details given, OR the notice is silent on any DPO (not triggered).
  DEFICIENT: a DPO is referenced but no contact details are provided.

### G3 — Art. 13(1)(c) — Purposes of the processing + legal basis (Art. 6(1)) for each
- Type: Unconditional.
- Required sub-parts: (i) each processing purpose; (ii) the Art. 6(1) legal basis for each
  purpose. This is GDPR's single most-missed element.
- PRESENT: purposes AND a legal basis for each are stated. DEFICIENT: purposes stated but
  legal basis missing for any/all (missing_subpart: "legal basis under Art. 6(1) for each
  stated purpose"), or a legal basis stated without the purposes. ABSENT: neither disclosed.

### G4 — Art. 13(1)(d) — Legitimate interests pursued (where Art. 6(1)(f) is a basis)
- Type: Conditional. Trigger: legitimate interests cited as the legal basis for any purpose.
- Required sub-part: a description of the specific legitimate interests pursued.
- PRESENT: LI basis used and the specific interests described, OR legitimate interests never
  relied upon (not triggered). DEFICIENT: LI cited as a basis but the specific interests not
  described.

### G5 — Art. 13(1)(e) — Recipients or categories of recipients
- Type: Unconditional.
- Required sub-part: the recipients or categories of recipients (an explicit "we do not
  share / disclose" statement satisfies it).
- PRESENT: recipients/categories stated, or an explicit no-disclosure statement. DEFICIENT:
  disclosure/sharing mentioned ("we may share your data") but no recipients or categories
  named. ABSENT: recipients not addressed at all.

### G6 — Art. 13(1)(f) — Third-country transfers + safeguards + how to obtain a copy
- Type: Conditional. Trigger: the notice indicates any transfer of data outside the
  EEA / to a third country or international organisation.
- Required sub-parts: (i) the fact of transfer; (ii) the safeguard relied on (adequacy
  decision, SCCs, BCRs, etc.); (iii) how to obtain a copy of the safeguards.
- PRESENT: transfers disclosed with the safeguard and how-to-obtain, OR no international
  transfer indicated (not triggered). DEFICIENT: transfers mentioned but the safeguard or
  the how-to-obtain-a-copy sub-part is missing.

### G7 — Art. 13(2)(a) — Retention period or the criteria to determine it
- Type: Unconditional.
- Required sub-part: a retention period OR the criteria used to determine it.
- PRESENT: a period or determinable criteria given. DEFICIENT: retention addressed only in
  vague terms ("as long as necessary", "for business purposes") with no criteria. ABSENT:
  retention not addressed.

### G8 — Art. 13(2)(b) — Data-subject rights: access, rectification, erasure, restriction, objection, portability
- Type: Unconditional.
- Required sub-parts: all six named rights.
- PRESENT: all six disclosed. DEFICIENT: rights addressed but one or more of the six omitted
  (missing_subpart: name the omitted right(s)). ABSENT: no data-subject rights disclosed.

### G9 — Art. 13(2)(c) — Right to withdraw consent at any time (where processing is consent-based)
- Type: Conditional. Trigger: consent cited as a legal basis, or consent-based processing
  otherwise described.
- Required sub-part: the right to withdraw consent at any time.
- PRESENT: consent-based processing present and the withdrawal right disclosed, OR consent
  is not used as a basis (not triggered). DEFICIENT: a withdrawal right stated but not "at
  any time" or with no method. ABSENT: consent-based processing present but the withdrawal
  right entirely undisclosed.

### G10 — Art. 13(2)(d) — Right to lodge a complaint with a supervisory authority
- Type: Unconditional.
- Required sub-part: the right to lodge a complaint with a supervisory authority.
- PRESENT: disclosed. DEFICIENT: a generic "contact us" / complaint route given but not
  framed as the right to complain to a supervisory authority. ABSENT: not disclosed. (This
  is distinct from the G8 rights list — a rights list that omits the complaint right does
  not make G10 present.)

### G11 — Art. 13(2)(e) — Whether provision of data is a statutory/contractual requirement + consequences of not providing
- Type: Conditional. Trigger: the notice frames provision of data as required for a
  contract, a service, or by law.
- Required sub-parts: (i) whether provision is a statutory/contractual requirement or
  necessary to enter a contract; (ii) the consequences of failing to provide the data.
- PRESENT: the requirement and consequences stated, OR no data is framed as a
  provision-requirement (not triggered). DEFICIENT: data described as required but the
  consequences of not providing are omitted.

### G12 — Art. 13(2)(f) — Existence of automated decision-making/profiling (Art. 22) + meaningful info about the logic
- Type: Conditional. Trigger: the notice describes automated decision-making or profiling
  producing legal/similarly significant effects.
- Required sub-parts: (i) the existence of ADM/profiling; (ii) meaningful information about
  the logic involved and its significance/envisaged consequences.
- PRESENT: ADM disclosed with meaningful logic info, OR no ADM/profiling indicated (not
  triggered). DEFICIENT: ADM/profiling mentioned but no meaningful information about the
  logic/significance.

---

## Article 14 additions (in scope only for not_from_subject / both / unspecified)

### G13 — Art. 14(1)(d) — Categories of personal data concerned
- Type: Unconditional (Art. 14 scope).
- Required sub-part: the categories of personal data processed.
- PRESENT: categories stated. DEFICIENT: processing described only in vague terms with no
  categories. ABSENT: categories not addressed.

### G14 — Art. 14(2)(f) — Source of the data (incl. whether from publicly accessible sources)
- Type: Unconditional (Art. 14 scope).
- Required sub-part: the source(s) the data came from, including whether from publicly
  accessible sources where relevant.
- PRESENT: the source is stated. DEFICIENT: a source is gestured at but left unspecified
  where specificity is required. ABSENT: the source is not addressed.
