from pydantic import BaseModel, Field


class QueryProfile(BaseModel):
    topic: str
    entities: list[str] = Field(default_factory=list)
    attributes: list[str] = Field(default_factory=list)
    constraints: dict[str, str] = Field(default_factory=dict)
    retrieval_query: str
