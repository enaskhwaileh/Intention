# IGBench results (20261024T230200Z_srv_test_llm31)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:bm25 | 0.807 | 0.530 | 0.345 | 0.927 | 0.867 | 0.750 | 0.100 |
| ig:llm/llm:bm25+rnorm=minmax | 0.810 | 0.510 | 0.345 | 0.927 | 0.867 | 0.750 | 0.100 |
| ig:llm/llm:bm25+repair=1 | 0.807 | 0.530 | 0.345 | 0.927 | 0.867 | 0.750 | 0.100 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.810 | 0.510 | 0.345 | 0.927 | 0.867 | 0.750 | 0.100 |
| ig:llm/llm:tfidf | 0.783 | 0.470 | 0.315 | 0.880 | 0.833 | 0.700 | 0.150 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.784 | 0.470 | 0.315 | 0.880 | 0.833 | 0.700 | 0.150 |
| ig:llm/llm:tfidf+repair=1 | 0.783 | 0.470 | 0.315 | 0.880 | 0.833 | 0.700 | 0.150 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.784 | 0.470 | 0.315 | 0.880 | 0.833 | 0.700 | 0.150 |
| ig:llm/llm:sbert | 0.744 | 0.460 | 0.300 | 0.846 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:sbert+rnorm=minmax | 0.737 | 0.430 | 0.285 | 0.821 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:sbert+repair=1 | 0.744 | 0.460 | 0.300 | 0.846 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.737 | 0.430 | 0.285 | 0.821 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:hybrid | 0.819 | 0.540 | 0.335 | 0.913 | 0.900 | 0.800 | 0.100 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.845 | 0.530 | 0.340 | 0.917 | 0.925 | 0.850 | 0.100 |
| ig:llm/llm:hybrid+repair=1 | 0.819 | 0.540 | 0.335 | 0.913 | 0.900 | 0.800 | 0.100 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.845 | 0.530 | 0.340 | 0.917 | 0.925 | 0.850 | 0.100 |
| ig:gold/llm:bm25 | 0.850 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:llm/index:bm25 | 0.802 | 0.540 | 0.350 | 0.936 | 0.842 | 0.700 | 0.150 |
| ig:gold/llm:bm25+repair=1 | 0.850 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:llm/index:bm25+repair=1 | 0.802 | 0.540 | 0.350 | 0.936 | 0.842 | 0.700 | 0.150 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:bm25 | 0.814 | 0.526 | 0.886 | 0.789 |
| ig:llm/llm:bm25+rnorm=minmax | 0.817 | 0.505 | 0.886 | 0.789 |
| ig:llm/llm:bm25+repair=1 | 0.814 | 0.526 | 0.886 | 0.789 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.817 | 0.505 | 0.886 | 0.789 |
| ig:llm/llm:tfidf | 0.792 | 0.463 | 0.851 | 0.737 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.793 | 0.463 | 0.851 | 0.737 |
| ig:llm/llm:tfidf+repair=1 | 0.792 | 0.463 | 0.851 | 0.737 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.793 | 0.463 | 0.851 | 0.737 |
| ig:llm/llm:sbert | 0.758 | 0.463 | 0.932 | 0.895 |
| ig:llm/llm:sbert+rnorm=minmax | 0.750 | 0.432 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1 | 0.758 | 0.463 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.750 | 0.432 | 0.932 | 0.895 |
| ig:llm/llm:hybrid | 0.826 | 0.537 | 0.921 | 0.842 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.853 | 0.526 | 0.947 | 0.895 |
| ig:llm/llm:hybrid+repair=1 | 0.826 | 0.537 | 0.921 | 0.842 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.853 | 0.526 | 0.947 | 0.895 |
| ig:gold/llm:bm25 | 0.847 | 0.537 | 0.974 | 0.947 |
| ig:llm/index:bm25 | 0.808 | 0.537 | 0.860 | 0.737 |
| ig:gold/llm:bm25+repair=1 | 0.847 | 0.537 | 0.974 | 0.947 |
| ig:llm/index:bm25+repair=1 | 0.808 | 0.537 | 0.860 | 0.737 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ctx:tfidf | 0.340 | 0.736 | 0.882 |
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:llm/llm:bm25 | 0.352 | 0.808 | 0.927 |
| ig:llm/llm:bm25+rnorm=minmax | 0.352 | 0.785 | 0.927 |
| ig:llm/llm:bm25+repair=1 | 0.352 | 0.808 | 0.927 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.352 | 0.785 | 0.927 |
| ig:llm/llm:tfidf | 0.343 | 0.740 | 0.880 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.343 | 0.740 | 0.880 |
| ig:llm/llm:tfidf+repair=1 | 0.343 | 0.740 | 0.880 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.343 | 0.740 | 0.880 |
| ig:llm/llm:sbert | 0.374 | 0.731 | 0.846 |
| ig:llm/llm:sbert+rnorm=minmax | 0.399 | 0.683 | 0.821 |
| ig:llm/llm:sbert+repair=1 | 0.374 | 0.731 | 0.846 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.683 | 0.821 |
| ig:llm/llm:hybrid | 0.362 | 0.812 | 0.913 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.412 | 0.802 | 0.917 |
| ig:llm/llm:hybrid+repair=1 | 0.362 | 0.812 | 0.913 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.412 | 0.802 | 0.917 |
| ig:gold/llm:bm25 | 0.395 | 0.829 | 0.940 |
| ig:llm/index:bm25 | 0.302 | 0.820 | 0.936 |
| ig:gold/llm:bm25+repair=1 | 0.395 | 0.829 | 0.940 |
| ig:llm/index:bm25+repair=1 | 0.302 | 0.820 | 0.936 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ctx:tfidf | 0.738 | 0.729 | 0.772 | 0.864 |
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:llm/llm:bm25 | 0.793 | 0.766 | 0.760 | 0.918 |
| ig:llm/llm:bm25+rnorm=minmax | 0.790 | 0.778 | 0.768 | 0.917 |
| ig:llm/llm:bm25+repair=1 | 0.793 | 0.766 | 0.760 | 0.918 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.790 | 0.778 | 0.768 | 0.917 |
| ig:llm/llm:tfidf | 0.742 | 0.763 | 0.801 | 0.897 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.740 | 0.764 | 0.811 | 0.891 |
| ig:llm/llm:tfidf+repair=1 | 0.742 | 0.763 | 0.801 | 0.897 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.740 | 0.764 | 0.811 | 0.891 |
| ig:llm/llm:sbert | 0.758 | 0.743 | 0.747 | 0.825 |
| ig:llm/llm:sbert+rnorm=minmax | 0.750 | 0.693 | 0.735 | 0.856 |
| ig:llm/llm:sbert+repair=1 | 0.758 | 0.743 | 0.747 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.750 | 0.693 | 0.735 | 0.856 |
| ig:llm/llm:hybrid | 0.793 | 0.782 | 0.820 | 0.906 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.840 | 0.801 | 0.829 | 0.917 |
| ig:llm/llm:hybrid+repair=1 | 0.793 | 0.782 | 0.820 | 0.906 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.840 | 0.801 | 0.829 | 0.917 |
| ig:gold/llm:bm25 | 0.793 | 0.833 | 0.841 | 0.918 |
| ig:llm/index:bm25 | 0.804 | 0.770 | 0.757 | 0.867 |
| ig:gold/llm:bm25+repair=1 | 0.793 | 0.833 | 0.841 | 0.918 |
| ig:llm/index:bm25+repair=1 | 0.804 | 0.770 | 0.757 | 0.867 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ctx:tfidf | 0.862 |
| ctx:sbert | 0.824 |
| ctx:hybrid | 0.860 |
| ig:llm/llm:bm25 | 0.879 |
| ig:llm/llm:bm25+rnorm=minmax | 0.879 |
| ig:llm/llm:bm25+repair=1 | 0.879 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.879 |
| ig:llm/llm:tfidf | 0.882 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.882 |
| ig:llm/llm:tfidf+repair=1 | 0.882 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.882 |
| ig:llm/llm:sbert | 0.938 |
| ig:llm/llm:sbert+rnorm=minmax | 0.903 |
| ig:llm/llm:sbert+repair=1 | 0.938 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.903 |
| ig:llm/llm:hybrid | 0.879 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.879 |
| ig:llm/llm:hybrid+repair=1 | 0.879 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.879 |
| ig:gold/llm:bm25 | 0.879 |
| ig:llm/index:bm25 | 0.882 |
| ig:gold/llm:bm25+repair=1 | 0.879 |
| ig:llm/index:bm25+repair=1 | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.585 | 0.775 |
| ig:llm/llm:bm25+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.585 | 0.775 |
| ig:llm/llm:bm25+repair=1 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.585 | 0.775 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.585 | 0.775 |
| ig:llm/llm:tfidf | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:tfidf+repair=1 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:sbert | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.623 | 0.775 |
| ig:llm/llm:sbert+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.623 | 0.775 |
| ig:llm/llm:sbert+repair=1 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.623 | 0.775 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.623 | 0.775 |
| ig:llm/llm:hybrid | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:hybrid+repair=1 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:gold/llm:bm25 | 1.000 | 1.000 | 1.000 | 0.905 | 0.895 | 0.895 | 0.895 | 0.105 | 0.580 | 0.797 |
| ig:llm/index:bm25 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.632 | 0.640 | 0.316 | 0.607 | 0.723 |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.905 | 0.895 | 0.895 | 0.895 | 0.105 | 0.580 | 0.797 |
| ig:llm/index:bm25+repair=1 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.632 | 0.640 | 0.316 | 0.607 | 0.723 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 16.4 / 16.7 / 22.1 | – | – | – | – | 16.7 / 17.0 / 22.5 | 0.352 |
| ctx:tfidf | – | 13.1 / 12.6 / 13.7 | – | – | – | – | 13.5 / 13.0 / 14.2 | 0.284 |
| ctx:sbert | – | 139.1 / 119.0 / 127.0 | – | – | – | – | 139.2 / 119.2 / 127.2 | 2.924 |
| ctx:hybrid | – | 111.4 / 102.3 / 132.1 | – | – | – | – | 111.6 / 102.5 / 132.4 | 2.345 |
| ig:llm/llm:bm25 | 3700.4 / 3929.1 / 4504.9 | 13.0 / 15.3 / 20.2 | 2982.2 / 3430.6 / 4878.4 | 50.0 / 42.5 / 54.7 | 373.2 / 249.6 / 919.2 | 0.3 / 0.3 / 0.5 | 7107.7 / 7051.8 / 9956.1 | 26.93 |
| ig:llm/llm:bm25+rnorm=minmax | 4.4 / 3.7 / 6.4 | 5.8 / 6.2 / 8.2 | 2.4 / 1.9 / 4.8 | 224.2 / 19.3 / 783.4 | 162.6 / 94.2 / 327.8 | 0.3 / 0.1 / 0.6 | 394.7 / 123.6 / 1052.5 | 3.13 |
| ig:llm/llm:bm25+repair=1 | 317.8 / 4.1 / 2036.7 | 5.0 / 5.2 / 7.0 | 535.5 / 1.4 / 3555.0 | 15.1 / 18.0 / 32.0 | 154.2 / 96.1 / 304.5 | 0.3 / 0.1 / 0.6 | 1023.7 / 300.7 / 3562.6 | 10.731 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 4.0 / 3.2 / 6.0 | 12.4 / 14.5 / 19.3 | 2.3 / 1.9 / 4.8 | 21.9 / 31.1 / 42.6 | 317.5 / 210.2 / 700.5 | 0.3 / 0.2 / 0.4 | 347.3 / 250.4 / 754.2 | 3.893 |
| ig:llm/llm:tfidf | 4.7 / 4.4 / 8.2 | 5.8 / 5.9 / 6.5 | 2.1 / 1.2 / 4.4 | 15.3 / 21.2 / 28.4 | 184.1 / 109.6 / 374.6 | 0.3 / 0.2 / 0.7 | 207.5 / 138.0 / 401.0 | 2.64 |
| ig:llm/llm:tfidf+rnorm=minmax | 4.3 / 3.9 / 7.2 | 4.8 / 4.8 / 5.4 | 2.0 / 1.0 / 5.3 | 47.2 / 18.2 / 27.0 | 202.3 / 88.8 / 556.8 | 0.3 / 0.1 / 0.8 | 256.7 / 112.7 / 589.3 | 2.809 |
| ig:llm/llm:tfidf+repair=1 | 11.1 / 10.4 / 17.0 | 13.9 / 13.0 / 21.2 | 2.4 / 1.8 / 5.0 | 22.5 / 32.9 / 43.2 | 354.0 / 210.8 / 789.2 | 0.3 / 0.3 / 0.6 | 391.8 / 254.7 / 836.0 | 4.96 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 4.4 / 4.0 / 6.5 | 11.9 / 13.5 / 14.2 | 2.3 / 1.8 / 4.6 | 22.2 / 32.1 / 40.8 | 368.3 / 214.4 / 806.7 | 0.3 / 0.3 / 0.7 | 399.1 / 255.0 / 853.9 | 5.131 |
| ig:llm/llm:sbert | 2.9 / 3.0 / 3.7 | 122.3 / 120.6 / 125.5 | 2.5 / 1.7 / 6.2 | 41.4 / 37.9 / 120.4 | 325.8 / 195.7 / 706.4 | 0.3 / 0.2 / 0.4 | 374.4 / 243.9 / 753.6 | 7.161 |
| ig:llm/llm:sbert+rnorm=minmax | 4.8 / 4.2 / 6.8 | 122.4 / 121.1 / 130.0 | 2.0 / 1.6 / 4.2 | 52.8 / 36.4 / 50.6 | 356.5 / 229.3 / 839.0 | 0.3 / 0.2 / 0.4 | 417.7 / 264.4 / 883.6 | 7.688 |
| ig:llm/llm:sbert+repair=1 | 4.4 / 4.2 / 6.9 | 118.0 / 103.8 / 124.8 | 2.1 / 1.4 / 4.6 | 21.7 / 24.8 / 45.0 | 314.5 / 123.4 / 628.2 | 0.2 / 0.2 / 0.3 | 344.3 / 172.0 / 672.9 | 7.38 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 4.6 / 4.1 / 7.3 | 123.4 / 122.0 / 128.4 | 2.6 / 1.9 / 5.3 | 24.3 / 30.6 / 46.3 | 307.1 / 227.1 / 715.4 | 0.3 / 0.3 / 0.4 | 340.3 / 267.9 / 755.0 | 6.743 |
| ig:llm/llm:hybrid | 3.7 / 3.6 / 5.5 | 143.4 / 141.0 / 160.4 | 2.4 / 1.6 / 5.2 | 25.4 / 36.4 / 45.3 | 417.4 / 215.1 / 1516.2 | 0.4 / 0.3 / 0.9 | 450.9 / 262.7 / 1562.9 | 8.603 |
| ig:llm/llm:hybrid+rnorm=minmax | 4.9 / 5.1 / 6.1 | 100.9 / 96.7 / 115.5 | 1.8 / 1.3 / 4.4 | 20.4 / 26.0 / 40.1 | 379.4 / 151.3 / 1255.0 | 0.3 / 0.2 / 0.4 | 408.1 / 196.7 / 1300.5 | 7.464 |
| ig:llm/llm:hybrid+repair=1 | 4.1 / 3.9 / 6.2 | 133.0 / 133.6 / 143.1 | 2.1 / 1.4 / 4.8 | 94.6 / 25.7 / 525.8 | 333.2 / 138.2 / 887.6 | 0.3 / 0.2 / 0.5 | 435.5 / 206.1 / 1387.5 | 7.131 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 5.2 / 4.3 / 8.6 | 85.9 / 82.8 / 86.8 | 2.6 / 1.4 / 7.1 | 16.8 / 21.1 / 30.8 | 212.3 / 129.5 / 670.8 | 0.3 / 0.1 / 0.6 | 238.1 / 159.8 / 697.4 | 4.899 |
| ig:gold/llm:bm25 | 0.1 / 0.1 / 0.1 | 6.3 / 6.2 / 9.3 | 1889.9 / 2095.3 / 4022.5 | 34.3 / 33.0 / 42.8 | 445.0 / 165.3 / 802.3 | 0.2 / 0.1 / 0.2 | 2371.2 / 2382.2 / 4496.6 | 19.818 |
| ig:llm/index:bm25 | 4.6 / 4.2 / 6.5 | 5.0 / 5.4 / 7.2 | 1.6 / 0.7 / 4.8 | 15.2 / 19.1 / 28.6 | 182.7 / 84.6 / 440.3 | 0.2 / 0.1 / 0.3 | 205.4 / 110.2 / 489.0 | 3.06 |
| ig:gold/llm:bm25+repair=1 | 0.1 / 0.1 / 0.1 | 9.7 / 8.1 / 16.3 | 201.1 / 2.7 / 5.2 | 177.9 / 36.7 / 656.3 | 712.1 / 298.9 / 1442.0 | 0.3 / 0.2 / 0.3 | 1093.4 / 553.7 / 2014.5 | 10.756 |
| ig:llm/index:bm25+repair=1 | 3.7 / 3.6 / 5.3 | 14.5 / 17.3 / 21.7 | 2.1 / 0.7 / 5.7 | 27.2 / 40.3 / 49.1 | 354.2 / 218.0 / 758.4 | 0.3 / 0.3 / 0.4 | 389.2 / 266.9 / 810.8 | 5.08 |

Context index build (one-off, ms): bm25: 68 (cached), hybrid: 15066 (cached), sbert: 1243 (cached), tfidf: 31 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | -0.006 | [-0.044, +0.023] | 0.754 | 4/8 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | mrr | -0.025 | [-0.075, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/index:bm25 | ctx:bm25 | ndcg@10 | -0.025 | [-0.072, +0.014] | 0.280 | 8/6 |
| ig:llm/index:bm25 | ctx:bm25 | mrr | -0.075 | [-0.175, +0.025] | 0.380 | 1/4 |
| ig:llm/index:bm25 | ctx:bm25 | useful@1 | -0.150 | [-0.350, +0.050] | 0.380 | 1/4 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | -0.018 | [-0.058, +0.016] | 0.433 | 7/7 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | mrr | -0.050 | [-0.150, +0.050] | 0.626 | 1/3 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | useful@1 | -0.100 | [-0.300, +0.100] | 0.626 | 1/3 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.031 | [-0.076, +0.011] | 0.207 | 6/9 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.050 | [-0.125, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | -0.100 | [-0.250, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | -0.020 | [-0.061, +0.015] | 0.377 | 7/7 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.050 | [-0.150, +0.050] | 0.626 | 1/3 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | -0.100 | [-0.300, +0.100] | 0.626 | 1/3 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.031 | [-0.076, +0.011] | 0.207 | 6/9 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.050 | [-0.125, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.100 | [-0.250, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.008 | [-0.041, +0.053] | 0.753 | 8/6 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.069 | [-0.050, +0.200] | 0.298 | 6/2 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.100 | [-0.150, +0.350] | 0.688 | 4/2 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.047 | [-0.018, +0.104] | 0.155 | 11/4 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.096 | [-0.017, +0.217] | 0.244 | 4/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.150 | [-0.050, +0.350] | 0.370 | 4/1 |
| ig:llm/llm:tfidf | ctx:tfidf | ndcg@10 | +0.007 | [-0.042, +0.052] | 0.771 | 8/6 |
| ig:llm/llm:tfidf | ctx:tfidf | mrr | +0.069 | [-0.050, +0.200] | 0.298 | 6/2 |
| ig:llm/llm:tfidf | ctx:tfidf | useful@1 | +0.100 | [-0.150, +0.350] | 0.688 | 4/2 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | -0.006 | [-0.044, +0.023] | 0.754 | 4/8 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | -0.025 | [-0.075, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | -0.025 | [-0.072, +0.014] | 0.280 | 8/6 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.075 | [-0.175, +0.025] | 0.380 | 1/4 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | -0.150 | [-0.350, +0.050] | 0.380 | 1/4 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.047 | [-0.018, +0.104] | 0.155 | 11/4 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.096 | [-0.017, +0.217] | 0.244 | 4/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.150 | [-0.050, +0.350] | 0.370 | 4/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.054 | [-0.026, +0.131] | 0.191 | 13/3 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.096 | [-0.037, +0.242] | 0.279 | 5/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.150 | [-0.100, +0.400] | 0.451 | 5/2 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | ndcg@10 | +0.007 | [-0.042, +0.052] | 0.771 | 8/6 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | mrr | +0.069 | [-0.050, +0.200] | 0.298 | 6/2 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | useful@1 | +0.100 | [-0.150, +0.350] | 0.688 | 4/2 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.021 | [-0.022, +0.062] | 0.365 | 10/6 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | -0.020 | [-0.061, +0.015] | 0.377 | 7/7 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.050 | [-0.150, +0.050] | 0.626 | 1/3 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | -0.100 | [-0.300, +0.100] | 0.626 | 1/3 |
| ig:gold/llm:bm25 | ctx:bm25 | ndcg@10 | +0.021 | [-0.022, +0.062] | 0.365 | 10/6 |
| ig:gold/llm:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/llm:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.054 | [-0.026, +0.131] | 0.191 | 13/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.096 | [-0.037, +0.242] | 0.279 | 5/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.150 | [-0.100, +0.400] | 0.451 | 5/2 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | -0.018 | [-0.058, +0.016] | 0.433 | 7/7 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | -0.050 | [-0.150, +0.050] | 0.626 | 1/3 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | -0.100 | [-0.300, +0.100] | 0.626 | 1/3 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.008 | [-0.041, +0.053] | 0.753 | 8/6 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | mrr | +0.069 | [-0.050, +0.200] | 0.298 | 6/2 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | useful@1 | +0.100 | [-0.150, +0.350] | 0.688 | 4/2 |
