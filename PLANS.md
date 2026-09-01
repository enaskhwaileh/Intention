# Canonical 12-milestone roadmap

This roadmap is the single planning authority. Every milestone ends with a
reviewable commit, deterministic verification, and an updated `STATUS.md`.
Unavailable external systems must fail explicitly rather than be approximated.

1. **Contract audit — complete.** Freeze the five-axis mathematical contract,
   validation boundaries, matcher semantics, and traceability matrix.
2. **Synthetic benchmark and cleanup — complete.** Remove superseded six-axis
   assets and establish multi-topic, all-action ranking-reversal fixtures.
3. **Capability-profiler validation — complete.** Freeze gold annotations,
   predicate scope, row granularity, immutable profiles, and diagnostics.
4. **Online interpretation and grounding — complete.** Enforce the
   provider schema, normalization-backed provenance, independent topical and
   grounding failures, frame/span metrics, and action semantics.
5. **Retrieval contracts and serialization — complete.** Freeze table serialization,
   candidate depth, retriever interfaces, and pinned lexical/semantic baseline
   identities. Entry gate: Milestone 4 hardening reviewed and merged.
6. **Evaluation library — complete and merged.** Finalize graded ranking metrics, action-switch
   diagnostics, paired statistics, confidence intervals, and leakage guards.
7. **IA-WikiTables benchmark construction.** Acquire licensed source data,
   create topic/action splits and pools, run human annotation, and adjudicate
   usefulness labels. No synthetic labels may be reported as real evidence.
8. **End-to-end experiment orchestration.** Produce immutable run bundles with
   configs, hashes, manifests, predictions, timings, and environment metadata.
9. **Ablations, oracles, and sensitivity.** Measure action removal, grounding
   errors, capability axes, fusion weights, candidate depth, and oracle bounds.
10. **Real-data smoke.** Run a small frozen subset on available pinned systems
    and stop on missing credentials, checkpoints, hardware, or licenses.
11. **Full evaluation.** Execute baselines and the proposed method on frozen
    splits, then compute corrected paired tests, intervals, and efficiency.
12. **Reporting and release.** Generate paper tables from immutable bundles,
    document limitations and reproducibility, and archive exact artifacts.

## Frozen scope decision before Milestone 5

`MONITOR` is permanently the fifth supported action for this research
contract. It expresses a single-table requirement for repeated observations
and optional temporal coverage. `INTEGRATE` is not an alias or replacement:
it would require a separate multi-table compatibility, join-key, and
composition contract. Adding it therefore requires a future contract revision,
new annotations, and new evaluation—not a retrieval or benchmark substitution.

## Current gate

Milestones 1–6, all Pre-Milestone-7 gates, M7A.1, and M7A.2a are merged and
complete. M7A.2b full acquisition/normalization is complete and awaiting review.
The gated sequence is:

1. M7A.2b — full corpus acquisition and normalization (current review gate).
2. M7B — development-only topical retriever bake-off.
3. Freeze the primary semantic encoder using development topical metrics only.
4. M7C — pooling and human annotation.

This staging does not change official Milestone 7 in the 12-milestone roadmap.
The final encoder remains unselected. Retrieval experiments, annotation, pool
freezing, and paper-result generation remain outside M7A.2b.
