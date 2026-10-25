# IGBench results (20261024T224933Z_srv_dev_llm_e5-base-v2)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.820 | 0.543 | 0.337 | 0.894 | 0.929 | 0.886 | 0.057 |
| ig:llm/llm:sbert | 0.816 | 0.554 | 0.337 | 0.894 | 0.929 | 0.886 | 0.057 |
| ig:llm/llm:sbert+rnorm=minmax | 0.824 | 0.543 | 0.334 | 0.892 | 0.929 | 0.886 | 0.057 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.826 | 0.519 | 0.943 | 0.906 |
| ig:llm/llm:sbert | 0.822 | 0.531 | 0.943 | 0.906 |
| ig:llm/llm:sbert+rnorm=minmax | 0.831 | 0.519 | 0.943 | 0.906 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.361 | 0.780 | 0.894 |
| ig:llm/llm:sbert | 0.361 | 0.791 | 0.894 |
| ig:llm/llm:sbert+rnorm=minmax | 0.361 | 0.786 | 0.892 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.948 | 0.829 | 0.835 | 0.773 | 0.798 |
| ig:llm/llm:sbert | 0.947 | 0.826 | 0.807 | 0.773 | 0.801 |
| ig:llm/llm:sbert+rnorm=minmax | 0.947 | 0.826 | 0.835 | 0.773 | 0.815 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.834 |
| ig:llm/llm:sbert | 0.830 |
| ig:llm/llm:sbert+rnorm=minmax | 0.829 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.476 | 1.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.476 | 1.000 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 114.5 / 93.1 / 131.6 | – | – | – | – | 114.6 / 93.2 / 131.7 | 4.125 |
| ig:llm/llm:sbert | 7.0 / 6.8 / 11.4 | 85.3 / 84.0 / 93.2 | 0.8 / 0.0 / 3.5 | 4.6 / 0.0 / 30.6 | 148.5 / 0.0 / 1437.1 | 0.4 / 0.3 / 0.6 | 161.5 / 8.1 / 1479.5 | 7.135 |
| ig:llm/llm:sbert+rnorm=minmax | 5.2 / 5.2 / 8.5 | 139.1 / 138.7 / 146.0 | 0.9 / 0.0 / 3.3 | 5.4 / 0.0 / 46.9 | 159.5 / 0.0 / 1491.5 | 0.4 / 0.3 / 0.6 | 171.8 / 6.8 / 1547.6 | 9.385 |

Context index build (one-off, ms): sbert: 12646 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.003 | [-0.011, +0.017] | 0.732 | 5/4 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.006 | [-0.022, +0.010] | 0.504 | 3/7 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
