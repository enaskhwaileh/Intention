# Controlled interpreter validation

The deterministic structured provider is evaluated on twelve developer-authored
cases: all five actions, aliases, value normalization, existential binding,
multiple-action ambiguity, no-action input, unsupported action, and missing
required arguments.

| Diagnostic | Controlled result |
|---|---:|
| Cases passing | 12/12 |
| Action accuracy | 1.000 |
| Action macro-F1 | 1.000 |
| Argument precision/recall/F1 | 1.000 / 1.000 / 1.000 |
| Joint-frame accuracy | 1.000 |
| Provenance-span accuracy | 1.000 |
| Grounding-decision accuracy | 1.000 |

These results validate deterministic contract behavior, not natural-language or
LLM generalization. Inputs use explicit argument syntax and a frozen alias
catalogue. A real provider requires independently labeled development/test
requests, exact provider/model revision, prompt, schema, raw outputs, latency,
and error analysis.

Hashes at this milestone:

- normalization: `37a607e127f7b85d27300dc5a872ec422909b19ac9b89fac5bb2ce3b53cde3c1`
- output schema: `beb861d71abdf7a11ddf175a3b6782283d45a3abb95ab1d3b0395ca72a4acd6b`
- controlled gold: `8a1443896974f72a5ef1874a9c98d2bf58dafaddcb9520cd870b560c955f7ff4`

Run:

```bash
PYTHONPATH=src python3 -m intention evaluate-interpreter
```

The evaluator reports strict joint-frame accuracy (action plus complete
argument map) and provenance-span accuracy (mean per-case span-set Jaccard), in
addition to action, argument, and grounding-decision metrics. Gold spans are
explicit source-text annotations with occurrence indices where text repeats.
