from dataclasses import dataclass


@dataclass(frozen=True)
class TableProfile:
    table: str
    columns: list[str]
    tags: list[str]
