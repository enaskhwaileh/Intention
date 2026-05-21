# Intention

Toy implementation of an intention profiling pipeline.

The project separates user inputs into query profiles, grounds them against a
small IEKL graph, instantiates operational profiles, validates them, and ranks
candidate table profiles.

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
pytest
python scripts/run_input_pipeline.py
python scripts/run_profile_validation.py
python scripts/run_toy_ranking.py
```
