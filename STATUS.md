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

## Current milestone

Milestone 5 retrieval contract PR is merged; its small hardening pass is on a
review branch. No external model integration, download, or benchmark run began.

## Commands and tests

Git state/history, complete inventory, and source/config/test/document inspection.
`pytest -q`: 213 passed. The normative suite includes contract,
multi-topic benchmark, strict annotation, profile repository, profiler boundary,
and metric regression tests.
`PYTHONPATH=src python3 -m intention smoke`: completed with knowledge hash
`1ddf47f9...6ec2c`; COMPARE ranks `country_rates` above `patient_records`.
The report verification reproduced final scores 0.6037896 and 0.4800000.
`python3 -m compileall -q src tests`: passed.
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

Exact external model revisions/checkpoints, WikiTables, human annotations,
credentials, accelerators, and `pyarrow` are absent. Thus no real-data smoke,
baseline comparison, benchmark labels, run bundle, ablation/sensitivity results,
confidence intervals, significance claims, efficiency measurements, or paper
tables were produced. Capability macro-F1, row-granularity accuracy, ordinal
agreement, throughput, and full orchestration remain pending.

## Next action

Review and merge the Milestone 5 retrieval-hardening PR. Stop before pinning or
adding external retrievers.
