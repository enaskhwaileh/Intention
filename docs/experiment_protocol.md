# Experiment protocol

All tuning uses training/development topics only. Every action variant of a topic stays in one split. Test remains sealed until configurations, prompts, templates, weights, thresholds, and checkpoints are frozen and hashed.

IA-WikiTables selects topics without performance signals, pools fixed-depth outputs from every declared system including Ours, deduplicates tables, and exports blinded tasks. Two annotators independently record topical relevance `z(q,T)` and ordinal usefulness `y(u,T)`; disagreements require adjudication. LLM output cannot be a final test judgment. Imports validate identities, label domains, completeness, duplication, and adjudication; leakage checks reject shared topics.

Runs record model/revision, serialization, instructions, dimension, depth, hardware, seed, Git commit, knowledge hash, dataset manifest, timings, predictions, and metrics. Unavailable baselines fail explicitly. Metrics include nDCG@5/10, MRR at `y>=2`, Useful-Recall@K, per-action and switch accuracy, diagnostics, ordinal agreement, paired topic bootstrap intervals, and corrected paired tests.
