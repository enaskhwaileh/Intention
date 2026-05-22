from intention.llm.base import LLMClient
from intention.schemas.intention import RawIntention
from intention.schemas.query import QueryProfile


class QueryIntentionSeparator:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def separate(self, user_input: str) -> tuple[QueryProfile, RawIntention]:
        payload = self.llm_client.separate_query_and_intention(user_input)
        return (
            QueryProfile(**payload["query_profile"]),
            RawIntention(**payload["raw_intention"]),
        )
