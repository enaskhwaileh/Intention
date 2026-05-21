from intention.ranking.intention_ranker import rank_tables
from intention.schemas.profile import OperationalProfile
from intention.schemas.table_profile import TableProfile


def test_ranking_prefers_matching_table():
    profile = OperationalProfile(
        input_id="q1",
        intention_id="analyze_sales",
        profile_type="analytical",
        entities=["revenue"],
        confidence=0.8,
    )
    tables = [
        TableProfile(table="inventory", columns=["sku"], tags=["stock"]),
        TableProfile(table="sales_orders", columns=["revenue"], tags=["sales"]),
    ]

    assert rank_tables(profile, tables)[0][0].table == "sales_orders"
