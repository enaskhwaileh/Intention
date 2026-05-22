from pydantic import BaseModel, Field


class TableProfile(BaseModel):
    table_id: str
    title: str
    semantic: dict[str, object] = Field(default_factory=dict)
    structural: dict[str, object] = Field(default_factory=dict)
    coverage: dict[str, object] = Field(default_factory=dict)
    quality: dict[str, object] = Field(default_factory=dict)
    behavioral: dict[str, object] = Field(default_factory=dict)
