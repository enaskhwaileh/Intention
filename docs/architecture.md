# Architecture contract

The research system operates on one table at a time. It does not silently turn
dataset discovery into multi-table integration.

## Canonical notation

```text
Interpret(u) -> (q_u, I_u)
Ground(I_u) -> Psi*(I_u)
Profile(T) -> Phi*(T)
Retrieve(q_u) -> candidates and topical relevance
Align(Psi*(I_u), Phi*(T)) -> alignment and evidence trace
Rank(relevance, alignment, feasibility) -> usefulness ranking
```

`Psi*(I)` is always the intended-action requirement profile. `Phi*(T)` is
always the table capability profile.

## Implemented in Phases 0–2

- Serializable validated domain contracts for every planned stage boundary.
- Canonical action, axis, evidence-state, feasibility-policy, and status enums.
- Versioned YAML registries for observable predicates and five actions.
- Registry validation covering predicate references, action coverage, version
  compatibility, and normalized category weights.
- Cross-profile validation against the registries.

The contracts do not imply that later profiling, interpretation, retrieval,
alignment, ranking, benchmark, evaluation, or notebook stages are implemented.

## Scientific boundaries

The axes organize predicates; they are not asserted to be statistically or
mathematically independent. A later aggregation implementation must prevent the
same evidence from being rewarded repeatedly.

The system estimates operational suitability. `predict` does not promise model
accuracy. `explain` means support for exploratory or associational analysis and
does not establish causal identification. The `relation` axis is canonical but
inactive for the primary single-table system.
