import pandas as pd

from intention_capability.extractors.quality import QualityExtractor


def test_quality_extractor_computes_missingness_and_duplicate_rate():
    df = pd.DataFrame(
        {
            "country": ["Italy", "Italy", None, ""],
            "rate": [0.1, 0.1, 0.2, 0.3],
        }
    )

    profile = QualityExtractor().extract(df)

    assert profile.missing_rate_per_column["country"] == 0.25
    assert profile.duplicate_row_rate == 0.25
    assert profile.empty_string_rate_per_column["country"] == 0.25
