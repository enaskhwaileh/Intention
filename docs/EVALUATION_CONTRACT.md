# Intended-action table discovery: evaluation contract

> Current M0 refresh: preserves but excludes the separately authored local IL extension from this commit; classification, regression, forecasting and survival remain the requested Predict scope. This task performs audit, cleanup and planning only; no M1 implementation. See [the audit](REPOSITORY_AUDIT_M0.md) for current verification and compatibility inventory.

Version: M0 proposal, 21 October 2026. This document fixes proposed measurement conventions before experiments; it does not assert an executed benchmark or approved scientific design. Open decisions are explicit. Scope initially Compare and Predict, with direct-observation Compare first, explicitly confirmed by the researcher after M0 delivery. Aggregate-then-compare is outside the initial scope.

Audit basis: [repository audit](REPOSITORY_AUDIT_M0.md). Delivery sequence: [implementation plan](IMPLEMENTATION_PLAN.md).

## 1. Question and claims

Central question: **Does procedure-grounded assessment improve intended-usefulness ranking over strong methods receiving the same full request?**

Usefulness means a table can support the stated analytical use under a separately declared operation policy, population, prediction setting, and available evidence. Topic relevance is a distinct label. A method's IL requirements are predictions about usefulness, never its definition or its gold-label generator.

Primary comparison is paired usefulness nDCG@10 on a fixed, independently judged test universe. Report Compare and Predict separately and topic-balanced overall results only after both exist. No superiority claim is possible from current replay fixtures. The first small run is a feasibility pilot; passing contracts or obtaining nonzero rankings is not publication-quality evidence.

## 2. Source feasibility checked in M0

### Main benchmark: UCI/OpenML candidate families

The intended strategy is a curated collection of real tables across several independent topics and source families, with new independent Compare/Predict requests and judgments. No final corpus is selected in M0. Only the following family was inspected as a feasibility example; it cannot supply topic-disjoint evaluation by itself.

**UCI Bike Sharing, dataset 275.** The [official record](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) provides file names, variable definitions, DOI `10.24432/C5W894`, and CC BY 4.0 terms. A bounded read of the [279,992-byte archive](https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip) verified actual `day.csv`, `hour.csv`, and `Readme.txt` contents:

| Artifact | Observed content | SHA-256 |
| --- | --- | --- |
| Archive | Three members | `b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401` |
| `day.csv` | 731 rows, 16 columns; dates 2011-01-01 through 2012-12-31 | `a6bcf826782d3c0fbfdcbeead17cd0884185a0dafe8ff10cd48a874ee7ba18be` |
| `hour.csv` | 17,379 rows, 17 columns, including `hr` | `e03de4ee4ef4dc376ac6e04bf829673c6269e8eba5c60fa121640fa2f829504f` |
| `Readme.txt` | Local variable definitions and licensing section | `b92c8628622948bf0828c43a1b315d1517c3d7fd63654730d0dea379b8e88175` |

Observed columns include date, calendar/weather variables, `casual`, `registered`, and `cnt`; a direct comparison of counts on explicitly named dates is a possible request, subject to annotation and grain binding. Hour-to-day aggregation is a different procedure. For prediction, `casual` and `registered` reveal components of the target and require leakage review. Observed weather may not be available at a future forecast origin. The landing page reports 17,389 instances, differing from the scanned hourly count; season/temperature descriptions also differ between web metadata and the bundled README. Preserve both sources and resolve these differences before semantic annotations. These findings support feasibility only, not final usefulness labels.

**OpenML dataset 42712.** The [metadata API](https://www.openml.org/api/v1/json/data/42712) returned `Bike_Sharing_Demand`, version `2`, file ID `22044627`, format ARFF, target `count`, ignored attributes `casual`/`registered`, original UCI source, and a description of renamed categories and reversed normalization. It records license text `Public`, which needs reconciliation with the original source's terms. Metadata SHA-256: `23b62eff919b312c2787b3b5d976054728e92aeac4d97719788461d7e426a687`. **Only metadata was downloaded; the OpenML row file and checksum were not verified.** It is a derivative of the same Bikeshare family, not an independent topic/source for a split. Do not assume other OpenML versions share its transformations.

Inspection files are temporary under `/tmp/intention-m0-source-audit-20261021/`; they are not a committed benchmark, normalized corpus, or split. M1 must inspect additional families, all required table contents, licensing, metadata, and request feasibility before selection. Prefer tables with documented population, units, observation grain, and target/feature timing. Raw individual-level tables may require aggregation that the current Compare route excludes; reject unsupported requests or explicitly approve an additional procedure rather than labeling such tables inherently useless.

### External evaluation: FollowTable

Read the [paper](https://arxiv.org/html/2605.00400v1) and [public repository](https://github.com/AriKing11/FollowTable_Benchmark). Inspected repository tree `bdff0a70fdf0651276a8f22350466c327903b205` was not truncated. It contains table directories with 23,784 WQT, 9,546 WTR, 11,586 TArX, and 13,258 IndusTR files. These are inventory counts, not a completed content validation.

Inspected at that revision:

- `data/WTR/query_instruction.json`: downloaded 1,234,550 bytes; SHA-256 `8ce9ac29b95f9b198db3cf6bf7743d5625c84256b2f49a89ad9a2868738452e3`. Parsed 60 query records, 267 instruction records, no `valid!=1` entries. Fields include `query`, top-level `query_positive`, and `outs` containing `instruction`, `instruction_type`, `query_positive`, `instruction_positive`, `all_tables`.
- `data/WTR/tables/0.txt`: actual Markdown table with title and NBA numerical comparisons; current CSV/JSON profiler cannot directly read this format. No full table scan was performed.
- [Loader](https://github.com/AriKing11/FollowTable_Benchmark/blob/bdff0a70fdf0651276a8f22350466c327903b205/experiments/src/followtable_eval/data.py): preserves top-level query positives, validates table references, skips explicitly invalid instructions, and treats table files as text.
- [Evaluation instructions](https://github.com/AriKing11/FollowTable_Benchmark/blob/bdff0a70fdf0651276a8f22350466c327903b205/experiments/src/README.md) and [metric source](https://github.com/AriKing11/FollowTable_Benchmark/blob/bdff0a70fdf0651276a8f22350466c327903b205/experiments/src/followtable_eval/evaluation/metrics.py): native evaluation compares original-query and instruction rankings, supports binary nDCG, and calls its full-ranking metric `group_nwrd`; real top-100 pre-sort candidates are used without inserting positives.

**Compatibility gates:** its topical and instruction-compliance labels do not establish Compare/Predict procedural usefulness. Use native labels only for a separately named instruction-following track. A usefulness subset requires new independent annotations and explicit scope selection. Preserve original query/instruction linkage; all variants stay in one topic partition. Preserve hierarchical headers or mark unsupported parsing. Resolve table-to-source-family identity and duplicates; check overlap with WikiTables/TABERTA regression data. The inspected tree has no LICENSE file and repository metadata reports no license: public accessibility is not sufficient redistribution permission. Resolve terms for data and code before redistribution/reuse. Paper terminology IRS versus released `group_nwrd` needs a documented formula mapping, not an assumed synonym. No external usefulness result is claimed.

### Optional regression track

The author's [EDBT 2025 paper](https://velgias.github.io/docs/KhwailehV25.pdf) describes semantic matching with ExS, ANNS, and CTS and links `https://github.com/enas88/mira_gui`. That URL returned a moved-repository response in the connector; the exact current artifact/revision was not established. The paper discusses field/cell-level matching and an `all-mpnet-base-v2` encoder; a generic table-vector cosine adapter would not reproduce the published method.

The [TABERTA model card](https://huggingface.co/EnasKhwaileh/TABERTA) and [file listing](https://huggingface.co/EnasKhwaileh/TABERTA/tree/main) expose multiple variants, including a `7_hybrid_model_reg` subfolder. Card usage points to a different-looking model path (`TABERTA/7_hybrid_model_reg`); resolve the actual repository/subfolder, commit, tokenizer/pooling, and exact table serialization against the intended paper. The card lists AFL-3.0. Model/card availability alone does not verify a runnable faithful baseline. Original topical/QA/schema-grounding labels can support regression of their native tasks, not intended usefulness. Audit training/evaluation overlap before treating any derivative table family as external.

### M0 cleanup refresh verification boundary

The refresh re-opened the public [UCI Bike Sharing page](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), [FollowTable repository](https://github.com/AriKing11/FollowTable_Benchmark), [TABERTA model card](https://huggingface.co/EnasKhwaileh/TABERTA), and [Qwen embedding model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B). These remain accessible. No corpus/model download or inference was performed. Pinned-file hashes and detailed source observations above are preserved from the earlier audit, not claimed freshly reproduced. Source availability does not establish independent usefulness labels or remove the faithful-baseline/protocol gates.

## 3. Required data records (M1 implementation target)

All formats are versioned and closed; unknown keys, duplicate IDs, invalid references, and hash mismatches fail preflight. UTF-8 exact request text is retained. JSON/JSONL fits current conventions; no additional configuration parser is needed for the first implementation.

| Record | Required fields and invariants |
| --- | --- |
| Corpus table manifest | `schema_version, corpus_version, table_id, source_family_id, source_name, source_url, source_dataset_id, source_version, license_text, license_url, acquired_at, source_file, source_sha256, normalized_path, normalized_sha256, format, row_count, columns, metadata_refs, transformation_history, duplicate_group_id, selection_reason`. Source family represents original collection/study lineage, not hosting site. Record unknown metadata explicitly; unresolved legal/provenance gates prevent inclusion. |
| Public request | `schema_version, request_id, topic_id, text, language, authorized_context_refs, operation_policy_id, provenance, version`. Author-declared action may be stored for analysis separately, but runtime must infer action from the same public request supplied to all methods. No usefulness labels, gold bindings, or procedure IDs are exposed. |
| Topical judgment (evaluator-only) | `request_id, table_id, label=related|unrelated|unresolved, evidence_refs, assessor_id, guideline_version, timestamp, adjudication`. Never inferred from usefulness or retrieval scores. |
| Usefulness judgment (evaluator-only) | `request_id, table_id, label=useful|not_useful|unresolved, operation_policy_id, feasible_analysis_description, decisive_evidence_refs, missing_evidence, rationale, assessor_id, guideline_version, timestamp, adjudication`. No automatic IL-predicate-to-label mapping. |
| Requirement judgment (evaluator-only) | `request_id, table_id, procedure_reference, requirement_reference, gold_verdict=supported|violated|unresolved, evidence_refs, assessor_id, guideline_version, adjudication`. Separate diagnostic annotation after usefulness; versioned mapping to predicted requirements. |
| Discovery split | `split_version, seed, assignment_method, topic_ids, request_ids, source_family_ids, table_ids, duplicate_group_ids, corpus_hash, requests_hash, assignment_hash, exclusions`. Separate development, validation, test. |
| Prediction row split | `table_id, request_id, target_spec, unit_id_definition, time_column, prediction_origin, horizon, train_row_ids, validation_row_ids, test_row_ids, grouping_policy, purge_gap, seed, source_sha256, split_hash`. Stored separately from discovery splits; rows/entities/time leakage checks mandatory. |

Byte hashes identify exact source files; canonical-content hashes additionally support normalized-table identity. Preserve source IDs even if two files are byte-identical. Derivatives, hourly/daily versions, mirrors, and near duplicates share a source-family/duplicate grouping. Do not invent a new independent family for each file or host.

## 4. Independent annotation rubric

Before annotation, researchers freeze an operation policy expressing what transformations are allowed. The initial policy is descriptive comparison of observed numerical measures within one logical table; widening it requires a new policy version. Predict policy must declare classification/regression/forecasting/survival and prediction-time information. Neither policy is a list of current IL predicates.

- **Useful:** a reviewer can describe a valid analysis satisfying the whole request under the policy, with concrete table cells/rows and source documentation supporting measures, population, grain, and timing. Performance of a future model is not guaranteed by this label.
- **Not useful:** affirmative evidence establishes an incompatibility that prevents the requested use under the policy, with no allowed alternative procedure resolving it. Examples: documented wrong population; wrong measure with no allowed derivation; a complete scoped scan proves required observations absent. Explain the incompatibility independently of the implementation.
- **Unresolved:** relevant evidence is missing, contradictory, ambiguous, sampled inadequately, or requires external clarification. A promising column name alone cannot establish useful; non-observation in a sample cannot establish not useful. A model's inability to find a procedure is not a negative gold label.

Unsupported/ambiguous requests receive a request-level annotation and stay in an abstention/robustness stratum. They are not silently relabeled not useful for every table. Researchers may issue a separately versioned clarified request; retain both records.

Have two independent annotators inspect requests, table content, and source documentation, blind to system outputs, IL predicate names, baseline identity, and scores. Record initial labels and reasons before adjudication by a third reviewer or documented consensus. Report agreement (raw and three-class Cohen's kappa where applicable), disagreement patterns, and unresolved rates. Do not force consensus on missing evidence. Requirement diagnostics may expose the frozen requirement definition to assess its truth, but must not rewrite previously assigned usefulness labels. Evaluate requirement fidelity/omission separately so systems cannot improve verdict F1 by proposing only easy requirements.

Choose requests from independent analyst needs and available domain documentation, not templates reverse-engineered from IL success cases. Include topically related near misses, multiple viable procedures, insufficient metadata, unsupported transformations, prediction leakage cases, and no-useful-table cases. Avoid selecting the corpus exclusively for what the current system already handles.

## 5. Partitions and gold isolation

Build a graph connecting request topics, source families, derivatives, duplicate groups, and known relevance/judgment links. Assign connected components to development/validation/test so **both topic IDs and source-family IDs are disjoint**, including distractors. Keep paraphrases/action variants of one topic together. A giant connected component is a feasibility problem requiring redesign or more sources, not permission for silent leakage. Save exclusions and component membership. Proposed proportions are 60/20/20 only if the independent component count supports them; no numeric split is created in M0. A tiny first-day corpus remains development-only.

Development is used to author/debug the IL and tune adapters. Validation selects ranking policy, candidate depth, prompts, and hyperparameters. Freeze code/config/artifacts before test evaluation. Repeated inspection of test errors invalidates the untouched-test claim; changes require a new holdout/version. Pretrained model contamination cannot be excluded merely by disjoint local splits; record known training overlap and its limits.

For downstream prediction, create an independent row split within each eligible table: chronological with a justified gap for forecasting, entity/group-disjoint where observations repeat, otherwise appropriately stratified classification or seeded regression splits. Fit preprocessing only on training rows. The ranking evidence budget must exclude held-out outcomes and post-outcome features for this track. Dataset-level table discovery and downstream prediction are separate experiments, with separate hashes and eligibility.

Runtime gets only an exported public corpus/request/evidence bundle. Gold files live in an evaluator-only directory or separate evaluator environment; ranking schemas have no qrel path and ranking modules cannot import annotation loaders. Inference completes and hashes immutable predictions before the evaluator reads gold. FollowTable's mixed public/label JSON is split by a trusted preparation step; its positive IDs and `all_tables` pools never enter runtime candidate construction. Verify isolation by changing gold labels and by removing gold access entirely: predictions must remain byte-equivalent excluding declared timing/run-ID fields. Simple convention alone is insufficient.

## 6. Baselines and availability

Availability means runnable and verified in the **current checkout**. None of the requested baseline adapters is presently available there. Existing pretrained releases do not imply local adapter availability. No model weights were downloaded or used in M0.

| Baseline | Status | Required faithful integration / gate |
| --- | --- | --- |
| BM25 | **Requiring integration** | Review/port historical `4ef9ed9:src/intention/retrieval/retrievers.py` into current package; pin tokenization, fields, k1/b, IDF, and tie rules. Use full request. Verify against hand-computed scores. |
| Our semantic-matching method (EDBT 2025) | **Blocked** | Resolve author repository redirect and intended ExS/ANNS/CTS variant, paper-faithful field/cell aggregation, encoder revision, parameters, original preprocessing, and artifact licensing. Do not rename generic cosine similarity as this method. |
| TABERTA | **Blocked for a faithful run** | Public card/variant folders exist; pin intended variant and exact repo/subfolder/revision, serialization, pooling/tokenizer, license, and reference outputs. Do not substitute TaBERT or a generic sentence encoder. |
| Qwen3 embeddings | **Requiring integration** | [Official implementation](https://github.com/QwenLM/Qwen3-Embedding) provides query instructions, last-token pooling/normalization and model sizes. Candidate pilot: `Qwen/Qwen3-Embedding-0.6B`; freeze full revision/tokenizer, serialization, max length, truncation and precision after hardware preflight. Historical harness may supply reusable mechanics. |
| Qwen3 reranker | **Requiring integration** | Candidate pilot: `Qwen/Qwen3-Reranker-0.6B`; preserve official pair formatting and yes/no-logit scoring. Score identical candidate IDs; not a standalone first-stage retriever. Pin revision and budget. Larger models require a separately declared run. |
| Direct LLM usefulness assessment | **Requiring integration; execution gated** | Reuse optional provider/config/failure conventions, but add a distinct full-request/table-evidence assessor without IL or gold. Pin model/prompt, parse structured useful/not-useful/unresolved output, citations, score policy, retries, and spend cap. Transport mocks do not verify this baseline. Use a pretrained/local model or approved provider after M0. |

All primary baselines receive the exact same full request, including intended action and constraints. Query-only/topic-only retrieval is an explicitly labeled ablation, not the strongest comparison. Give methods the same public table facts, metadata, and authorized context; serialize those facts according to their faithful model formats. Record truncation and inaccessible evidence. Include an evidence-matched direct LLM baseline so a gain cannot be attributed solely to access to extra documentation/profile facts. Do not expose IL-derived decisions as baseline input. Precompute table evidence consistently; report its cost even when amortized.

No fine-tuning is needed for the first pilot. Parameter selection uses development/validation only. If a published method cannot be integrated faithfully, report it as blocked and narrow claims; never fill its result row with an approximation or fabricated zero. A partial pilot with BM25/Qwen is permissible, but not evidence against the missing published methods.

## 7. Two evaluation settings

**Controlled reranking:** freeze candidate IDs/order/hash for each request before scoring and before accessing gold. For a very small pilot, use every table in the public partition to avoid candidate selection effects. At scale, freeze a union of declared full-request BM25/dense top-N lists with deterministic merging/capping and no gold injection. All rerankers receive identical candidates and evidence budgets. Report candidate recall, corpus-relative primary nDCG, and optional clearly named candidate-conditional nDCG. Never replace a hard candidate with a known positive.

**End-to-end retrieval:** each first-stage method searches the same public corpus partition from the full request. A reranker is paired with a declared first-stage method and candidate depth. Report candidate Recall@N and final metrics; an absent useful table cannot be recovered by reranking. Include candidate generation latency/cost and index-build cost separately. Use a shared-candidate experiment to isolate assessment from candidate quality before interpreting end-to-end gains.

Freeze candidate depth, per-table evidence selection, preprocessing, and runtime behavior before held-out evaluation. Log all failures and abstentions. Unavailable methods are not executed; failed individual requests from an otherwise runnable system remain in the denominator, subject to the metric eligibility rules below.

## 8. Metric conventions and incomplete judgments

### Label eligibility

Gold `useful=1`, `not_useful=0`; unresolved and unjudged have **no binary gain assigned**. Unjudged means no annotation; unresolved means an annotation that cannot decide. Preserve both in files and reports.

The primary confirmatory universe consists of requests whose entire frozen evaluation corpus partition has adjudicated binary usefulness judgments and at least one useful table. This strict rule makes denominators and ideal rankings identifiable and identical across systems. A small exhaustively judged corpus makes it achievable; if it is unaffordable, **do not report a confirmatory primary score**. Report a clearly labeled pilot/pooled diagnostic and redesign annotation coverage before scaling.

Do not remove unresolved items from ranked lists and renumber positions, or count them as known negatives. For incomplete pools report judged@10, known-useful hits@10, and separately labeled sensitivity scenarios (unknown gains all zero versus all one, with recomputed ideal gains); these are assumptions, not guaranteed metric bounds or primary scores. Expand judging using method-blind pooled results plus random corpus samples, recording pool depth, contributors, and selection bias. Do not use pooled qrels to claim exhaustive corpus recall.

Requests with **no known useful table** are separated into (a) fully judged no-positive corpus, and (b) incomplete/unresolved corpus. For (a), nDCG/recall are undefined and excluded from their mean, with counts reported; assess correct abstention and false recommendations separately. For (b), no conclusion that no useful table exists is allowed. Request-level ambiguity/unsupported cases also form a named robustness stratum. Report every eligibility/exclusion count so favorable filtering is visible.

### Definitions

| Metric | Frozen convention |
| --- | --- |
| **Usefulness nDCG@10 (primary)** | `DCG=sum(g_i/log2(i+1), i=1..10)` with binary gains, unreturned positions zero. `IDCG` uses **all useful tables in the frozen corpus judgment universe**, not just returned/candidate items. Divide when IDCG>0; otherwise N/A. Candidate-conditional IDCG is supplementary only. |
| Success@1 | 1 if the first returned table is useful, otherwise 0, on the same primary eligible requests. Empty ranking/abstention/failure = 0. No-positive stratum reported separately. |
| Recall@10 | Distinct useful IDs in first 10 divided by all useful IDs in the frozen corpus, for eligible requests. Do not divide by useful tables in retrieved results alone. |
| Candidate Recall@N | Distinct useful IDs among actual first-stage candidates divided by all useful corpus IDs. Report N, candidate count and positive-miss requests. Conditional reranking scores cannot hide these misses. |
| Requirement-verdict macro-F1 | Three classes supported/violated/unresolved. Align predictions to independently annotated fixed procedure/requirement instances; missing/failed verdicts map to unresolved and are separately counted. Per-class `2TP/(2TP+FP+FN)`, zero for zero denominator by convention; fixed three-class macro, confusion matrix, counts and per-predicate breakdown. Also report extraction fidelity, omitted/extra requirements, and a conditional-on-correct-grounding analysis; conditional F1 alone is insufficient. |
| False-support rate | Among predicted-supported requirements with adjudicated **decidable** gold, fraction whose gold is violated. Zero denominator = N/A. Separately report predicted support on unresolved gold (“unsupported assertion rate”) over all adjudicated predicted-support cases; never claim missing evidence is a verified violation. Report both so abstention cannot conceal unsupported claims. |
| Coverage | Request grounding coverage = grounded requests / all attempted; verdict decision coverage = supported-or-violated / all expected requirement instances; recommendation coverage = requests with a non-abstaining recommendation / attempted; judged@10 = decided judged returned positions / returned positions (empty = N/A). Include unresolved, unjudged and failure counts separately. |
| Latency | Wall-clock milliseconds per stage/request: serialization, inference, retrieval, assessment, ranking, total; median/p95 with sample count; cold and warm runs separated; batch size/concurrency/hardware recorded. Shared indexing/profiling costs reported separately and amortization stated. |
| Cost | Actual provider input/cached/output tokens, calls/retries, dated tariff, currency, total/per-request cost. Unknown usage is null with reason, never zero. Local models: zero external API charge plus measured wall/device time and an explicit compute-cost assumption if estimated. Include preprocessing and failed calls. |

Reject duplicate ranked IDs and out-of-corpus IDs; do not silently deduplicate malformed predictions. Tie-break by score descending then stable table ID ascending, or a documented deterministic ordinal key for the procedure method. Rank fewer than 10 without padding fake tables. A request failure yields an empty ranking and zero retrieval metrics on an otherwise eligible positive request; failure counts remain prominent. Invalid/corrupted entire run artifacts fail evaluation, not a normal result row.

Aggregate request scores within topic first, then average topics equally. Preserve per-request and per-topic scores and action strata. Compare systems using paired differences on the same eligible topics. When the independent topic/component sample supports it, compute 95% paired cluster-bootstrap intervals with 10,000 resamples and a recorded seed; use the larger connected leakage component as resampling unit if dependencies span topics. Predeclare a pragmatic gate (e.g. at least 20 independent test units) before confirmatory use; it is not a guarantee of power. Below that gate report descriptive pilot differences and sample counts, not significance claims. Design the eventual sample size from development variability and a scientifically meaningful effect, without inspecting holdout effects. Declare the primary baseline/comparison before test runs; label other comparisons exploratory or adjust for multiplicity.

## 9. Run provenance and reproducibility

One planned experiment entry point extends the existing CLI:

```sh
python -m intention_grounding.cli --config configs/experiments/compare_pilot.json
```

**This flag/config does not exist yet.** It is an M2/M3 implementation target, not a command to run in M0. The config selects runtime public data/splits, procedure catalog, model registry, candidate setting/depth, evidence limits, frozen ranking policy, seed, device, budgets, and a versioned output root. An evaluator subprocess alone receives the separate evaluation config and gold location; these are never supplied to ranking components. The same command launches the two isolated phases after inference artifacts have been finalized.

Each unique output directory must include resolved redacted configuration/hash; code commit plus dirty diff hash (confirmatory runs require clean code); Python/dependency lock and hardware; model/checkpoint/tokenizer revisions and prompt/serialization hashes; AB/schema versions/hashes; corpus/request/split/row-split/candidate/index hashes; table/source evidence; interpretations and separate procedure bindings; per-requirement verdicts and evidence; immutable scored predictions; stage failures; timing; token/cost accounting; evaluator/judgment versions; eligibility counts; per-request/per-topic/aggregate metrics; and a manifest listing artifact hashes and completion state. Interrupted runs cannot appear completed. Atomic publication and strict cache keys prevent stale evidence/predictions from crossing dataset/model versions. No secrets or raw exception headers in logs.

## 10. Decisions requiring researcher review

1. Confirm the current methodology source; no intended-action paper manuscript is available in this checkout. Resolve contradictions with historical weighted-axis/topical-only design.
2. **Resolved:** the researcher confirmed direct-observation Compare first. Aggregate-then-compare remains outside the initial scope; widening the operation policy requires a later explicit decision. Do not select tables/labels to conceal unsupported transformations.
3. **Catalog scope confirmed:** classification, regression, forecasting and survival are separate Predict branches. **Open:** pilot order, task-specific prediction-time availability, target/population/horizon, survival follow-up policy, downstream success criteria and the current methodology-paper location. Generic row-count thresholds are not justified defaults.
4. Approve independent annotators, operation policies, topic/family grouping, and feasible exhaustive pilot judgment effort. Decide whether source metadata conflicts can be resolved.
5. Review the proposed ordinal ranking/abstention policy in the implementation plan; it is a transparent pilot hypothesis, not a validated scientific optimum.
6. Resolve published baseline artifacts, FollowTable terms/protocol and source overlap, then choose model sizes/hardware and execution budget. No automatic paid or large-download run follows from M0.

These decisions gate later milestones. Their absence does not prevent delivery of this audit and plan; it prevents silently implementing invented science.
