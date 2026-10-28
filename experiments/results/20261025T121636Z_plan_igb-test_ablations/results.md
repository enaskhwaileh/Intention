# IGBench results (20261025T121636Z_plan_igb-test_ablations)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
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
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
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
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ig:gold/gold:bm25 | 0.395 | 0.829 | 0.948 |
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
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ig:gold/gold:bm25 | 0.805 | 0.833 | 0.849 | 0.918 |
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
| ctx:bm25 | 0.871 |
| ig:gold/gold:bm25 | 0.882 |
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
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
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
| ctx:bm25 | – | 5.5 / 5.3 / 6.5 | – | – | – | – | 5.6 / 5.5 / 6.7 | 0.118 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.2 | 3.5 / 3.1 / 5.9 | 0.8 / 0.2 / 3.0 | 29.4 / 29.3 / 49.8 | 363.2 / 243.6 / 735.9 | 0.1 / 0.1 / 0.1 | 394.6 / 274.7 / 772.8 | 2.638 |
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.1 | 4.0 / 3.2 / 6.0 | 0.8 / 0.2 / 3.1 | 37.1 / 21.7 / 87.0 | 346.2 / 249.9 / 675.1 | 0.1 / 0.1 / 0.1 | 385.3 / 269.0 / 761.6 | 2.59 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.1 | 5.3 / 3.2 / 6.2 | 0.8 / 0.2 / 3.1 | 20.0 / 19.1 / 29.4 | 342.0 / 234.5 / 676.6 | 0.1 / 0.1 / 0.1 | 364.0 / 253.0 / 705.8 | 2.559 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.1 | 5.4 / 3.5 / 6.3 | 0.8 / 0.2 / 3.0 | 21.1 / 18.8 / 31.4 | 339.7 / 233.5 / 664.5 | 0.1 / 0.1 / 0.1 | 362.9 / 252.9 / 696.0 | 2.519 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.1 | 5.4 / 3.1 / 6.5 | 0.8 / 0.2 / 3.2 | 25.1 / 21.5 / 30.0 | 345.0 / 237.2 / 660.1 | 0.1 / 0.1 / 0.1 | 372.2 / 276.4 / 689.6 | 2.668 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.1 | 4.1 / 3.1 / 6.0 | 0.8 / 0.2 / 3.1 | 33.8 / 25.9 / 74.5 | 343.5 / 239.0 / 661.8 | 0.1 / 0.1 / 0.1 | 379.4 / 283.0 / 691.8 | 2.596 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.1 | 4.1 / 3.2 / 6.1 | 0.8 / 0.2 / 3.0 | 30.2 / 26.2 / 69.0 | 346.0 / 239.1 / 663.4 | 0.1 / 0.1 / 0.1 | 378.2 / 261.9 / 695.6 | 2.558 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.1 | 4.0 / 3.2 / 6.0 | 0.8 / 0.2 / 3.0 | 13.1 / 9.1 / 17.5 | 243.6 / 77.9 / 634.2 | 0.0 / 0.0 / 0.0 | 258.2 / 98.9 / 653.3 | 1.639 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.1 | 4.0 / 3.2 / 6.1 | 0.8 / 0.2 / 3.2 | 50.2 / 48.2 / 84.7 | 570.9 / 462.9 / 1219.3 | 0.2 / 0.2 / 0.2 | 624.0 / 504.6 / 1287.1 | 5.853 |
| ig:gold/gold:bm25+bind=0.7 | 0.1 / 0.1 / 0.1 | 5.8 / 3.2 / 6.1 | 0.8 / 0.2 / 3.1 | 19.3 / 18.7 / 28.6 | 282.9 / 123.5 / 646.3 | 0.1 / 0.1 / 0.1 | 304.1 / 142.7 / 676.6 | 2.025 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.1 | 5.3 / 3.2 / 6.3 | 2.1 / 0.4 / 6.8 | 26.9 / 20.3 / 43.1 | 333.1 / 240.2 / 662.3 | 0.1 / 0.1 / 0.1 | 363.4 / 299.1 / 694.6 | 2.664 |
| ig:rule/gold:bm25 | 0.9 / 0.4 / 1.4 | 4.1 / 3.8 / 5.5 | 0.5 / 0.2 / 1.1 | 7.1 / 0.0 / 27.5 | 161.8 / 0.0 / 519.7 | 0.5 / 0.4 / 1.2 | 171.2 / 2.7 / 554.3 | 1.859 |

Context index build (one-off, ms): bm25: 55 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+alpha=1.0 | ctx:bm25 | ndcg@10 | -0.061 | [-0.167, +0.029] | 0.298 | 8/10 |
| ig:gold/gold:bm25+alpha=1.0 | ctx:bm25 | mrr | -0.009 | [-0.180, +0.150] | 1.000 | 3/2 |
| ig:gold/gold:bm25+alpha=1.0 | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
| ig:gold/gold:bm25+comb=linear | ctx:bm25 | ndcg@10 | -0.021 | [-0.099, +0.050] | 0.629 | 9/8 |
| ig:gold/gold:bm25+comb=linear | ctx:bm25 | mrr | +0.006 | [-0.144, +0.150] | 1.000 | 3/2 |
| ig:gold/gold:bm25+comb=linear | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
| ig:gold/gold:bm25+k=100 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25+k=100 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25+k=100 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/index:bm25 | ctx:bm25 | ndcg@10 | +0.018 | [-0.032, +0.064] | 0.492 | 11/6 |
| ig:gold/index:bm25 | ctx:bm25 | mrr | +0.033 | [-0.075, +0.158] | 0.748 | 3/2 |
| ig:gold/index:bm25 | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
| ig:gold/gold:bm25+k=20 | ctx:bm25 | ndcg@10 | +0.032 | [-0.013, +0.072] | 0.186 | 12/4 |
| ig:gold/gold:bm25+k=20 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25+k=20 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:bm25+comb=lexicographic | ctx:bm25 | ndcg@10 | -0.082 | [-0.183, +0.007] | 0.133 | 7/11 |
| ig:gold/gold:bm25+comb=lexicographic | ctx:bm25 | mrr | -0.005 | [-0.172, +0.150] | 1.000 | 3/2 |
| ig:gold/gold:bm25+comb=lexicographic | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
| ig:gold/gold:bm25+alpha=0.75 | ctx:bm25 | ndcg@10 | -0.019 | [-0.093, +0.051] | 0.640 | 9/8 |
| ig:gold/gold:bm25+alpha=0.75 | ctx:bm25 | mrr | +0.010 | [-0.137, +0.150] | 1.000 | 3/2 |
| ig:gold/gold:bm25+alpha=0.75 | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
| ig:gold/gold:bm25+soft=0 | ctx:bm25 | ndcg@10 | +0.025 | [-0.019, +0.066] | 0.294 | 11/5 |
| ig:gold/gold:bm25+soft=0 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25+soft=0 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:bm25+alpha=0.25 | ctx:bm25 | ndcg@10 | +0.031 | [-0.013, +0.072] | 0.197 | 11/4 |
| ig:gold/gold:bm25+alpha=0.25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25+alpha=0.25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:bm25+bind=0.7 | ctx:bm25 | ndcg@10 | +0.045 | [+0.017, +0.076] | 0.004 | 12/2 |
| ig:gold/gold:bm25+bind=0.7 | ctx:bm25 | mrr | +0.083 | [+0.000, +0.183] | 0.248 | 3/0 |
| ig:gold/gold:bm25+bind=0.7 | ctx:bm25 | useful@1 | +0.150 | [+0.000, +0.350] | 0.248 | 3/0 |
| ig:rule/gold:bm25 | ctx:bm25 | ndcg@10 | +0.000 | [-0.021, +0.017] | 0.979 | 6/4 |
| ig:rule/gold:bm25 | ctx:bm25 | mrr | -0.025 | [-0.125, +0.050] | 1.000 | 1/2 |
| ig:rule/gold:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.250, +0.100] | 1.000 | 1/2 |
