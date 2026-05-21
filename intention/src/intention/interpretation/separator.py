import re

from intention.schemas.query import QueryInput, QueryProfile


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def separate_query(query: QueryInput) -> QueryProfile:
    tokens = TOKEN_PATTERN.findall(query.text.lower())
    return QueryProfile(input_id=query.id, text=query.text, tokens=tokens)
