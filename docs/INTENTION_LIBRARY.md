# Intention Library 1.0.0

Status: development; review: author_specified_unreviewed. Generated from `intention_grounding/library/intention-library-v1.0.json` by `python -m intention_grounding.il`.

## Assessment axes

- **sem**: Concept meaning: the bound attributes denote the requested concepts with compatible definitions.
- **str**: Table structure and observational unit: rows, keys, groupings and their association.
- **cov**: Scope and group coverage: the requested scope, groups and periods are present.
- **qual**: Data quality: completeness and validity of the bound values.
- **aff**: Affordance: the intermediate quantities required by the procedure can be obtained.

## Extraction vocabulary

| Label | Meaning |
|---|---|
| `measure` | A quantity the user wants to analyse (e.g. vaccination rate, wage). |
| `second_measure` | A second quantity related to the first (e.g. in an association). |
| `group_dimension` | The attribute along which observations are compared or grouped (e.g. country, age group). |
| `groups` | Explicitly named groups or entities (e.g. Germany, France; men, women). |
| `statistic` | An explicitly requested summary (e.g. mean, total, documented values). |
| `target` | The outcome to be predicted. |
| `predictor` | An attribute proposed as input to a prediction or explanation. |
| `time_dimension` | An explicit reference to time as an axis (e.g. over time, by month). |
| `time_grain` | An explicit observation grain (e.g. daily, weekly, yearly). |
| `time_points` | Explicit dates or periods to be contrasted. |
| `subject` | The entity whose values are of interest when no comparison dimension is given. |
| `unassigned` | Relevant wording retained without a confident role. |
| scope `geography` | Geographic restriction (e.g. in Europe). |
| scope `period` | Temporal restriction (e.g. in 2021, between 2011 and 2012). |
| scope `population` | Restriction on the observed population (e.g. adults, women). |
| scope `condition` | Any other selection condition. |

## Families, variants and procedures

### compare

Descriptively contrast a measure across groups, entities or time points.

#### `compare.group_means`

Comparable arithmetic means of measure m for each group of dimension g within scope.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| measure | measure | yes | 1..1 | – |
| group_dimension | group_dimension | yes | 1..1 | – |
| statistic | statistic | yes | 1..1 | mean, average, arithmetic mean, avg, mean of, on average |
| groups | groups | no | 2..n | – |

**Procedure `means.raw`**: `Mean_m . Group_g . Filter_F` — Pairs (group, mean of m). Applicability: `{"rule": "excluded_if_statistic_mentions", "terms": ["reported", "documented", "published", "stored", "official"]}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `compare.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The comparison outcome is defined for the requested measure. |
| `compare.common.group_concept` | hard | intention | sem | `concept_bound(concept=$group_dimension, slot=group, kind=dimension, values=$groups)` | binding | Groups are defined by the requested comparison dimension. |
| `compare.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Filter's selection contract: observations within the requested scope are identifiable. |
| `compare.common.comparable` | hard | intention | sem | `single_definition(slot=measure)` | binding | Group results use one measure definition and unit. |
| `means.raw.observation` | hard | Mean | str | `observation_level(slot=measure)` | measure_kind | Mean input contract: each contributing value is an observation, not an existing summary (rate, mean or cumulative total). |
| `means.raw.membership` | hard | Group | str | `categorical_membership(slot=group)` | profile | Selected observations carry a discrete group membership. |
| `means.raw.association` | hard | composition | str | `co_located(slots=['measure', 'group'])` | profile | Measure and group refer to the same row (Filter-Group-Mean dependency). |
| `means.raw.valid` | hard | Mean | aff | `valid_per_group(slot=measure, group_slot=group, groups=$groups, min_valid=1)` | scoped_counts | A defined arithmetic mean requires a nonempty set of valid numerical inputs for every included group. |
| `compare.common.groups` | hard | intention | cov | `groups_covered(slot=group, groups=$groups, min_groups=2, valid_slot=measure)` | scoped_counts | At least two groups have results, including every explicitly requested group. |
| `means.raw.completeness` | soft | Mean | qual | `completeness(slot=measure)` | profile | Valid-value completeness of the measure. |
| `common.size` | soft | intention | qual | `size_indicator(slot=measure, reference_rows=1000)` | profile | More valid observations give more stable summaries (saturating). |

**Procedure `means.stored`**: `Project_{g,m} . Filter_F` — Pairs (group, documented mean of m). Applicability: `{"rule": "excluded_if_statistic_mentions", "terms": ["raw", "individual", "observations", "records", "compute from"]}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `compare.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The comparison outcome is defined for the requested measure. |
| `compare.common.group_concept` | hard | intention | sem | `concept_bound(concept=$group_dimension, slot=group, kind=dimension, values=$groups)` | binding | Groups are defined by the requested comparison dimension. |
| `compare.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Filter's selection contract: observations within the requested scope are identifiable. |
| `compare.common.comparable` | hard | intention | sem | `single_definition(slot=measure)` | binding | Group results use one measure definition and unit. |
| `means.stored.summary` | hard | Project | aff | `summary_kind(slot=measure, kinds=['mean'])` | measure_kind | Selected values are documented arithmetic means of the measure. |
| `means.stored.association` | hard | composition | str | `co_located(slots=['measure', 'group'])` | profile | Each documented mean is linked to its group. |
| `means.stored.valid` | hard | Project | aff | `valid_per_group(slot=measure, group_slot=group, groups=$groups, min_valid=1)` | scoped_counts | Each included group has a documented mean. |
| `compare.common.groups` | hard | intention | cov | `groups_covered(slot=group, groups=$groups, min_groups=2, valid_slot=measure)` | scoped_counts | At least two groups have results, including every explicitly requested group. |
| `means.stored.completeness` | soft | Project | qual | `completeness(slot=measure)` | profile | Completeness of documented summaries. |

#### `compare.observed_values`

One documented value of measure m for each requested entity or time point, or for each observed group of dimension g when no groups are named.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| measure | measure | yes | 1..1 | – |
| groups | groups, time_points | no | 2..n | – |
| group_dimension | group_dimension | no | 1..1 | – |
| statistic | statistic | no | 1..1 | documented, reported, recorded, observed, value, values, level |

At least one of: groups / group_dimension.

**Procedure `values.lookup`**: `Lookup_{m,G} . Filter_F` — Pairs (requested key, documented value of m). Applicability: `{"rule": "always"}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `compare.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The comparison outcome is defined for the requested measure. |
| `compare.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Filter's selection contract: observations within the requested scope are identifiable. |
| `compare.common.comparable` | hard | intention | sem | `single_definition(slot=measure)` | binding | Group results use one measure definition and unit. |
| `values.lookup.keys` | hard | Lookup | str | `keys_bound(groups=$groups, dimension=$group_dimension)` | scoped_values | Requested entities or time points are identifiable through a key attribute. |
| `values.lookup.present` | hard | intention | cov | `keys_present(groups=$groups)` | scoped_counts | Every requested key occurs in scope. |
| `values.lookup.valid` | hard | Lookup | aff | `valid_per_key(slot=measure, groups=$groups)` | scoped_counts | Every requested key has a valid value of the measure. |
| `values.lookup.unique` | soft | Lookup | str | `unique_per_key(slot=measure, groups=$groups)` | scoped_counts | One value per key; multiple rows require an explicit selection rule. |

### aggregate

Combine observations of a measure into totals for the requested scope or groups.

#### `aggregate.group_totals`

The total of an additive measure m for the scope, or for each group of dimension g.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| measure | measure | yes | 1..1 | – |
| statistic | statistic | yes | 1..1 | total, sum, number, count, how many, overall, combined, aggregate |
| group_dimension | group_dimension | no | 1..1 | – |
| groups | groups | no | 1..n | – |

**Procedure `totals.raw`**: `Sum_m . Group_g . Filter_F` — Pairs (group, total of m), or one total for the scope. Applicability: `{"rule": "excluded_if_statistic_mentions", "terms": ["reported", "documented", "published", "official"]}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `aggregate.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The total is defined for the requested measure. |
| `aggregate.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Observations within the requested scope are identifiable. |
| `totals.raw.additive` | hard | Sum | aff | `additive_measure(slot=measure)` | measure_kind | Sum requires values that add over rows: counts or amounts, not rates, means or cumulative totals. |
| `totals.raw.grouping` | hard | Group | str | `optional_grouping(concept=$group_dimension, groups=$groups)` | binding | When a grouping is requested, rows carry that membership. |
| `totals.raw.valid` | hard | Sum | aff | `valid_per_group(slot=measure, group_slot=group, groups=$groups, min_valid=1, group_optional=True)` | scoped_counts | Every included group has at least one valid value. |
| `totals.raw.completeness` | soft | Sum | qual | `completeness(slot=measure)` | profile | Missing values bias totals downward. |
| `common.size` | soft | intention | qual | `size_indicator(slot=measure, reference_rows=1000)` | profile | More valid observations give more stable summaries (saturating). |

**Procedure `totals.stored`**: `Project_{g,m} . Filter_F` — Pairs (group, documented total of m). Applicability: `{"rule": "excluded_if_statistic_mentions", "terms": ["raw", "individual", "records", "compute from"]}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `aggregate.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The total is defined for the requested measure. |
| `aggregate.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Observations within the requested scope are identifiable. |
| `totals.stored.summary` | hard | Project | aff | `summary_kind(slot=measure, kinds=['total', 'cumulative'])` | measure_kind | Selected values are documented totals. |
| `totals.stored.grouping` | hard | Project | str | `optional_grouping(concept=$group_dimension, groups=$groups)` | binding | Documented totals are linked to the requested grouping. |
| `totals.stored.valid` | hard | Project | aff | `valid_per_group(slot=measure, group_slot=group, groups=$groups, min_valid=1, group_optional=True)` | scoped_counts | Each included group has a documented total. |

### predict

Learn a model that predicts an outcome for unseen observations.

#### `predict.classification`

A model assigning a categorical outcome y to individual observations from features X.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| target | target, measure | yes | 1..1 | – |
| predictor | predictor, group_dimension, second_measure | no | 1..n | – |

**Procedure `learn.classifier`**: `Fit_{y,X} . Filter_F` — A fitted classifier for y. Applicability: `{"rule": "always"}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `predict.common.target` | hard | intention | sem | `concept_bound(concept=$target, slot=target)` | binding | The outcome to be predicted is an attribute of the table. |
| `predict.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Training observations within the requested scope are identifiable. |
| `classifier.target_categorical` | hard | Fit | aff | `target_type(slot=target, type=categorical)` | profile | Classification requires a discrete outcome with a small number of classes. |
| `predict.common.observation` | hard | Fit | str | `row_level_target(slot=target)` | measure_kind | Each row is one observation with its own outcome, not an aggregate or rate over many units. |
| `predict.common.features` | hard | Fit | str | `features_available(slot=target, predictors=$predictor, min_features=2)` | profile | Attributes other than the outcome (and identifiers) are available as features. |
| `classifier.label_variation` | hard | Fit | aff | `label_variation(slot=target, min_per_class=5)` | profile | At least two classes are observed with enough examples each. |
| `predict.common.labelled` | hard | Fit | aff | `min_valid_rows(slot=target, min_rows=30)` | profile | Fitting requires a nonempty training set; 30 labelled rows is the declared minimum of this release. |
| `predict.common.feature_completeness` | soft | Fit | qual | `feature_completeness(slot=target)` | profile | Mean valid-value fraction over candidate features. |
| `classifier.balance` | soft | Fit | qual | `class_balance(slot=target)` | profile | Normalised entropy of the class distribution. |
| `predict.common.size` | soft | Fit | qual | `size_indicator(slot=target, reference_rows=1000)` | profile | More labelled rows support more reliable fitting (saturating at the reference size). |

#### `predict.regression`

A model estimating a numerical outcome y for individual observations from features X.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| target | target, measure | yes | 1..1 | – |
| predictor | predictor, group_dimension, second_measure | no | 1..n | – |

**Procedure `learn.regressor`**: `Fit_{y,X} . Filter_F` — A fitted regressor for y. Applicability: `{"rule": "always"}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `predict.common.target` | hard | intention | sem | `concept_bound(concept=$target, slot=target)` | binding | The outcome to be predicted is an attribute of the table. |
| `predict.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Training observations within the requested scope are identifiable. |
| `regressor.target_numeric` | hard | Fit | aff | `target_type(slot=target, type=numeric)` | profile | Regression requires a numerical outcome. |
| `predict.common.observation` | hard | Fit | str | `row_level_target(slot=target)` | measure_kind | Each row is one observation with its own outcome, not an aggregate or rate over many units. |
| `predict.common.features` | hard | Fit | str | `features_available(slot=target, predictors=$predictor, min_features=2)` | profile | Attributes other than the outcome (and identifiers) are available as features. |
| `regressor.target_variation` | hard | Fit | aff | `numeric_variation(slot=target)` | profile | The outcome takes more than one value. |
| `predict.common.labelled` | hard | Fit | aff | `min_valid_rows(slot=target, min_rows=30)` | profile | Fitting requires a nonempty training set; 30 labelled rows is the declared minimum of this release. |
| `predict.common.feature_completeness` | soft | Fit | qual | `feature_completeness(slot=target)` | profile | Mean valid-value fraction over candidate features. |
| `predict.common.size` | soft | Fit | qual | `size_indicator(slot=target, reference_rows=1000)` | profile | More labelled rows support more reliable fitting (saturating at the reference size). |

### explain

Describe how two attributes vary together, as a basis for explaining an outcome.

#### `explain.association`

A description of how measure m varies with attribute a over co-observed rows.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| measure | measure, target | yes | 1..1 | – |
| predictor | predictor, second_measure, group_dimension | yes | 1..n | – |

**Procedure `assoc.pairwise`**: `Associate_{m,a} . Filter_F` — Association statistics between m and each bound a. Applicability: `{"rule": "always"}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `explain.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The explained quantity is an attribute of the table. |
| `explain.common.partner` | hard | intention | sem | `concept_bound(concept=$predictor, slot=partner, kind=any)` | binding | The explanatory attribute is an attribute of the same table. |
| `explain.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Observations within the requested scope are identifiable. |
| `assoc.numeric_outcome` | hard | Associate | aff | `numeric_measure(slot=measure)` | profile | The explained quantity is numerical or binary. |
| `assoc.co_observed` | hard | Associate | str | `co_observed(slots=['measure', 'partner'], min_rows=10)` | profile | Both attributes are observed together on enough rows. |
| `assoc.variation` | hard | Associate | aff | `both_vary(slots=['measure', 'partner'])` | profile | An association is undefined for a constant attribute. |
| `assoc.completeness` | soft | Associate | qual | `completeness(slot=measure)` | profile | Pairwise completeness. |
| `common.size` | soft | intention | qual | `size_indicator(slot=measure, reference_rows=1000)` | profile | More valid observations give more stable summaries (saturating). |

### monitor

Follow a measure over time for the requested subject or scope.

#### `monitor.trend`

The ordered series of measure m over time for the requested subject or scope.

| Role | Labels | Required | Cardinality | Admissible |
|---|---|---|---|---|
| measure | measure | yes | 1..1 | – |
| time_dimension | time_dimension | no | 1..1 | – |
| time_grain | time_grain | no | 1..1 | – |
| groups | groups, subject | no | 1..n | – |

**Procedure `series.raw`**: `Order_t . Filter_F` — Time-ordered values of m for the scope or each requested subject. Applicability: `{"rule": "always"}`.

| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |
|---|---|---|---|---|---|---|
| `monitor.common.concept` | hard | intention | sem | `concept_bound(concept=$measure, slot=measure)` | binding | The monitored quantity is an attribute of the table. |
| `monitor.common.scope` | hard | Filter | cov | `scope_satisfiable(scope=$scope)` | scoped_values | Observations within the requested scope are identifiable. |
| `series.time` | hard | Order | str | `time_bound(slot=time)` | profile | A parseable time attribute orders the observations. |
| `series.numeric` | hard | Order | aff | `numeric_measure(slot=measure)` | profile | The monitored values are numerical. |
| `series.subjects` | hard | intention | cov | `keys_present(groups=$groups, optional=True)` | scoped_counts | Every requested subject occurs in scope. |
| `series.length` | hard | Order | aff | `distinct_times(slot=time, min_points=3)` | scoped_counts | A trend requires at least three distinct time points in scope. |
| `series.grain` | soft | intention | str | `grain_compatible(slot=time, grain=$time_grain)` | profile | The observed grain is at least as fine as the requested grain. |
| `series.completeness` | soft | Order | qual | `completeness(slot=measure)` | profile | Missing values interrupt the series. |

## Operators

| Operator | Inputs | Outputs | Preconditions | Missing values |
|---|---|---|---|---|
| Filter | rows | rows | Every scope restriction is evaluable on the rows. | Rows whose scope attribute is missing are excluded and counted. |
| Group | rows | groups of rows | Rows carry a membership value for g. | Rows with missing g are excluded and counted. |
| Mean | numeric values per group | one mean per group | Values are numeric observations on a meaningful arithmetic scale. At least one valid value per group. | Available-case: declared missing values are excluded. |
| Sum | numeric values per group | one total per group | Values are additive over rows (not rates, means or cumulative totals). | Missing values are excluded and counted; no imputation. |
| Project | rows | selected attributes | Selected attributes exist. | Missing documented values remain missing. |
| Lookup | rows | one value per requested key | Exactly one valid value per requested key in scope. | A missing value makes the key unresolved; duplicates are not aggregated. |
| Order | rows | rows ordered by time | A parseable time attribute. | Rows with missing time are excluded and counted. |
| Fit | labelled rows (X, y) | a fitted model | Each row is one observation with an outcome label. The outcome varies. Features other than y exist. | Rows with missing y are excluded; feature missingness is reported. |
| Associate | co-observed pairs (m, a) | an association statistic | Both attributes are observed on the same rows and vary. | Pairwise-complete rows. |

## Evidence rules

- **binding**: A slot is bound when the Aligner's binder links the requested concept to an attribute through documented descriptions, attribute names or attribute values, with a recorded match score at or above the release threshold. No binding yields unresolved; absence of a concept is never treated as violation.
- **scoped_values**: Scope restrictions are matched against full-scan attribute values, documented table scope (title/description), or a declared membership mapping (geography gazetteer). Supported when every restriction is satisfiable; violated when the restriction's attribute is bound and a full scan shows no member; unresolved otherwise.
- **scoped_counts**: Counts over a full scan of the scoped rows. Positive counts establish support; zero counts establish violation only after an exhaustive scan.
- **measure_kind**: The measure kind (count, amount, level, rate, mean, cumulative, proportion) is read from the documentation and name by declared keyword rules; undocumented kinds are unresolved.
- **profile**: Values computed by the Table Profiler on the full table (types, distinct counts, missingness, ranges).

## Expression index

*compare* → compare, *comparison* → compare, *contrast* → compare, *versus* → compare, *vs* → compare, *difference between* → compare, *differ* → compare, *higher* → compare, *lower* → compare, *total* → aggregate, *sum* → aggregate, *how many* → aggregate, *aggregate* → aggregate, *add up* → aggregate, *predict* → predict, *prediction* → predict, *forecast* → predict, *classify* → predict, *model* → predict, *estimate whether* → predict, *explain* → explain, *relationship* → explain, *relate* → explain, *association* → explain, *associated* → explain, *correlate* → explain, *correlation* → explain, *affect* → explain, *influence* → explain, *depend* → explain, *track* → monitor, *monitor* → monitor, *trend* → monitor, *over time* → monitor, *evolve* → monitor, *evolution* → monitor, *change over* → monitor, *follow* → monitor, *how has* → monitor, *how have* → monitor, *changed* → monitor, *what drives* → explain, *related* → explain

## Release log

- 1.0.0: First release of the Intention Library (replaces the earlier Action Base). Structure follows L = (J, O, P, R, E, v): families and variants, operator contracts, procedure templates, requirement records, expression index and release.
- Seven variants over five families (compare, aggregate, predict, explain, monitor); nine procedures; 55 requirement records over the axes sem, str, cov, qual, aff.
- compare.observed_values: groups optional when a group dimension is given (documented default: all observed groups).

