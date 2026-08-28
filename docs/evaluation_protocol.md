# Milestone 6 evaluation contract

The versioned authority is `configs/evaluation/protocol.yaml`. Controlled
fixtures are not paper evidence.

## Metric layers

1. **Interpretation/grounding:** action/argument, joint-frame, provenance, and
   grounding-decision metrics remain separate.
2. **Retrieval:** candidate recall at 5/10/20 and the candidate-set upper bound.
3. **Usefulness ranking:** graded nDCG@5/10, MRR and Useful-Recall at `y >= 2`,
   per-action summaries, action-switch pairs, and action-aware deltas.
4. **Annotation/agreement:** ordinal labels 0–3, quadratic weighted kappa, and
   fail-closed missing, duplicate, or incomplete judgments.
5. **Statistical comparison:** topic-first aggregation, paired bootstrap with
   2,000 iterations/seed 2026, paired sign permutation, and Holm correction
   across all predeclared primary system comparisons.

Ties use ascending table ID after descending score. Test labels cannot tune
thresholds, K, fusion weights, calibration, or prompts.

```bash
PYTHONPATH=src python3 -m intention evaluate-controlled
```

The fixture is marked `paper_result: false`. No IA-WikiTables annotation or
real model run occurs.
