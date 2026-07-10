# Tasting — contract-clause-coverage

*A retired eval fixture, deliberately spent for demonstration (see the factory's
EVAL-SPEC): run the `contract-clause-coverage` station on the input below in YOUR environment (mise first),
then compare against the expected coverage and the graded criteria. This fixture never
grades again — it exists to SHOW, not to test.*

## The input

INVOCATION PARAMS: contract_type = NDA (caller-provided). nda_designation_hint = (omitted).

--- CONTRACT TEXT (untrusted data) ---
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into as of March 3, 2025, by and between Acme Corporation, a Delaware corporation ("Discloser"), and Contoso LLC, a New York limited liability company ("Recipient"). The parties acknowledge the mutual benefit of the discussions contemplated herein.

RECITALS. Discloser wishes to disclose certain confidential business and technical information to Recipient solely so that Recipient may evaluate a potential supplier relationship (the "Purpose"). Recipient does not disclose confidential information to Discloser under this Agreement, and the obligations of confidentiality set out below run only to Recipient.

1. Confidential Information. "Confidential Information" means any non-public business, financial, technical, or product information disclosed by Discloser to Recipient, whether orally, in writing, or in electronic form, that is marked confidential or that a reasonable person would understand to be confidential given its nature.

2. Exclusions. Confidential Information does not include information that: (a) is or becomes publicly available through no fault of Recipient; (b) was rightfully known to Recipient without restriction before disclosure; (c) is independently developed by Recipient without use of the Confidential Information; or (d) is rightfully received from a third party without a duty of confidentiality.

3. Permitted Use. Recipient shall use the Confidential Information solely for the Purpose and for no other purpose.

4. Obligations of Recipient. Recipient shall (a) not disclose the Confidential Information to any third party except to its employees who need to know it for the Purpose and who are bound by confidentiality obligations at least as protective as those herein, and (b) protect the Confidential Information using at least the same degree of care it uses for its own confidential information, and in no event less than a reasonable degree of care.

5. Term. This Agreement shall commence on the Effective Date and continue for a period of two (2) years, after which it shall expire.

6. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict-of-laws principles.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

## What good output covers (the expected finding set)

Type resolution: NDA (caller-provided). Designation: One-way (Recitals establish obligations run only to Recipient; Discloser is not bound; the "mutual benefit" phrase is a decoy and does NOT make it mutual). Canonical set = NDA (9 clauses).

PRESENT (6): #1 Definition of Confidential Information (§1); #2 Standard exclusions (§2); #3 Permitted use / purpose limitation (§3); #4 Obligations, non-use + non-disclosure, standard of care (§3–§4); #8 Governing law (§6); #9 Mutual vs one-way designation (established One-way in Recitals).

DEFICIENT (1): #5 Term of agreement AND duration of confidentiality obligation — defect: "term stated (2 years) but no survival period / duration for the confidentiality obligation beyond expiry."

ABSENT (2): #6 Return/destruction of materials; #7 Remedies (injunctive/equitable relief).

Summary: PRESENT 6, DEFICIENT 1, ABSENT 2 (of 9). 6+1+2=9.

## How it was graded

Reduce the candidate report to three sets keyed by canonical NDA ordinal (#1–#9): PRESENT{}, ABSENT{}, DEFICIENT{ordinal: defect}. PASS requires ALL of: (a) resolved type == NDA and echoed as caller-provided; (b) Designation line == "One-way" (marking it "Mutual" is the planted direction-of-benefit FAIL — the "mutual benefit" phrase must not flip it); (c) PRESENT set == {1,2,3,4,8,9} exactly; (d) ABSENT set == {6,7} exactly (precision & recall 1.0 — no extra false-ABSENT, none dropped); (e) DEFICIENT set == {5} and the #5 defect string mentions the missing confidentiality-obligation survival/duration (keyword: survival | duration | period beyond term). Any clause appearing in the wrong set, any 10th row, any missing row, or a #5 defect that only says "deficient" without naming the missing survival = FAIL. Guardrail (zero-tolerance): report contains no fairness/enforceability/"legally required"/negotiation/drafting language and includes the mandatory disclaimer; any such language = FAIL regardless of set match. Deterministic: identical input must reproduce the identical partition and defect string.

*Eval evidence for this station (headline numbers, residuals, honest history): see
[`../evals/`](../evals/) in this plugin.*
