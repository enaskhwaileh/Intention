# IGBench results (20261024T212415Z_srv_dev_bge-base-en-v1.5)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.806 | 0.531 | 0.337 | 0.886 | 0.858 | 0.743 | 0.143 |
| ig:gold/gold:sbert | 0.793 | 0.554 | 0.340 | 0.875 | 0.945 | 0.914 | 0.029 |
| ig:rule/index:sbert | 0.797 | 0.549 | 0.349 | 0.897 | 0.924 | 0.886 | 0.029 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.525 | 0.845 | 0.719 |
| ig:gold/gold:sbert | 0.794 | 0.550 | 0.940 | 0.906 |
| ig:rule/index:sbert | 0.798 | 0.544 | 0.917 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.294 | 0.777 | 0.886 |
| ig:gold/gold:sbert | 0.359 | 0.793 | 0.875 |
| ig:rule/index:sbert | 0.356 | 0.796 | 0.897 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.986 | 0.825 | 0.831 | 0.716 | 0.771 |
| ig:gold/gold:sbert | 0.937 | 0.853 | 0.828 | 0.731 | 0.682 |
| ig:rule/index:sbert | 0.948 | 0.859 | 0.838 | 0.691 | 0.707 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.842 |
| ig:gold/gold:sbert | 0.853 |
| ig:rule/index:sbert | 0.855 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.505 | 0.783 |
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.480 | 0.778 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 102.0 / 91.2 / 98.1 | – | – | – | – | 102.0 / 91.2 / 98.2 | 3.673 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 91.9 / 91.9 / 104.8 | 0.2 / 0.2 / 0.3 | 95.9 / 29.9 / 451.2 | 888.1 / 287.8 / 4074.6 | 0.1 / 0.1 / 0.1 | 1077.3 / 494.6 / 4252.0 | 38.823 |
| ig:rule/index:sbert | 0.4 / 0.2 / 0.7 | 90.5 / 89.5 / 98.6 | 0.3 / 0.3 / 0.7 | 51.2 / 20.7 / 273.4 | 789.4 / 153.0 / 4160.6 | 0.1 / 0.1 / 0.1 | 933.0 / 296.3 / 4275.8 | 33.634 |

Context index build (one-off, ms): sbert: 11348 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.010 | [-0.051, +0.029] | 0.640 | 13/16 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.066 | [+0.004, +0.137] | 0.064 | 5/1 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.143 | [+0.029, +0.257] | 0.064 | 5/0 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.015 | [-0.070, +0.036] | 0.654 | 14/17 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.087 | [+0.014, +0.169] | 0.031 | 6/1 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.171 | [+0.057, +0.286] | 0.031 | 6/0 |
