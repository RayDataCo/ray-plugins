<!-- iteration: 0 -->

# Interpretation — Management by Exception

Variances are **signals to investigate, not verdicts.** A number alone never proves a manager
failed; it points to a question worth asking. Read this at Step 7 to turn computed variances
into a ranked investigation list.

## 1. Materiality — apply BOTH gates

A variance earns investigation only if it is large **in absolute dollars AND as a % of that
element's standard cost base**. Both gates, not either:

- **Absolute gate** — e.g. ≥ $1,000 (set to a level meaningful for the operation).
- **Percentage gate** — e.g. ≥ 2% of the standard cost base for that element.

A variance that clears only one gate is usually noise. Example: a $500 VOH spending variance at
1.2% of base, or a $300 DL rate variance at 0.4%, both **drop as noise** even if another line is
flagged. Do not let a large absolute dollar amount alone promote a line if the % is trivial, and
do not chase a high % on a tiny dollar base.

## 2. Controllability and responsibility centers

Assign each variance to the center that owns its driver, then **rank by materiality ×
controllability** — never by raw dollars alone:

| variance | typical owner |
|---|---|
| DM price | purchasing |
| DM quantity / usage | production |
| DL rate | HR / labor market |
| DL efficiency | production / supervision |
| VOH spending | production / facilities |
| FOH spending | facilities / fixed-cost owner |
| FOH production-volume | **none — capacity artifact** |
| sales-volume | sales / commercial |

### The production-volume rule (do not violate)

The **FOH production-volume variance is NOT controllable.** It arises purely because actual
output differs from the denominator (normal-capacity) level used to set the FOH rate — it
measures capacity utilization, not spending. Therefore:

- Label it explicitly a **denominator / capacity artifact**.
- Assign it **no controllable spending owner**.
- **Never rank it #1 just because it is the largest absolute dollar.** The controllability
  filter demotes it below smaller-but-controllable variances. Ranking a variance set purely by
  absolute dollars (so production-volume lands on top) is the classic interpretation error.

## 3. Gaming / linkage signatures (cross-variance reading)

Variances interact; read them in pairs, not in isolation. Named signatures to flag:

- **Cheap-material-drives-waste:** favorable DM **price** + unfavorable DM **usage** ⇒
  purchasing bought cheaper, lower-quality material that production then wasted/reworked. The
  immaterial favorable price may have *caused* the material unfavorable usage — surface the link
  and cross-reference the two owners (purchasing ↔ production) even when DM price alone is below
  the materiality threshold.
- **Low-skill-labor:** favorable DL **rate** + unfavorable DL **efficiency** ⇒ cheaper, less-
  skilled labor that took longer. Wage savings financed by lost productivity.
- **Rushed-throughput:** favorable DL efficiency + unfavorable DM usage / quality ⇒ speed bought
  at the cost of scrap.
- **Overtime/expedite:** unfavorable DL rate + favorable DL efficiency ⇒ overtime premium to hit
  output.

When a linkage fires, investigate the *pair* and the tradeoff decision behind it, not each line
in isolation.

## 4. Standard currency

A variance is only as trustworthy as the standard it is measured against. Note whether standards
are **currently attainable** (realistic, recently updated) vs **ideal** (perfection, no waste)
vs **stale** (set long ago). Ideal or stale standards **manufacture** chronic unfavorable
variances that reflect a bad benchmark, not bad performance — flag this before concluding
anyone underperformed.

## 5. Framing rule

Phrase every conclusion as an investigation prompt: "DL efficiency is $9,500 U (11.9%) — ask
production what changed in staffing/setup this month," NOT "production failed." Signal, not
verdict.
