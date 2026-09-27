# Intention grounding

The current pipeline is `interpreter → canonical Action Base grounder → local table profiler → conservative axis comparison`. The CLI at `intention_grounding.cli:main` is the canonical entry point. It uses manually authored replay responses and a bundled synthetic CSV by default. These verify software contracts; they do not measure model accuracy or real dataset suitability.

## Environment and offline run

Python 3.10 or newer is required. This checkout has `./.venv` (Python 3.10 with the project and required dependencies) and a parent `../.venv` (Python 3.9, below the supported version). Use the existing repository environment; neither environment needs to be recreated or removed for this walkthrough. From the repository root:

```bash
./.venv/bin/python -m unittest discover -s tests -v
./.venv/bin/python -m intention_grounding.cli --mode offline --output outputs/pipeline
```

The CLI creates a unique `outputs/pipeline/run-*/` directory containing raw provider responses, validated interpretation, grounding/card, table profiles, comparison, and a run manifest. `outputs/` is ignored by Git. To install into another existing Python 3.10+ environment, use `python -m pip install -e .` there. The installed `intention-grounding` console script is equivalent to `python -m intention_grounding.cli`.

For a step-by-step view, open [the offline walkthrough](notebooks/pipeline_walkthrough.ipynb) with a Python 3.10+ kernel using an environment where this project is installed. Jupyter is optional and is **not installed** in this checkout's `./.venv`; the parent `../.venv` has Jupyter but its Python 3.9 kernel is too old. If you want to use the existing repository environment for Jupyter, install the optional notebook dependencies into it, then launch from the root:

```bash
uv pip install --python .venv/bin/python -e '.[notebook]'
./.venv/bin/python -m notebook notebooks/pipeline_walkthrough.ipynb
```

Select the Python kernel belonging to `./.venv` if Jupyter offers more than one. The notebook prints `sys.executable` in its first cell so you can verify the selected kernel. No new virtual environment is needed.

## Data and scope

`intention_grounding/fixtures/offline_table.csv` is a four-row synthetic table. `intention_grounding/data/` contains older, asserted query labels and table descriptions for the legacy workflow; these are not observed table scans or verified suitability labels for the current pipeline. No WikiDBs-10k archive or extracted WikiDBs tables were found in this checkout. The WikiDBs source metadata file describes a possible future input, with local acquisition marked `not-acquired`; it is not proof of downloaded data. The current pipeline has no verified gold intended-action or table-suitability annotations for that corpus.

The profiler records observed columns, primitive types, missingness, row counts, numeric ranges, and file SHA-256 evidence. It does not infer semantic column meaning, units, populations, or observation relations. The aligner therefore marks requirements `unknown` rather than claiming suitability. The draft Action Base supports direct-observation descriptive comparisons; its complete-grid derivation is documented but is not activated by the current grounder response format.

## Optional live Groq use

Live execution requires the optional `groq` package. Install it into the existing environment if needed with `uv pip install --python .venv/bin/python -e '.[groq]'`. Copy the names-only template to the ignored project configuration file and open it in an editor. The copy command preserves an existing `.env` file:

```bash
cp -n .env.example intention_grounding/.env
${EDITOR:-vi} intention_grounding/.env
```

Use `KEY=value` syntax with no spaces around `=`. Set `GROQ_API_KEY` there, then list the model IDs available to your authenticated account:

```bash
./.venv/bin/python -m intention_grounding.cli --list-models
```

That command makes one authenticated model-list API call and prints IDs only. Set `GROQ_MODEL_ID` in the same `.env` file to one of those IDs, then run:

```bash
./.venv/bin/python -m intention_grounding.cli --mode groq \
  --input-id request-1 --input 'Compare annual income in France in 2019 versus 2021.' \
  --dataset /absolute/path/to/local-table.csv --output outputs/live
```

The application reads `intention_grounding/.env` from the package path, regardless of the working directory. Already exported process variables take precedence, and `--model` can override `GROQ_MODEL_ID`. Keep the file local and never put a key in a command argument, notebook, or tracked file. Live mode makes up to two Groq calls. Provider failures write only a fixed exception label and, when available, a numeric HTTP status or allowlisted error code to the run artifact. Raw exception text, request headers, and credentials are never saved. The notebook remains offline unless its opt-in flag is deliberately enabled. Tests and CI use no live calls. See [repository map](docs/REPOSITORY_MAP.md) for file roles and cleanup candidates.
