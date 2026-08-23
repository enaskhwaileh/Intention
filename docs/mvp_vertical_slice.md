# Intended-action grounding MVP

This milestone demonstrates one claim: for the same topical query and the same
four tables, changing the intended action changes the usefulness ranking.

The fixed topical order is `A > B > C > D`. The action-conditioned results are:

- compare: `B > C > A > D`
- predict: `C > B > A > D`

## Pipeline

The pipeline loads a fixed `QueryProfile`, grounds a manually selected action,
instantiates and validates its configured requirements, loads manual capability
profiles, retains each requirement's best deterministic match, computes weighted
alignment and usefulness, applies a soft required-evidence gate, and creates an
explanation from the stored match trace.

Typed objects live in `src/intention_mvp/models.py`. Action predicates and
requirements are in `configs/actions.json`; all scoring weights are in
`configs/scoring.json`. The shared vaccine query, relevance scores, candidate
schemas, capabilities, confidence values, and provenance are in
`fixtures/vaccine_mvp.json`.

The operational axes are provisionally `content`, `structure`, `analysis`,
`scope`, `relation`, and `quality`. Relation is centralised in the catalogue but
inactive in this prototype.

## Install and test

Python 3.10 or newer is required.

```bash
python -m pip install -e ".[dev]"
pytest
```

The package has no runtime dependencies.

## Run the demo

```bash
python scripts/run_vaccine_mvp.py
python scripts/run_vaccine_mvp.py --json-output outputs/vaccine_mvp.json
```

It prints the three rankings, concise score/gate explanations, and a complete
machine-readable JSON result. The optional flag writes a standalone JSON
artifact; generated output files are intentionally ignored by Git.

## Limitations

This is deliberately a small deterministic vertical slice. Automatic input
interpretation, automatic action detection, automatic table profiling,
large-scale retrieval, embeddings, vector databases, LLM calls, learned scoring
or calibration, model training, external APIs, integration actions, web APIs,
and user interfaces are outside this milestone.

The matching rules are inspectable baselines, not general semantic equivalence.
Manual capability confidence encodes fixture-specific partial support. Future
work can replace loaders and matching components without changing the pipeline
result contract.
