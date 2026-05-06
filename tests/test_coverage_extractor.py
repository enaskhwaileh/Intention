import pandas as pd

from intention_capability.extractors.coverage import CoverageExtractor
from intention_capability.extractors.structural import StructuralExtractor


def test_coverage_extractor_summarizes_categorical_numeric_and_geo_columns():
    df = pd.DataFrame(
        {
            "country": ["Italy", "France", "Italy"],
            "mild_rate": [0.1, 0.2, 0.3],
        }
    )
    structural = StructuralExtractor().extract(df)

    profile = CoverageExtractor().extract(df, structural=structural)

    assert profile.categorical_coverage["country"] == 2
    assert profile.numeric_ranges["mild_rate"] == {"min": 0.1, "max": 0.3}
    assert "country" in profile.geographic_columns
