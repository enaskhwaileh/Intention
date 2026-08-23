# Design reconciliation

This document prevents the executable checkpoint, the architecture described
in the eventual paper, and unresolved research choices from being conflated.

## Current implemented MVP

The implementation is a deterministic, offline vertical slice built around one
manually authored vaccine scenario.

- `QueryProfile`, `GroundedAction`, `RequirementProfile`, and
  `CapabilityProfile` are immutable dataclasses.
- Action templates and predicates are configured in `configs/actions.json`.
- Scoring parameters are configured in `configs/scoring.json`.
- Query, relevance, candidates, capabilities, confidence, and provenance are
  loaded from `fixtures/vaccine_mvp.json`.
- Only `compare` and `predict` have requirement templates.
- Matching uses exact predicate compatibility plus transparent equality,
  containment, and set-overlap rules.
- Each requirement retains its highest-scoring capability match on the same
  axis.
- Alignment combines required and optional matches. Usefulness combines
  alignment with topical relevance. Failure of required evidence causes a soft
  multiplicative demotion.
- Explanations report satisfied, partially satisfied, and missing requirements
  with component scores and available provenance.
- Unsupported actions fall back to relevance-only ranking.

The catalogue currently names six provisional axes: `content`, `structure`,
`analysis`, `scope`, `relation`, and `quality`. `relation` is inactive. The
configured relevance/alignment weights, required/optional weights, thresholds,
and demotion multiplier are fixed for the demonstration. Neither the axes nor
the numerical settings should be described as final or empirically validated.

## Intended paper architecture

The paper should describe the method at conceptual boundaries that can survive
changes to individual implementations:

1. interpret a user's topical information need and intended downstream action;
2. translate the grounded action into explicit operational requirements;
3. describe candidate datasets through evidence-backed capability profiles;
4. align action requirements with dataset capabilities;
5. combine topical relevance and action alignment subject to required-evidence
   handling; and
6. return an action-conditioned ranking with inspectable explanations.

The current MVP supplies one executable instance of stages 2 through 6, with
manual inputs standing in for stages 1 and 3. The paper must label manual and
automatic components accurately. Any broader architecture, learned component,
or semantic matcher belongs to future work until implemented and evaluated.

The deleted pre-cleanup implementation at commit `030fe82` contains earlier
experiments with intention graphs, input interpretation, capability extraction,
and typed validation. It is historical evidence of prior exploration, not part
of this checkpoint and not automatically the intended final architecture.

## Unresolved design decisions

The following require explicit research decisions and evidence:

- What action vocabulary is in scope, and how actions and arguments are
  grounded from user input.
- Whether the six provisional axes are complete, independent, consistently
  defined, or the right abstraction for the paper.
- How requirements are authored, learned, validated, and versioned.
- How table capabilities and their provenance are extracted from real data and
  metadata.
- Which matching functions should support lexical, structural, semantic, and
  granularity compatibility.
- Whether required evidence should filter, demote, or participate in a
  constrained ranking objective.
- How relevance, alignment, confidence, thresholds, and optional evidence
  should be calibrated. The current fixed values are not final.
- Which relevance-only, task-aware, learning-to-rank, or dataset-search systems
  form appropriate baselines.
- Which domains, actions, queries, candidate sets, annotations, and metrics are
  sufficient to support the paper's claims.
- How uncertainty, conflicting evidence, ties, missing metadata, and invalid
  profiles should affect ranking and explanation.
- Which parts of the approach must remain deterministic and explainable if
  learned or LLM-assisted components are introduced.

No choice in this section is resolved merely because the MVP has a convenient
implementation default.
