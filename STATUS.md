# Status

## Completed

- Repository/Git audit and dedicated `codex/experimental-evaluation` branch.
- Legacy/new-contract conflict identified and documented.
- Strict hashed five-action/five-axis knowledge configuration.
- Synthetic profiler, interpretation/grounding, existential binding,
  requirement construction, topical-only BM25, all matcher types, exact
  alignment/ranking equations, and bottom fallback.
- Leakage-safe splits, pooling/annotation validation, core metrics, paired
  statistics, fail-closed baseline registry, run writer, and LaTeX generation.
- Supervisor-facing method report with a reproduced score derivation for the
  controlled COMPARE example.
- Milestone 1 contract audit: all seven knowledge-layer components are exposed,
  nested configuration is fail-closed, matching operators are explicit,
  scoring inputs are cross-validated, and the contract-to-code matrix is
  recorded in `docs/contract_traceability.md`.
- Milestone 2 cleanup removed the self-contained legacy MVP/six-axis cluster,
  duplicate configurations, stale phase documents, and generated caches. All
  deleted tracked material remains recoverable from Git history.
- Versioned multi-topic synthetic benchmark with three topics, six action
  variants, all five supported actions, three action-switch pairs, strict gold
  validation, and a fail-on-mismatch CLI runner.
- Milestone 3 gold annotation contract, all-eleven-predicate synthetic gold,
  structured row-granularity ontology, versioned immutable capability-profile
  storage, complete/sample evidence distinction, improved identifier/grouping/
  temporal/repetition extraction, and profiler diagnostics.
- Milestone 4 strict structured interpretation schema, exact provenance spans,
  raw/validated provider artifact separation, versioned alias normalization,
  ambiguity and missing-argument policies, configured external-provider
  boundary, and controlled action/argument evaluation.
- Milestone 4 hardening separates topical-extraction and grounding failures,
  prevents action-bearing provider failures from becoming topical queries,
  validates the complete Draft 2020-12 schema, checks argument/span support
  after normalization, and reports joint-frame and provenance-span accuracy.
- `PREDICT.observational_unit` now creates an operational required
  `row_granularity` requirement (including explicit structured-unit and
  existential matching). Knowledge contract version 2.1.0 is bound by hash.
- `MONITOR` is frozen as the fifth single-table action; `INTEGRATE` is a
  future multi-table contract, not a substitution. The canonical 12-milestone
  roadmap and credential-free deterministic GitHub Actions workflow are added.
- A small credential-free Milestone Demonstrator exposes every implemented
  pipeline boundary as structured JSON. Immutable reconstructed archives cover
  Milestones 1–3 at their source commits; Milestone 4 has a regenerable current
  snapshot and executable notebook. All artifacts are labeled synthetic and
  explicitly excluded from paper-result claims.
- Milestone 5 contract stage freezes the provider-independent retrieval request
  and Draft 2020-12 result schema, normalized candidates and ranks, identity,
  revision, serialization, timing, and explicit failure states. BM25 implements
  the common interface as the deterministic reference adapter.
- BM25's `title_description_schema_v1` exposes only title, description, and
  ordered column names. K=20 is the current deterministic default; development
  depths are 5/10/20/50 and sensitivity depths are 5/10/20/50/100.
- The pipeline enforces topical-only first-stage input. `TABERTA-Hybrid` is
  topical-only, while `TABERTA-FullInput` is explicitly a separate baseline.
  The versioned external registry remains fail-closed with no substitutions.
- Milestone 5 demonstrator output adds retriever identity, serialization,
  candidate ranks/scores, timing, and status without modifying Milestones 1–4.
- Milestone 5 contract PR #10 is merged. Retrieval hardening separates the
  common evidence-access policy from model-specific serialization; external
  adapters remain blocked with null serialization until their exact published
  format is registered.
- Candidate artifacts preserve native raw scores and normalized relevance.
  Normalization identity/version and model, checkpoint, adapter, serialization,
  registry, and configuration hashes make fusion inputs reproducible.
- K=20 is the deterministic default, not a paper-level choice. Final K will be
  selected on development data only using the frozen recall-saturation rule;
  the existing sensitivity depths remain unchanged.
- Retrieval raw scores, normalized relevance, and all latency components must
  be finite. The tracked Milestone 5 snapshot records its merged
  `base_implementation_commit`; actual checkout SHAs belong in runtime/CI
  artifacts and are not hard-coded self-referentially.
- Milestone 5 hardening PR #11 is merged. Milestone 6 freezes a versioned,
  hashed evaluation protocol with separate interpretation, retrieval,
  usefulness-ranking, annotation/agreement, and statistical-comparison layers.
- Controlled tests cover nDCG@5/10, MRR at y>=2, Useful-Recall, candidate
  recall/upper bounds, per-action and action-switch diagnostics, action-aware
  deltas, quadratic weighted kappa, topic-first aggregation, paired bootstrap,
  paired sign permutation with a Holm family, deterministic ties, complete
  judgments, and fail-closed test-label tuning guards.
- The Milestone 6 demonstrator adds only a deterministic evaluation summary;
  Milestones 1–5 remain checksum-protected and all fixture outputs are labeled
  non-paper results.
- Milestone 6 hardening preserves separate topical relevance (`0/1/2`) and
  intended-action usefulness (`0/1/2/3`) qrels, agreement, and completeness.
  Normative ranking evaluation consumes scored table IDs against complete
  qrels for a declared universe and rejects duplicate, unknown, or unjudged
  tables.
- nDCG ideal gain and end-to-end Useful-Recall denominators use the complete
  declared universe even when useful tables are not returned. Candidate-set
  recall remains separately named; action-switch diagnostics accept tied
  optimal tables; per-action aggregation is topic-first; and bootstrap
  intervals use the configured confidence level.
- Milestone 6 PR #12 is merged into `main`. `evaluate_paper_ranking` is now the
  explicit normative qrel-based paper-evaluation entry point; label-list
  metrics remain controlled legacy regression helpers only.
- The Pre-Milestone-7 architecture gate freezes provider-independent embedding,
  topical-only semantic retrieval, deterministic neural table serialization,
  Qdrant index, authoritative Parquet/DuckDB table storage, versioned profile
  storage, artifact manifests, external LLM interpretation, optional semantic
  profiler enrichment, hybrid RRF, and development-only encoder selection.
- TABERTA is excluded from the new primary architecture. BM25 remains an
  infrastructure/reference condition. Verified Gemini, Voyage, and Qwen
  candidates are fail-closed and no final encoder has been selected.
- Pre-Milestone-7 architecture freeze PR #13 is merged. Operational hardening
  corrects current Gemini embedding/LLM contracts, preserves raw cosine scores
  behind development-pending calibration, and implements optional Hugging Face,
  Qdrant, Parquet/DuckDB, offline-indexing, online-retrieval, and mocked external
  structured-LLM paths without downloads in deterministic CI.
- Pre-Milestone-7 operational hardening PR #14 is complete and merged. The
  post-merge hardening review branch makes overflow handling exact and
  fail-closed, derives smoke readiness from runtime state, and strengthens
  Qdrant and artifact invalidation without redesigning the architecture.
- Post-merge hardening PR #15 is complete and merged. Milestone 7 is entered at
  M7A.1 with a pinned, executable audit of the canonical WWW 2018 WikiTables
  query and qrel resources.
- M7A.1 PR #16 is merged. M7A.2a freezes the corpus preflight, loss-minimizing
  logical record, deterministic sharding, index, rejection, and checksum
  contracts without acquiring or normalizing the full corpus.
- M7A.2a PR #17 is merged. M7A.2b acquired and verified the canonical archive,
  implemented the real source adapter, normalized all 1,652,771 tables, and
  resolved every one of the 2,932 qrel-referenced table IDs.

## Current milestone

Current substage: Milestone 7A.2b complete, awaiting PR review. The verified
archive SHA-256 is `cc8f509a...21ce47`; its real JSON-object format maps exact
table keys to qrel IDs. All 1,652,771 source records were normalized with zero
rejections; logical corpus digest `27b81172...c589c`. The full index resolves
2,932/2,932 qrel tables and affects zero judgments. The 3,120/3,117 discrepancy
remains unresolved. No encoder is selected; no pool, annotation, or paper
result exists.

## Commands and tests

Git state/history, complete inventory, and source/config/test/document inspection.
`pytest -q`: 321 passed. The normative suite includes contract,
multi-topic benchmark, strict annotation, profile repository, profiler boundary,
and metric regression tests.
`PYTHONPATH=src python3 -m intention smoke`: completed with knowledge hash
`1ddf47f9...6ec2c`; COMPARE ranks `country_rates` above `patient_records`.
The report verification reproduced final scores 0.6037896 and 0.4800000.
`python3 -m compileall -q src tests`: passed.
`PYTHONPATH=src python3 -m intention preflight-wikitables-corpus`: passed
offline with tracked verified archive/format/corpus evidence and
`requires_verification` redistribution status. Explicit acquisition streamed,
hashed, ZIP-tested, and atomically promoted the canonical archive; a subsequent
offline reuse revalidated it without downloading.
`PYTHONPATH=src python3 -m intention synthetic-benchmark`: six of six cases
passed; three final winners differ from their relevance-only winners.
`PYTHONPATH=src python3 -m intention evaluate-profiler`: controlled macro-F1,
value score, provenance validity, and structured granularity diagnostics are
1.000 on six developer-authored tables. Macro-F1 covers nine predicates with
positive support; `identifier_only` has no positive case and four geographic
judgments are excluded as unknown.
`PYTHONPATH=src python3 -m intention evaluate-interpreter`: 12/12 controlled
cases; action accuracy/macro-F1, argument precision/recall/F1, joint-frame
accuracy, provenance-span accuracy, and grounding-decision accuracy are 1.000.
This is deterministic contract evidence, not an external LLM result.
GitHub Actions repeats the offline suite and five deterministic CLI checks on
Python 3.10 and 3.11 without credentials, and verifies the current demo
snapshot.

## Artifacts

No paper results. Smoke output is not an experiment run or metric claim.

## Blockers

Immutable API-model checkpoint revisions, the full WikiTables corpus and its
redistribution-license verification, human annotations,
credentials, downloaded weights, validated accelerators, and Qdrant service
are absent. DuckDB and `pyarrow` are locally available and their real storage
round trip passes, but remain optional in base CI. Thus no learned end-to-end smoke,
baseline comparison, benchmark labels, run bundle, ablation/sensitivity results,
confidence intervals, significance claims, efficiency measurements, or paper
tables were produced. Capability macro-F1, row-granularity accuracy, ordinal
agreement, throughput, and full orchestration remain pending.

## Next action

Review M7A.2b. After review only: M7B development-only retriever bake-off,
encoder freeze, then M7C pooling and human annotation.
