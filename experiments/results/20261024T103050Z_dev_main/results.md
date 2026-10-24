# IGBench results (20261024T103050Z_dev_main)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.13.17 on Linux-6.18.44-fc-v153-x86_64-with-glibc2.39. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ctx:lsa | 0.743 | 0.486 | 0.320 | 0.851 | 0.849 | 0.743 | 0.143 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:rule/index:bm25 | 0.788 | 0.531 | 0.331 | 0.875 | 0.909 | 0.829 | 0.114 |
| ig:gold/gold:tfidf | 0.801 | 0.520 | 0.337 | 0.875 | 0.876 | 0.771 | 0.171 |
| ig:rule/index:tfidf | 0.762 | 0.520 | 0.323 | 0.842 | 0.841 | 0.714 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ctx:lsa | 0.744 | 0.463 | 0.850 | 0.750 |
| ig:gold/gold:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:rule/index:bm25 | 0.801 | 0.519 | 0.932 | 0.875 |
| ig:gold/gold:tfidf | 0.816 | 0.519 | 0.896 | 0.812 |
| ig:rule/index:tfidf | 0.774 | 0.519 | 0.857 | 0.750 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ctx:tfidf | 0.799 |
| ctx:lsa | 0.822 |
| ig:gold/gold:bm25 | 0.860 |
| ig:rule/index:bm25 | 0.843 |
| ig:gold/gold:tfidf | 0.819 |
| ig:rule/index:tfidf | 0.825 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/index:bm25 | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |
| ig:gold/gold:tfidf | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.538 | 0.803 |
| ig:rule/index:tfidf | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.497 | 0.802 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 7.4 / 4.9 / 6.5 | – | – | – | – | 7.5 / 5.1 / 6.6 | 0.27 |
| ctx:tfidf | – | 5.3 / 5.2 / 5.9 | – | – | – | – | 5.5 / 5.4 / 6.1 | 0.198 |
| ctx:lsa | – | 31.2 / 27.3 / 40.7 | – | – | – | – | 31.5 / 27.5 / 41.0 | 1.135 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.2 | 6.2 / 6.2 / 11.8 | 0.2 / 0.2 / 0.3 | 1080.6 / 412.8 / 3665.5 | 983.1 / 453.6 / 3702.9 | 0.1 / 0.1 / 0.2 | 2071.9 / 1405.5 / 5394.2 | 74.636 |
| ig:rule/index:bm25 | 0.3 / 0.2 / 0.8 | 9.7 / 5.7 / 11.3 | 0.3 / 0.3 / 0.6 | 127.0 / 11.5 / 588.8 | 946.5 / 145.6 / 4285.5 | 0.1 / 0.1 / 0.2 | 1085.5 / 433.3 / 4430.4 | 39.119 |
| ig:gold/gold:tfidf | 0.1 / 0.1 / 0.1 | 7.5 / 7.6 / 11.6 | 0.2 / 0.2 / 0.3 | 65.8 / 27.8 / 233.3 | 946.6 / 285.9 / 3910.0 | 0.2 / 0.1 / 0.2 | 1021.8 / 333.5 / 4023.0 | 36.836 |
| ig:rule/index:tfidf | 0.2 / 0.2 / 0.3 | 6.4 / 6.3 / 10.6 | 0.3 / 0.3 / 0.5 | 18.1 / 8.1 / 57.9 | 809.3 / 157.2 / 3798.8 | 0.1 / 0.1 / 0.2 | 835.5 / 205.9 / 3824.9 | 30.12 |

Context index build (one-off, ms): bm25: 47 (cached), lsa: 1074 (cached), tfidf: 9 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:tfidf | ctx:tfidf | ndcg@10 | +0.032 | [+0.011, +0.054] | 0.005 | 19/5 |
| ig:rule/index:tfidf | ctx:tfidf | mrr | +0.045 | [+0.002, +0.098] | 0.094 | 5/1 |
| ig:rule/index:tfidf | ctx:tfidf | useful@1 | +0.057 | [+0.000, +0.143] | 0.505 | 2/0 |
| ig:gold/gold:tfidf | ctx:tfidf | ndcg@10 | +0.069 | [+0.035, +0.106] | 0.000 | 23/5 |
| ig:gold/gold:tfidf | ctx:tfidf | mrr | +0.081 | [-0.005, +0.167] | 0.088 | 7/1 |
| ig:gold/gold:tfidf | ctx:tfidf | useful@1 | +0.114 | [-0.029, +0.257] | 0.223 | 5/1 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.019 | [-0.000, +0.041] | 0.069 | 16/8 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.014 | [-0.009, +0.052] | 0.751 | 2/1 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
