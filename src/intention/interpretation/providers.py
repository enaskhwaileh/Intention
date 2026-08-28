"""Fail-closed provider construction from versioned configuration."""
from pathlib import Path
import yaml
from .interpreter import DeterministicInterpreter,ExternalStructuredProvider

def load_provider(path=None,client=None):
    path=Path(path) if path else Path(__file__).resolve().parents[3]/"configs/models/interpreter.yaml"; raw=yaml.safe_load(path.read_text())
    expected={"schema_version","provider","model","revision","temperature","raw_artifact_policy","validated_artifact_policy"}
    if not isinstance(raw,dict) or set(raw)!=expected or raw["schema_version"]!="1.0.0" or raw["temperature"]!=0 or raw["raw_artifact_policy"]!="retain" or raw["validated_artifact_policy"]!="separate": raise ValueError("invalid interpreter provider configuration")
    if raw["provider"]=="deterministic": return DeterministicInterpreter()
    return ExternalStructuredProvider(raw["provider"],raw["model"],str(raw["revision"]),client)
