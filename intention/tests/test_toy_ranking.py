from pathlib import Path

from intention.iekl.graph_loader import load_iekl_graph
from intention.interpretation.intention_grounder import IntentionGrounder
from intention.interpretation.profile_instantiator import ProfileInstantiator
from intention.interpretation.validator import ProfileValidator
from intention.ranking.profile_tester import ProfileTester
from intention.schemas.intention import RawIntention
from intention.schemas.table_profile import TableProfile


ROOT = Path(__file__).resolve().parents[1]


def test_compare_table_satisfying_predicates_scores_higher():
    graph = load_iekl_graph(ROOT / "resources/iekl/intention_graph.yaml")
    grounded = IntentionGrounder(graph).ground(
        RawIntention(
            intent_phrase="compare vaccines",
            candidate_intention_type="compare",
            slots={},
        )
    )
    profile = ProfileValidator(graph).validate(
        ProfileInstantiator(graph).instantiate("q2", grounded)
    )
    matching = TableProfile(
        table_id="matching",
        title="Matching compare table",
        semantic={
            "has_compared_entities": True,
            "has_grouping_variable": True,
            "has_comparable_measure": True,
        },
        structural={"has_compatible_granularity": True},
        coverage={},
        quality={},
        behavioral={},
    )
    missing = TableProfile(
        table_id="missing",
        title="Incomplete compare table",
        semantic={"has_compared_entities": True},
        structural={},
        coverage={},
        quality={},
        behavioral={},
    )
    tester = ProfileTester()

    matching_score = tester.test(profile, matching)["intention_alignment_score"]
    missing_score = tester.test(profile, missing)["intention_alignment_score"]

    assert matching_score > missing_score
