# Intended-Action Grounding for Dataset Discovery

## Method report and controlled synthetic demonstration

**Implementation status:** verified synthetic proof of concept  
**Branch:** `codex/experimental-evaluation`  
**Test status:** 50 automated tests passing  
**Scope of claims:** controlled synthetic example; no real-dataset effectiveness claim yet

## Executive summary

Conventional dataset retrieval ranks tables mainly by whether their text and
schema appear relevant to a topic. This can return a table that is strongly
related to the subject but unsuitable for the analysis the user intends to
perform. The implemented framework adds a second signal: whether observable
table capabilities satisfy requirements derived from the user's intended
action.

The framework therefore separates a request into:

1. a **topical query**, used only for first-stage retrieval; and
2. a **grounded action with validated arguments**, used to construct analytical
   requirements.

For every candidate table, it combines topical relevance with action–capability
alignment:

\[
U(T\mid q_u,g_u)=\lambda_r r(q_u,T)+\lambda_a A(T,g_u).
\]

In the controlled example, a patient-record table receives the highest
relevance score for “vaccine side effects.” Nevertheless, a country-rate table
is ranked first when the requested action is to compare rates between countries.
Its final score rises above the relevance leader because its capabilities match
the grounded comparison requirements.

This is the current achievement: the executable system demonstrates that an
action-aware usefulness score can correct a relevance-only ordering. It is not
yet evidence that the method improves results on WikiTables or another real
benchmark.

## 1. Research problem

Suppose two users search for the same topic:

- “Vaccine side effects — compare rates across countries.”
- “Vaccine side effects — predict an individual patient's outcome.”

Both requests concern the same topic, so a topic-only retriever may produce a
similar or identical candidate ordering. However, the useful table is different:

- comparison requires a numeric rate and a country grouping field;
- prediction requires an observed outcome, varying labels, and non-identifier
  attributes at an appropriate observational level.

The framework models this distinction explicitly instead of expecting topical
similarity to act as a proxy for analytical usefulness.

## 2. Current implementation

The executable pipeline contains the following stages:

```text
Versioned knowledge layer
          |
User request -> interpretation -> grounded action -> requirements
      |                                            |
      +-> topical query -> first-stage retrieval -> candidates
Tables -> offline profiling -> capability profiles |
             requirements + capabilities -> alignment
                                          -> final usefulness ranking
```

The supported actions are:

- `COMPARE`
- `AGGREGATE`
- `PREDICT`
- `EXPLAIN`
- `MONITOR`

`EXPLAIN` means exploratory association, not causal identification. `PREDICT`
means that observable evidence needed for predictive analysis is present; it
does not promise predictive performance.

The operational axes are:

| Axis | Meaning |
|---|---|
| `sem` | semantic/content evidence |
| `str` | structural suitability |
| `cov` | temporal or geographic coverage |
| `qual` | quality evidence |
| `aff` | analytical affordance |

All actions, arguments, predicates, matching rules, templates, and weights are
defined in a strict versioned knowledge file. The interpreter cannot invent new
vocabulary. The current knowledge configuration has SHA-256 hash
`06d14d1e00f138d58ce25e32a7790edfbaf890eadfc172474b93e5593fdb539a`.

## 3. Offline table profiling

Before ranking, each table is converted into a capability profile. Evidence is
extracted from metadata, schema, content, and complete-table statistics in the
synthetic implementation.

Each capability records:

\[
\gamma=(p,x,v,s,c,\operatorname{prov}),
\]

where `p` is a controlled predicate, `x` is its axis, `v` is the value, `s` is
`observed`, `estimated`, or `inferred`, `c` is confidence, and provenance states
where and how the evidence was obtained.

Unknown evidence remains absent. It is not converted into false evidence.
Inferred capabilities receive lower confidence than directly observed ones.

## 4. Online interpretation and grounding

The controlled input is:

```text
vaccine side effects compare measure=rate, comparison dimension=country
```

The interpreter separates it into:

| Component | Extracted value |
|---|---|
| Topical query \(q_u\) | `vaccine side effects` |
| Action | `COMPARE` |
| `measure` | `rate` |
| `comparison_dimension` | `country` |

Only `vaccine side effects` is supplied to first-stage retrieval. The action
words and arguments do not influence the relevance score. This separation is
important for both interpretability and experimental control.

The action catalogue declares that `COMPARE` requires both `measure` and
`comparison_dimension`. Since they are present and valid, grounding succeeds:

\[
g_u=(\text{COMPARE},\{\text{measure=rate},
\text{comparison dimension=country}\}).
\]

If grounding fails, the system creates no action requirements and safely falls
back to relevance-only ranking.

## 5. Requirement construction

The grounded action instantiates the `COMPARE` template:

| Polarity | Predicate | Axis | Expected value | Purpose |
|---|---|---|---|---|
| Required | `numeric_measure` | `sem` | `rate` | Requested measure must be observable and numeric |
| Required | `grouping_field` | `str` | `country` | Rows must support comparison across countries |
| Optional | `missingness_at_most` | `qual` | `0.2` | Prefer sufficiently complete evidence |

A geographic-coverage requirement would also be created if a geographic scope
were explicitly supplied. Missing required argument values are never guessed.

## 6. Controlled candidate tables

### Table A: `country_rates`

| country | rate | year |
|---|---:|---:|
| Italy | 2.1 | 2020 |
| France | 2.8 | 2020 |

Relevant profiled capabilities include:

| Capability | Value | Evidence state | Confidence |
|---|---|---|---:|
| `numeric_measure` | `rate` | observed | 1.0 |
| `grouping_field` | `country` | inferred | 0.8 |
| `missingness_at_most` | `0.0` | observed | 1.0 |
| `row_granularity` | `country` | observed metadata | 1.0 |

### Table B: `patient_records`

| patient_id | outcome | age | year |
|---|---:|---:|---:|
| a | 0 | 34 | 2020 |
| b | 1 | 57 | 2021 |
| c | 0 | 45 | 2021 |

This table has strong topic-bearing text and useful patient-level predictive
attributes. It does not contain the requested `rate` measure or `country`
grouping field.

## 7. First-stage relevance

The current executable proof of concept uses normalized **BM25 lexical
relevance**, calculated from table titles, descriptions, and column names.
It does not yet use TABERTA or another neural semantic encoder.

For the topical query `vaccine side effects`, the scores are:

| Relevance-only rank | Table | Relevance \(r(q,T)\) |
|---:|---|---:|
| 1 | `patient_records` | 1.0000 |
| 2 | `country_rates` | 0.3655 |

The patient table is therefore the relevance-only winner. This is plausible:
its title and description have stronger lexical overlap with the topical query.
But relevance alone does not establish suitability for comparing country rates.

## 8. Requirement–capability matching

For each requirement, only capabilities with the same predicate and axis are
considered:

\[
m(\rho,T)=\max_{\gamma}
M_p(\widehat v,v)c.
\]

The value match is multiplied by evidence confidence.

### Table A matches

| Requirement | Raw value match | Confidence | Final match |
|---|---:|---:|---:|
| Numeric measure `rate` | 1.0 | 1.0 | 1.0 |
| Grouping field `country` | 1.0 | 0.8 | 0.8 |
| Missingness at most 0.2 | 1.0 | 1.0 | 1.0 |

The grouping match is reduced to 0.8 because grouping support was inferred by a
cardinality heuristic rather than directly declared.

### Table B matches

| Requirement | Final match |
|---|---:|
| Numeric measure `rate` | 0.0 |
| Grouping field `country` | 0.0 |
| Missingness at most 0.2 | 1.0 |

The absence of the first two capabilities is treated as unknown/unmatched
evidence, not as fabricated support.

## 9. Axis aggregation

Required requirements use a minimum, so one weak required condition can expose
a bottleneck:

\[
R_x(T)=\min_{\rho_j\text{ required on }x}m(\rho_j,T).
\]

Optional and negative requirements use means. Empty required, optional, and
negative sets have values 1, 0, and 0 respectively. The axis score is:

\[
S_x=R_x[(1-\eta_o)+\eta_oO_x][1-\eta_nN_x].
\]

The synthetic defaults are \(\eta_o=0.2\) and \(\eta_n=0.5\).

For Table A:

| Axis | Calculation | Axis score |
|---|---|---:|
| `sem` | \(1.0(1-0.2)\) | 0.80 |
| `str` | \(0.8(1-0.2)\) | 0.64 |
| `qual` | \(1.0[(1-0.2)+0.2(1.0)]\) | 1.00 |

Only these three axes are active. The original `COMPARE` weights for them are
0.35, 0.30, and 0.10. They are renormalized by their active total, 0.75:

\[
A(T_A,g)=
\frac{0.35}{0.75}(0.80)+
\frac{0.30}{0.75}(0.64)+
\frac{0.10}{0.75}(1.00)
=0.7627.
\]

Table B fails the active semantic and structural requirements, giving:

\[
A(T_B,g)=0.1333.
\]

## 10. Final usefulness scores

The synthetic configuration gives topical relevance 40% of the final score and
action alignment 60%:

\[
U(T)=0.4r(q,T)+0.6A(T,g).
\]

### Table A

\[
U(T_A)=0.4(0.3655)+0.6(0.7627)=0.6038.
\]

### Table B

\[
U(T_B)=0.4(1.0000)+0.6(0.1333)=0.4800.
\]

### Final comparison

| Table | Relevance | Alignment | Final usefulness | Final rank |
|---|---:|---:|---:|---:|
| `country_rates` | 0.3655 | 0.7627 | **0.6038** | **1** |
| `patient_records` | **1.0000** | 0.1333 | 0.4800 | 2 |

The action-aware method changes the ordering. The table with the strongest
topic relevance is not selected first because it lacks the evidence required
for the requested comparison. The lower-relevance table becomes first because
it contains the requested rate and country grouping structure.

## 11. What the example demonstrates

The verified example supports these implementation-level conclusions:

1. Topical relevance and analytical usefulness are represented separately.
2. Retrieval sees only the topical query, while alignment sees the grounded
   action requirements.
3. Capability evidence is inspectable and confidence-weighted.
4. Required evidence acts as an axis-level bottleneck.
5. Action alignment can reverse a relevance-only ordering.
6. Changing the action while retaining the topic can change the correct table.
7. Invalid or unsupported actions produce a safe relevance-only fallback.

## 12. What the example does not yet demonstrate

The following claims must not yet be made:

- that the framework statistically improves nDCG, MRR, or recall on WikiTables;
- that action-aware ranking outperforms TABERTA, Qwen, Birdie, or EDBT25;
- that the current weights generalize to real topics;
- that the heuristic capability profiler has high extraction accuracy;
- that the current deterministic interpreter represents natural user language;
- that the scores are calibrated probabilities;
- that `EXPLAIN` establishes causality or `PREDICT` guarantees accuracy.

The example is a successful, tested proof of mechanism. Benchmark effectiveness
requires frozen development choices, topic-level splits, human usefulness
judgments, external baseline runs, and evaluation on an untouched test set.

## 13. Next scientific validation

The recommended next stages are:

1. Freeze a real WikiTables source and dataset manifest.
2. Select topics independently of system performance.
3. Create multiple action variants per topic.
4. Split by topic before tuning to prevent action-variant leakage.
5. Integrate pinned first-stage semantic retrievers and rerankers.
6. Pool fixed-depth outputs from all systems, including Ours.
7. Obtain two independent human judgments for topical relevance and usefulness,
   followed by adjudication.
8. Tune weights and thresholds on development topics only.
9. Report nDCG@5/10, MRR, Useful-Recall, per-action results, action-switch
   accuracy, diagnostics, confidence intervals, corrected significance tests,
   and efficiency.
10. Generate paper tables only from immutable recorded run artifacts.

## 14. Reproduction

From the repository root:

```bash
cd /datastore-beast/servers/Enas/intention/intention_repo/Intention
pytest -q
PYTHONPATH=src python3 -m intention smoke \
  --input "vaccine side effects compare measure=rate, comparison dimension=country"
```

To demonstrate that the same topic can favor a different table when the action
changes:

```bash
PYTHONPATH=src python3 -m intention smoke \
  --input "vaccine side effects predict outcome=outcome"
```

## 15. Suggested supervisor presentation message

> Our current implementation demonstrates a tested proof of mechanism for
> action-aware dataset discovery. A conventional relevance stage ranks a
> patient-record table first for the topic “vaccine side effects.” When the
> request is grounded as COMPARE with measure `rate` and grouping dimension
> `country`, the framework constructs explicit requirements and aligns them
> against evidence-backed table capabilities. The country-rate table receives
> lower topical relevance but much higher action alignment, changing the final
> ordering. This shows why topical relevance alone is insufficient for
> action-conditioned usefulness. The result is currently synthetic and should
> be presented as an implementation achievement and proof of mechanism, not yet
> as benchmark evidence of general effectiveness.

