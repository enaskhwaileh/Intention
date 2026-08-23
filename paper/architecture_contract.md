# Paper architecture contract

The manuscript and implementation must use:

```text
Interpret(u) -> (q_u, I_u)
Ground(I_u) -> Psi*(I_u)
Profile(T) -> Phi*(T)
Retrieve(q_u) -> candidate tables and relevance scores
Align(Psi*(I_u), Phi*(T)) -> alignment and evidence trace
Rank(relevance, alignment, feasibility) -> usefulness ranking
```

The existing figure that reverses Psi and Phi is incorrect. `Psi*(I)` always
denotes action requirements; `Phi*(T)` always denotes table capabilities.

Five actions are in scope: compare, aggregate, predict, explain, and monitor.
Explain is exploratory/associational, not causal. Relation is an inactive
organizational axis in the primary single-table system.

The name IAGuide is unresolved. Documentation must not silently adopt or remove
it until the project owner decides.
