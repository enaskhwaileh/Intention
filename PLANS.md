# Experimental evaluation plan

## Audit

The repository began as a clean deterministic vaccine MVP on `full-pipeline-architecture`. It has legacy `src/intention_mvp` code and partial domain/registry scaffolding. There are no notebooks, downloaded datasets, data manifests, CI workflows, or real experiment artifacts. Tests cover the MVP and early registries. The tree was clean when this branch was created.

Reusable: packaging, YAML loading patterns, immutable dataclasses, fixture, and offline pytest setup. Obsolete: six legacy axes, category-local weights, `Psi*(I)`, soft feasibility multipliers, and MVP scoring. These remain regression history only.

## Milestones

1. Governance and exact contract.
2. Strict versioned knowledge layer with five actions/axes and hash.
3. Synthetic profiling, interpretation, topical retrieval, alignment, ranking, fallback, and reversal tests.
4. Benchmark validation, topic splitting, metrics, statistics, timings, ablations and sensitivity.
5. Immutable run bundles and fail-closed LaTeX reporting.
6. Pinned external integrations and real-data smoke when resources exist.

Each milestone requires tests and a focused commit. Synthetic acceptance is `python -m intention smoke` without credentials.

## Risks and open decisions

Exact TABERTA-Hybrid, Birdie, EDBT25, and Qwen revisions require authoritative artifacts and hardware; unavailable systems are blocked, never substituted. Human annotators, WikiTables path/license, semantic model revision, and development-selected hyperparameters are experiment inputs. Heuristic profiler evidence remains `inferred`/`estimated` until evaluated.

## Milestone record

- Milestone 1, contract audit: completed and verified. See
  `docs/contract_traceability.md`. The audit made numerical/interval rule
  parameters explicit, strengthened fail-closed validation and score bounds,
  and expanded the suite from 50 to 195 passing tests without changing the
  controlled example's ranking or scores.
