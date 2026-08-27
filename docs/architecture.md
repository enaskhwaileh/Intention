# Normative architecture

```text
configs/knowledge/knowledge.yaml -> strict K_G loader
                                      |
user text -> provider -> validation -> grounding -> requirements
     |                                               |
     +-> topical query -> retriever -> candidates    |
tables -> profiler -> capability profiles            |
                 requirements + capabilities -> alignment
                                                   -> usefulness ranking
benchmark -> human labels -> evaluation -> immutable runs -> LaTeX
```

The system discovers one table at a time. Candidate generation receives only
the topical query. Action-bearing input is used by interpretation and grounding,
not by the default first-stage retriever.

```text
src/intention/
  knowledge/       # K_G schema, validation, and hashing
  profiling/       # offline capability evidence
  interpretation/  # providers, normalization, grounding, requirements
  retrieval/       # common first-stage interface
  alignment/       # matching and exact axis equations
  ranking/         # usefulness combination
  benchmarks/      # construction, annotation, leakage controls
  baselines/       # reproducibility-gated adapters
  evaluation/      # metrics and statistics
  reporting/       # immutable runs and generated tables
```

The exact equations live in `docs/method_contract.md`; their code and tests are
indexed in `docs/contract_traceability.md`.
