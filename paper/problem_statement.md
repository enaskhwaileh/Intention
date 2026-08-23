# Problem statement

Given a natural-language request `u` and a collection of individual candidate
tables, separate the topical information need `q_u` from intended action `I_u`.
Ground the action into requirement profile `Psi*(I_u)`, profile each table
independently as `Phi*(T)`, retrieve by topic, and estimate operational
suitability from relevance, alignment, and explicit feasibility evidence.

Hypothesis: a topically relevant table is not necessarily suitable for the
analytical action a user intends to perform.

The task is single-table discovery. The system does not claim downstream model
accuracy or causal validity.
