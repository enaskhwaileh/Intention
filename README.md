# Intended-Action Grounding for Dataset Discovery

This repository implements a fail-closed research pipeline:

`interpreter -> canonical-AB grounder -> local table profiler -> axis comparison`

The canonical Action Base is `intention_grounding/docs/ab_proposal/action-base-v0.1.json`, version
`0.1.0-draft` (proposal dated 26 September 2026). Files in `intention_grounding/kb/` and
`scripts/grounder_production.py` are legacy inputs and are not used by the new pipeline.

## Install and verify offline

Python 3.10 or newer is required.

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m intention_grounding.cli --mode offline --output outputs/pipeline
```

The offline replay fixtures are manually authored software-contract fixtures, not empirical model
evaluation and not an accuracy measurement. The command prints a two-line summary and writes separate
raw interpreter and grounder responses, validated interpretation, grounding/card, table profiles,
comparison, and run manifest files beneath a unique run directory.

## WikiDBs-10k data

No WikiDBs-10k archive or extracted WikiDBs tables were present in the inspected checkout on
27 September 2026. The files under `intention_grounding/data/` are older project fixtures, contain
asserted meanings/suitability, and are not treated as WikiDBs observations. Nothing is downloaded or
duplicated automatically.

The official WikiDBs-10k v1 record is `https://doi.org/10.5281/zenodo.8227452`, published
29 August 2023 under CC BY 4.0. Zenodo lists `wikidbs_10k.zip` with MD5
`71ebb739508f1a54b79c2112687d5d83`; this repository has not downloaded or independently checked that
archive. After obtaining it, verify that checksum, record the actual acquisition date (and preferably a
local SHA-256), then pass extracted CSV files or JSON arrays of row objects explicitly:

```bash
.venv/bin/python -m intention_grounding.cli --mode offline \
  --dataset /absolute/path/to/table-a.csv --dataset /absolute/path/to/table-b.json \
  --dataset-metadata intention_grounding/fixtures/wikidbs10k-source-metadata.json \
  --max-tables 2 --output outputs/wikidbs-smoke
```

Inputs are sorted by path and `--max-tables N` selects the first N, giving a reproducible subset.
Content SHA-256-derived IDs remain stable table IDs. `wikidbs10k-source-metadata.json` records official release
metadata separately from the deliberately unset local acquisition state; update the latter after retrieval.
WikiDBs is a Wikidata-derived relational table corpus. It does not provide gold intended-action or table
suitability labels; any future task labels must be clearly versioned project annotations.

The profiler performs a complete local scan for row counts, column names, observed primitive types,
missingness, distinct counts, and finite numeric ranges, each with file SHA-256 evidence. It does not infer
column meaning, units, relation bindings, or suitability. Consequently unsupported AB predicates remain
`unknown`, never silently satisfied.

## Opt-in live Groq run

Install the optional SDK, choose a currently available model explicitly, and provide the key only through
the environment. Never commit `.env` or keys.

```bash
.venv/bin/python -m pip install -e '.[groq]'
export GROQ_API_KEY='...'
.venv/bin/python -m intention_grounding.cli --mode groq --model YOUR_GROQ_MODEL \
  --input-id request-1 --input 'Compare annual income in France in 2019 versus 2021.' \
  --dataset /absolute/path/to/wikidbs-table.csv --output outputs/live
```

Live execution is never used by default tests or CI. Both model stages use constrained JSON responses;
all IDs, argument references, evidence references, inherited roles, cardinalities, and AB versions are
then validated locally. Provider failures and malformed/unsupported/ambiguous/insufficient results do not
emit a grounded card.

Known limitations: the canonical AB only supports direct-observation descriptive comparison; the first
grounder response format does not activate the AB's manually reviewed complete-grid derivation; and the
local profiler cannot yet establish semantic, unit/population, or logical observation-relation predicates.
