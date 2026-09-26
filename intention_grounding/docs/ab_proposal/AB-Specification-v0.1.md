# Action Base v0.1 — Compare branch

Status: proposed research specification, 26 September 2026. This is a reviewable seed AB, not an empirically validated taxonomy or a deployed grounder. The canonical draft lives in `intention_grounding/docs/ab_proposal/`; runtime AB files under `intention_grounding/kb/` are unchanged. No LLM execution or retrieval experiment is claimed.

## 1. Scope and component contract

The Action Base (AB) is a versioned catalogue of action definitions, selection rules, typed arguments, and table-requirement templates. The interpreter extracts a query profile and action expressions with arguments and exact source spans. The grounder selects a supported AB action, binds arguments, expands inherited templates, and validates the resulting requirement card. The aligner evaluates the card against table-profile evidence.

The AB does not contain user-specific country names or dates as new action classes. Those are runtime bindings. It also does not contain table-satisfaction results.

v0.1 covers descriptive comparison of an already available numerical measure in one table. It admits long or wide representations if the profiler can expose the same logical observation relation. Aggregation, interpolation, joins, conversion, statistical inference, causal claims, and derived rates are outside this first operational route. Their absence means unsupported by this route, not intrinsically useless data. This restriction must be reported in evaluation and relaxed through explicit future transformation routes.

The inventory is deliberately not labelled a complete set of seven actions. Other families remain unimplemented.

## 2. Four action nodes

| ID | Parent | Meaning | Selection evidence |
| --- | --- | --- | --- |
| compare | — | Contrast comparable observations of the same numerical measure; abstract in v0.1 | Comparison goal, without enough detail to choose a supported specialization |
| compare.groups | compare | Contrast a measure across at least two specified groups | Explicit groups and measure |
| compare.groups.trajectories | compare.groups | Contrast how that measure changes over time across groups | Group comparison plus explicit temporal trajectory/change comparison |
| compare.time | compare | Contrast one subject's measure across at least two specified time points | One subject and explicit cross-time comparison |

A time filter alone does not select trajectories. “Compare annual rates in France and Spain in 2020” selects compare.groups with a one-year scope. “Compare how rates changed in France and Spain from 2019 to 2021” can select trajectories, but unspecified cadence remains unresolved in this seed implementation. Do not infer a trend model or causal analysis from “change.”

Hierarchy means specialization, not execution order. Aggregate-then-compare is a composition, not another inheritance edge. Parent requirements are inherited unchanged; children add requirements. Requirement replacement is prohibited in v0.1. Contradictory bindings return inconsistent_input rather than being silently overridden.

## 3. Input requirements

Each extracted value carries a half-open Unicode code-point span [start,end) into the exact stored input, or a reference to authorized external context. Validate input[start:end] == source_text. Normalizations need a rule identifier and original value. Missing values are explicit, not fabricated.

Required binding roles depend on the selected node. compare.groups requires measure, group_dimension, and at least two distinct groups. compare.groups.trajectories adds at least two time points and a time grain. compare.time requires measure, subject, time points, and time grain. Topic and entity normalization are not assumed solved by the AB.

For an unspecified year range cadence or population definition, retain the distinction between an unresolved user argument and missing table evidence. A missing cadence can prevent template instantiation; unknown population comparability can instead produce a grounded card whose later alignment remains unknown.

## 4. Predicate registry and axis semantics

| Predicate | Axis | Evaluation contract |
| --- | --- | --- |
| measure_semantics | sem | Bound measure variable represents the requested concept, with provenance supporting the mapping |
| observation_binding | str | A consistent logical observation relation binds measure to every supplied subject/group/time role; unrelated columns cannot satisfy this |
| group_coverage | cov | Every requested group has at least one observation in the bound relation and requested context |
| time_coverage | cov | Every requested time point has an observation at the requested grain, within supplied subject/group scope |
| paired_temporal_support | str | At least two distinct shared time points have observations for every requested group under the same bindings and grain |
| complete_requested_grid | cov | Every explicitly requested group × time cell is represented; activated only by explicit exhaustive coverage |
| usable_numeric_observations | qual | Required comparison observations have finite usable numerical values; unresolved conflicting duplicates cannot establish satisfaction |
| comparable_measure_definition | aff | Evidence supports compatible units, measure definitions, and applicable population/denominator definitions across the compared observations |

All predicates use one shared logical measure variable m and observation relation o within each action instance. The profiler must support relational evidence, not just a bag of independent column properties. Column names alone cannot prove units or denominator equivalence.

Evidence interface: each profile claim records predicate/fact ID, role bindings, value, provenance, extraction method, scope, and completeness of inspection. Unknown is returned if evidence is insufficient. Sampling can establish witnessed presence; non-observation in a sample cannot establish absence from the full table.

Affordance is a derived evidence check, not an independent opaque “comparison-ready” score. Its evidence dependencies must be retained to avoid double counting in any future scoring scheme. No axis weights or similarity thresholds are fixed by this version.

## 5. Requirement representation

A requirement contains ID, originating action instance, predicate ID, axis, bound arguments, required/preferred/forbidden modality, table scope, and provenance. v0.1 concrete examples use required conditions only. No arbitrary quality thresholds are inserted.

Required predicates are combined with all_of. Future supported alternatives must use explicit any_of branches with preserved bindings. A forbidden predicate is evaluated by the same evidence rules: unknown does not mean safely absent.

For all_of: any violated requirement yields violated; all satisfied yields satisfied; otherwise unknown. For any_of: any satisfied branch yields satisfied; all violated yields violated; otherwise unknown. A contradictory profile should be reported as a data/validation error or unresolved conflict, not silently averaged away.

The grounder never writes satisfied/violated/unknown table judgments into its card. Those belong to alignment. It returns status grounded, ambiguous, insufficient_input, unsupported, or inconsistent_input. A partially identified parent is preserved as a candidate, not passed off as a fully grounded actionable card.

## 6. Template instantiation

1. Validate interpreter provenance, schema, and explicit unresolved items.
2. Select the most specific supported action justified by the request; a child must satisfy its parent's meaning too.
3. Verify required arguments and minimum cardinalities; preserve uncertainty.
4. Gather ancestor and local requirement IDs, without duplicate IDs.
5. Activate conditional requirements only from their declared trigger.
6. Bind action roles and shared profile variables; attach user and AB-rule provenance.
7. Verify predicate IDs, axes, version, logic references, and absence of unresolved required bindings.
8. Return a grounded card, or a non-grounded status with reasons and candidate interpretations.

The JSON catalogue is declarative design data, not a formal parser or an executable DSL. Selection rules are controlled prose pending operationalization. The companion examples are manually constructed interpretations and template-expansion illustrations; they are not outputs of an executed grounder, model outputs, or evaluation results.

## 7. Why exhaustive coverage is conditional

“Compare unemployment rates over 2015–2024” does not necessarily require every group-year cell. Extract a phrase such as “every year” literally, retaining its exact source span. It is not the value `complete_grid` and `fixture_literal_v1` must never claim that transformation.

`derive_explicit_group_time_grid_v1` is a separate, **declarative grounding derivation**, defined in the catalogue, not an AB-M1 interpreter normalization. Inputs are resolved groups, a finite temporal domain, explicit granularity, the literal coverage expression, and its reviewed scope. All five conditions must be supported:

1. At least two distinct requested groups are resolved.
2. The temporal domain and endpoint/inclusion semantics are resolved.
3. Temporal granularity is explicit.
4. Coverage is exhaustive over that domain at that granularity.
5. That exhaustive requirement unambiguously applies to every requested group in the same action.

The output is request-specific `coverage_policy=complete_grid`. Its provenance records `source=grounding_derivation`, the versioned rule ID, binding references, evidence references for **each** condition, and explicitly manual `reviewed_conditions` annotations. Multiple or overlapping evidence spans are allowed; “every year” alone cannot establish groups, domain, or all-groups scope. The literal coverage extraction remains a separate record. The complete-grid requirement's origin retains the derivation provenance as well as its binding evidence.

The positive trajectory example now explicitly says “for each of France and Spain in every year from 2019 to 2021 inclusive” and separately says “annual”. It retains evidence for the groups, inclusive range, granularity, exhaustive phrase, and quantifier scope. A date range alone or “annual” alone never activates complete-grid coverage. If any condition is missing or ambiguous, do not derive the policy; retain missing information or competing readings. A full grid also does not assert that any table satisfies it.

`default_available_observations_v1` remains a **proposal-level system policy**, registered separately in the catalogue. Its output is `available_observations`, with `source=system_policy`; it is never user evidence and cannot repair unresolved required bindings. Trajectories still require at least two shared time points.

“Between 2019 and 2021” remains ambiguous between endpoints and an interval unless context resolves it. Neither reading supplies an implicit yearly cadence. Positive endpoint examples explicitly name annual observations and contrast 2019 versus 2021; inclusive range expansion is fixture-specific and requires explicit annual granularity and inclusive semantics. All fixture normalization rules are research annotations, separate from AB-M1's unchanged `casefold-v1` and `annual-v1`.

The offline consistency check validates references, exact spans, rule structure, and the completeness of manually annotated activation evidence. It rejects incomplete activation certificates and checks negative annotations; it does not parse natural language, decide semantic entailment, implement a grounder, or establish scientific validity.

## 8. LLM boundary

Provide candidate action definitions, argument schemas, inclusion/exclusion rules, and examples to an AB-aware resolver. Require action IDs, bindings, source spans, alternative interpretations, and missing arguments. The LLM cannot add registry entries or claim table satisfaction. A deterministic validator rejects unknown IDs, invented bindings, invalid spans, and incompatible cardinalities. Model self-confidence is not evidence calibration.

For four nodes, providing the complete branch is simpler than adding an embedding retrieval layer. If AB scale later requires candidate retrieval, measure candidate recall separately. No specific model or prompt is prescribed by this specification.

## 9. Review cases

| Request | Expected outcome |
| --- | --- |
| Compare annual unemployment rates in France and Spain in 2020. | compare.groups; one-year context does not imply trajectories |
| Compare how annual unemployment rates changed for each of France and Spain in every year from 2019 to 2021 inclusive. | compare.groups.trajectories; full-grid requirement active |
| Compare the unemployment rate in France between 2019 and 2021. | ambiguous endpoints versus interval; cadence unresolved |
| Compare the annual unemployment rate in France in 2019 versus 2021. | compare.time; two explicitly contrasted annual observations |
| Compare these datasets. | insufficient_input; measure and comparison entities unresolved |
| Compare unemployment trends in France and Spain. | candidate trajectories, but insufficient_input for this route: time points/grain unresolved |
| Is France's unemployment rate significantly higher than Spain's? | unsupported inferential comparison, not silently reduced to descriptive comparison |
| Compare annual totals computed from monthly sales. | unsupported transformation route in v0.1 |
| Compare or forecast unemployment rates; I have not decided. | ambiguous; preserve alternatives, do not interpret as user acceptance of either result |

Profile-side counterexamples: unrelated measure and time columns must fail relation binding; a sampled profile missing a group yields unknown, not violated; incompatible documented units violate comparability if no conversion route exists; no unit metadata yields unknown; national totals cannot satisfy a requested unemployment rate; raw microdata requiring aggregation are unsupported by this operational route, not universally unsuitable.

## 10. Scientific status and next review

Every action and requirement in this release is a proposed author-designed specification. Semantic concepts, population compatibility, and representation normalization still require operational definitions and annotation guidance. They cannot be established from column types alone.

Review each requirement against positive and near-miss tables, annotate independently, and record disagreement. Evaluate action selection, binding, requirement fidelity, and abstention separately. Freeze a version before held-out evaluation. Compare flat versus hierarchical AB and unconstrained versus AB-constrained requirement generation; do not assume hierarchy is better.

References carried forward from the preceding literature check provide conceptual precedents, not validation of this catalogue:

- Brehmer and Munzner (2013), A Multi-Level Typology of Abstract Visualization Tasks: goals, means, inputs/outputs, and task composition. https://www.cs.ubc.ca/labs/imager/tr/2013/MultiLevelTaskTypology/
- Amar, Eagan, and Stasko (2005), Low-Level Components of Analytic Activity in Information Visualization: empirical construction of a limited task inventory. https://perso.telecom-paristech.fr/eagan/new/media/papers/amar05.pdf
- Baker (2014), FrameNet: A Knowledge Base for Natural Language Processing: frame and argument representation. https://aclanthology.org/W14-3001/
- PDDL (1998): explicit action parameters and preconditions as a modeling precedent. https://www.cs.cmu.edu/~mmv/planning/readings/98aips-PDDL.pdf
- W3C SHACL (2017): declarative constraint validation as an engineering precedent. https://www.w3.org/TR/shacl/

No novelty or empirical performance claim follows from these references. The next substantive decision is whether the direct-observation Compare scope matches the desired benchmark, or whether aggregate-then-compare must be supported before expanding other families.
