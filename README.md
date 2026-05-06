# intention-capability-extractor

`intention-capability-extractor` is a small Python project for building deterministic, offline capability profiles for tabular datasets. It is the Version 0 extraction stage of an intention-aware dataset discovery framework.

The project does not implement ranking, user intention parsing, usefulness scoring, embeddings, LLM calls, external APIs, or learned models. Its purpose is to create a simple, inspectable foundation for representing what a table can support before any downstream discovery or recommendation layer is added.

## Motivation

Dataset discovery often needs more than keyword search. A user may need a table that can support comparison, aggregation, prediction, joining, or explanation. Before a system can rank datasets for those intentions, it needs an offline representation of each table's capabilities.

This repository extracts that representation with deterministic rules. The rules are intentionally modest so every profile can be inspected, reproduced, and improved over time.

## Capability Axes

The primary profile is organized around four capability axes:

- **Semantic**: keywords, measure-like terms, frequent entity candidates, and shallow domain hints from table and column names.
- **Structural**: row and column counts, inferred column types, numeric columns, categorical columns, dates, identifiers, grouping candidates, and measure candidates.
- **Coverage**: categorical cardinality, top categorical values, numeric ranges, temporal ranges, and simple geographic column detection.
- **Quality**: missingness, duplicate rows, uniqueness ratios, constant columns, and empty string rates.

The project also derives an **action-affordance layer**:

- `compare`
- `aggregate`
- `predict`
- `join`
- `explain`

These affordances are simple labels (`strong`, `moderate`, `possible`, `weak`) computed from the lower-level capability axes. For example, comparison is strong when a table has both grouping candidates and measure candidates.

## Why These Axes

These axes were selected because they are useful before a user-specific ranking model exists:

- Semantic signals describe what the table appears to be about.
- Structural signals describe how the table can be operated on.
- Coverage signals describe what value space the table covers.
- Quality signals describe whether the table is likely to be usable.
- Action affordances translate raw profile signals into early hints about analytical tasks the table may support.

Together, they form a compact offline table profile that can later feed intention parsing, dataset matching, and usefulness scoring.

## Repository Structure

```text
intention-capability-extractor/
├── data/
│   ├── raw/
│   └── toy/
├── notebooks/
├── outputs/
│   └── profiles/
├── scripts/
│   └── run_profile_extraction.py
├── src/
│   └── intention_capability/
│       ├── extractors/
│       ├── utils/
│       ├── io.py
│       ├── models.py
│       └── pipeline.py
└── tests/
```

## Installation

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Run Toy Examples

Single file mode:

```bash
python scripts/run_profile_extraction.py \
  --input data/toy/aggregated_vaccine_side_effects.csv \
  --table-id aggregated_vaccine_side_effects \
  --table-name "Aggregated vaccine side effects by country and brand" \
  --output outputs/profiles/aggregated_vaccine_side_effects.json
```

Directory mode:

```bash
python scripts/run_profile_extraction.py \
  --input-dir data/toy \
  --output-dir outputs/profiles
```

## Run Tests

```bash
pytest
```

## Current Scope and Limitations

This is Version 0. The implementation is intentionally shallow and deterministic:

- No embeddings or semantic vector search.
- No LLM-based interpretation.
- No external APIs.
- No learned type inference or ranking model.
- No user intention parsing.
- No usefulness scoring.

The current pipeline is best viewed as a working foundation for offline table capability representation. Future versions can add richer profiling, learned models, and downstream ranking while keeping these starter profiles as transparent baseline signals.
