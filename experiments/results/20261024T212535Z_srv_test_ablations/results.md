# IGBench results (20261024T212535Z_srv_test_ablations)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

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
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.1 | 7.1 / 5.0 / 7.6 | 0.2 / 0.1 / 0.2 | 27.5 / 19.6 / 82.9 | 260.4 / 112.6 / 534.5 | 0.1 / 0.1 / 0.1 | 296.2 / 154.4 / 558.3 | 6.236 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.1 | 17.3 / 4.8 / 88.4 | 0.1 / 0.1 / 0.2 | 15.7 / 17.0 / 18.9 | 271.1 / 116.7 / 552.4 | 0.1 / 0.1 / 0.1 | 305.3 / 193.8 / 657.2 | 6.438 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.1 | 9.1 / 4.3 / 9.1 | 0.1 / 0.1 / 0.2 | 28.0 / 17.9 / 94.3 | 268.3 / 120.9 / 551.9 | 0.1 / 0.1 / 0.1 | 306.6 / 168.7 / 573.0 | 6.463 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.1 | 10.1 / 4.3 / 9.0 | 0.1 / 0.1 / 0.2 | 15.8 / 17.2 / 19.7 | 276.8 / 113.5 / 528.8 | 0.1 / 0.1 / 0.1 | 303.9 / 135.2 / 548.1 | 6.407 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.1 | 5.3 / 5.1 / 8.0 | 0.2 / 0.1 / 0.2 | 28.4 / 16.7 / 101.7 | 280.9 / 117.4 / 555.2 | 0.1 / 0.1 / 0.1 | 315.9 / 195.3 / 671.7 | 6.66 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.1 | 8.5 / 4.9 / 8.0 | 0.2 / 0.1 / 0.2 | 19.6 / 17.0 / 18.6 | 274.3 / 136.6 / 556.8 | 0.1 / 0.1 / 0.1 | 303.7 / 161.5 / 577.9 | 6.404 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.1 | 5.1 / 4.3 / 7.6 | 0.1 / 0.1 / 0.2 | 11.3 / 6.9 / 9.0 | 85.8 / 61.8 / 154.7 | 0.0 / 0.0 / 0.0 | 102.9 / 73.3 / 194.0 | 2.176 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.1 | 8.6 / 4.2 / 8.6 | 0.1 / 0.1 / 0.2 | 251.5 / 220.4 / 494.6 | 495.2 / 219.8 / 1286.5 | 0.2 / 0.2 / 0.2 | 757.3 / 528.6 / 1440.5 | 15.95 |
| ig:gold/gold:bm25+bind=0.7 | 0.1 / 0.1 / 0.1 | 9.3 / 4.2 / 7.7 | 0.1 / 0.1 / 0.2 | 22.7 / 17.7 / 25.2 | 215.1 / 95.7 / 338.5 | 0.1 / 0.1 / 0.1 | 248.3 / 130.5 / 364.6 | 5.247 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.1 | 5.2 / 5.3 / 7.9 | 0.3 / 0.2 / 0.3 | 20.8 / 17.2 / 19.1 | 263.5 / 164.2 / 333.4 | 0.1 / 0.1 / 0.1 | 290.9 / 190.8 / 356.8 | 6.135 |
| ig:rule/gold:bm25 | 0.5 / 0.1 / 0.7 | 4.4 / 4.3 / 7.2 | 0.1 / 0.1 / 0.1 | 8.7 / 0.0 / 17.9 | 91.1 / 0.0 / 139.8 | 0.1 / 0.1 / 0.1 | 105.7 / 5.9 / 241.0 | 2.224 |

Context index build (one-off, ms): bm25: 59 (cached), lsa: 1703 (cached), tfidf: 11 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
