# IGBench results (20261025T180424Z_plan_igb-dev_hybrid_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:llm/llm:hybrid | 0.805 | 0.531 | 0.337 | 0.888 | 0.850 | 0.743 | 0.171 |
| ig:llm/llm:hybrid+repair=1 | 0.815 | 0.537 | 0.340 | 0.891 | 0.869 | 0.771 | 0.143 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.824 | 0.543 | 0.334 | 0.886 | 0.890 | 0.800 | 0.114 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.809 | 0.543 | 0.331 | 0.881 | 0.852 | 0.743 | 0.171 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |
| ig:llm/llm:hybrid | 0.811 | 0.512 | 0.867 | 0.781 |
| ig:llm/llm:hybrid+repair=1 | 0.823 | 0.519 | 0.888 | 0.812 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.833 | 0.525 | 0.911 | 0.844 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.816 | 0.525 | 0.870 | 0.781 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:llm/llm:hybrid | 0.308 | 0.779 | 0.888 |
| ig:llm/llm:hybrid+repair=1 | 0.311 | 0.784 | 0.891 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.316 | 0.789 | 0.886 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.298 | 0.787 | 0.881 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |
| ig:llm/llm:hybrid | 0.984 | 0.874 | 0.832 | 0.718 | 0.721 |
| ig:llm/llm:hybrid+repair=1 | 0.984 | 0.880 | 0.856 | 0.746 | 0.721 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.984 | 0.860 | 0.854 | 0.735 | 0.793 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.984 | 0.856 | 0.818 | 0.720 | 0.773 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:hybrid | 0.808 |
| ig:llm/llm:hybrid | 0.809 |
| ig:llm/llm:hybrid+repair=1 | 0.821 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.818 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.808 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.520 | 0.693 |
| ig:llm/llm:hybrid+repair=1 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.568 | 0.740 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.568 | 0.740 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.944 | 0.774 | 0.935 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:hybrid | – | 89.3 / 77.1 / 89.0 | – | – | – | – | 89.4 / 77.2 / 89.2 | 3.22 |
| ig:llm/llm:hybrid | 5.0 / 4.7 / 9.0 | 76.9 / 76.2 / 83.7 | 1.6 / 1.1 / 4.0 | 13.1 / 0.0 / 31.6 | 924.4 / 0.0 / 3966.2 | 0.3 / 0.1 / 0.9 | 945.1 / 10.0 / 4002.3 | 19.602 |
| ig:llm/llm:hybrid+repair=1 | 7.9 / 7.4 / 17.3 | 78.6 / 76.6 / 90.7 | 2.1 / 1.3 / 5.6 | 48.3 / 21.6 / 397.4 | 1147.6 / 112.7 / 4154.4 | 0.2 / 0.1 / 0.9 | 1207.0 / 278.5 / 4188.1 | 22.306 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 6.6 / 6.3 / 9.6 | 78.1 / 76.2 / 87.2 | 1.9 / 1.4 / 5.7 | 15.8 / 19.9 / 31.6 | 1101.4 / 109.8 / 3956.8 | 0.2 / 0.1 / 0.6 | 1126.8 / 154.5 / 3988.8 | 21.899 |
| ig:llm/llm:hybrid+repair=1+align=0 | 7.6 / 6.1 / 16.4 | 77.5 / 75.2 / 86.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.6 / 0.5 / 1.1 | 8.2 / 6.8 / 16.9 | 3.257 |

Context index build (one-off, ms): hybrid: 10251 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | ndcg@10 | -0.005 | [-0.012, +0.002] | 0.203 | 6/10 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | mrr | -0.024 | [-0.062, +0.000] | 0.247 | 0/3 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | +0.002 | [-0.025, +0.024] | 0.919 | 14/9 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.007 | [-0.069, +0.050] | 0.748 | 1/2 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.009 | [-0.032, +0.009] | 0.525 | 10/6 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.026 | [-0.074, +0.000] | 0.504 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.010 | [-0.001, +0.023] | 0.107 | 11/11 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | +0.014 | [-0.014, +0.057] | 1.000 | 1/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
