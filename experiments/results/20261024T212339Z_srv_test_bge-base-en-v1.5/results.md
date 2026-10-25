# IGBench results (20261024T212339Z_srv_test_bge-base-en-v1.5)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.510 | 0.305 | 0.879 | 0.975 | 0.950 | 0.000 |
| ig:gold/gold:sbert | 0.781 | 0.540 | 0.340 | 0.937 | 0.929 | 0.900 | 0.000 |
| ig:rule/index:sbert | 0.751 | 0.490 | 0.335 | 0.887 | 0.892 | 0.850 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.804 | 0.495 | 0.974 | 0.947 |
| ig:gold/gold:sbert | 0.775 | 0.526 | 0.925 | 0.895 |
| ig:rule/index:sbert | 0.744 | 0.474 | 0.886 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.437 | 0.797 | 0.879 |
| ig:gold/gold:sbert | 0.345 | 0.824 | 0.937 |
| ig:rule/index:sbert | 0.295 | 0.735 | 0.887 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.794 | 0.763 | 0.799 | 0.867 |
| ig:gold/gold:sbert | 0.778 | 0.830 | 0.674 | 0.856 |
| ig:rule/index:sbert | 0.783 | 0.812 | 0.591 | 0.813 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.871 |
| ig:gold/gold:sbert | 0.903 |
| ig:rule/index:sbert | 0.913 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.614 | 0.761 |
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.568 | 0.648 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 107.4 / 87.1 / 170.4 | – | – | – | – | 107.4 / 87.1 / 170.5 | 2.256 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 91.7 / 91.5 / 95.0 | 0.2 / 0.2 / 0.3 | 116.5 / 49.8 / 271.4 | 299.9 / 153.3 / 883.3 | 0.1 / 0.1 / 0.1 | 509.4 / 349.5 / 998.2 | 10.721 |
| ig:rule/index:sbert | 0.5 / 0.2 / 0.7 | 89.5 / 88.8 / 93.6 | 0.3 / 0.3 / 0.4 | 48.5 / 27.6 / 47.6 | 317.8 / 146.1 / 1062.9 | 0.1 / 0.1 / 0.1 | 458.1 / 280.6 / 1344.9 | 9.646 |

Context index build (one-off, ms): sbert: 69470

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.057 | [-0.157, +0.022] | 0.306 | 9/10 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.083 | [-0.219, +0.037] | 0.375 | 1/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.100 | [-0.300, +0.100] | 0.631 | 1/3 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.028 | [-0.096, +0.029] | 0.439 | 10/9 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.046 | [-0.154, +0.050] | 0.499 | 1/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
