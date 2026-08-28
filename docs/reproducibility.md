# Reproducibility

## Synthetic checkpoint

```bash
python3 -m pip install -e ".[dev]"
pytest -q
python -m intention smoke
python -m intention synthetic-benchmark
python -m intention evaluate-profiler
python -m intention evaluate-interpreter
python -m intention evaluate-controlled
python -m intention demo-snapshot --check
```

The core suite stays offline. CLI commands include `smoke`, `demo-snapshot`,
`profile`, `interpret`,
`retrieve`, `build-benchmark`, `run-baselines`, `run-main`, `run-ablations`,
`run-sensitivity`, `evaluate`, and `generate-paper-tables`. Use `ruff check .`
and `mypy src` for lint and type checks.

## Run provenance

Every run is a new `artifacts/runs/<run_id>/` with configuration/hash, Git commit,
environment, dataset manifest, knowledge version, metrics, per-query metrics,
predictions, timings, and logs. Runners refuse overwrite; reporting fails on
missing fields. Full experiments require explicit data, pinned models, and
compute. No external result is claimed unless `STATUS.md` lists its verified ID.
