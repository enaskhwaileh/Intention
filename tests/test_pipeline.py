from pathlib import Path

import pandas as pd

from intention_capability.models import CapabilityProfile
from intention_capability.pipeline import CapabilityExtractionPipeline


TOY_DIR = Path(__file__).resolve().parents[1] / "data" / "toy"


def test_pipeline_returns_capability_profile():
    df = pd.read_csv(TOY_DIR / "aggregated_vaccine_side_effects.csv")

    profile = CapabilityExtractionPipeline().run(
        df,
        table_id="aggregated_vaccine_side_effects",
        table_name="Aggregated vaccine side effects by country and brand",
    )

    assert isinstance(profile, CapabilityProfile)
    assert profile.table_id == "aggregated_vaccine_side_effects"


def test_action_affordance_strong_compare_and_aggregate_for_aggregated_table():
    df = pd.read_csv(TOY_DIR / "aggregated_vaccine_side_effects.csv")

    profile = CapabilityExtractionPipeline().run(
        df,
        table_id="aggregated_vaccine_side_effects",
        table_name="Aggregated vaccine side effects by country and brand",
    )

    assert profile.action_affordance.compare == "strong"
    assert profile.action_affordance.aggregate == "strong"


def test_action_affordance_predict_possible_or_strong_for_patient_table():
    df = pd.read_csv(TOY_DIR / "patient_adverse_events.csv")

    profile = CapabilityExtractionPipeline().run(
        df,
        table_id="patient_adverse_events",
        table_name="Patient adverse events",
    )

    assert profile.action_affordance.predict in {"possible", "strong"}
