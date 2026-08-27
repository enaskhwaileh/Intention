# Intended-Action Grounding for Dataset Discovery

This repository implements action-aware table discovery. It separates topical
relevance from the analytical action a user intends to perform, profiles table
capabilities, aligns grounded requirements with that evidence, and combines
relevance and alignment into a usefulness ranking.

## Current verified scope

- Strict versioned five-action/five-axis knowledge layer.
- Deterministic profiling and interpretation for synthetic evaluation.
- Topical-only BM25 candidate retrieval.
- Exact requirement–capability alignment and usefulness equations.
- Leakage-safe benchmark utilities, metrics, run provenance, and reporting.
- Controlled synthetic action-switch demonstrations.

No real-data effectiveness or external-model result is currently claimed. See
`STATUS.md` for verified work and blockers.

## Setup and verification

```bash
python3 -m pip install -e '.[dev]'
pytest -q
python3 -m intention smoke
```

Without an editable install:

```bash
PYTHONPATH=src python3 -m intention smoke
```

Controlled comparison example:

```bash
PYTHONPATH=src python3 -m intention smoke \
  --input "vaccine side effects compare measure=rate, comparison dimension=country"
```

Run all three controlled topic/action pairs:

```bash
PYTHONPATH=src python3 -m intention synthetic-benchmark
```

## Authoritative documents

- `docs/method_contract.md` — mathematics and scientific boundaries.
- `docs/contract_traceability.md` — contract-to-code-and-test mapping.
- `docs/experiment_protocol.md` — leakage-safe evaluation protocol.
- `docs/reproducibility.md` — commands and run artifacts.
- `PLANS.md` and `STATUS.md` — milestones and verified state.
- `docs/supervisor_method_report.md` — detailed controlled example.
- `docs/synthetic_benchmark.md` — multi-topic action-switch benchmark.
