# Capability annotation and row-granularity protocol

## Scope and independence

Gold annotation is defined independently of profiler output. Annotators receive
the table, metadata, schema, permitted complete-table statistics, and these
instructions; they do not see system predictions. Synthetic labels are
developer-authored regression gold. Real evaluation requires two independent
annotators and adjudication.

## Judgment schema

The unit is one table and one controlled predicate. Every predicate receives
exactly one judgment: `supported`, `not_supported`, `unknown`, or
`not_applicable`. Supported judgments require a normalized value and evidence.
Unknown is never scored as negative. Human numerical confidence is prohibited;
`certainty` is `clear` or `ambiguous`, with a reason for ambiguity.

Evidence records a `source_type` (`metadata`, `column`, `cell_range`,
`table_statistic`, `documentation`, or `multiple_sources`), a source locator,
and `inspection_scope` (`complete_table`, `sample`, or `declared_metadata`).

## Predicate tiers

- Tier 1, directly observable: `has_field`, `numeric_measure`,
  `temporal_coverage`, `geographic_coverage`, `missingness_at_most`, and
  `adequate_variation`.
- Tier 2, structurally derived: `grouping_field`, `non_identifier_features`,
  `identifier_only`, and `repeated_observations`.
- Tier 3, interpretive: `row_granularity`.

All eleven predicates are frozen and annotated. A numeric identifier is not a
numeric measure. A grouping field must define meaningful groups rather than
near-unique record identities. Repeated observations require repeated units
across time or ordered events; shared dates alone are insufficient.

## Structured row granularity

`kind` is one of `entity`, `event`, `entity_time`, `group`, `group_time`,
`aggregate_total`, `mixed`, or `unknown`. The value also records
`entity_fields`, `entity_type`, `time_fields`, `time_unit`, `grouping_fields`,
`aggregation_status` (`observed`, `aggregated`, `mixed`, or `unknown`), and a
description. Declared identifiers and inferred identifiers are recorded
separately in evidence/provenance.

Evaluation reports kind accuracy, aggregation-status accuracy, entity/time/
grouping field F1, and exact structured accuracy. Predicate detection reports
per-predicate and macro precision/recall/F1; unknown and not-applicable records
are excluded but counted. Predicate-specific values and provenance validity are
reported separately.
