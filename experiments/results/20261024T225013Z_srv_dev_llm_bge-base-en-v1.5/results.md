# IGBench results (20261024T225013Z_srv_dev_llm_bge-base-en-v1.5)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.806 | 0.531 | 0.337 | 0.886 | 0.858 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.804 | 0.537 | 0.337 | 0.886 | 0.863 | 0.743 | 0.143 |
| ig:llm/llm:sbert+rnorm=minmax | 0.807 | 0.537 | 0.329 | 0.878 | 0.863 | 0.743 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.525 | 0.845 | 0.719 |
| ig:llm/llm:sbert | 0.806 | 0.531 | 0.850 | 0.719 |
| ig:llm/llm:sbert+rnorm=minmax | 0.810 | 0.531 | 0.850 | 0.719 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.294 | 0.777 | 0.886 |
| ig:llm/llm:sbert | 0.306 | 0.786 | 0.886 |
| ig:llm/llm:sbert+rnorm=minmax | 0.306 | 0.786 | 0.878 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.986 | 0.825 | 0.831 | 0.716 | 0.771 |
| ig:llm/llm:sbert | 0.986 | 0.811 | 0.838 | 0.716 | 0.766 |
| ig:llm/llm:sbert+rnorm=minmax | 0.986 | 0.811 | 0.854 | 0.716 | 0.767 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.842 |
| ig:llm/llm:sbert | 0.840 |
| ig:llm/llm:sbert+rnorm=minmax | 0.839 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.455 | 1.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.455 | 1.000 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 155.8 / 138.8 / 148.4 | – | – | – | – | 155.9 / 138.9 / 148.5 | 5.614 |
| ig:llm/llm:sbert | 5.6 / 5.2 / 9.4 | 135.9 / 134.7 / 144.8 | 0.6 / 0.0 / 2.5 | 4.7 / 0.0 / 39.8 | 157.9 / 0.0 / 967.4 | 0.3 / 0.3 / 0.5 | 169.6 / 6.9 / 1010.6 | 8.968 |
| ig:llm/llm:sbert+rnorm=minmax | 5.1 / 4.9 / 9.1 | 137.0 / 136.0 / 144.5 | 0.8 / 0.1 / 3.0 | 4.7 / 0.0 / 42.8 | 148.9 / 0.0 / 1040.5 | 0.4 / 0.3 / 0.6 | 160.2 / 5.8 / 1096.3 | 8.728 |

Context index build (one-off, ms): sbert: 15665 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.000 | [-0.017, +0.016] | 0.979 | 5/5 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.005 | [-0.038, +0.048] | 1.000 | 2/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.004 | [-0.011, +0.004] | 0.353 | 3/7 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.005 | [-0.038, +0.048] | 1.000 | 2/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
