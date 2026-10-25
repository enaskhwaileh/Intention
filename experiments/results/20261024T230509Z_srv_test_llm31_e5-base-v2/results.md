# IGBench results (20261024T230509Z_srv_test_llm31_e5-base-v2)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.778 | 0.490 | 0.305 | 0.880 | 0.950 | 0.900 | 0.000 |
| ig:llm/llm:sbert | 0.771 | 0.520 | 0.325 | 0.906 | 0.933 | 0.900 | 0.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.794 | 0.550 | 0.320 | 0.893 | 0.967 | 0.950 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.771 | 0.520 | 0.325 | 0.906 | 0.933 | 0.900 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.794 | 0.550 | 0.320 | 0.893 | 0.967 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.775 | 0.474 | 0.947 | 0.895 |
| ig:llm/llm:sbert | 0.773 | 0.516 | 0.930 | 0.895 |
| ig:llm/llm:sbert+rnorm=minmax | 0.797 | 0.547 | 0.965 | 0.947 |
| ig:llm/llm:sbert+repair=1 | 0.773 | 0.516 | 0.930 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.797 | 0.547 | 0.965 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.390 | 0.778 | 0.880 |
| ig:llm/llm:sbert | 0.390 | 0.761 | 0.906 |
| ig:llm/llm:sbert+rnorm=minmax | 0.395 | 0.830 | 0.893 |
| ig:llm/llm:sbert+repair=1 | 0.390 | 0.761 | 0.906 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.395 | 0.830 | 0.893 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.731 | 0.783 | 0.755 | 0.853 |
| ig:llm/llm:sbert | 0.708 | 0.794 | 0.742 | 0.845 |
| ig:llm/llm:sbert+rnorm=minmax | 0.729 | 0.828 | 0.755 | 0.871 |
| ig:llm/llm:sbert+repair=1 | 0.708 | 0.794 | 0.742 | 0.845 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.729 | 0.828 | 0.755 | 0.871 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.875 |
| ig:llm/llm:sbert | 0.875 |
| ig:llm/llm:sbert+rnorm=minmax | 0.875 |
| ig:llm/llm:sbert+repair=1 | 0.875 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.875 |

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
| ctx:sbert | – | 175.9 / 146.4 / 155.4 | – | – | – | – | 176.1 / 146.5 / 155.5 | 3.698 |
| ig:llm/llm:sbert | 4.5 / 4.6 / 6.6 | 141.3 / 140.5 / 147.2 | 2.5 / 1.7 / 6.1 | 43.2 / 33.3 / 77.4 | 358.5 / 150.9 / 1024.8 | 0.2 / 0.2 / 0.4 | 410.8 / 204.7 / 1077.1 | 8.834 |
| ig:llm/llm:sbert+rnorm=minmax | 3.4 / 3.3 / 4.2 | 140.0 / 137.8 / 147.2 | 2.4 / 1.8 / 5.2 | 29.1 / 34.6 / 57.8 | 432.7 / 231.1 / 1508.5 | 0.3 / 0.2 / 0.4 | 469.7 / 285.5 / 1552.8 | 9.607 |
| ig:llm/llm:sbert+repair=1 | 4.4 / 3.9 / 7.1 | 144.4 / 142.7 / 152.9 | 2.0 / 1.5 / 4.2 | 125.3 / 34.8 / 717.0 | 418.3 / 162.3 / 1377.3 | 0.2 / 0.2 / 0.3 | 551.7 / 329.8 / 1407.4 | 8.324 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 5.3 / 4.6 / 8.0 | 98.2 / 97.3 / 107.2 | 1.8 / 1.1 / 5.5 | 16.6 / 20.0 / 33.8 | 194.6 / 114.6 / 407.4 | 0.2 / 0.1 / 0.2 | 219.4 / 142.1 / 448.9 | 5.293 |

Context index build (one-off, ms): sbert: 17414 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.004 | [-0.035, +0.045] | 0.852 | 8/8 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.017 | [-0.025, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.050 | [+0.000, +0.150] | 1.000 | 1/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.004 | [-0.035, +0.045] | 0.852 | 8/8 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.017 | [-0.025, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.050 | [+0.000, +0.150] | 1.000 | 1/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.017 | [-0.057, +0.019] | 0.395 | 9/8 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.017 | [-0.050, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.017 | [-0.057, +0.019] | 0.395 | 9/8 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.017 | [-0.050, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
