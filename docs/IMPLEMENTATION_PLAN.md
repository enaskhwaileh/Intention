# Incremental implementation plan

> Supporting appendix. Start with the [main project guide](../README.md) for current architecture, demonstration, models and testing. Historical audit statements are dated records, not current capability claims.

> Current M0 refresh: preserves the previously authorized IL extension (23 families, including classification, regression, forecasting and survival). This task performs audit, cleanup and planning only; no M1 implementation. See [the audit](REPOSITORY_AUDIT_M0.md) for current verification and compatibility inventory.

Milestone 0 delivery, 21 October 2026. Only M0 is performed in this task. All paths and commands in M1–M5 are explicit future targets; new test/config/module names do not claim existing functionality.

Researcher decision recorded after M0 delivery: retain direct-observation Compare first; aggregate-then-compare remains outside the initial scope. Predict catalog scope is confirmed as classification, regression, forecasting and survival. The pilot order, task-specific policies and any newer methodology-paper location remain unresolved. This clarification does not authorize starting M1.

Read with [the audit](REPOSITORY_AUDIT_M0.md) and [evaluation contract](EVALUATION_CONTRACT.md). Continue from `2833adbed071de88574b6fd18437934680cfb241` and preserve the current `intention_grounding` package, CLI, interpreter validation, replay fixtures, IL inheritance, and provider-error handling. Do not restore a parallel `src/intention` pipeline. Historical functions may be selectively ported with attribution/revision notes and revised contracts.

## Smallest complete vertical slice

One explicit descriptive Compare request, multiple real tables with verified metadata, full-request candidates, grounded procedure requirements, evidence-backed three-valued verdicts, a reproducible ranking, and independently judged evaluation. Start with direct observed measures on one logical table as specified in the current IL; aggregation, joins, inference, conversions and forecasting remain explicit unsupported routes until separately specified. Prediction expands the same interfaces in M4.

A single table and replayed response demonstrate mechanics but cannot evaluate discovery. A real-data pilot must include useful candidates and topically related incompatible/unresolved candidates, with annotations independent of the IL. The selected corpus must make this possible without treating artificially altered tables as real benchmark observations.

### A. Request → interpretation → procedures and requirements

Preserve interpreter schema 1.0 and exact text/evidence offsets unless an additive capability requires an explicitly versioned migration. Runtime `Request` carries request ID, exact text, language, authorized context, and operation-policy version. Gold action/binding annotations are evaluator-only. Reuse `interpret()`'s separation of provider failure and semantic status.

Evolve the single-card output into a versioned grounding envelope:

```text
GroundingEnvelope
  schema_version, request_id, request_hash, interpretation_ref, il_version/hash
  status: grounded | ambiguous | insufficient_input | unsupported |
          inconsistent_input | invalid_interpretation | provider_failure |
          invalid_model_response
  action_instances[]: {id, interpretation_action_ref, bindings, evidence_refs}
  procedures[]: {id, action_instance_id, procedure_definition_id, steps,
                 bindings, binding_provenance, requirements[], requirement_logic}
  goal_logic: all_of(action instances) or explicitly accepted any_of(...)
  applicability: per-procedure supported/unresolved/unsupported with reasons
  candidates[], missing_arguments[], reasons[], provider_metadata
```

Each procedure is a distinct legitimate way to accomplish the same resolved action. Do not merge its requirements with another procedure into one stronger conjunction. Preserve procedure-local role bindings and shared observation variables. Action hierarchy remains separate from procedure order. For an initially supported goal, procedures may contain only one direct-observation step; the envelope still supports multiple alternatives without a redesign.

Each requirement has stable ID scoped to procedure, originating action/template/version, predicate, axis, modality (`required|preferred|forbidden`), bound arguments, table/observation scope, activation provenance and request evidence refs. The grounder creates requirements, never table verdicts. No runtime creation of arbitrary predicates. Validate closed types, abstract actions, all required roles, exact evidence, semantic selection gates, and reference resolution. Full-grid coverage requires the explicit certificate described in the canonical IL or returns unresolved/unsupported; never silently replace it with available observations.

**Semantics:** competing interpretations remain ambiguous and cannot become a convenient `any_of`. Explicitly accepted goals may use `any_of`; joint goals require `all_of`. Alternative procedures within a resolved goal use `any_of` with all separate branch evidence retained. Unsupported procedure != useless table. No guessed values, inherited legacy statistical thresholds, or model-confidence shortcuts. Reject a partially fulfilled joint request as complete. Existing consumers can receive a legacy single-card projection only when there is exactly one complete procedure; never silently collapse multiple branches. Record projection/schema version.

### B. Table → profile evidence

Extend `profile_table()` rather than replacing it. Keep immutable raw-file hashes and primitive scans. A profile v2 adds table/source-family identity, metadata provenance, normalized logical observation relations, role-binding candidates, scoped facts, and method/inspection completeness:

```text
EvidenceFact = {id, table_id, predicate_or_fact, value,
  bindings, observation_relation_id, source_refs[{file_hash,locator}],
  extraction_method/version, scope, completeness: full|sample|metadata_only,
  observed_at, dependencies[], limitations[], conflict_refs[]}
```

Locators identify columns, row IDs/cells, metadata passages, or a reproducible scoped scan. A negative finding needs a complete scan over a justified scope and identity. Sampling can witness a present value, not prove its absence. Header semantics/units/population need cited metadata or a reviewed evidence-producing semantic mapper, not primitive type inference. A mapper's unsupported hypothesis remains unresolved. Dependency IDs prevent a derived comparability claim being counted twice as independent evidence.

For M2, implement one supported representation with complete evidence first, and mark other representations unsupported; do not pretend broad long/wide/Markdown support. Preserve the existing source CSV/JSON profiler contracts with explicit version conversion. No manually supplied “suitable” flags become profile facts.

### C. Request + evidence → verdicts → ranking

`assess(grounding, table_profile, evidence_policy)` returns one record for every requirement of every procedure:

```text
RequirementVerdict = {request_id, table_id, action_instance_id, procedure_id,
  requirement_id, verdict: supported|violated|unresolved,
  evidence_refs[], missing_evidence[], reason_code,
  evaluator_id/version, scope, bindings, dependency_refs[]}
```

Supported/violated decisions require evidence refs that resolve to the exact input profile/source version. Unresolved decisions cite inspected evidence and a missing/conflicting-evidence record; when no data exist, reference a provenance-bearing inspection failure/absence record rather than inventing supporting facts. Require no empty unexplained verdicts. Contradictory facts yield unresolved/conflict or a validation failure.

Map old `unknown` to `unresolved` only at an explicit versioned boundary; old artifacts retain their original vocabulary. Required predicates use all-of: any violation → violated; all supported → supported; otherwise unresolved. Any-of alternatives: any supported branch → supported; all violated → violated; otherwise unresolved. A forbidden requirement reverses a decisive predicate truth, while missing evidence stays unresolved. Preferred requirements do not become hard gates. Evaluate each procedure separately before the goal formula. Runtime errors remain distinct from substantive violations.

**Proposed pilot ranking policy, requiring scientific review:** use a transparent lexicographic order `(goal_evidence_state, full_request_retrieval_score, stable_table_id)`, with supported before unresolved before violated; retrieval score descending and table ID ascending. Preserve the three states as categorical evidence summaries, not probabilities. Keep every candidate in output; recommendation status can abstain when no supported goal exists. Do not reward shorter procedures by counting satisfied predicates, double-count derived facts, or add unsupported numeric axis weights. Unknown has no numeric satisfaction value. A best-supported procedure may determine a table's goal state only under the explicit any-of semantics; save all alternatives and the selected explanation. If interpretation is unsupported/ambiguous, retain a separately labeled topical fallback ranking and abstention, never claim procedural support.

This ordering is a testable baseline policy, not an established optimum; compare it with retrieval-only and direct LLM assessment. Frozen development/validation work may select another justified policy before held-out testing, with a new version and no test-based tuning. Unknown must not silently become violation through scoring. Failure and abstention policies enter the evaluation denominators.

### D. Runtime/evaluation boundary and one command

Extend `intention_grounding.cli` with a config-file experiment path, keeping its existing flags/replay path working. JSON configs follow existing dependencies and conventions. Only the evaluator process may open gold. Runtime reads a public bundle, completes immutable prediction artifacts, then the orchestrator starts evaluation in a separate context. The evaluator may read runtime results; the ranker may not read evaluation records or label-derived candidate lists.

Planned command (not implemented in M0):

```sh
python -m intention_grounding.cli --config configs/experiments/compare_pilot.json
```

Output contract and all required run identities are defined in [evaluation contract §9](EVALUATION_CONTRACT.md#9-run-provenance-and-reproducibility). Config must explicitly select network permission/budget, model availability, corpus/split hashes, candidate regime, evidence policy, ranking version and output root. Default test config is offline; no automatic download/train/live-call fallback. Missing models or metadata produce an explicit blocked/failure state. Preserve credentials outside configs and logs.

## Milestone 0: audit and evaluation contract (this task)

**Purpose:** establish actual capabilities and provenance, test current mechanics, define reviewable contracts and a feasible staged study.

**Dependencies:** current checkout and readable project documents; small public metadata/source reads; offline test dependencies. No scientific design choices need to be invented to complete the audit.

**Files:** maintain `docs/REPOSITORY_AUDIT_M0.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/EVALUATION_CONTRACT.md`, README and repository map. Bounded terminology aliases/prompt prose and verified redundant-file removals are recorded in the audit; preserve the pre-existing IL extension.

**Deliverables:** verified branch/commit/status and remote-main relation; component matrix and reproducible gaps; source/baseline feasibility; data/annotation/split/metric contracts; exact staged plan. Existing outputs classified by provenance.

**Verification:** commands and outcomes in audit §5; 47 offline tests, 13 replay cases, CLI smoke, compileall, documentation links/whitespace, `git diff --check` and final `git status --short --branch`.

**Acceptance:** three consistent documents; no unsupported accuracy/retrieval claims; scientific/access blockers explicit; existing files preserved; no M1 implementation, merge or push. This task stops when these conditions hold.

## Milestone 1: data contracts and evaluation readiness

**Purpose:** create trustworthy inputs and evaluation boundaries before building retrieval against unverified labels.

**Dependencies:** M0; confirmed direct-observation Compare scope; researcher decisions on Predict pilot order and task-specific policies (may remain deferred to M4), methodology authority, and annotation resources; licensed/inspectable candidate data. One family is insufficient for disjoint evaluation.

**Exact planned files:**

- Add `intention_grounding/schemas/{corpus,request,judgment,discovery_split,prediction_row_split}.schema.json`.
- Add `intention_grounding/benchmarks/{__init__,manifest,public_bundle,splits}.py` and evaluator-only `intention_grounding/evaluation/{__init__,judgments}.py`.
- Add `configs/benchmarks/pilot_sources.json`; add `data/manifests/pilot-v1.jsonl`, `data/requests/pilot-v1.jsonl`, `data/splits/pilot-v1.json` **only after selection/validation**, and separate controlled-access `data/annotations/pilot-v1/` records as license/access permit. Raw/normalized data remain ignored per existing `.gitignore`.
- Add `docs/ANNOTATION_PROTOCOL.md`, `docs/DATA_PROVENANCE.md`; update `README.md` (repository layout), `README.md` to fix environment instructions and link the current contracts.
- Add `tests/test_benchmark_contracts.py`, `tests/test_split_isolation.py`, `tests/test_gold_isolation.py`; update package data in `pyproject.toml` for new schemas.

**Deliverables:** closed schemas; truthful source/version/license and immutable hashes; independent label workflow; duplicate/source-family graph; public export free of labels; topic/family-disjoint manifests or an explicit development-only pilot designation. Audit each candidate's actual rows and metadata. Select no final dataset before these checks.

**Verification commands (future):**

```sh
python -m unittest discover -s tests -p 'test_benchmark_contracts.py' -v
python -m unittest discover -s tests -p 'test_split_isolation.py' -v
python -m unittest discover -s tests -p 'test_gold_isolation.py' -v
python -m intention_grounding.benchmarks.manifest --validate configs/benchmarks/pilot_sources.json
python -m unittest discover -s tests -v
```

**Acceptance criteria:**

1. Every selected table is loadable and linked to source/version/license, bytes/hash, documented transformations, source family, and metadata conflicts. UCI/OpenML mirrors cannot cross partitions. Missing metadata blocks selection or is explicitly unresolved; CLI's WikiDBs fallback cannot label a different source.
2. Independent requests and topical/usefulness judgments use useful/not-useful/unresolved evidence rubric; two-annotator/adjudication protocol is ready and at least a small pilot is independently reviewed. No generated gold from IL or model outputs.
3. All IDs/references/hashes validate; duplicate IDs, missing files, corrupt hashes, split overlap and derived-source leakage fail. Public export contains no label/gold binding/candidate-positive fields.
4. Development/validation/test topic and family sets are disjoint if a split is claimed. Insufficient independent groups produce a documented development-only dataset, not a fake holdout. Prediction row-split schema is distinct even if downstream experiments are deferred.
5. Frozen metric/eligibility conventions are accepted before experiments; annotated unresolved/unjudged/no-positive cases survive round-trip loading. Existing 47-test behavior remains passing.

No retrieval experiment is required for M1. Its acceptance does not imply final scientific sample size or publication readiness.

## Milestone 2: one complete Compare pipeline on real tables

**Purpose:** complete the existing vertical slice through candidates, substantive evidence assessment, and ranking.

**Dependencies:** M1 public corpus/requests, settled Compare operation policy, evidence definitions and provisional ranking policy; pretrained resolver access if used. Paid calls remain opt-in under an explicit run budget.

**Exact planned files:**

- Modify `intention_grounding/{action_base,grounder,profiler,aligner,cli}.py` and canonical `intention_grounding/docs/ab_proposal/action-base-v0.2.json` and `docs/INTENTION_LIBRARY.md` with version migration notes; preserve old replay compatibility.
- Add `intention_grounding/schemas/{grounding,profile,verdict,ranking,experiment}.schema.json`.
- Add `intention_grounding/{evidence,predicates,ranking,experiment}.py`, `intention_grounding/retrieval/{__init__,bm25,serialization}.py`, and `intention_grounding/experiment_config.py`.
- Add `configs/experiments/compare_pilot.json`, `configs/experiments/compare_offline_smoke.json`, `configs/ranking/compare_v1.json`; update `pyproject.toml`, `README.md`, `README.md` (repository layout), and `notebooks/pipeline_walkthrough.ipynb` as necessary for the same pipeline.
- Modify `tests/test_pipeline.py`; add `tests/test_grounding_procedures.py`, `tests/test_profile_evidence.py`, `tests/test_requirement_verdicts.py`, `tests/test_ranking.py`, `tests/test_experiment_artifacts.py`.

**Deliverables:** strict nonabstract/multi-procedure grounding; explicit unhandled-goal/coverage outcomes; one real supported table representation; scoped relational/metadata evidence; three-state verdicts with locators; full-request BM25 candidate retrieval; deterministic ordinal ranking/abstention; config-driven unique run manifests and predictions. Port historical BM25 mechanics only after correctness review. Reuse current interpreter validation rather than adding a second extraction path.

**Verification commands (future):**

```sh
python -m unittest discover -s tests -p 'test_grounding_procedures.py' -v
python -m unittest discover -s tests -p 'test_profile_evidence.py' -v
python -m unittest discover -s tests -p 'test_requirement_verdicts.py' -v
python -m unittest discover -s tests -p 'test_ranking.py' -v
python -m unittest discover -s tests -p 'test_experiment_artifacts.py' -v
python -m intention_grounding.cli --config configs/experiments/compare_offline_smoke.json
python -m unittest discover -s tests -v
```

**Acceptance:** real request/table run has multiple ranked candidates and complete provenance; all supported/violated verdicts cite resolving evidence; missing/sample-only/conflicting evidence stays unresolved; all procedure branches and joint/alternative semantics are preserved. Abstract IDs and malformed proposals fail safely; explicit coverage is not dropped; profiler preserves empty headers and boolean identity. A hand-reviewed positive, a genuine incompatible candidate and an unresolved case exercise the three states without deriving gold from code. No assertion of superiority. Repeated offline run produces identical semantic predictions (excluding run IDs/timestamps/timing); altered input hashes invalidate caches. Gold access cannot change ranking.

## Milestone 3: baselines and controlled evaluation

**Purpose:** test the central hypothesis against faithful full-request methods with identical candidates and evidence access.

**Dependencies:** M2, independent adjudications, executable evaluation contract, exact published baseline artifacts, model revisions/hardware, and an approved compute budget. Blocked methods stay visibly blocked; a limited pilot is not a full baseline study.

**Exact planned files:**

- Add `intention_grounding/baselines/{__init__,registry,semantic_matching,taberta,qwen_embedding,qwen_reranker,direct_llm}.py`; reuse M2 BM25 as the BM25 adapter.
- Add `intention_grounding/evaluation/{metrics,runner,statistics,followtable}.py` and `intention_grounding/benchmarks/followtable.py` after terms/protocol gates; extend `experiment.py`, `experiment_config.py`, `cli.py` for isolated evaluation and multi-method configs.
- Add `configs/baselines/registry.json`, `configs/evaluation/pilot.json`, `configs/experiments/compare_controlled.json`, `configs/experiments/compare_end_to_end.json`; update optional dependencies in `pyproject.toml`, and add `requirements/experiments.lock` after environment resolution.
- Add `tests/test_baseline_contracts.py`, `tests/test_metrics.py`, `tests/test_evaluation_runner.py`, `tests/test_followtable_adapter.py`; extend `tests/test_gold_isolation.py`, `tests/test_experiment_artifacts.py`; update `README.md` (repository layout) and `README.md`.

**Deliverables:** explicit available/requiring-integration/blocked registry; pinned pretrained adapters and reference-output parity for published methods; controlled candidate export/hash; full-request and evidence-matched comparisons; unjudged/unresolved-safe metrics, topic-level paired estimates, native FollowTable track kept distinct. No fine-tuning.

**Verification commands (future):**

```sh
python -m unittest discover -s tests -p 'test_baseline_contracts.py' -v
python -m unittest discover -s tests -p 'test_metrics.py' -v
python -m unittest discover -s tests -p 'test_evaluation_runner.py' -v
python -m unittest discover -s tests -p 'test_gold_isolation.py' -v
python -m unittest discover -s tests -p 'test_followtable_adapter.py' -v
python -m intention_grounding.cli --config configs/experiments/compare_controlled.json
python -m intention_grounding.cli --config configs/experiments/compare_end_to_end.json
```

Last two commands are executed only after model/budget/data preflight; tests use offline fixtures and do not download weights or call paid services.

**Acceptance:** every method sees the same full request; controlled candidates match exactly and contain no inserted gold positives; published-method identity/serialization verified or explicitly blocked. Hand-calculated nDCG/recall/F1 cases include missing positives outside candidate lists, zero denominators, unresolved gold, duplicates, short rankings and failures. Candidate recall and all eligibility/coverage denominators are visible. Gold permutation/removal cannot change runtime output. Cost/latency is measured, not fabricated. First experiment is labeled a pilot. Full scientific comparison remains gated while required faithful baselines are unavailable.

## Milestone 4: Predict procedures and diagnostics

**Purpose:** add prediction suitability to the same action/procedure/evidence/ranking interfaces.

**Dependencies:** M1–M3 contracts, researcher-approved task taxonomy and prediction-time information policy, independently annotated Predict requests, row/entity/time split design. Settle whether downstream utility means feasible supervised prediction, forecasting, or measured performance; do not equate them.

**Exact planned files:** modify `intention_grounding/action_base.py`, `grounder.py`, `profiler.py`, `predicates.py`, `aligner.py`, and the canonical IL catalog/specification with a new version; modify `interpreter/schema.json` and `interpreter/providers.py` only if new explicit roles require a versioned migration. Add `intention_grounding/prediction/{__init__,diagnostics,row_splits,downstream}.py`, `configs/experiments/predict_pilot.json`, `configs/prediction/pilot.json`, `tests/test_predict_procedures.py`, `tests/test_prediction_leakage.py`, `tests/test_prediction_splits.py`; update `tests/test_grounding_procedures.py`, `docs/ANNOTATION_PROTOCOL.md`, `README.md` (repository layout), `README.md` and schema package data as needed.

**Deliverables:** separate procedures for approved prediction task(s), explicit target/features/unit/population/time/horizon bindings, target availability and leakage evidence, missingness/label-distribution diagnostics with no unjustified hard minimum-N rule, row-level split manifests separate from discovery partitions. Observational adequacy is not proof of predictive performance. Downstream fitting, if scientifically requested, is a separately budgeted experiment with frozen estimators/preprocessing; retrieval models remain pretrained. Do not train in M0 or make downstream fitting a hidden pilot dependency.

**Verification commands (future):**

```sh
python -m unittest discover -s tests -p 'test_predict_procedures.py' -v
python -m unittest discover -s tests -p 'test_prediction_leakage.py' -v
python -m unittest discover -s tests -p 'test_prediction_splits.py' -v
python -m intention_grounding.cli --config configs/experiments/predict_pilot.json
python -m unittest discover -s tests -v
```

**Acceptance:** classification/regression is not forced to require time; forecasting does require an explicit temporal use specification. Target-derived features (e.g. count components), post-outcome measurements, entity overlap and future leakage are rejected or unresolved as evidence warrants. Row test outcomes are inaccessible to ranking/profiling in the downstream track. Ambiguous targets/horizons abstain. Compare regressions pass. Predict usefulness and downstream performance are reported as separate endpoints with independent labels and a declared task metric, not a universal accuracy threshold.

## Milestone 5: frozen experiments and reproducible report

**Purpose:** produce a reviewable scientific report only after contracts, faithful comparisons and independent data are adequate.

**Dependencies:** M1–M4 acceptance; clean frozen code/dependency/model/config versions; licensed data, locked untouched test partitions and judgments; sufficient independent test units/sample design; resolved baseline and protocol blockers. External FollowTable is optional until compatible and licensed.

**Exact planned files:** add `configs/experiments/{compare_frozen,predict_frozen,followtable_external}.json`, `configs/evaluation/frozen.json`, `intention_grounding/evaluation/report.py`, `tests/test_report_reproducibility.py`, `docs/EXPERIMENT_REPORT.md`, `docs/REPRODUCIBILITY.md`, and small shareable `reports/frozen-v1/{artifact_manifest.json,metrics.json,per_topic.csv}`. Large source/model/run artifacts stay outside tracked source with hashes/authorized storage locations. Update `README.md`, `README.md` (repository layout) and `.github/workflows/deterministic.yml` for offline artifact checks only.

**Deliverables:** versioned predictions, evidence and immutable run manifests; controlled and end-to-end tables; per-action/topic results, paired uncertainty where justified, candidate recall, verdict fidelity/false-support, coverage/failure rates, costs/timing, scope and contamination limitations; independently reproducible metrics and report. Report blocked/omitted methods explicitly and avoid stronger claims than the evidence permits.

**Verification commands (future):**

```sh
python -m intention_grounding.cli --config configs/experiments/compare_frozen.json
python -m intention_grounding.cli --config configs/experiments/predict_frozen.json
python -m intention_grounding.evaluation.report --manifest reports/frozen-v1/artifact_manifest.json --verify
python -m unittest discover -s tests -p 'test_report_reproducibility.py' -v
python -m unittest discover -s tests -v
git diff --check
```

Run external evaluation with the same CLI/config pattern only after its gates clear. Report verification reuses saved predictions and never reruns paid models automatically.

**Acceptance:** clean code/config/model/data/split hashes match each manifest; full evidence/error/timing/cost records exist; metric recomputation from frozen predictions reproduces the report; all methods use declared identical information/candidates in controlled comparisons; holdout was not used for selection; uncertainty reflects independent topics rather than rows; no unresolved labels silently converted to negatives; no claim of publication-quality superiority from a first-day pilot. Freeze failures invalidate the relevant claim instead of being omitted.

## Stop condition for this task

Deliver the three M0 documents, verified tests/status, blockers and M1 criteria. Preserve pre-existing implementation changes and all data; limit source edits to the recorded M0 cleanup/terminology changes. Do not create M1 schemas/configs/manifests, begin baseline implementation, merge, or push.
