from dataclasses import dataclass


@dataclass(frozen=True)
class QueryInput:
    id: str
    text: str


@dataclass(frozen=True)
class QueryProfile:
    input_id: str
    text: str
    tokens: list[str]
