# Experimental protocol status

No paper experiment has been run. The preserved vaccine fixture is a regression
demonstration and not independent validation.

The future protocol must distinguish candidate retrieval, reranking within a
fixed pool, and end-to-end performance. It must compare topical and full-input
BM25, available approved neural retrieval, simple schema filtering, the
action-grounded reranker, and oracle action/requirement variants. Unavailable
systems must be labeled unavailable rather than implemented.

Ground truth must be independently judged and must not replay the evaluated
rules. Development and test topics must be separated. Report actual metrics,
uncertainty, disagreements, exclusions, and failure cases only after measured.
