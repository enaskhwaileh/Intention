# Synthetic capability-profiler validation

## Result scope

This is a regression evaluation on six small developer-authored tables with
independently stored gold annotations. It validates schema, metrics, provenance,
and controlled behavior. It is not an estimate of real-corpus accuracy.

Gold file: `fixtures/synthetic_capability_gold.json`  
SHA-256: `675062af966b9817a175f75a1628ae2ece42f3bdd614cc754a49ffcd37451cda`  
Knowledge hash: `1ddf47f9f4de2bf508c57ea7dbd5b8af266003b57767ad1d3e414d923cd6ec2c`

## Recorded controlled metrics

| Diagnostic | Result | Denominator/qualification |
|---|---:|---|
| Capability-predicate macro-F1 | 1.000 | 9 predicates with positive support |
| Predicate-specific value macro score | 1.000 | supported values only |
| Provenance structural validity | 1.000 | all emitted capabilities |
| Row-granularity kind accuracy | 1.000 | 6 tables |
| Aggregation-status accuracy | 1.000 | 6 tables |
| Granularity field macro-F1 | 1.000 | entity/time/grouping fields |
| Exact structured-granularity accuracy | 1.000 | description excluded |

`identifier_only` has six negative and zero positive gold cases, so its F1 is
undefined and excluded from macro-F1. Four `geographic_coverage` judgments are
`unknown` and excluded rather than converted to negatives. These exclusions are
part of the output, not hidden post-processing.

## Behavior validated

- Numeric identifier columns are not measures.
- Declared keys and name-inferred identifiers are distinct in provenance.
- Missingness, variation, and temporal statistics distinguish complete scans
  from sample estimates; sample evidence is `estimated` with lower confidence.
- Shared dates do not establish longitudinal support. The same entity must have
  observations at multiple times.
- Row granularity is compositional and distinguishes entity observations from
  aggregated group/group-time rows.
- Capability profiles include profiler version, knowledge hash, table checksum,
  complete/sample flag, and deterministic capabilities.
- The repository refuses to overwrite a table profile with different content.

## Known limitations

The examples were constructed alongside the method-development process, have
no ambiguous cases, contain no positive `identifier_only` table, and are too
small to stress sampling, type errors, mixed granularity, composite declared
keys, noisy dates, or semantic geography extraction. Real-data claims require
an independently annotated and adjudicated set with positive and negative
support for every predicate.

## Command

```bash
PYTHONPATH=src python3 -m intention evaluate-profiler
```
