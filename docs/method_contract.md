# Normative method contract

This supersedes conflicting definitions for the new implementation. `src/intention_mvp` is regression-only.

Actions are `COMPARE`, `AGGREGATE`, `PREDICT`, `EXPLAIN`, and `MONITOR`. `EXPLAIN` is associational, never causal. `PREDICT` tests evidence availability, not performance. The only axes are `sem`, `str`, `cov`, `qual`, and `aff`. `K_G=(A,X,P,G,M,B,V)` is strict versioned configuration; providers cannot extend its vocabularies.

A capability is `(predicate,axis,value,state,confidence,provenance)`, where state is `observed`, `estimated`, or `inferred`. Missing evidence is absent, never false. Provenance distinguishes declared/inferred keys and complete/sample statistics.

Interpretation separates topical `q_u` from declared action/arguments. Valid grounding yields `g_u=(a_u,theta_u)`; otherwise bottom. Required values are never guessed; permitted existential values use `*`. Invalid grounding returns `(q_u,bottom,empty requirements)`. Requirements are `(predicate,axis,expected,polarity,provenance)`. Retrieval receives only `q_u`.

For same-predicate/axis capabilities, `m=max(M_p(expected,value)*confidence)`, or zero if absent. Per axis, `R=min(required)` (empty 1), `O=mean(optional)` (empty 0), `N=mean(negative)` (empty 0), and `S=R*((1-eta_o)+eta_o*O)*(1-eta_n*N)`. Renormalize action weights over active axes and set `A=sum(weight*S)`. Grounded `U=lambda_r*r+lambda_a*A`, where lambdas are nonnegative and sum to one; bottom uses `U=r`. Scores remain in `[0,1]`.

Matcher types: exact, normalized equality, semantic compatibility, numerical comparison, set containment, interval overlap/containment, granularity compatibility, and existential satisfaction.
