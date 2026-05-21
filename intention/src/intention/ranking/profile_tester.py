from intention.schemas.profile import OperationalProfile
from intention.schemas.table_profile import TableProfile


def score_table(profile: OperationalProfile, table_profile: TableProfile) -> float:
    profile_terms = set(profile.entities + [profile.intention_id, profile.profile_type])
    table_terms = set(table_profile.tags + table_profile.columns)
    if not profile_terms:
        return 0.0
    return len(profile_terms.intersection(table_terms)) / len(profile_terms)
