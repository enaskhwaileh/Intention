# Ten-day completion plan

This plan preserves the deterministic checkpoint while turning it into a
reviewable paper and reproducibility package. Architectural or scoring changes
should occur only after the corresponding research decision is recorded.

## Day 1: checkpoint and scope

- Preserve and push the deterministic MVP on `mvp-restart`.
- Freeze the verified claim and list claims that are not yet supported.
- Define the target venue, format constraints, authors, and review workflow.
- Exit criterion: reproducible checkpoint plus an agreed one-paragraph research
  question and contribution statement.

## Day 2: literature map

- Search dataset discovery, task-aware retrieval, query intent, data
  affordances, explainable ranking, and dataset recommendation.
- Maintain a source table with claim, method, evidence, and relationship to this
  work.
- Exit criterion: categorized bibliography and a defensible related-work gap.

## Day 3: method specification

- Define the input/output contract and notation for actions, requirements,
  capabilities, matches, gates, scores, and explanations.
- Mark every manual, configured, automatic, and future component.
- Exit criterion: method section draft consistent with executable behavior.

## Day 4: evaluation protocol

- Select research questions, baselines, metrics, domains, actions, and candidate
  sets.
- Specify annotation, adjudication, and reproducibility procedures.
- Predefine ablations and parameter-sensitivity checks.
- Exit criterion: experiment protocol that can falsify or qualify the claims.

## Days 5 and 6: implementation and experiments

- Add evaluation data and scripts without changing checkpoint behavior.
- Run relevance-only and selected task-aware baselines.
- Record environment, commands, seeds where applicable, raw outputs, and
  failures.
- Exit criterion: reproducible result artifacts and a complete experiment log.

## Day 7: analysis

- Produce main results, ablations, sensitivity analysis, and error cases.
- Separate observed evidence from interpretation.
- Exit criterion: reviewed tables/figures with traceable source artifacts.

## Day 8: full manuscript

- Draft abstract, introduction, related work, method, evaluation, results,
  limitations, ethics, and conclusion.
- Exit criterion: complete paper with no placeholder sections.

## Day 9: internal review

- Audit every claim against code, results, or citations.
- Improve figures, terminology, and explanation examples.
- Run an independent reproducibility pass from documented commands.
- Exit criterion: resolved critical review comments and clean checks.

## Day 10: release candidate

- Finalize manuscript formatting and supplementary material.
- Verify repository tree, licensing, data handling, and credential hygiene.
- Tag or otherwise identify the exact code revision supporting the paper.
- Exit criterion: submission-ready paper and reproducibility package.

## Daily operating rules

- Keep the manuscript, code, and reported results synchronized.
- Commit small, reviewable changes; do not overwrite raw experiment outputs.
- Record design decisions before changing the method or scoring behavior.
- Treat the current fixture result as a demonstration until broader evidence is
  collected.
- End each day with tests, a Git status check, and a written next-day handoff.
