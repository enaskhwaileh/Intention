# Paper outline

## Working title

Intended-Action Grounding for Dataset Discovery

## Abstract

- Problem: topical relevance does not fully determine whether a dataset is
  useful for a downstream action.
- Proposed idea: ground intended actions into operational requirements and
  align them with evidence-backed dataset capabilities.
- Method summary, evaluation setting, principal results, and limitations.
- Do not report performance claims until supported by completed experiments.

## 1. Introduction

- Motivate the gap between topic matching and action suitability.
- Provide a concrete compare-versus-predict example.
- State the research question and scoped contributions.
- Distinguish the executable proof of concept from validated generality.

## 2. Related work

- Dataset search and discovery.
- Query intent and task-aware information retrieval.
- Dataset recommendation and data-product selection.
- Data profiling, metadata extraction, and semantic matching.
- Explainable and constrained ranking.

## 3. Problem formulation

- Define query profile, intended action, operational requirement, dataset
  capability, evidence/provenance, and action-conditioned usefulness.
- Specify inputs, outputs, assumptions, and failure cases.
- Define the distinction between topical relevance and operational alignment.

## 4. Method

- Action grounding and argument representation.
- Requirement-profile construction and validation.
- Capability-profile construction and validation.
- Requirement-capability matching.
- Required-evidence handling and ranking.
- Provenance-grounded explanation generation.
- Clearly identify which components are manual in the evaluated system.

## 5. Current deterministic instantiation

- Vaccine-side-effects scenario and four candidate tables.
- Compare and predict action templates.
- Transparent matching rules and configuration.
- Demonstration rankings and explanation traces.
- State that provisional axes and fixed weights are MVP choices, not settled
  theory or calibrated parameters.

## 6. Evaluation

- Research questions.
- Datasets, domains, actions, queries, and candidate pools.
- Annotation and adjudication protocol.
- Baselines.
- Ranking, robustness, explanation, and efficiency metrics.
- Reproducibility procedure.

## 7. Results

- Main action-conditioned ranking results.
- Comparison with topical relevance and other baselines.
- Ablation study.
- Weight and threshold sensitivity.
- Qualitative explanations and failure analysis.

## 8. Discussion

- Interpretation of supported findings.
- Generalizability and dependence on metadata quality.
- Manual authoring versus automated components.
- Implications for dataset-search interfaces.

## 9. Limitations and responsible use

- Scope and representativeness of evaluation.
- Subjectivity in action requirements and capability judgments.
- Bias, uncertainty, provenance quality, and possible ranking harms.
- Boundaries of deterministic and LLM-assisted implementations.

## 10. Conclusion

- Restate the supported contribution without exceeding the evidence.
- Identify the next empirical and implementation steps.

## Reproducibility appendix

- Repository revision and environment.
- Exact commands.
- Configuration and fixture descriptions.
- Full results, additional ablations, and known deviations.
