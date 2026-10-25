# IGBench results (20261024T224509Z_srv_test_llm_bge-base-en-v1.5)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.510 | 0.305 | 0.879 | 0.975 | 0.950 | 0.000 |
| ig:llm/llm:sbert | 0.763 | 0.520 | 0.315 | 0.853 | 0.921 | 0.900 | 0.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.811 | 0.520 | 0.320 | 0.899 | 0.967 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.804 | 0.495 | 0.974 | 0.947 |
| ig:llm/llm:sbert | 0.756 | 0.505 | 0.917 | 0.895 |
| ig:llm/llm:sbert+rnorm=minmax | 0.807 | 0.505 | 0.965 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.437 | 0.797 | 0.879 |
| ig:llm/llm:sbert | 0.387 | 0.768 | 0.853 |
| ig:llm/llm:sbert+rnorm=minmax | 0.437 | 0.805 | 0.899 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.794 | 0.763 | 0.799 | 0.867 |
| ig:llm/llm:sbert | 0.766 | 0.836 | 0.636 | 0.832 |
| ig:llm/llm:sbert+rnorm=minmax | 0.766 | 0.798 | 0.802 | 0.894 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.871 |
| ig:llm/llm:sbert | 0.900 |
| ig:llm/llm:sbert+rnorm=minmax | 0.871 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.485 | 0.800 |
| ig:llm/llm:sbert+rnorm=minmax | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.485 | 0.800 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 157.4 / 133.3 / 248.4 | – | – | – | – | 157.5 / 133.4 / 248.5 | 3.309 |
| ig:llm/llm:sbert | 3.2 / 3.1 / 4.3 | 142.5 / 141.3 / 147.1 | 1.5 / 1.6 / 3.0 | 36.3 / 0.0 / 61.3 | 244.1 / 0.0 / 764.9 | 0.3 / 0.3 / 0.5 | 286.2 / 5.4 / 1196.6 | 5.842 |
| ig:llm/llm:sbert+rnorm=minmax | 3.9 / 3.4 / 6.4 | 144.5 / 142.8 / 151.4 | 1.4 / 1.6 / 2.6 | 14.0 / 0.0 / 42.1 | 265.2 / 0.0 / 737.0 | 0.3 / 0.3 / 0.5 | 285.7 / 7.2 / 783.4 | 6.176 |

Context index build (one-off, ms): sbert: 12906 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.000 | [-0.028, +0.030] | 0.994 | 5/7 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | -0.008 | [-0.025, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.046 | [-0.138, +0.020] | 0.366 | 6/8 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.054 | [-0.153, +0.000] | 0.493 | 0/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
