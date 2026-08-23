# Predicate catalogue

Predicates describe observable table properties. They do not encode final
decisions such as `suitable_for_prediction = true`.

The canonical axes are `content`, `structure`, `analysis`, `scope`, `relation`,
and `quality`. They are organizational categories, not assumed independent
dimensions. `relation` is inactive for the primary single-table architecture.

Every predicate identifier is namespaced by axis and ends with a major version,
for example `content.observed_outcome.v1`. The machine-readable catalogue,
descriptions, value kinds, active axes, and registry version are in
`configs/predicates.yaml`.

Phase 3 must define how offline evidence derives each implemented capability;
catalogue membership alone is not an extraction implementation.
