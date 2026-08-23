# Project context

This file records verified facts about the repository at the `mvp-restart`
checkpoint. It does not claim that provisional design choices are final or that
the current demonstration is an empirical evaluation.

## Repository state

- The Git remote named `origin` is `git@github.com:enaskhwaileh/Intention.git`.
- The checkpoint branch is based on the history containing cleanup commit
  `5a9fdd720419e0555bcd7a3adee0efd9304876d4`.
- Cleanup commit `5a9fdd7` removed the previous implementation.
- The current MVP was added after that cleanup without restoring the deleted
  legacy files.
- The project requires Python 3.10 or newer and declares no runtime
  dependencies.
- The offline test suite is configured for `pytest` and contains 12 tests.

## Implemented purpose and scenario

The repository implements a deterministic vertical slice for
intended-action-aware dataset ranking. It uses one fixed query, "COVID-19
vaccine side effects in Europe.", and four manually specified candidate-table
profiles.

The fixture supplies the query profile, topical relevance scores, table
schemas, capability claims, confidence values, and provenance. The action
catalogue supplies two actions, `compare` and `predict`, and their required and
optional requirements. The scoring configuration supplies fixed weights and a
required-evidence demotion multiplier.

For the supplied fixture, the implementation produces:

```text
Relevance: A > B > C > D
Compare:   B > C > A > D
Predict:   C > B > A > D
```

## Implemented pipeline

The code:

1. loads the fixed query and manually selected action;
2. instantiates and validates configured action requirements;
3. loads and validates manually authored table-capability profiles;
4. selects the best deterministic capability match for each requirement;
5. computes weighted alignment and action-conditioned usefulness;
6. applies a soft demotion when required evidence is below threshold; and
7. emits ranking results with match traces and provenance-based explanations.

Unsupported actions and invalid requirement profiles fall back to topical
relevance ranking.

## Current boundaries

The repository does not implement automatic query interpretation, automatic
action detection, automatic table profiling, semantic retrieval, embeddings,
vector search, model training, LLM calls, external APIs, a web service, or a
user interface. It contains no paper manuscript, bibliography, large-scale
experiment, user study, or independently annotated evaluation dataset.

The six axes in the current catalogue and the scoring weights in
`configs/scoring.json` are implemented configuration choices for this MVP.
Their presence does not establish them as a final taxonomy or validated paper
parameters.

## Verification commands

Run the tests from the repository root:

```bash
pytest -q
```

Run the demonstration:

```bash
python3 scripts/run_vaccine_mvp.py
```
