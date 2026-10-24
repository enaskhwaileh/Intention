# IGBench results (20261024T224444Z_srv_test_llm_e5-base-v2)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.778 | 0.490 | 0.305 | 0.880 | 0.950 | 0.900 | 0.000 |
| ig:llm/llm:sbert | 0.777 | 0.520 | 0.320 | 0.899 | 0.938 | 0.900 | 0.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.809 | 0.510 | 0.330 | 0.911 | 0.950 | 0.900 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.775 | 0.474 | 0.947 | 0.895 |
| ig:llm/llm:sbert | 0.773 | 0.505 | 0.934 | 0.895 |
| ig:llm/llm:sbert+rnorm=minmax | 0.807 | 0.495 | 0.947 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.390 | 0.778 | 0.880 |
| ig:llm/llm:sbert | 0.345 | 0.804 | 0.899 |
| ig:llm/llm:sbert+rnorm=minmax | 0.383 | 0.792 | 0.911 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.731 | 0.783 | 0.755 | 0.853 |
| ig:llm/llm:sbert | 0.736 | 0.829 | 0.665 | 0.858 |
| ig:llm/llm:sbert+rnorm=minmax | 0.736 | 0.831 | 0.759 | 0.901 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.875 |
| ig:llm/llm:sbert | 0.945 |
| ig:llm/llm:sbert+rnorm=minmax | 0.878 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.516 | 0.762 |
| ig:llm/llm:sbert+rnorm=minmax | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.516 | 0.762 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 151.9 / 129.0 / 142.4 | – | – | – | – | 152.0 / 129.2 / 142.5 | 3.193 |
| ig:llm/llm:sbert | 4.3 / 4.2 / 5.8 | 92.5 / 91.7 / 98.3 | 1.3 / 1.3 / 2.7 | 65.3 / 0.0 / 26.8 | 124.2 / 0.0 / 166.2 | 0.2 / 0.1 / 0.4 | 195.8 / 6.8 / 1046.9 | 4.101 |
| ig:llm/llm:sbert+rnorm=minmax | 4.2 / 3.7 / 6.4 | 87.6 / 89.5 / 92.6 | 1.6 / 1.0 / 3.5 | 7.3 / 0.0 / 24.4 | 115.4 / 0.0 / 139.6 | 0.2 / 0.1 / 0.6 | 129.1 / 7.4 / 172.4 | 3.368 |

Context index build (one-off, ms): sbert: 18628 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.019 | [-0.022, +0.058] | 0.378 | 8/4 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.000 | [-0.075, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.012 | [-0.074, +0.036] | 0.736 | 9/5 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.013 | [-0.113, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
