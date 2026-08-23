# Action taxonomy

The canonical registry supports five intended actions.

| Action | Operational interpretation | Required arguments | Scientific boundary |
| --- | --- | --- | --- |
| compare | Compare an observable measure across groups | measure, comparison dimension | Requires compatible observations; relevance alone is insufficient |
| aggregate | Aggregate an observable measure, optionally by groups | measure | Does not imply that every measure is statistically aggregatable |
| predict | Assess whether observations can support predictive modelling | outcome, observational unit | Makes no model-accuracy claim |
| explain | Explore factors associated with an observed outcome | outcome | Does not establish causality |
| monitor | Track a measure or event through repeated observations | measure, temporal granularity | Requires observable time and repetition |

Aliases, ambiguity resolution, and argument extraction belong to Phase 4 and
are not implemented yet. Registry definitions are versioned in
`configs/actions.yaml`.
