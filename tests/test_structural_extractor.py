import pandas as pd

from intention_capability.extractors.structural import StructuralExtractor


def test_structural_extractor_detects_numeric_and_categorical_columns():
    df = pd.DataFrame(
        {
            "country": ["Italy", "France", "Italy"],
            "brand": ["Pfizer", "Moderna", "Pfizer"],
            "mild_rate": [0.1, 0.2, 0.3],
        }
    )

    profile = StructuralExtractor().extract(df)

    assert "mild_rate" in profile.numeric_columns
    assert "country" in profile.categorical_columns
    assert "brand" in profile.grouping_candidates
    assert "mild_rate" in profile.measure_candidates
