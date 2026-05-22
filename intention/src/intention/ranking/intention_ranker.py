from intention.ranking.profile_tester import ProfileTester
from intention.schemas.profile import OperationalIntentionProfile
from intention.schemas.table_profile import TableProfile


def rank_tables(
    profile: OperationalIntentionProfile,
    table_profiles: list[TableProfile],
) -> list[dict]:
    tester = ProfileTester()
    ranked = [tester.test(profile, table_profile) for table_profile in table_profiles]
    return sorted(ranked, key=lambda row: row["intention_alignment_score"], reverse=True)
