# Milestone 6 evaluation contract

The versioned authority is `configs/evaluation/protocol.yaml`. Controlled
fixtures are not paper evidence.

## Metric layers

1. **Interpretation/grounding:** action/argument, joint-frame, provenance, and
   grounding-decision metrics remain separate.
2. **Retrieval:** first-stage candidate recall at 5/10/20 and separately named
   candidate-set recall. This is not end-to-end Useful-Recall.
3. **Usefulness ranking:** graded nDCG@5/10, MRR and Useful-Recall at `y >= 2`,
   per-action summaries, action-switch pairs, and action-aware deltas.
4. **Annotation/agreement:** topical relevance uses `0/1/2`; intended-action
   usefulness uses `0/1/2/3`. They remain separate judgments with separately
   reported quadratic weighted kappa and completeness. Missing, duplicate, or
   incomplete judgments fail closed.
5. **Statistical comparison:** topic-first aggregation, paired bootstrap with
   2,000 iterations/seed 2026, paired sign permutation, and Holm correction
   across all predeclared primary system comparisons.

The normative ranking input is a list of scored table IDs plus complete qrels
covering the declared table universe. Unknown or duplicate returned IDs and
missing judgments fail closed. Ties use ascending table ID after descending
score. For nDCG, ideal DCG is computed from every judged table in the declared
universe; an omitted table contributes no retrieved gain but remains in the
ideal. End-to-end Useful-Recall divides by all tables with usefulness `>= 2` in
that universe. Candidate-set recall is reported under its own name.

Action-switch correctness accepts any table tied for maximum action-specific
usefulness. Per-action and corpus summaries first average request variants
within topic, then average topics. Bootstrap interval quantiles come from the
configured confidence level. Test labels cannot tune thresholds, K, fusion
weights, calibration, or prompts.

```bash
PYTHONPATH=src python3 -m intention evaluate-controlled
```

The fixture is marked `paper_result: false`. No IA-WikiTables annotation or
real model run occurs.
