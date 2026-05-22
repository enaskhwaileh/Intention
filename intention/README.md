# Intention

Input-side implementation of an intention interpretation pipeline.

The project separates user inputs into query profiles and raw intentions,
grounds raw intentions against a lightweight IEKL graph, instantiates
operational intention profiles, validates them, and exposes the intermediate
artifacts needed by downstream ranking.

## Layout

- `configs/`: pipeline and LLM configuration.
- `resources/iekl/`: graph, profile schema, and validation rules.
- `data/`: example JSONL inputs and generated toy outputs.
- `src/intention/`: package source code.
- `scripts/`: runnable entry points for common pipeline steps.
- `tests/`: pytest coverage for graph loading, validation, pipeline, and ranking.

## Quick Start

```bash
pip install -e .[dev]
python scripts/run_input_pipeline.py
pytest
```

Without editable install, run:

```bash
PYTHONPATH=src python3 scripts/run_input_pipeline.py
PYTHONPATH=src pytest
```
