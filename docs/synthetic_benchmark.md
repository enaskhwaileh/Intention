# Controlled multi-topic synthetic benchmark

## Purpose

This benchmark tests mechanism and regression behavior without external models,
credentials, or human judgments. It is not empirical evidence of real-corpus
effectiveness. Its design controls the topical candidate pool while changing
the intended action.

## Coverage

| Topic | Variant 1 | Expected winner | Variant 2 | Expected winner |
|---|---|---|---|---|
| Vaccine side effects | `COMPARE` rate by country | country rates | `PREDICT` outcome | patient outcomes |
| Employment workforce outcomes | `AGGREGATE` salary by department | department salary | `EXPLAIN` turnover | worker outcomes |
| Public transport delays | `COMPARE` delay by route | route summary | `MONITOR` delay | repeated time series |

All five supported actions appear at least once. Each topic uses the same two
tables and exactly the same topical prefix for both action variants. The test
suite verifies that first-stage relevance scores are identical across the pair.

## Verified result

Six of six gold action/ranking cases pass. In three cases, the final usefulness
winner differs from the relevance-only winner:

| Case | Relevance-only winner | Action-aware winner |
|---|---|---|
| Health `COMPARE` | patient outcomes | country rates |
| Employment `EXPLAIN` | department salary (relevance tie broken by ID) | worker outcomes |
| Transport `MONITOR` | route summary | repeated time series |

The complementary action in each topic selects the other table, establishing
three controlled action-switch pairs. Expected results are declared in the
versioned fixture rather than inferred from a later system run.

## Files and command

- Fixture: `fixtures/synthetic_benchmark.json`
- Strict loader/runner: `src/intention/benchmarks/synthetic.py`
- Regression tests: `tests/test_synthetic_benchmark.py`

```bash
PYTHONPATH=src python3 -m intention synthetic-benchmark
```

The command exits nonzero if any declared action or ranking expectation fails.

## Scientific limitations

- Tables, requests, and gold rankings are author-constructed.
- BM25 is the first-stage retriever; no neural semantic result is claimed.
- Capability extraction uses deterministic heuristics that have not yet been
  evaluated against independently annotated real tables.
- Weights are controlled experiment defaults, not calibrated parameters.
- The benchmark detects regressions and illustrates the action-switch mechanism;
  it cannot support general effectiveness or significance claims.

## Cleanup performed with this milestone

Reference analysis identified a self-contained superseded cluster: the old
six-axis domain registry, deterministic MVP package, duplicate JSON/YAML
configurations, vaccine MVP runner/fixture/tests, and phase-era documents that
described those definitions. These were removed because the normative pipeline
did not import them and the project does not plan to use their conflicting
formulation. Generated Python and pytest caches were also removed. Git history
retains every deleted file if historical inspection is needed.
