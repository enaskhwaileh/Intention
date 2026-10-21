# Intention Library

> Supporting appendix. Start with the [main project guide](../README.md) for current architecture, demonstration, models and testing. Historical audit statements are dated records, not current capability claims.

The canonical library is [action-base-v0.2.json](../intention_grounding/docs/ab_proposal/action-base-v0.2.json). It defines **23 families, 62 concrete intentions, and 66 procedure alternatives**. This is an extensible, author-designed research draft, not an exhaustive or empirically validated taxonomy. The original v0.1 catalog remains available unchanged for reproducibility.

## Coverage

| Family | Concrete intentions |
| --- | --- |
| compare | `compare.groups`, `compare.groups.trajectories`, `compare.time` |
| retrieve | `retrieve.lookup`, `retrieve.filter`, `retrieve.sort`, `retrieve.top_k` |
| summarize | `summarize.profile`, `summarize.distribution`, `summarize.statistics` |
| aggregate | `aggregate.grouped`, `aggregate.count`, `aggregate.temporal` |
| associate | `associate.correlation`, `associate.categorical`, `associate.conditional` |
| predict | `predict.classification`, `predict.regression`, `predict.forecasting`, `predict.survival` |
| cluster | `cluster.partition`, `cluster.density` |
| detect | `detect.anomaly`, `detect.change` |
| explain | `explain.association`, `explain.model`, `explain.causal` |
| test | `test.difference`, `test.independence`, `test.goodness_of_fit` |
| estimate | `estimate.parameter`, `estimate.interval` |
| monitor | `monitor.threshold`, `monitor.drift` |
| integrate | `integrate.join`, `integrate.union`, `integrate.entity_resolution` |
| prepare | `prepare.clean`, `prepare.deduplicate`, `prepare.impute`, `prepare.derive`, `prepare.reshape`, `prepare.sample` |
| validate | `validate.schema`, `validate.quality` |
| visualize | `visualize.distribution`, `visualize.relationship`, `visualize.temporal` |
| recommend | `recommend.items` |
| optimize | `optimize.allocation`, `optimize.multiobjective` |
| simulate | `simulate.scenario`, `simulate.sensitivity` |
| spatial | `spatial.proximity`, `spatial.region` |
| network | `network.paths`, `network.communities` |
| text | `text.classification`, `text.extraction`, `text.summary` |
| discover | `discover.topical`, `discover.compatible` |

## Runtime support

Three existing Compare intentions support grounding: `compare.groups`, `compare.groups.trajectories`, and `compare.time`. The remaining 59 concrete intentions are `catalog_only`: they have declarative requirements and procedures, but no runtime grounder or executor. No intention has analytical execution implemented, and the current aligner still returns unknown verdicts.

The live grounder sees only the implemented Compare branch. Requests that explicitly propose catalog-only actions return `unsupported` without producing a grounded card. Abstract family names cannot be grounded. Adding a catalog entry does not enable runtime support: a separate code capability boundary prevents that.

Compare remains direct-observation comparison. Aggregate-then-compare may eventually be represented as a composition of distinct intentions, but this extension does not enable it. The existing full-grid grounding and multi-goal limitations remain. Retrieval, ranking, benchmark evaluation, and analytical execution are future work.

## Inspect the library offline

From the repository root, using the project's Python environment:

```sh
python -m intention_grounding.cli --list-intentions
python -m intention_grounding.cli --intention predict.forecasting
python -m intention_grounding.cli --intention explain.causal
```

These inspection commands require no model provider and write no pipeline artifacts. `--il` (or compatibility alias `--ab`) can select the frozen v0.1 catalog. Python callers can use `load_intention_library`, `list_intentions`, and `describe_intention` from `intention_grounding.action_base`.

An intention description includes inherited roles and separate procedure alternatives. Each procedure includes its own additional roles, requirement templates, predicate definitions, input scope, output contract, and evidence policy. Requirement templates are **unbound and not evaluated**; conditional activation and evidence assessment still need runtime integration.

## Prediction and procedure alternatives

Prediction includes classification, regression, forecasting, and survival. Classification and regression each declare linear and tree procedure alternatives. Forecasting distinguishes univariate forecasting from forecasting with covariates. Survival declares event and duration roles and follow-up requirements. This covers the requested prediction categories, not every possible model algorithm.

Supervised prediction records prediction timing and feature availability without requiring a time-series axis. Forecasting requires a time axis and horizon; its univariate procedure does not require covariates. Procedure selection remains declarative. The current interpreter schema has not been expanded to bind every new role.

Association, model explanation, and causal explanation are separate intentions. Causal explanation distinguishes randomized-design and observational-identification procedures and requires design evidence. A fitted predictive relationship alone cannot establish a causal explanation.

## Evidence and composition

The intended verdicts are `supported`, `violated`, and `unresolved`. Missing evidence remains unresolved. Evidence contracts describe support and violation criteria and require attributable evidence; benchmark gold must never be used by runtime assessment. These contracts do not imply that assessors are implemented.

No universal sample-size cutoff, confidence threshold, or scoring weight is introduced. Structural cardinalities, such as requiring two variables for correlation, describe the operation's arguments rather than statistical adequacy. Method-dependent assumptions require explicit assessment in a future implementation.

Inheritance shares requirements; it does not specify execution order. Joint requested goals use `all_of`; explicitly accepted alternatives use `any_of`. Competing interpretations remain ambiguous rather than being silently treated as accepted alternatives. Procedure alternatives preserve their own bindings and requirements. Multi-table and model-dependent procedures declare their input scope instead of assuming every task fits one table.

An unmapped request must be preserved for review rather than forced into a nearby label. Catalog examples are illustrative sketches, not gold annotations or complete bound requests; missing arguments must remain unresolved.

## Extending and validating

1. Define the intention, parent, required roles, examples, and exclusions. Reuse a family only when its inherited requirements apply.
2. Declare distinct procedures with their own roles, evidence requirements, input scope, and output contract.
3. Add any new predicates and requirement templates with explicit evidence semantics. Do not encode arbitrary statistical thresholds as universal requirements.
4. Keep new entries `catalog_only` until interpreter binding, grounding, evidence assessment, and relevant tests are implemented and reviewed. Changing a metadata flag is insufficient.
5. Validate references, inheritance, ownership, and capability boundaries with the loader and run the test suite:

```sh
python -m unittest discover -s tests -v
```

The library tests cover inventory, prediction alternatives, causal distinctions, legacy compatibility, malformed catalogs, unsupported-action handling, and offline inspection. They establish software consistency, not scientific validity or completeness.

## Conceptual references

[Brehmer and Munzner's multi-level task typology](https://www.cs.ubc.ca/labs/imager/tr/2013/MultiLevelTaskTypology/) and [Amar, Eagan, and Stasko's low-level analytic tasks](https://sites.cc.gatech.edu/gvu/ii/vistasks/) provide conceptual precedents for describing analytical intention. The expanded library is a project-specific proposal; these references do not validate its complete inventory or evidence contracts.
