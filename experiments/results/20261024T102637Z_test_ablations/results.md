# IGBench results (20261024T102637Z_test_ablations)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.13.17 on Linux-6.18.44-fc-v153-x86_64-with-glibc2.39. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.806 | 0.550 | 0.355 | 0.956 | 0.923 | 0.900 | 0.000 |
| ig:gold/gold:bm25+comb=lexicographic | 0.742 | 0.510 | 0.325 | 0.875 | 0.912 | 0.900 | 0.000 |
| ig:gold/gold:bm25+soft=0 | 0.854 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:gold/gold:bm25+alpha=0.25 | 0.861 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:gold/gold:bm25+alpha=0.75 | 0.808 | 0.550 | 0.355 | 0.956 | 0.927 | 0.900 | 0.000 |
| ig:gold/gold:bm25+alpha=1.0 | 0.764 | 0.530 | 0.340 | 0.894 | 0.907 | 0.900 | 0.000 |
| ig:gold/gold:bm25+k=20 | 0.862 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:gold/gold:bm25+k=100 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:gold/gold:bm25+bind=0.7 | 0.875 | 0.560 | 0.350 | 0.944 | 1.000 | 1.000 | 0.000 |
| ig:gold/index:bm25 | 0.847 | 0.550 | 0.355 | 0.948 | 0.950 | 0.900 | 0.050 |
| ig:rule/gold:bm25 | 0.829 | 0.540 | 0.340 | 0.925 | 0.892 | 0.800 | 0.100 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.800 | 0.537 | 0.919 | 0.895 |
| ig:gold/gold:bm25+comb=lexicographic | 0.733 | 0.495 | 0.907 | 0.895 |
| ig:gold/gold:bm25+soft=0 | 0.851 | 0.537 | 0.974 | 0.947 |
| ig:gold/gold:bm25+alpha=0.25 | 0.858 | 0.537 | 0.974 | 0.947 |
| ig:gold/gold:bm25+alpha=0.75 | 0.802 | 0.537 | 0.923 | 0.895 |
| ig:gold/gold:bm25+alpha=1.0 | 0.756 | 0.516 | 0.903 | 0.895 |
| ig:gold/gold:bm25+k=20 | 0.858 | 0.537 | 0.974 | 0.947 |
| ig:gold/gold:bm25+k=100 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:gold/gold:bm25+bind=0.7 | 0.873 | 0.547 | 1.000 | 1.000 |
| ig:gold/index:bm25 | 0.843 | 0.537 | 0.947 | 0.895 |
| ig:rule/gold:bm25 | 0.824 | 0.526 | 0.886 | 0.789 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:bm25+comb=linear | 0.882 |
| ig:gold/gold:bm25+comb=lexicographic | 0.849 |
| ig:gold/gold:bm25+soft=0 | 0.882 |
| ig:gold/gold:bm25+alpha=0.25 | 0.882 |
| ig:gold/gold:bm25+alpha=0.75 | 0.882 |
| ig:gold/gold:bm25+alpha=1.0 | 0.882 |
| ig:gold/gold:bm25+k=20 | 0.882 |
| ig:gold/gold:bm25+k=100 | 0.882 |
| ig:gold/gold:bm25+bind=0.7 | 0.921 |
| ig:gold/index:bm25 | 0.882 |
| ig:rule/gold:bm25 | 0.850 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+comb=lexicographic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+soft=0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+alpha=0.25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+alpha=0.75 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+alpha=1.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+k=20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.631 | 0.768 |
| ig:gold/gold:bm25+k=100 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.552 | 0.747 |
| ig:gold/gold:bm25+bind=0.7 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.717 | 0.606 |
| ig:gold/index:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.947 | 1.000 | 0.000 | 0.571 | 0.732 |
| ig:rule/gold:bm25 | 1.000 | 0.815 | 0.950 | 0.381 | 0.316 | 0.316 | 0.263 | 0.684 | 0.478 | 0.550 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.1 | 14.4 / 5.7 / 12.2 | 0.2 / 0.2 / 0.3 | 8.2 / 8.5 / 11.2 | 1018.8 / 154.3 / 548.0 | 0.1 / 0.1 / 0.2 | 1043.0 / 168.0 / 560.9 | 21.924 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.1 | 5.3 / 5.7 / 7.6 | 0.2 / 0.2 / 0.3 | 9.2 / 9.1 / 13.8 | 982.0 / 150.1 / 586.9 | 0.1 / 0.1 / 0.2 | 998.1 / 170.2 / 600.3 | 20.991 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.1 | 4.8 / 4.7 / 7.2 | 0.2 / 0.1 / 0.2 | 8.3 / 8.4 / 11.6 | 971.8 / 131.6 / 539.8 | 0.1 / 0.1 / 0.2 | 986.1 / 149.8 / 552.5 | 20.736 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.1 | 11.7 / 5.4 / 10.8 | 0.2 / 0.2 / 0.3 | 10.6 / 9.9 / 16.1 | 948.9 / 118.3 / 615.2 | 0.1 / 0.1 / 0.1 | 972.7 / 142.9 / 627.2 | 20.468 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.1 | 5.9 / 5.7 / 10.8 | 0.2 / 0.2 / 0.3 | 9.6 / 10.0 / 14.9 | 1090.6 / 125.5 / 566.7 | 0.1 / 0.1 / 0.2 | 1107.7 / 137.8 / 579.2 | 23.295 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.1 | 6.3 / 6.6 / 9.8 | 0.2 / 0.2 / 0.4 | 22.6 / 10.2 / 13.6 | 1065.3 / 141.4 / 712.0 | 0.1 / 0.1 / 0.2 | 1095.9 / 226.1 / 734.0 | 23.052 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.1 | 6.6 / 6.5 / 10.9 | 0.2 / 0.2 / 0.3 | 4.9 / 4.7 / 7.7 | 98.5 / 68.3 / 193.6 | 0.1 / 0.1 / 0.1 | 111.1 / 79.4 / 204.7 | 2.356 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.1 | 6.5 / 6.4 / 9.8 | 0.2 / 0.2 / 0.3 | 2105.4 / 1472.9 / 4651.1 | 1221.8 / 288.6 / 947.1 | 0.3 / 0.2 / 0.4 | 3336.6 / 1997.9 / 6592.2 | 70.129 |
| ig:gold/gold:bm25+bind=0.7 | 0.1 / 0.1 / 0.1 | 16.9 / 7.8 / 15.8 | 0.3 / 0.2 / 0.4 | 18.0 / 12.1 / 19.3 | 981.7 / 88.1 / 497.0 | 0.1 / 0.1 / 0.2 | 1018.5 / 120.7 / 524.5 | 21.435 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.2 | 5.8 / 5.6 / 8.6 | 0.4 / 0.4 / 0.6 | 18.1 / 11.2 / 17.2 | 1077.3 / 169.1 / 606.4 | 0.1 / 0.1 / 0.2 | 1103.1 / 185.2 / 638.0 | 23.203 |
| ig:rule/gold:bm25 | 0.6 / 0.2 / 1.2 | 7.5 / 7.6 / 13.1 | 0.2 / 0.2 / 0.2 | 3.4 / 0.0 / 13.1 | 98.3 / 0.0 / 206.7 | 0.1 / 0.1 / 0.2 | 111.2 / 10.4 / 229.1 | 2.343 |

Context index build (one-off, ms): bm25: 45 (cached), lsa: 1215 (cached), tfidf: 9 (cached)
