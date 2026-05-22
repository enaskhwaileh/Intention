from pydantic import BaseModel, Field


class RawIntention(BaseModel):
    intent_phrase: str
    candidate_intention_type: str
    slots: dict[str, object] = Field(default_factory=dict)


class GroundedIntention(BaseModel):
    intention_type: str
    goal: str
    slots: dict[str, object] = Field(default_factory=dict)
    required_predicates: list[str] = Field(default_factory=list)
    optional_predicates: list[str] = Field(default_factory=list)
    negative_predicates: list[str] = Field(default_factory=list)
