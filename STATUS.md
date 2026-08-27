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

## Current milestone

Milestone 2 planning: stronger multi-topic synthetic benchmark.

## Commands and tests

Git state/history, complete inventory, and source/config/test/document inspection.
`pytest -q`: 195 passed in 2.87s.
`PYTHONPATH=src python3 -m intention smoke`: completed with knowledge hash
`fed97189...2c43c`; COMPARE ranks `country_rates` above `patient_records`.
The report verification reproduced final scores 0.6037896 and 0.4800000.
`python3 -m compileall -q src tests`: passed.
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

Agree on the topic/action coverage and gold-ranking construction policy for the
stronger synthetic benchmark before adding new fixtures.
