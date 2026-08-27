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

## Current milestone

External integrations and full experimental execution (blocked on resources).

## Commands and tests

Git state/history, complete inventory, and source/config/test/document inspection.
`pytest -q`: 50 passed in 0.51s.
`PYTHONPATH=src python3 -m intention smoke`: completed with knowledge hash
`06d14d1...539a`; COMPARE ranks `country_rates` above `patient_records`.
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

Freeze external resources on development topics, complete remaining diagnostics
and orchestration, install evaluation dependencies, then run real-data smoke.
