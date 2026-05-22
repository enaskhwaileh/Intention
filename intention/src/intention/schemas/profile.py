from pydantic import BaseModel, Field


class EvidenceRequirement(BaseModel):
    predicate: str
    axis: str
    expected_evidence: list[str] = Field(default_factory=list)
    reason: str
    priority: str
    testable_from: list[str] = Field(default_factory=list)


class NegativeEvidence(BaseModel):
    predicate: str
    reason: str


class OperationalIntentionProfile(BaseModel):
    input_id: str
    intention_type: str
    goal: str
    unit_of_analysis: str | None = None
    required_evidence: list[EvidenceRequirement] = Field(default_factory=list)
    optional_evidence: list[EvidenceRequirement] = Field(default_factory=list)
    negative_evidence: list[NegativeEvidence] = Field(default_factory=list)
    validation_status: str = "unchecked"
    validation_errors: list[str] = Field(default_factory=list)
