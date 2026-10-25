# IGBench results (20261024T230603Z_srv_test_llm31_bge-base-en-v1.5)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.510 | 0.305 | 0.879 | 0.975 | 0.950 | 0.000 |
| ig:llm/llm:sbert | 0.757 | 0.520 | 0.310 | 0.873 | 0.929 | 0.900 | 0.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.812 | 0.530 | 0.320 | 0.886 | 0.967 | 0.950 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.757 | 0.520 | 0.310 | 0.873 | 0.929 | 0.900 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.812 | 0.530 | 0.320 | 0.886 | 0.967 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.804 | 0.495 | 0.974 | 0.947 |
| ig:llm/llm:sbert | 0.759 | 0.516 | 0.925 | 0.895 |
| ig:llm/llm:sbert+rnorm=minmax | 0.817 | 0.526 | 0.965 | 0.947 |
| ig:llm/llm:sbert+repair=1 | 0.759 | 0.516 | 0.925 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.817 | 0.526 | 0.965 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.437 | 0.797 | 0.879 |
| ig:llm/llm:sbert | 0.387 | 0.797 | 0.873 |
| ig:llm/llm:sbert+rnorm=minmax | 0.437 | 0.810 | 0.886 |
| ig:llm/llm:sbert+repair=1 | 0.387 | 0.797 | 0.873 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.437 | 0.810 | 0.886 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.794 | 0.763 | 0.799 | 0.867 |
| ig:llm/llm:sbert | 0.725 | 0.726 | 0.783 | 0.829 |
| ig:llm/llm:sbert+rnorm=minmax | 0.783 | 0.751 | 0.821 | 0.921 |
| ig:llm/llm:sbert+repair=1 | 0.725 | 0.726 | 0.783 | 0.829 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.783 | 0.751 | 0.821 | 0.921 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.871 |
| ig:llm/llm:sbert | 0.900 |
| ig:llm/llm:sbert+rnorm=minmax | 0.881 |
| ig:llm/llm:sbert+repair=1 | 0.900 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.881 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.633 | 0.775 |
| ig:llm/llm:sbert+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.633 | 0.775 |
| ig:llm/llm:sbert+repair=1 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.633 | 0.775 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.633 | 0.775 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 166.3 / 138.3 / 143.9 | – | – | – | – | 166.4 / 138.4 / 144.0 | 3.495 |
| ig:llm/llm:sbert | 3.0 / 3.0 / 3.7 | 145.0 / 141.3 / 157.2 | 2.2 / 1.9 / 4.2 | 32.2 / 41.0 / 63.3 | 405.5 / 229.9 / 1028.7 | 0.3 / 0.2 / 0.3 | 445.0 / 277.5 / 1078.0 | 9.005 |
| ig:llm/llm:sbert+rnorm=minmax | 3.5 / 3.4 / 5.2 | 126.0 / 134.8 / 144.9 | 2.5 / 1.8 / 5.2 | 30.8 / 36.3 / 60.7 | 395.6 / 222.7 / 1057.3 | 0.3 / 0.3 / 0.4 | 434.6 / 268.3 / 1101.7 | 8.263 |
| ig:llm/llm:sbert+repair=1 | 5.0 / 4.2 / 7.8 | 135.9 / 138.8 / 148.4 | 2.0 / 1.7 / 4.2 | 103.7 / 32.0 / 517.9 | 387.5 / 206.8 / 961.9 | 0.3 / 0.2 / 0.3 | 499.9 / 271.6 / 1007.0 | 8.179 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 3.8 / 3.6 / 5.1 | 141.0 / 139.8 / 145.7 | 2.1 / 1.7 / 4.1 | 27.8 / 33.0 / 60.1 | 359.3 / 229.8 / 1011.6 | 0.3 / 0.2 / 0.3 | 394.8 / 275.4 / 1051.6 | 7.928 |

Context index build (one-off, ms): sbert: 14805 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.001 | [-0.035, +0.037] | 0.970 | 7/7 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.008 | [-0.025, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.001 | [-0.035, +0.037] | 0.970 | 7/7 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | -0.008 | [-0.025, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.051 | [-0.105, -0.004] | 0.049 | 6/10 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.046 | [-0.129, +0.000] | 0.502 | 0/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.051 | [-0.105, -0.004] | 0.049 | 6/10 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.046 | [-0.129, +0.000] | 0.502 | 0/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
