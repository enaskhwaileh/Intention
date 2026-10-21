# Milestone 0: repository audit

> Supporting appendix. Start with the [main project guide](../README.md) for current architecture, demonstration, models and testing. Historical audit statements are dated records, not current capability claims.

Current audit refresh: 21 October 2026. This task performs M0 only and preserves the previously authorized IL extension. The historical audit is retained below with an explicit boundary. No paid calls, training, retrieval experiments, large downloads, commit, push or merge were performed in this refresh.

## Verified starting and final state

- Starting branch: `main`; recovery commit: `2833adbed071de88574b6fd18437934680cfb241`.
- Starting working tree: **not clean**. Seven tracked modifications: README, repository map, IL loader, CLI, grounder, walkthrough notebook and pipeline tests. Six untracked files: audit, implementation plan, evaluation contract, IL guide, v0.2 catalog and IL tests. All were preserved; this refresh builds on them. Entry content hashes are recorded temporarily in `/tmp/intention-m0-entry-files.json`.
- Dedicated cleanup branch: `cleanup/m0-audit-20261021`. Final HEAD remains the recovery commit. Both `main...HEAD` and local `origin/main...HEAD` are `0 0`; no fetch occurred in this refresh, so this is not a new assertion about remote server state.
- No `AGENTS.md` found in the repository or ancestors checked through `/`. Package dependencies and CI inspected; no secret files or secret values read or printed.
- Final tree is intentionally uncommitted: inherited IL work, bounded terminology changes, documentation updates and two verified deletions. No renames or archive directory were introduced.

## Current component audit

Paths are relative to `intention_grounding/` unless noted. Verification refers to offline mechanics, not semantic accuracy.

| Component / paths | Actual input → output and status | Tests / remaining work |
| --- | --- | --- |
| Interpreter: `interpreter/{core,providers}.py`, `schema.json` | Request + provider → validated structured intention record / safe failure. **Implemented and verified** for replay, schema, evidence spans and mocked providers; live accuracy **implemented but unverified**. | `tests/test_interpreter.py`, `test_groq_config.py`; independent semantic evaluation absent. |
| IL: `action_base.py`, `docs/ab_proposal/action-base-v0.2.json` | Catalog → checked inheritance, roles, procedures, evidence contracts; inspection JSON. **Implemented and verified**: 23 families, 62 concrete intentions, 66 procedures. | `test_intention_library.py`, `test_ab_proposal.py`; definitions scientifically unvalidated, 59 concrete intentions catalog-only. v0.1 remains frozen/loadable. |
| Grounder: `grounder.py` | Structured record + IL + model proposal → one grounded intention or explicit rejection. **Implemented and verified** for three Compare leaves; live selection **unverified**. | `test_pipeline.py`, `test_intention_library.py`; abstract/malformed IDs now safely rejected by prior IL work. Multiple procedure branches, joint goals and full-grid activation still incomplete. |
| Candidate retriever | Full request + corpus → candidate IDs/scores: **missing**. | No current tests/implementation; explicit `--dataset` paths are not retrieval. Historical BM25 is a port candidate only. |
| Profiler: `profiler.py` | CSV/JSON + provenance → primitive statistics, hash and scan evidence. **Implemented and verified** for fixtures; broad data semantics **unverified**. | `test_pipeline.py`; header-only CSV loses columns, JSON booleans become numbers, semantic units/populations absent. |
| Requirement assessment: `aligner.py` | Grounded intention + profiles → all requirements `unknown`, no supporting evidence links. **Stub** with tested conservative behavior. | `test_pipeline.py`; no substantive supported/violated assessment. |
| Ranker | Candidates + assessments → usefulness order: **missing**. | No implementation/tests; aggregation/abstention policy remains proposed. |
| Dataset/annotation loaders | CSV/JSON profiler reader exists; versioned corpus/request/judgment/split loaders **missing**. | Fixture tests only. Legacy label files are not independently established usefulness gold. |
| Evaluation metrics | Immutable predictions + evaluator-only judgments → metrics: **missing**. | Definitions in evaluation contract only; no measured retrieval results. |
| Baseline adapters | Full-request BM25, semantic matching, TABERTA, Qwen embeddings/reranker, direct LLM usefulness: **missing** in current package. | Historical BM25/encoder code is unverified reuse material. Semantic matching and faithful TABERTA artifacts remain blocked; other adapters require integration. |
| Entry/logging: `cli.py`, root `pyproject.toml`, walkthrough | One offline/live request + explicit tables → seven unique-run artifacts. **Implemented and verified** offline; complete experiment runner **missing**. | Pipeline/config tests and offline notebook. No config matrix, rankings, split hashes, costs or metrics yet. |

The canonical route remains one package and `python -m intention_grounding.cli`; no competing pipeline was added. The smallest complete pipeline, contract boundaries and proposed future commands are in [the plan](IMPLEMENTATION_PLAN.md). Synthetic tables/manual replay are contract checks, never retrieval evidence.

## Cleanup manifest

For removed tracked files, recovery is `git show 2833adbed071de88574b6fd18437934680cfb241:<original-path>`. No untracked file or unique dataset/output was removed.

| Original path(s) | Decision / reason | Reference and provenance checks |
| --- | --- | --- |
| `intention_grounding/scripts/_test_archive/test4_grounder_execution_trace_working.py` | **Removed**; exact byte duplicate of retained `test4_grounder_execution_trace.py`. | `cmp` succeeded; inspected retained content; whole-repo reference search including notebook JSON, CI, package resources and runtime imports found no consumer. Git recovery at starting commit; no unique data. |
| `intention_grounding/scripts/test_interpreter_production.py` | **Removed**; only a docstring redirecting to current tests, no executable assertions. | Read entire file; only current map mentioned it. Updated map; CI discovers root `tests/`, no imports. Git recovery at starting commit. |
| `intention_grounding/scripts/grounder_production.py` | **Retained**, header corrected to historical compatibility only. | `tests/test_interpreter.py` imports it to verify rejection of current records; preserves historical result reproducibility. It is not the canonical pipeline. |
| `intention_grounding/kb/*`, `data/*`, `results/*` | **Retained**. Distinct designs, labels, table descriptions and outputs may hold unique provenance. | Compared the two similarly named catalogs: substantially different, not duplicate copies. Legacy grounder loads v1.0; historical scripts reference schema/protocol. Generic thresholds are not current methodology. |
| `intention_grounding/scripts/_test_archive/*` other than duplicate; `_archive_2026-09-16/*.ipynb` | **Retained** pending provenance resolution. | Scripts read/write older results; notebooks hold stored outputs/errors. No blanket deletion or execution of historical experiments. |
| `intention_grounding/AB-M1.md`, `kb/RATIONAL_GROUNDER_DESIGN.md` | **Retained**, historical-status notices added. | Unique design/verification history; stale production/publication-ready claims are explicitly nonauthoritative. |
| Frozen v0.1 proposal, examples and fixtures | **Retained unchanged**. | Current tests and legacy loading reference them; needed for reproducibility. |
| `action_base.py`, `cli.py`, `grounder.py`, `interpreter/providers.py`, root `pyproject.toml` | **Updated** for preferred IL terminology/API aliases, compatible CLI flag, versioned prompt wording and package description. | Inventory below; same implementation and serialized schema. Existing and alias parity checks pass; no live accuracy claim. |
| README, `docs/*.md`, walkthrough | **Updated** for current capabilities, map, decisions, compatibility and next milestone. | Existing IL extension retained. README is the documentation entry point; future paths/commands labeled proposed. |
| `.gitignore`, dependencies, CI | **Retained unchanged** after review. | Existing ignores cover caches, builds, outputs, raw/normalized/runtime data and secrets. jsonschema/dotenv used; Groq/Jupyter optional. CI already checks the canonical route; no unused runtime dependency established. |
| Ignored local outputs, environments and caches | **Retained**. | No need to delete outside-scope user state or evidence. Verification artifacts go to temporary directories. |

Uncertain cleanup candidates: establish whether historical notebooks/scripts are the only recipes for the legacy results; identify original annotators/review procedure for legacy labels; identify provenance for asserted table descriptions; determine which historical design passages the actual methodology manuscript retains. Keep those files until answered. No current manuscript was found or claimed consistent.

## Current verification and blockers

Baseline before cleanup: **47 tests passed** with `/tmp/intention-m0-audit-20261021/bin/python -m unittest discover -s tests -q`. After cleanup: **47 tests passed**, including both `--il` and legacy `--ab` loading the frozen catalog. All notebook code cells passed with live calls disabled, including its temporary offline CLI run. Preferred Python API aliases resolve to the identical implementation. `compileall`, `git diff --check`, and maintained-document local-link checks passed. Read-only probes reconfirmed the documented empty-header and boolean-type profiler gaps. No regression was introduced by the cleanup. Only Python 3.13 was exercised locally; the CI matrix was inspected, not run remotely. Final status: 12 modified tracked files, 2 tracked deletions and 6 preserved untracked files; HEAD unchanged on the cleanup branch. Environment: isolated Python 3.13 with existing runtime dependencies; no new installation or paid SDK calls.

Outstanding implementation issues: full-grid requests can be weakened; multi-goal/procedure grounding is incomplete; empty CSV headers and boolean typing are wrong; custom datasets without supplied metadata inherit inappropriate WikiDBs metadata. The README now supplies explicit metadata in its live command. Fixing these substantive issues belongs to the planned implementation milestones; this refresh does not claim them fixed.

Confirmed decisions: direct-observation Compare first; broad Predict catalog includes classification, regression, forecasting and survival. Still open: pilot order, task-specific adequacy policies, independent annotation resources, ranking/abstention policy, methodology authority, faithful published baseline identities, external dataset terms/protocol alignment and compute budget. A refreshed read of UCI, FollowTable, TABERTA and Qwen public pages confirms source availability only; earlier pinned-file findings below remain historical, not freshly reproduced downloads. See [evaluation contract](EVALUATION_CONTRACT.md) for source links and explicit metric conventions.

**Next: M1, not started.** Accept only versioned loadable corpus records with truthful provenance/licenses/hashes/source-family IDs; independently reviewed usefulness judgments; topic/family-disjoint discovery splits or an explicit development-only designation; separate prediction row splits; validators and tests proving evaluator-only gold isolation. No retrieval experiment is needed for M1 acceptance.

## Current M0 refresh: interface inventory before changes

This refresh starts from the already extended IL working tree. The sections under **Earlier audit record** below are historical evidence, not the current capability report. No current project manuscript is available; paper consistency is not claimed.

| Surface | Existing spelling | M0 disposition and dependent consumers |
| --- | --- | --- |
| Maintained prose and package description | Action Base, intended-action | Use Intention Library (IL), intention-grounded table discovery, intention expression, intention type. Update README, map, plan, prompt prose and package description together. |
| CLI catalog option | `--ab` | Add preferred `--il`, retaining `--ab` as a compatibility alias; both map to `args.il`. Existing tests and scripts remain valid. |
| Library Python API | `load_action_base`, `validate_action_base`, `ActionBaseError`, `CANONICAL_AB_PATH` | Add intention-named aliases in the existing module and use them in the canonical CLI. Keep one implementation; preserve old imports. |
| Versioned serialized interfaces | `actions`, `action_id`, `ab_version`, `ab_path`, `grounded_card`, `unknown`; interpreter schema 1.0 and catalog versions | Retain exact keys for backward compatibility in M0; they map to intentions, IL identity, grounded intention, and unresolved respectively. A breaking schema rename needs a versioned migration of fixtures, templates, model responses, notebook, manifests and archived artifacts. This is a documented remaining terminology migration, not an assertion that all identifiers are already normalized. |
| Prompts | AB/action prose; version identifiers | Change descriptive prose to intention/IL; retain exact schema-key references and increment prompt versions. Offline tests do not validate live model equivalence. |
| Frozen proposals and historical artifacts | Original author vocabulary | Preserve historical content, filenames, IDs and recorded outputs. Mark historical prose as noncanonical. Preserve all published titles, external field names and bibliographic entries exactly. |

## Earlier audit record

## 1. Actual repository state

| Item | Observed state |
| --- | --- |
| Checkout | `/Users/enaso/Desktop/play ground/Intention` |
| Branch | `main`, tracking `origin/main` |
| HEAD | `2833adbed071de88574b6fd18437934680cfb241` |
| Commit subject/date | `groq is changed now`; 27 September 2026 |
| Initial working tree | Clean: `git status --short --branch` printed only `## main...origin/main`; `git diff --stat` was empty |
| Relationship to local main | HEAD is main; `git rev-list --left-right --count main...HEAD` returned `0 0` |
| Relationship to origin/main | `git rev-list --left-right --count origin/main...HEAD` returned `0 0` |
| Remote verification | Read-only GitHub API `repos/enaskhwaileh/Intention/commits/main` returned the same full SHA; no fetch/reset was needed |
| Instructions | No `AGENTS.md` found in the checkout or checked ancestors `/`, `/Users`, `/Users/enaso`, Desktop, and `play ground`. Historical branch instructions are not checkout instructions. The user's M0-only scope controls this work. |
| Runtime | `python3`: Python 3.13.0, `/usr/local/opt/python@3.13/bin/python3.13` |
| Environments | Repository `.venv` is absent. Parent `../.venv` exists and reports Python 3.9.6, below `requires-python >=3.10`; it was left untouched. |
| Package | `intention-grounding` 0.2.0; setuptools; required `jsonschema==4.23.0`, `python-dotenv>=1.0,<2`; optional Groq and notebook extras |
| Audit changes | Only three new Markdown documents in `docs/`; existing tracked files preserved. Test bytecode is ignored; audit environments, source samples, and generated demo artifacts are under `/tmp`. |

The initial status was verified directly; previous conversation statements were not used as repository evidence. No credential files or environment-variable values were printed.

### Historical implementation that should not be overlooked

The local reference `origin/codex/m7b-qwen-full-provenance` at `4ef9ed9` contains a previous `src/intention/` implementation, configuration, benchmark adapters, and evaluation code. It is an **ancestor** of current HEAD, not an unmerged future implementation: `git merge-base --is-ancestor ... HEAD` succeeded and `git rev-list --left-right --count ...HEAD` returned `0 15`. Later commits replaced that architecture. `origin/codex/pre-m7-postmerge-hardening` at `6bcb101` also preserves earlier contracts.

Read-only inspection of these historical files identified reuse candidates:

- `4ef9ed9:src/intention/retrieval/retrievers.py`: standard-library BM25 implementation.
- `4ef9ed9:src/intention/retrieval/{registry,contracts,serialization}.py`: explicit adapter availability, identities, and serialization.
- `4ef9ed9:src/intention/evaluation/{metrics,statistics,protocol,ranking}.py`: metric and topic-aggregation machinery; only selected code was inspected, none executed.
- `4ef9ed9:src/intention/benchmarks/{source_audit,ia_wikitables,wikitables,corpus}.py`: historical provenance/loading candidates; inventory inspected, not revalidated.
- `4ef9ed9:src/intention/evaluation/{m7b_full,topical_bakeoff}.py`: historical encoder harness candidates, not current functionality.

Do not restore `src/intention/` wholesale or add its CLI beside the current pipeline. Port only reviewed functions into `intention_grounding/`, with current contracts and tests. Historical scoring uses missing capability match = zero and topical-only retrieval; both conflict with this task's unresolved-evidence and full-request comparisons. Its `ndcg(labels,k)` derives the ideal ranking from supplied labels, so reuse requires an explicit complete judgment universe rather than just retrieved results.

The historical `artifacts/runs/m7b-qwen06-full-9cf339c/provenance.json` claims a validated full-corpus Qwen encoding run, but explicitly says `paper_result=false`, `development_evaluation_performed=false`, and `holdout_evaluated=false`. Referenced corpus/index artifacts were not available or checked here. This is a historical provenance assertion, not a reproduced retrieval or usefulness result.

## 2. Component audit

Status vocabulary: **implemented and verified** = named behavior exercised offline; **implemented but unverified** = code exists but behavior/accuracy was not exercised; **stub** = an explicit placeholder without the required substantive behavior; **missing** = no implementation in the current checkout. A component can have verified mechanics and unverified scientific behavior.

| Component and actual paths | Input → output contract | Implemented behavior and status | Missing behavior / limits | Supporting tests |
| --- | --- | --- | --- | --- |
| Interpreter: `intention_grounding/interpreter/core.py`, `schema.json`, `providers.py`; wrapper `scripts/interpreter_production.py` | `input_id`, exact request string, explicit provider → envelope `{metadata, raw_response, interpretation, failure, provider_error}`. Interpretation schema 1.0 holds query fields, evidence spans, actions, candidate readings, arguments, relationships, status, diagnostics. | **Implemented and verified:** strict JSON parsing, closed schema, Unicode spans, literal/reference integrity, two normalization rules, relationship/status checks, manual replay. **Implemented but unverified:** live Groq extraction accuracy. | No independent empirical action/argument benchmark; span validity does not prove semantic entailment. External-context evidence is not supported. | `tests/test_interpreter.py`: 13 methods; schema, semantic fixture expectations, normalization, relationship/status, malformed inputs, legacy boundary, mocked Groq, network-blocked replay. |
| Intention Library / Action Base: `intention_grounding/action_base.py`, `docs/ab_proposal/action-base-v0.1.json`, `AB-Specification-v0.1.md`, `grounded-card-examples-v0.1.json` (last three under `intention_grounding/`) | AB path / optional expected version → validated dictionary; action ID → ancestry. | **Implemented and verified:** canonical draft `0.1.0-draft`, parent/reference/axis checks; four Compare nodes, eight predicates. Proposal consistency is checked. | No current Predict procedures; no complete closed AB schema; limited type/error handling. Taxonomy and predicates remain author-designed hypotheses. Hierarchy is specialization, not procedure execution. | `tests/test_ab_proposal.py`: 4 methods; `test_pipeline.py::test_action_base_validation`, inheritance test. |
| Grounder: `intention_grounding/grounder.py` | Validated interpreter envelope + AB + explicit provider + run ID → status, raw proposal, one `grounded_card` or null, reasons, safe provider diagnostics. Proposal has exactly `ab_version,input_id,action_id,bindings,evidence`. | **Implemented and verified:** validates known IDs, referenced argument indices/roles, minimum cardinalities, evidence membership; expands inherited requirements into one `all_of` card; gates ambiguous/insufficient/unsupported interpretations. **Unverified:** live model selection/semantic fidelity. | Exactly one action is proposed; no preserved procedure alternatives, joint-goal execution, or complete-grid certificate. Abstract-action rejection and malformed-type robustness are deficient (see probes). Inclusion/exclusion prose is not executable semantic validation. | `test_pipeline.py`: valid grounding/inheritance, unknown ID/version, missing evidence, non-grounded states/provider failure. |
| Candidate retriever | Needed: full request + corpus/index + depth → candidate IDs, scores, ranks, provenance. | **Missing** in current checkout. `--dataset` simply enumerates explicitly supplied files. | No lexical/dense search, candidate recall, index identity, retrieval serialization. Historical code is a reuse source only. | None in current checkout. |
| Table profiler: `intention_grounding/profiler.py` | Local `.csv` / `.json` array of objects or `{rows:[...]}` + dataset ID + metadata → schema 1.0 profile, columns, row count, source SHA-256, primitive statistics, scan evidence. | **Implemented and verified** for bundled CSV: full local scan, finite numeric count/ranges, nulls, hash evidence. **Implemented but unverified** for broad real-data formats and semantics. | No logical relation, units/population definitions, group/time evidence, role mapping, scope-aware negative evidence, or prediction leakage diagnostics; reads full table into memory. Header-only CSV and boolean issues reproduced below. | `test_pipeline.py::test_profile_and_unknown_alignment`; CLI integration. Coverage is narrow. |
| Requirement assessment / aligner: `intention_grounding/aligner.py` | Card or null + profiles → `{status,policy,tables,notice}`; each requirement has axis, modality, state, reason, evidence refs. | **Stub**, with verified conservative behavior: every requirement and table gets `unknown`; missing card gives `not_run`. | No predicate evaluator, positive/negative verdicts, evidence-linked decisions, or actual three-valued aggregation. `profile_evidence_refs` stays empty. Policy name does not imply implemented logic. | `test_profile_and_unknown_alignment` verifies unknown and missing-evidence behavior, not usefulness. |
| Ranking | Needed: candidates + separate per-procedure verdicts → deterministic usefulness ranking and explanations. | **Missing**. | No procedure aggregation, scoring, rank output, abstention/fallback policy, or stable tie-breaking contract. | None. |
| Benchmark loading / evaluation | Needed: versioned corpus/requests/splits; evaluator-only judgments + immutable predictions → metrics. | **Missing**. JSON fixture loading exists, not a benchmark harness. | No real corpus manifest, usefulness qrels, split validation, metric implementation, annotation loader, or gold/runtime separation. | Fixture consistency tests do not cover these capabilities. |
| Baseline adapters | Needed: full request + allowed table evidence → candidates or scores with exact model identity. | **Missing** as baselines. Existing Groq providers perform interpretation/grounding only. | BM25, published semantic matching, TABERTA, Qwen embedding/reranker, direct usefulness LLM all need adapters or artifact resolution. | Mocked Groq transport tests are not baseline tests. |
| Experiment entry point / result logging: `intention_grounding/cli.py`, `pyproject.toml`, `interpreter/demo.py`, `notebooks/pipeline_walkthrough.ipynb` | CLI flags → one replay or live request, explicit tables, unique output directory with seven artifacts. | **Implemented and verified:** offline orchestration, unique run IDs, raw/validated provider outputs, profiles, comparison, manifest; provider failures sanitized. **Implemented but unverified:** real live runs. | No config-file experiment matrix, code/dirty-tree hash, environment lock, split/index hashes, predictions/ranks, stage timings, token usage/cost, evaluation or run-resume validation. File/profile errors can terminate before complete artifacts. | `test_pipeline.py` CLI integration/failure tests; `tests/test_groq_config.py` (4 methods); notebook live opt-in/preflight test. |

Current CLI artifacts: `interpreter.raw.txt`, `interpretation.json`, `grounder.raw.txt`, `grounding.json`, `table-profiles.json`, `comparison.json`, `run.json`. The manifest records run ID/time/mode, AB path/version, input ID, table paths, and artifact directory. Provider metadata separately records configured live model/prompt/settings. This is useful scaffolding to extend.

## 3. Existing data and result provenance

| Files | Observed origin and evidential limits |
| --- | --- |
| `intention_grounding/fixtures/offline_table.csv`, `offline-source-metadata.json` | Explicitly synthetic four-row France/Germany income table. Source label is “project test fixture,” not a verified redistribution license for a research corpus. |
| `intention_grounding/interpreter/fixtures/replay.json` | 13 manually authored responses, including expected invalid cases. No model predictions. |
| `intention_grounding/docs/ab_proposal/grounded-card-examples-v0.1.json` | Manually authored proposal examples and reviewed derivation annotations; not executed scientific results. |
| `notebooks/pipeline_walkthrough.ipynb` | Stored outputs in 11 code cells; offline replay and synthetic profiling; live cell says calls were skipped. Kernel metadata is internally dated/inconsistent with the absent environment. |
| `intention_grounding/data/queries_input.json`, `ground_truth_labels.json` | Legacy request inventory; label metadata describes 18 queries and single/multiple actions. No independent assessor provenance or request-table usefulness labels. “ground_truth” in the filename is not validation. |
| `intention_grounding/data/dataset_tables.json` | Five asserted vaccine-domain table descriptions, total-record assertion 5,680; no corresponding observed row files. |
| `intention_grounding/kb/data_schema.json` | Four different asserted table descriptions, total-record assertion 65,200. Not the same corpus as `dataset_tables.json`; no verified acquisition/checksum record. |
| `intention_grounding/results/interpreter_output.json` | 18 legacy action/confidence/reasoning records, prompt-version/date metadata. No raw responses, provider/model revision, request IDs from a service, or reproducible run manifest. Actual model-call provenance cannot be established from this file. |
| `intention_grounding/results/grounder_output.json` | 18 legacy deterministic action-to-condition lookup outputs. They contain no retrieved tables or usefulness rankings. |
| `intention_grounding/_archive_2026-09-16/*.ipynb` | Both contain Groq call code and stored outputs; advanced notebook also contains a stored error. This suggests historical execution attempts, but does not authenticate the legacy result JSON or establish a reproducible accuracy experiment. Not executed in M0. |
| `intention_grounding/fixtures/wikidbs10k-source-metadata.json` | States `acquisition_date=not-acquired`, with an externally asserted archive checksum. No archive or real WikiDBs rows were found in the current checkout. |

No current committed output establishes retrieval effectiveness, intended usefulness, or downstream predictive performance. M0 generated only offline contract artifacts and temporary source-inspection files.

## 4. Specification/code discrepancies and verified gaps

Authority for the current Compare route is the canonical `intention_grounding/docs/ab_proposal/AB-Specification-v0.1.md`, reconciled with actual current code. No current project paper manuscript was found in this checkout. The EDBT 2025 semantic-matching paper is a baseline source, not the intended-action project's methodology. The older Git method contract and historical rational-grounder design must not silently override the current draft or the user's explicit evaluation requirements.

1. **Abstract action accepted:** the specification says an unresolved parent remains a candidate. A valid replay proposal changed to `action_id="compare"` returns `grounded` with abstract child `compare`. Validator never rejects `abstract=true`.
2. **Coverage request can be weakened:** `_build_card` unconditionally sets `available_observations` and skips dictionary-valued activation rules. Complete-grid requests cannot activate their specified requirement in the current response format. This needs explicit refusal/unresolved status until a valid derivation is implemented, not a claim of complete grounding.
3. **Alternatives/joint requests lost:** interpreter represents `joint`, `accepted_alternatives`, and competing readings; grounder prompts for exactly one ID. It cannot certify complete fulfillment of joint goals or preserve all applicable procedures.
4. **Malformed proposal can crash:** `action_id=[]` causes an uncaught `TypeError` at membership lookup rather than a safe `invalid_model_response`. Existing tests do not cover this type mutation.
5. **Profile edge cases:** a header-only CSV produces `column_names=[]`; JSON booleans are classified as `number` because float parsing precedes boolean detection. Reproduced without source edits.
6. **Provenance mismatch:** custom `--dataset` without `--dataset-metadata` defaults to WikiDBs metadata, irrespective of actual source. The metadata description says stable table IDs are filenames, but profiler uses `dataset_id:sha256[:16]`. Mandatory truthful corpus identity must replace this fallback before real experiments.
7. **Documentation drift:** README's existing Python 3.10 `.venv` is absent; the canonical AB document still calls itself non-executable design while current code loads it. AB-M1 is a historical report, not a present capability list.
8. **Methodology conflict:** `kb/RATIONAL_GROUNDER_DESIGN.md` calls itself publication-ready, imposes generic Compare/Predict row/column thresholds, treats Predict as forecasting, and describes only lookup grounding. Current draft rejects those generic thresholds and uses a second model proposal plus deterministic validation. No empirical evidence here supports “publication-ready.”
9. **Historical method conflict:** ancestor `docs/method_contract.md` restricts retrieval to topical `q_u`, scores missing evidence as zero, and combines weighted axes. This task requires strong full-request baselines, separate procedure alternatives, and unresolved evidence; migrating the ancestor formula unchanged would violate the requested study.
10. **Statistical validity unestablished:** exact text spans prove provenance, not the correctness of a model's procedure selection, units interpretation, or population match. These need independently annotated semantic checks.

These are audit findings; no fixes were made in M0. The next implementation stages include regression checks for them.

## 5. Verification performed

Initial command from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

Failed with three module-import errors (`test_groq_config`, `test_interpreter`, `test_pipeline`): `ModuleNotFoundError: No module named 'jsonschema'`. Four AB proposal tests passed; unittest reported seven entries, three errors. `dotenv` was also absent in this interpreter. This was environment failure, not a failing assertion in the implementation.

An initial `uv venv --offline /tmp/intention-m0-audit-20261021 --python /usr/local/bin/python3` and cached dependency install failed because the default cache attempted a write outside the sandbox. A temporary cache avoided that; a network install initially failed DNS inside the sandbox, then succeeded with approved execution. Exact successful setup:

```sh
uv venv --offline --cache-dir /tmp/intention-m0-uv-cache --python /usr/local/bin/python3 /tmp/intention-m0-audit-20261021
uv pip install --python /tmp/intention-m0-audit-20261021/bin/python --cache-dir /tmp/intention-m0-uv-cache jsonschema==4.23.0 'python-dotenv>=1.0,<2'
```

Installed only six small runtime packages in the isolated environment: `attrs==26.1.0`, `jsonschema==4.23.0`, `jsonschema-specifications==2025.9.1`, `python-dotenv==1.2.4`, `referencing==0.37.0`, `rpds-py==2026.9.1`. The optional Groq SDK was not installed. Imports used the checkout from its root; editable package installation/console-script packaging was not verified.

| Exact command | Outcome |
| --- | --- |
| `/tmp/intention-m0-audit-20261021/bin/python -m unittest discover -s tests -v` | **33 tests passed** on Python 3.13.0. Groq/model-list tests use mocks or missing-configuration paths. Includes replay with network blocked. |
| `/tmp/intention-m0-audit-20261021/bin/python -m intention_grounding.cli --mode offline --output /tmp/intention-m0-artifacts-20261021/pipeline` | Exit 0; one four-row table; interpretation `unambiguous`, grounding `grounded`, alignment `unknown`; seven artifacts in `run-08e1ccfe21f5`. |
| `/tmp/intention-m0-audit-20261021/bin/python -m intention_grounding.interpreter.demo --output-root /tmp/intention-m0-artifacts-20261021/interpreter` | Exit 0; **13/13 expected replay outcomes**, including expected rejections; `manual-replay-ijcl_9mm`. |
| `/tmp/intention-m0-audit-20261021/bin/python -m compileall -q intention_grounding tests` | Exit 0. |
| `PYTHONPATH=. /tmp/intention-m0-audit-20261021/bin/python /tmp/intention-m0-contract-probes.py` | Read-only audit probes reproduced abstract grounding, uncaught malformed-ID error, empty-header loss, boolean-as-number. Details below. |
| `git diff --check` | Passed at documentation delivery. New Markdown files also checked for trailing whitespace and broken local links. |

CI declares Python 3.10, 3.11, and 3.13 in `.github/workflows/deterministic.yml`; only local 3.13 was run. No claim about current remote CI, live provider compatibility, or model accuracy is made.

The temporary probe used `cli._offline_inputs()`, `interpret(...)`, `load_action_base()`, and `ground(...)` with `ReplayGrounderProvider`. Its two proposal mutations were `proposal['action_id']='compare'` and `proposal['action_id']=[]`. Two temporary tables were exactly `country,year,income\n` and `[{"flag": true}, {"flag": false}]`. Outputs were respectively `grounded compare`, `TypeError`, `[]`, and `number`. This describes reproducible inputs even after `/tmp` is cleaned.

## 6. External feasibility audit and blockers

See [evaluation contract, source feasibility](EVALUATION_CONTRACT.md#2-source-feasibility-checked-in-m0) for URLs, hashes, inspected content, baseline availability, and limitations. Small inspection files total approximately 1.52 MB; no corpus ingestion or model-weight download was performed. GitHub connector inspected FollowTable code; its oversized annotation fetch was unsupported, so a bounded public download was used for the one annotation file. OpenML's browser view/API were inaccessible through web extraction; a bounded metadata request succeeded. The semantic-matching publication's GitHub URL redirected, and the connector could not follow the repository-ID endpoint; exact implementation access remains unresolved.

After M0 delivery, the researcher confirmed **direct-observation Compare first**, resolving its initial transformation scope. Aggregate-then-compare stays out of scope. The reply “yes” to the combined Predict/paper question did not identify a Predict task or a newer methodology document. Remaining blocking scientific decisions are **Predict task type**, **independent usefulness annotation feasibility**, **ranking/abstention policy**, and **which current methodology document supersedes conflicting historical designs**. Access/reproducibility gates include exact semantic-matching artifact, TABERTA serialization/checkpoint mapping, FollowTable redistribution terms and native protocol alignment, additional independent source families/topics, and model hardware/budget selection. No dataset or ranking formula is declared scientifically final.

M0 ends here. The next milestone is **M1: data contracts, provenance, independent annotation protocol, and split manifests**, with the precise deliverables and acceptance criteria in [the implementation plan](IMPLEMENTATION_PLAN.md#milestone-1-data-contracts-and-evaluation-readiness). M1 has not started.

## Presentation follow-up (after M0 publication)

The researcher requested a single main guide and a supervisor demonstration interface. `README.md` now consolidates architecture, datasets, baselines, LLM requirements, testing and the roadmap. `docs/REPOSITORY_MAP.md` was removed after its responsibilities and unresolved provenance questions were incorporated into the main guide; maintained links were updated. Unique evaluation, milestone, IL and audit details remain clearly labeled appendices. No original data, annotations, results or fixtures were removed.

The local interface (`dashboard.py`, `dashboard_checks.py`, `ui/`) reuses current components and displays manual replay, primitive evidence, unknown verdicts, IL definitions and actual offline unittest results. It does not implement retrieval or claim model superiority. A project-local ignored environment and `run_demo.command` support the demonstration. The existing uncommitted IL extension is preserved.

Verification: 53 offline tests pass, including six interface tests; Chrome exercised pipeline execution, catalog filtering/details, expected malformed-input rejection and the real test-suite button. A downloaded JSON report was verified against the actual 53-test result and source identity; responsive width was checked. Compilation, launcher syntax, maintained documentation links and whitespace checks passed. Local socket tests require permission to bind localhost in restricted sandboxes; the first sandbox attempt was blocked, and the permitted run passed. No paid inference or model downloads occurred.
