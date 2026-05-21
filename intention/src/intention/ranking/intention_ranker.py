from intention.ranking.profile_tester import score_table
from intention.schemas.profile import OperationalProfile
from intention.schemas.table_profile import TableProfile


def rank_tables(
    profile: OperationalProfile,
    table_profiles: list[TableProfile],
    top_k: int = 3,
) -> list[tuple[TableProfile, float]]:
    ranked = [(table, score_table(profile, table)) for table in table_profiles]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:top_k]
