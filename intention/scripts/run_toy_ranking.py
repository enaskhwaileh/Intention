from pathlib import Path

from intention.ranking.intention_ranker import rank_tables
from intention.schemas.profile import OperationalIntentionProfile
from intention.schemas.table_profile import TableProfile
from intention.utils.io import read_jsonl


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    outputs = read_jsonl(root / "data/outputs/input_pipeline_outputs.jsonl")
    profiles = [
        OperationalIntentionProfile(**row["operational_intention_profile"])
        for row in outputs
        if row["operational_intention_profile"]["intention_type"] == "compare"
    ]
    tables = [
        TableProfile(**row)
        for row in read_jsonl(root / "data/table_profiles/toy_table_profiles.jsonl")
    ]
    for profile in profiles:
        print(rank_tables(profile, tables))
