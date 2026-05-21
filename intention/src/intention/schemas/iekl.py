from dataclasses import dataclass


@dataclass(frozen=True)
class IEKLNode:
    id: str
    label: str
    keywords: list[str]
    profile_type: str


@dataclass(frozen=True)
class IEKLEdge:
    source: str
    target: str
    relation: str
