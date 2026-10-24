# IGBench results (20261024T212109Z_srv_dev_e5-base-v2)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.820 | 0.543 | 0.337 | 0.894 | 0.929 | 0.886 | 0.057 |
| ig:gold/gold:sbert | 0.757 | 0.549 | 0.329 | 0.853 | 0.920 | 0.886 | 0.057 |
| ig:rule/index:sbert | 0.775 | 0.549 | 0.343 | 0.893 | 0.902 | 0.857 | 0.086 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.826 | 0.519 | 0.943 | 0.906 |
| ig:gold/gold:sbert | 0.757 | 0.525 | 0.933 | 0.906 |
| ig:rule/index:sbert | 0.777 | 0.525 | 0.913 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.361 | 0.780 | 0.894 |
| ig:gold/gold:sbert | 0.360 | 0.783 | 0.853 |
| ig:rule/index:sbert | 0.356 | 0.801 | 0.893 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.948 | 0.829 | 0.835 | 0.773 | 0.798 |
| ig:gold/gold:sbert | 0.854 | 0.809 | 0.772 | 0.745 | 0.648 |
| ig:rule/index:sbert | 0.893 | 0.843 | 0.794 | 0.682 | 0.690 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.834 |
| ig:gold/gold:sbert | 0.865 |
| ig:rule/index:sbert | 0.847 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.520 | 0.792 |
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.494 | 0.783 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 96.2 / 84.9 / 91.9 | – | – | – | – | 96.3 / 85.0 / 92.0 | 3.467 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 91.6 / 92.1 / 98.8 | 0.2 / 0.2 / 0.3 | 226.3 / 66.2 / 666.6 | 889.4 / 304.4 / 3816.9 | 0.1 / 0.1 / 0.1 | 1208.7 / 645.8 / 4006.5 | 43.561 |
| ig:rule/index:sbert | 0.4 / 0.2 / 0.7 | 90.4 / 90.1 / 97.3 | 0.3 / 0.3 / 0.4 | 108.5 / 21.0 / 411.7 | 651.8 / 184.2 / 2492.9 | 0.1 / 0.1 / 0.1 | 852.6 / 334.1 / 3059.5 | 30.734 |

Context index build (one-off, ms): sbert: 11155 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.045 | [-0.084, -0.011] | 0.019 | 8/22 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.027 | [-0.083, +0.009] | 0.506 | 1/2 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.063 | [-0.124, -0.008] | 0.037 | 8/23 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.009 | [-0.079, +0.043] | 1.000 | 2/1 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
