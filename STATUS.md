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

## Current milestone

Milestone 3 planning: capability profiler validation.

## Commands and tests

Git state/history, complete inventory, and source/config/test/document inspection.
`pytest -q`: 172 passed in 2.95s after removing 29 legacy tests and adding six
multi-topic benchmark tests.
`PYTHONPATH=src python3 -m intention smoke`: completed with knowledge hash
`fed97189...2c43c`; COMPARE ranks `country_rates` above `patient_records`.
The report verification reproduced final scores 0.6037896 and 0.4800000.
`python3 -m compileall -q src tests`: passed.
`PYTHONPATH=src python3 -m intention synthetic-benchmark`: six of six cases
passed; three final winners differ from their relevance-only winners.
`ruff` and `mypy` are not installed; dependencies are declared. This shell has
no default `python` shim, so verification used `python3`.

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

Define the capability-profiler gold annotation schema, predicate scope, and
row-granularity policy before changing extraction heuristics.
