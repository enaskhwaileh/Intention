# Dataset recommendation and IGBench construction

## What the evaluation needs

The paper claims that usefulness depends on the intended analysis, not only on topical relevance. Testing that claim
requires tables that

1. share a topic but differ in what they can support: observational unit (individual vs. aggregate rows),
   grain (daily vs. yearly, country vs. continent), measure kind (counts vs. rates vs. cumulative totals), structure
   (long, wide, aggregated cells) and coverage (period, geography);
2. carry real documentation (titles, descriptions, attribute descriptions), so that requirements on meaning can be
   assessed from evidence rather than column names alone;
3. come with requests that keep the topic fixed while changing the intention (RQ2), across the five families of the
   Intention Library (compare, aggregate, predict, explain, monitor);
4. have graded usefulness judgements *conditional on the intention*, among enough topical distractors to make
   ranking non-trivial;
5. are public, licensed for research, and reproducible from pinned sources.

## Existing benchmarks

| Benchmark | Unit / corpus | Queries and labels | Fit for intention grounding |
|---|---|---|---|
| TARGET (Ji et al., 2025) | Tables from OTT-QA, FeTaQA, TabFact, Spider, BIRD | QA / fact-checking / text-to-SQL questions; relevance = the table that answers the question | Topical relevance for downstream generation; no analytical intention and no notion of a table being on-topic but unusable. Useful as a context-matching sanity check. |
| NLCTables (Cui et al., SIGIR 2025) | 22,080 tables, 627 queries | Query table + natural-language conditions (NL-only, union, join, fuzzy); 21,200 relevance annotations | Conditions describe table content and compatibility, not the analysis to be performed. |
| FollowTable (Jin et al., SIGIR 2026) | Instruction-following table retrieval | Topic + explicit instruction constraints (inclusion, exclusion, column semantics, entity centering, aggregation level); IRS metric | Closest: "aggregation level" and "column semantics" constraints overlap with our str/sem requirements. Instructions are stated constraints, whereas our requests state an analysis whose requirements must be derived. Recommended as the external benchmark once its data is public. |
| CS-TDS / KATS (Wei et al., VLDB 2026) | Dataset mentions in CS papers | Task descriptions; binary labels from the dataset actually used | Dataset entities, not tables; no table evidence to assess. |
| LakeBench (Deng et al., VLDB 2024) | Data lakes | Join / union discovery | Compatibility, not analytical usefulness. |

None of them labels usefulness *conditional on the analytical intention*, and none pairs requests that share a topic
but differ in intention. A purpose-built benchmark is therefore part of the contribution; external benchmarks serve
as secondary evidence of generality.

## Recommendation

**Primary: IGBench (built in this repository).** Real, documented open tables organised into topic clusters, with
intention-paired requests and graded intention-conditional labels.

- *COVID-19* (Our World in Data, CC BY 4.0, commit `dc00e72`): 12 tables that reproduce the situation of Figure 1 with
  real data: country-by-date vaccinations; vaccination by age group (rates within groups) and by manufacturer
  (cumulative counts); US states; hospital indicators in long format; testing; excess mortality; daily cases in long
  and wide format; a latest-value country profile (one row per country, with continent and demographics); a regional
  summary (continent aggregates only, the analogue of Table A); a weekly country panel. The derived tables are
  documented in the manifest (`derivation`).
- *Bike sharing* (UCI 275 and 560, CC BY 4.0): daily and hourly Washington DC counts and hourly Seoul demand.
- *Rdatasets* (commit `1dcc2bf`, 3,285 tables after filtering ≤100k rows, ≤5 MB, ≥1 numeric attribute): datasets
  shipped with CRAN packages, with R help pages parsed into table and attribute documentation. It provides both large
  numbers of realistic distractors and natural topic clusters whose members differ in structure: Titanic (passenger
  rows vs. contingency tables), wages (hourly vs. weekly vs. annual, person-level vs. averages per age), housing
  (house sales vs. town medians), diabetes, air quality, cars, births, life expectancy, crime, experiments.

| | Value |
|---|---|
| Tables | 3,300 (OWID 12, UCI 3, Rdatasets 3,285; 102 source families) |
| Attributes | 47,283; 55% with documentation; 542 tables without attribute documentation |
| Development queries | 36 over 11 topics (31 with an intention, 3 without, 1 insufficient by design, 1 with no useful table); 476 judgements |
| Held-out test queries | 21 over 8 new topics; 238 judgements; authored and labelled after the design freeze |
| Labels | 2 useful / 1 topical only / 0 not relevant (default); notes record the reason for borderline labels |

**Secondary (generality, RQ1):** FollowTable, mapping its aggregation-level and column-semantics instructions to
Intention Library variants and reporting nDCG and its Instruction Responsiveness Score; optionally the BIRD part of
TARGET for context matching at scale.

## Why not the earlier vaccine benchmark

The earlier plan assembled five vaccine tables (rollout, adverse events, effectiveness, trials, hesitancy) partly
from access-restricted sources (VigiBase) and partly synthetically. IGBench keeps the same domain for the running
example through Our World in Data, but uses only public, documented tables, adds thousands of distractors, and covers
several domains, so results are not tied to one hand-built scenario.

## Labelling protocol (to finalise before reporting)

1. Two annotators judge every pooled table (all cluster tables + top-20 of every system) for each query, reading the
   table documentation and a sample of rows, using the definitions above. They do not see system outputs.
2. Disagreements are adjudicated by a third annotator; report Cohen's κ per label level.
3. A table is *useful* (2) when it contains the data the stated analysis needs without combining tables; *topical*
   (1) when it is about the requested subject but cannot support the analysis as stated; otherwise 0.
4. Freeze the labels, the IL release and the system configuration before running the held-out evaluation.

The current labels were drafted by the framework author with assistance and are marked
`draft_author_labels_unreviewed` in the benchmark files; the evaluation scripts report this status in every result.

## Extending IGBench

Add a topic by listing its cluster tables in `benchmarks/igbench_v1/build_queries.py` (or a new builder), writing
3–5 requests that keep the topic and vary the intention, and labelling every cluster table. Any CSV collection with
documentation can be added to the corpus through `corpus.py` (records: `table_id, title, description, path,
columns[{name, description}]`). A target size for the paper is about 150 requests over 30 topics.
