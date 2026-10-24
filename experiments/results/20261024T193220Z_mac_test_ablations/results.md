# IGBench results (20261024T193220Z_mac_test_ablations)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3301 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.12.3 on macOS-15.7.9-x86_64-i386-64bit. Warm caches: False.

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

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.345 | 0.791 | 0.956 |
| ig:gold/gold:bm25+comb=lexicographic | 0.345 | 0.704 | 0.875 |
| ig:gold/gold:bm25+soft=0 | 0.395 | 0.829 | 0.948 |
| ig:gold/gold:bm25+alpha=0.25 | 0.395 | 0.824 | 0.940 |
| ig:gold/gold:bm25+alpha=0.75 | 0.345 | 0.829 | 0.956 |
| ig:gold/gold:bm25+alpha=1.0 | 0.345 | 0.729 | 0.894 |
| ig:gold/gold:bm25+k=20 | 0.395 | 0.829 | 0.948 |
| ig:gold/gold:bm25+k=100 | 0.395 | 0.829 | 0.948 |
| ig:gold/gold:bm25+bind=0.7 | 0.445 | 0.839 | 0.944 |
| ig:gold/index:bm25 | 0.345 | 0.829 | 0.948 |
| ig:rule/gold:bm25 | 0.389 | 0.817 | 0.925 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.763 | 0.826 | 0.733 | 0.900 |
| ig:gold/gold:bm25+comb=lexicographic | 0.690 | 0.799 | 0.693 | 0.793 |
| ig:gold/gold:bm25+soft=0 | 0.803 | 0.833 | 0.849 | 0.908 |
| ig:gold/gold:bm25+alpha=0.25 | 0.801 | 0.825 | 0.876 | 0.917 |
| ig:gold/gold:bm25+alpha=0.75 | 0.771 | 0.826 | 0.723 | 0.906 |
| ig:gold/gold:bm25+alpha=1.0 | 0.754 | 0.826 | 0.634 | 0.829 |
| ig:gold/gold:bm25+k=20 | 0.805 | 0.833 | 0.868 | 0.918 |
| ig:gold/gold:bm25+k=100 | 0.805 | 0.833 | 0.849 | 0.918 |
| ig:gold/gold:bm25+bind=0.7 | 0.845 | 0.840 | 0.860 | 0.911 |
| ig:gold/index:bm25 | 0.805 | 0.833 | 0.849 | 0.868 |
| ig:rule/gold:bm25 | 0.832 | 0.758 | 0.742 | 0.912 |

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
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.1 | 6.2 / 5.9 / 10.2 | 0.2 / 0.1 / 0.2 | 24.0 / 22.5 / 29.7 | 1043.8 / 169.0 / 705.9 | 0.1 / 0.1 / 0.1 | 1075.6 / 193.7 / 733.1 | 22.604 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.1 | 6.2 / 6.0 / 9.6 | 0.2 / 0.1 / 0.2 | 23.4 / 20.8 / 26.2 | 1031.7 / 158.9 / 721.0 | 0.1 / 0.1 / 0.1 | 1062.9 / 187.5 / 746.7 | 22.344 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.1 | 6.4 / 6.1 / 9.7 | 0.2 / 0.1 / 0.2 | 26.5 / 21.4 / 26.9 | 1056.6 / 218.3 / 725.7 | 0.1 / 0.1 / 0.1 | 1091.0 / 262.6 / 751.2 | 22.937 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.1 | 6.2 / 5.6 / 9.7 | 0.2 / 0.1 / 0.2 | 27.7 / 21.6 / 32.6 | 1058.6 / 163.3 / 722.5 | 0.1 / 0.1 / 0.1 | 1094.0 / 194.9 / 748.5 | 22.998 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.1 | 10.4 / 6.4 / 10.1 | 0.2 / 0.1 / 0.2 | 23.3 / 21.0 / 25.2 | 1087.3 / 164.4 / 720.7 | 0.1 / 0.1 / 0.1 | 1122.5 / 202.8 / 749.8 | 23.598 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.1 | 9.9 / 6.5 / 10.1 | 0.2 / 0.1 / 0.2 | 22.7 / 20.3 / 26.6 | 1090.1 / 211.8 / 717.0 | 0.1 / 0.1 / 0.1 | 1124.2 / 259.8 / 743.5 | 23.633 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.1 | 6.3 / 6.0 / 10.0 | 0.2 / 0.1 / 0.2 | 5.7 / 5.3 / 7.9 | 115.1 / 87.0 / 219.4 | 0.0 / 0.0 / 0.0 | 128.1 / 94.6 / 230.8 | 2.703 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.1 | 6.0 / 5.3 / 10.0 | 0.2 / 0.1 / 0.2 | 530.0 / 450.3 / 1040.0 | 1312.3 / 306.7 / 1532.0 | 0.2 / 0.2 / 0.3 | 1850.9 / 796.6 / 2613.1 | 38.912 |
| ig:gold/gold:bm25+bind=0.7 | 0.1 / 0.1 / 0.1 | 6.4 / 6.7 / 9.9 | 0.2 / 0.1 / 0.2 | 23.6 / 21.1 / 24.9 | 1032.6 / 126.1 / 485.8 | 0.1 / 0.1 / 0.1 | 1064.1 / 163.9 / 513.7 | 22.378 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.1 | 6.6 / 5.7 / 10.0 | 0.4 / 0.3 / 0.4 | 13.6 / 14.5 / 18.8 | 1088.9 / 177.2 / 491.3 | 0.1 / 0.1 / 0.1 | 1110.8 / 191.0 / 513.7 | 23.351 |
| ig:rule/gold:bm25 | 0.5 / 0.2 / 0.9 | 5.7 / 5.9 / 9.2 | 0.1 / 0.1 / 0.1 | 8.2 / 0.0 / 16.0 | 101.9 / 0.0 / 182.8 | 0.1 / 0.1 / 0.1 | 117.3 / 7.8 / 204.9 | 2.467 |

Context index build (one-off, ms): bm25: 49 (cached), lsa: 8771, tfidf: 15 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
