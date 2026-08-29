from dataclasses import asdict,dataclass
from pathlib import Path
import json
from jsonschema import Draft202012Validator

SCHEMA=json.loads((Path(__file__).resolve().parents[3]/"configs/architecture/artifact_manifest_schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA); VALIDATOR=Draft202012Validator(SCHEMA)

@dataclass(frozen=True)
class ArtifactManifest:
    manifest_version:str; table_id:str; source:dict; normalized_table:dict; serialization:dict; encoder:dict; vector_collection:dict; capability_profile:dict

def validate_artifact_manifest(manifest:ArtifactManifest|dict):
    payload=asdict(manifest) if isinstance(manifest,ArtifactManifest) else manifest
    errors=sorted(VALIDATOR.iter_errors(payload),key=lambda error:tuple(map(str,error.absolute_path)))
    if errors: raise ValueError(f"invalid artifact manifest: {errors[0].message}")
    return payload
