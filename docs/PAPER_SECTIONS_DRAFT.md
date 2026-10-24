# Draft text for Sections 3.4–3.7 and 4 (aligned with the implementation)

Notation follows Sections 2–3 of the manuscript. Numbers in Section 4 refer to the runs in `experiments/results/`
and must be regenerated after the labels are reviewed.

---

## 3.4 Context-Based Candidate Table Retrieval

Context matching restricts assessment to tables that concern the subject of the request. Each table $T$ is
serialised from its documentation and schema: title, description, the name and description of every attribute, and a
small set of categorical values. The context query $q_u$ produced by the Interpreter, or the original input $u$ when
interpretation fails, is scored against every serialisation, giving $r(q_u, T) \in [0, 1]$. The framework is agnostic
to the scoring model; we instantiate it with BM25, TF-IDF and latent semantic analysis (LSA) cosine similarity,
Sentence-BERT cosine similarity, and a hybrid of lexical and dense scores. BM25 scores are divided by the maximum score
for the query, and cosine similarities are clipped to $[0, 1]$. The $k$ highest-scoring tables form the candidate set
$C_k(q_u)$ that is passed to the Table Profiler; ties are broken by table identifier. Because only candidates are
assessed, reranking cannot recover a useful table that context matching does not retrieve (Section 2); we therefore
report candidate recall separately.

## 3.5 Table Evidence Extraction and Profiling

The Table Profiler computes a capability profile $\Phi(T)$ from a full scan of the table and its documentation. For
every attribute it records the observed type (numeric, binary, categorical, temporal, text), the number of valid
values and the missing fraction under a declared set of missing-value markers, the number of distinct values and the
most frequent values, numeric ranges and integrality, and, for temporal attributes, the observed extent and grain
(hour, day, week, month, quarter, year). Categorical values are matched against a declared gazetteer, a membership
mapping from countries to continents with recorded provenance, to determine the geographic level of an attribute
(country, continent, sub-national region). The documented *measure kind* of every numeric attribute (count, amount,
level, rate, mean or cumulative total) is read from its name and description by declared keyword rules; an attribute
without documentation retains its kind only as an undocumented default, which cannot establish requirements on
meaning. At table level the profile records identifier attributes, entity–time keys (panel structure), wide layouts
(one attribute per entity or date) and aggregated-cell layouts (rows that are cells of a contingency table with a
frequency attribute).

Profiles are cached by table content and documentation hash and by profiler version, so they are computed once per
table. Requirements that depend on the requested scope or groups cannot be decided from a profile alone; for these the
Aligner obtains *scoped evidence* (Section 3.6) by evaluating counts over the selected rows of the full table. Profiles
and scoped evidence describe what a table contains; they do not decide whether it is useful.

## 3.6 Requirement–Evidence Alignment

The Aligner implements $A(T, \iota_u) = \mathrm{Assess}(\Phi(T), \Psi_u)$ in three steps.

*Slot binding.* The instantiated requirements refer to symbolic slots: the measure $m$, the comparison dimension $d$,
the outcome $y$, explanatory attributes, a time attribute and the scope $\Omega_u$. The Aligner binds each slot to an
attribute of $T$ using only table evidence. A concept phrase is reduced to its head concept (for example *survival* in
*survival rate of passengers*, *vaccinated* in *share of people fully vaccinated*). An attribute is a candidate binding
when the head concept is evidenced by the attribute itself: its name, its description, or, for binary attributes, its
value labels. The score combines the evidence for the head with the evidence for the remaining words, including the
documented measure kind (a requested *rate* matches an attribute documented as a rate) and the table documentation,
which contributes context but is never sufficient on its own. Geographic dimensions are bound through the geographic
level of an attribute; when a column mixes levels, the binding retains only values of the requested level. Requested
group values, dates and years are matched against observed values. A binding below the release threshold leaves the
slot unbound, and every binding records its score and evidence.

*Requirement evaluation.* Each instantiated requirement $\rho$ is evaluated by its registered predicate under its
evidence rule and receives the verdict supported, violated or unresolved together with the evidence used. Absence of
a binding never yields violation; violation requires evidence of a negation. Examples are a documented measure kind
that contradicts the operator contract (an existing rate or cumulative total cannot be averaged as observations by
$P_{\text{raw}}$); a geographic attribute whose observed level cannot provide the requested distinction (continent
aggregates for a comparison across countries); a full scan of the scoped rows that finds no member of a requested
group or no valid value for an included group; a table whose rows are aggregated cells for a prediction over
individuals; or the absence of any parseable time attribute for a trend. Scope restrictions are satisfied by observed
values, by the declared membership mapping, or by documented table-wide scope, and they define the row selection used
by all scoped counts. Soft indicators (completeness of the bound measure within scope, class balance, number of
labelled rows) take values in $[0, 1]$ or are unavailable when their denominator is undefined.

*Combination.* For a procedure $P$ with hard requirements $H^u_P$, the procedure state is supported if all hard
requirements are supported, violated if any is violated, and unresolved otherwise. The procedure score is
$$a_P = \begin{cases} 0 & \text{if } P \text{ is violated} \\ \frac{|\{\rho \in H^u_P : \text{supported}\}|}{|H^u_P|}\,\big(1 - \beta + \beta\,\bar s_P\big) & \text{otherwise,}\end{cases}$$
where $\bar s_P$ is the mean of the available soft indicators and $\beta = 0.2$. Unresolved requirements contribute
no support, so insufficient evidence lowers the score without being treated as violation. Across alternative
procedures the grounded intention is supported if at least one procedure is supported, violated if every eligible
procedure is violated, and unresolved otherwise, and $A(T, \iota_u) = \max_{P \in \mathcal{P}_u} a_P$. The Aligner
returns the categorical states, $A$, the bindings and every verdict with its evidence.

## 3.7 Table Ranking

The ranking function combines context matching and usefulness as $U(T \mid q_u, \iota_u) = F(r(q_u, T), A(T, \iota_u))$
when grounding succeeds, and $U = r(q_u, T)$ otherwise (Eq. 8). We use
$$F(r, A) = r\,\big(\lambda + (1 - \lambda)\,A\big), \qquad \lambda = 0.5,$$
which is nondecreasing in both arguments, maps $[0,1]^2$ to $[0,1]$, and satisfies $F(r, A) \le r$: usefulness
modulates topical relevance but cannot make an off-topic table relevant. A table with $A = 0$ keeps half of its context
score, so violated tables are demoted rather than removed, and a fully supported table keeps its full score. We
compare this form with the linear combination $F(r, A) = (1-\alpha) r + \alpha A$ and with a lexicographic order
(supported, unresolved, violated; then $A$; then $r$). Ties are broken by table identifier. The output is the ordered
list $\widehat{R}_u$ of the $k$ tables with the highest $U$, each accompanied by its verdicts and evidence.

---

## 4 Experimental Evaluation (setup)

**Corpus and benchmark.** IGBench-v1 contains 3,300 documented tables from Our World in Data (COVID-19), the UCI bike
sharing datasets and Rdatasets (Section *Dataset*, `docs/DATASET.md`). Requests are organised by topic; within a topic
they keep the subject fixed and vary the intention across the five families of the Intention Library. Each request
has a gold extraction, a gold grounding and graded usefulness labels for all tables of its topic cluster
(2 = useful for the stated intention, 1 = topical only, 0 = not relevant). The development set (36 requests, 11 topics)
was used to build the system; the held-out set (21 requests, 8 new topics) was written and labelled after the
Intention Library, profiler and Aligner were frozen.

**Systems.** Context-only rankers on the full input $u$ (BM25, TF-IDF, LSA, Sentence-BERT, hybrid) are compared with
the framework on top of each of them. The framework runs with (i) gold extraction and grounding, which isolates the
contribution of grounding and alignment; (ii) automatic rule-based extraction and expression-index grounding, which
requires no model; and (iii) LLM extraction and grounding. Instruction-aware and structure-aware retrievers
(e.g. instruction-tuned embeddings, TABERTA, semantic matching) are added as further context matchers.

**Metrics.** RQ1: nDCG@10 with graded gains, P@5, P@10, R@10, MRR and Useful@1 over requests with at least one useful
table, and the rate at which a topical-only table is ranked first. Paired approximate randomization tests (10,000
permutations) and bootstrap 95% confidence intervals compare each framework configuration with its context matcher.
RQ2: intention-swap accuracy, the probability that, for two requests of the same topic with different intentions, a
table useful only for the first ranks above a table useful only for the second in the first request's ranking (0.5
means indifference). RQ3: extraction (intention presence, argument and scope F1), grounding (status, family, variant,
binding accuracy), context-only fallback rate, and the precision and recall of the Aligner's supported state against
the usefulness labels. RQ4: ablations of the combination function, the soft indicators, $k$, the binding threshold
and gold versus automatic components; the running time of every stage (interpreter, context matching, grounder,
profiler, aligner, ranking) with cold and warm caches; and profiling and alignment time as a function of table size
on a random sample of the corpus.
