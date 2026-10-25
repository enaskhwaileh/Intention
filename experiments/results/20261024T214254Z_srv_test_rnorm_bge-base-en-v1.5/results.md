# IGBench results (20261024T214254Z_srv_test_rnorm_bge-base-en-v1.5)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.843 | 0.550 | 0.335 | 0.918 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.823 | 0.540 | 0.330 | 0.912 | 0.950 | 0.900 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.840 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:sbert+rnorm=minmax | 0.819 | 0.526 | 0.947 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.437 | 0.831 | 0.918 |
| ig:rule/index:sbert+rnorm=minmax | 0.387 | 0.821 | 0.912 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.803 | 0.804 | 0.843 | 0.923 |
| ig:rule/index:sbert+rnorm=minmax | 0.803 | 0.803 | 0.817 | 0.856 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.885 |
| ig:rule/index:sbert+rnorm=minmax | 0.885 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.614 | 0.761 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.568 | 0.648 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 107.4 / 88.1 / 95.1 | 0.2 / 0.2 / 0.2 | 37.6 / 19.6 / 27.6 | 303.4 / 154.8 / 884.0 | 0.1 / 0.1 / 0.1 | 449.6 / 298.7 / 995.1 | 9.458 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.2 / 0.7 | 83.8 / 83.5 / 86.4 | 0.3 / 0.2 / 0.3 | 42.7 / 19.7 / 37.3 | 317.8 / 146.3 / 1082.6 | 0.1 / 0.1 / 0.1 | 446.3 / 251.0 / 1313.1 | 9.394 |

Context index build (one-off, ms): sbert: 9730 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
