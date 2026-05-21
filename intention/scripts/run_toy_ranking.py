from pathlib import Path

from intention.ranking.intention_ranker import rank_tables
from intention.schemas.profile import OperationalProfile
from intention.schemas.table_profile import TableProfile
from intention.utils.io import read_jsonl


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    profiles = [OperationalProfile(**row) for row in read_jsonl(root / "data/outputs/operational_profiles.jsonl")]
    tables = [TableProfile(**row) for row in read_jsonl(root / "data/table_profiles/toy_table_profiles.jsonl")]
    for profile in profiles:
        ranked = rank_tables(profile, tables)
        print(profile.input_id, [(table.table, score) for table, score in ranked])
