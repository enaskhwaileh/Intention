# IGBench results (20261025T121527Z_plan_igb-dev_timing)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:rule/index:bm25 | 0.788 | 0.531 | 0.331 | 0.875 | 0.909 | 0.829 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ig:gold/gold:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:rule/index:bm25 | 0.801 | 0.519 | 0.932 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ig:gold/gold:bm25 | 0.311 | 0.781 | 0.882 |
| ig:rule/index:bm25 | 0.321 | 0.782 | 0.875 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ig:gold/gold:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:rule/index:bm25 | 0.964 | 0.831 | 0.807 | 0.699 | 0.770 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ig:gold/gold:bm25 | 0.860 |
| ig:rule/index:bm25 | 0.843 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/index:bm25 | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.0 / 4.9 / 7.3 | – | – | – | – | 5.1 / 5.0 / 7.5 | 0.184 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 4.4 / 4.3 / 6.9 | 0.1 / 0.1 / 0.2 | 39.4 / 40.1 / 76.2 | 931.7 / 318.3 / 3774.4 | 0.1 / 0.1 / 0.1 | 976.9 / 376.6 / 3810.9 | 35.198 |
| ig:rule/index:bm25 | 0.4 / 0.1 / 0.6 | 6.3 / 4.7 / 8.8 | 0.2 / 0.2 / 0.3 | 32.7 / 39.0 / 53.4 | 841.6 / 123.1 / 3629.2 | 0.1 / 0.1 / 0.1 | 882.4 / 178.2 / 3680.6 | 31.793 |

Context index build (one-off, ms): bm25: 53 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.019 | [-0.000, +0.041] | 0.069 | 16/8 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.014 | [-0.009, +0.052] | 0.751 | 2/1 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
