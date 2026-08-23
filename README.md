# Intended-Action Grounding for Dataset Discovery

This repository contains the first executable vertical slice for
intended-action-aware dataset ranking.

The `full-pipeline-architecture` branch is building a scientifically explicit
research system in reviewed phases. Phases 0–2 add validated domain contracts
and versioned registries for five canonical actions while preserving this
deterministic vertical slice as a regression implementation. See
`docs/implementation_status.md`; planned modules are not described as working.

For the unchanged query **“COVID-19 vaccine side effects in Europe.”** and the
same four candidate tables, the prototype deterministically produces:

```text
Relevance: A > B > C > D
Compare:   B > C > A > D
Predict:   C > B > A > D
```

Run it:

```bash
python scripts/run_vaccine_mvp.py
```

Run the offline test suite:

```bash
pytest
```

Validate the environment and registries:

```bash
python3 scripts/verify_environment.py
```

See [docs/mvp_vertical_slice.md](docs/mvp_vertical_slice.md) for architecture,
installation, scoring, limitations, and deliberately postponed work. Repository
inspection and implementation assumptions are recorded in
[docs/mvp_implementation_status.md](docs/mvp_implementation_status.md).
