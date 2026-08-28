# Contract-to-code traceability

This matrix records the normative method implementation. The superseded MVP,
six-axis registry, duplicate configurations, and their tests were removed after
reference analysis established that they formed a self-contained unused cluster.
They remain recoverable from Git history.

| Contract element | Configuration | Implementation | Verification |
|---|---|---|---|
| \(\mathcal A\), five actions | `configs/knowledge/knowledge.yaml:actions` | `knowledge/layer.py` | exact-vocabulary and strict-schema tests |
| \(\mathcal X\), five axes | `knowledge.yaml:axes` | `KnowledgeLayer.axes` | exact order/set test |
| \(\mathcal P\), predicates and \(\xi(p)\) | `knowledge.yaml:predicates.*.axis` | `PredicateDef` | unknown predicate and axis-mismatch rejection |
| \(\mathcal G\), action templates | `knowledge.yaml:actions.*.requirements` | `requirements()` | grounding/profile tests |
| \(\mathcal M\), matching rules | `knowledge.yaml:predicates.*.matcher` | `match_value()` | every rule/operator/mode tests |
| \(\mathcal B\), axis weights | `knowledge.yaml:actions.*.weights` | `align()` normalization | strict sum/domain and active-axis tests |
| \(\mathcal V\), constraints | `knowledge.yaml:validation` | `load_knowledge()`, `ground()`, `align()` | fail-closed nested mutation tests |
| \(\gamma=(p,x,v,s,c,prov)\) | predicate catalogue | `contracts.Capability`, `profile_table()` | gold predicate/value/provenance tests |
| \(u\to(q_u,\iota_u)\to g_u\) | output schema + normalization catalogue | `ProviderArtifact`, `ground()` | action/argument/span/ambiguity/fallback tests |
| \(\Psi(g_u)\to\Psi^*(g_u)\) | action templates | `requirements()` | conditional and existential tests |
| topical-only \(\mathcal C_{q_u}\) | retrieval contract + registry | `RetrievalRequest`, `BM25Retriever`, `pipeline.run()` | `test_pipeline_passes_only_topical_query_to_first_stage_retriever` |
| \(m(\rho,T)=\max M_pc\) | predicate matcher | `alignment/scoring.py` | maximum/confidence/missing tests |
| \(R_x,O_x,N_x\) conventions | experiment etas | `align()` | empty-set and min/mean-ablation tests |
| \(S_x\), active weight normalization, \(A\) | action weights | `align()` | component trace and bounded grid tests |
| grounded \(U=\lambda_rr+\lambda_aA\) | experiment config | `ranking/ranker.py` | weight/relevance/bounds/reversal tests |
| bottom \(U=r\) | none | `rank()` | exact fallback test |
| knowledge version/hash | complete YAML | `load_knowledge()` | deterministic SHA-256 test |

Offline profile identity and persistence are implemented by
`CapabilityProfile`, `build_profile()`, and `CapabilityRepository`. Gold schema,
four-state unknown handling, and structured granularity are defined in
`profiling/annotations.py` and evaluated by `profiling/evaluation.py`.

Raw provider artifacts, strict structured validation, normalization, ambiguity,
and validated grounding are separated by `interpretation/schema.py`,
`normalization.py`, `providers.py`, and `interpreter.py`. Controlled action and
argument diagnostics are implemented in `interpretation/evaluation.py`.

## Audit decisions

- `mean` aggregation for required requirements is accepted only through the
  explicit ablation value `required_aggregation="mean"`; other values fail.
- Numerical direction and interval behavior are predicate-specific configuration
  parameters, rather than implicit behavior hidden in matcher code.
- Retrieval scores entering the convex usefulness equation must be normalized
  to `[0,1]`; invalid retriever output fails before ranking.
- Scoring validates every requirement and capability against the loaded
  predicate-to-axis mapping. Providers and stored profiles therefore cannot
  inject new predicates or axes at ranking time.
- Semantic compatibility has no silent lexical approximation. It requires an
  explicitly configured scorer returning a bounded value; without one, the
  matcher fails clearly. No current synthetic predicate uses this rule.
