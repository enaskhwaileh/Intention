# Experimental evaluation plan

## Audit

The repository began this work as a deterministic vaccine MVP on
`full-pipeline-architecture`. That superseded implementation was removed in
Milestone 2 after equivalent normative coverage and reference analysis. There
are no notebooks, downloaded datasets, data manifests, CI workflows, or real
experiment artifacts. The tree was clean when this branch was created.

Reusable foundations were packaging, YAML loading patterns, immutable
dataclasses, fixtures, and offline pytest setup. Obsolete six-axis definitions,
category-local weights, old notation, feasibility multipliers, and MVP scoring
remain available only through Git history.

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
- Milestone 2, repository cleanup and multi-topic synthetic benchmark:
  completed and verified. Superseded conflicting assets were removed after
  reference analysis. The versioned benchmark covers all five actions in six
  cases across three paired topics, with three relevance-to-usefulness ranking
  corrections.
- Milestone 3, capability-profiler validation: completed and verified. It adds
  the four-state gold protocol, three predicate tiers, structured granularity,
  strict annotations for six tables, immutable versioned profile storage,
  complete/sample provenance, and controlled profiler diagnostics.
- Milestone 4, online interpretation and grounding: completed and verified. It
  adds a provider-independent JSON Schema, raw/validated artifact separation,
  versioned normalization, explicit ambiguity states, fail-closed external
  provider boundary, and twelve-case action/argument evaluation.
