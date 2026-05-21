import yaml

from intention.interpretation.validator import validate_profile
from intention.schemas.profile import OperationalProfile


def test_validate_profile_accepts_valid_profile():
    rules = yaml.safe_load(
        """
        required_fields: [input_id, intention_id, profile_type, entities]
        min_confidence: 0.25
        allowed_profile_types: [analytical]
        """
    )
    profile = OperationalProfile(
        input_id="q1",
        intention_id="analyze_sales",
        profile_type="analytical",
        entities=["sales"],
        confidence=0.8,
    )

    assert validate_profile(profile, rules)["valid"] is True
