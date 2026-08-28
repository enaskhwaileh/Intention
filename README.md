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
- Frozen provider-independent retrieval results, topical-only routing,
  versioned table serialization, candidate-depth policy, and fail-closed
  external retriever registry.

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

Evaluate profiling against controlled gold annotations:

```bash
PYTHONPATH=src python3 -m intention evaluate-profiler
```

Evaluate deterministic interpretation and grounding:

```bash
PYTHONPATH=src python3 -m intention evaluate-interpreter
```

Regenerate the credential-free Milestone Demonstrator:

```bash
PYTHONPATH=src python3 -m intention demo-snapshot
```

The executable notebook is `notebooks/system_demo.ipynb`. Its stored
synthetic artifacts are under `demo_snapshots/` and are not paper results.

## Authoritative documents

- `docs/method_contract.md` — mathematics and scientific boundaries.
- `docs/contract_traceability.md` — contract-to-code-and-test mapping.
- `docs/experiment_protocol.md` — leakage-safe evaluation protocol.
- `docs/reproducibility.md` — commands and run artifacts.
- `PLANS.md` and `STATUS.md` — milestones and verified state.
- `docs/supervisor_method_report.md` — detailed controlled example.
- `docs/synthetic_benchmark.md` — multi-topic action-switch benchmark.
- `docs/capability_annotation_protocol.md` and `docs/profiler_validation.md` —
  gold policy, structured granularity, and controlled diagnostics.
- `docs/interpretation_protocol.md` and `docs/interpreter_validation.md` —
  structured provider boundary, ambiguity rules, and controlled diagnostics.
- `docs/retrieval_contract.md` — Milestone 5 first-stage input, serialization,
  result, depth, timing, and availability contracts.
- `notebooks/system_demo.ipynb` and `demo_snapshots/` — executable pipeline
  observability and immutable milestone archives.
