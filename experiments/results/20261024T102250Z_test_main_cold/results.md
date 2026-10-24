# IGBench results (20261024T102250Z_test_main_cold)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.13.17 on Linux-6.18.44-fc-v153-x86_64-with-glibc2.39. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ctx:lsa | 0.806 | 0.540 | 0.345 | 0.896 | 0.829 | 0.700 | 0.150 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.355 | 0.948 | 0.900 | 0.800 | 0.050 |
| ig:gold/gold:tfidf | 0.834 | 0.510 | 0.345 | 0.935 | 0.917 | 0.850 | 0.000 |
| ig:rule/index:tfidf | 0.823 | 0.500 | 0.340 | 0.927 | 0.917 | 0.850 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ctx:lsa | 0.799 | 0.526 | 0.820 | 0.684 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:bm25 | 0.821 | 0.526 | 0.895 | 0.789 |
| ig:gold/gold:tfidf | 0.833 | 0.495 | 0.912 | 0.842 |
| ig:rule/index:tfidf | 0.821 | 0.484 | 0.912 | 0.842 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ctx:tfidf | 0.862 |
| ctx:lsa | 0.863 |
| ig:gold/gold:bm25 | 0.882 |
| ig:rule/index:bm25 | 0.882 |
| ig:gold/gold:tfidf | 0.882 |
| ig:rule/index:tfidf | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:rule/index:bm25 | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:gold/gold:tfidf | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.589 | 0.747 |
| ig:rule/index:tfidf | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.562 | 0.634 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 10.0 / 5.2 / 8.1 | – | – | – | – | 10.2 / 5.4 / 8.3 | 0.214 |
| ctx:tfidf | – | 5.0 / 4.7 / 5.6 | – | – | – | – | 5.1 / 4.8 / 5.7 | 0.108 |
| ctx:lsa | – | 31.4 / 28.6 / 39.0 | – | – | – | – | 31.7 / 28.9 / 39.3 | 0.667 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.2 | 6.8 / 7.1 / 11.0 | 0.3 / 0.2 / 0.3 | 2005.4 / 1468.5 / 3647.4 | 1083.3 / 132.2 / 535.6 | 0.1 / 0.1 / 0.2 | 3097.6 / 1822.3 / 4446.4 | 65.081 |
| ig:rule/index:bm25 | 0.4 / 0.2 / 0.9 | 6.0 / 5.5 / 10.1 | 0.4 / 0.3 / 0.5 | 96.9 / 34.1 / 246.7 | 1087.4 / 169.2 / 464.9 | 0.1 / 0.1 / 0.2 | 1192.7 / 220.3 / 566.7 | 25.079 |
| ig:gold/gold:tfidf | 0.1 / 0.1 / 0.2 | 8.0 / 7.5 / 12.1 | 0.2 / 0.3 / 0.3 | 310.8 / 68.2 / 276.0 | 217.2 / 115.5 / 581.9 | 0.1 / 0.1 / 0.2 | 537.8 / 263.4 / 829.0 | 11.33 |
| ig:rule/index:tfidf | 0.2 / 0.2 / 0.3 | 6.6 / 6.8 / 10.0 | 0.3 / 0.3 / 0.4 | 13.2 / 9.3 / 21.3 | 207.9 / 108.6 / 357.1 | 0.1 / 0.1 / 0.2 | 229.7 / 158.2 / 372.6 | 4.854 |

Context index build (one-off, ms): bm25: 45 (cached), lsa: 1296 (cached), tfidf: 11 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:tfidf | ctx:tfidf | ndcg@10 | +0.046 | [-0.003, +0.090] | 0.086 | 12/4 |
| ig:rule/index:tfidf | ctx:tfidf | mrr | +0.152 | [+0.035, +0.275] | 0.038 | 8/1 |
| ig:rule/index:tfidf | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
| ig:gold/gold:tfidf | ctx:tfidf | ndcg@10 | +0.057 | [+0.006, +0.103] | 0.046 | 12/4 |
| ig:gold/gold:tfidf | ctx:tfidf | mrr | +0.152 | [+0.035, +0.275] | 0.038 | 8/1 |
| ig:gold/gold:tfidf | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.922 | 9/6 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
