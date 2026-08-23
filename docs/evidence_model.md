# Evidence model

Every future match must distinguish five evidence states:

- `satisfied`
- `partially_satisfied`
- `unknown`
- `contradicted`
- `not_applicable`

Unknown means evidence is absent or insufficient. Contradicted means observable
evidence conflicts with the requirement. These states must not share an
implicit score or feasibility outcome.

Capability evidence requires its source element, derivation method, profiler
version, and optional source statistic. Match traces retain the requirement,
observed capability, confidence, evidence state, score, provenance, and a human
readable explanation.

The contracts are implemented. Evidence inference, deduplication, feasibility,
and aggregation are Phase 6 work.
