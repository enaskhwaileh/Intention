# Implementation status

## Complete

- Phase 0 safety and baseline inspection.
- Phase 1 domain contracts, canonical notation, package boundary, configuration
  contract, migration plan, and paper-support scaffolding.
- Phase 2 versioned action and predicate registries with validation.
- Preserved deterministic vaccine MVP and its regression tests.

## Not implemented

- Offline table profiling.
- Online input interpretation and grounding.
- BM25, TABERTA, and fallback retrieval interfaces.
- Requirement-capability matching and evidence-state inference.
- Feasibility policies and action-conditioned ranking in `src/intention`.
- Full pipeline orchestration and stage artifacts.
- Benchmark downloads, adapters, annotations, baselines, evaluation, ablations,
  executed notebook, and measured paper results.

`src/intention_mvp` remains the executable regression implementation. It is not
presented as the full architecture.
