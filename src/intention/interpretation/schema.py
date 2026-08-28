"""Provider artifact and structured interpretation schema validation."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
from intention.knowledge.layer import KnowledgeLayer

SCHEMA_VERSION="1.0.0"; AMBIGUITY={"unambiguous","ambiguous","insufficient"}
STRUCTURED_OUTPUT_SCHEMA=json.loads((Path(__file__).resolve().parents[3]/"configs/interpretation/output_schema.json").read_text())

@dataclass(frozen=True)
class ProviderArtifact:
    provider: str
    model: str
    revision: str
    schema_version: str
    content: dict[str,Any]
    raw_response: Any
    def __post_init__(self):
        if not all(isinstance(x,str) and x for x in (self.provider,self.model,self.revision,self.schema_version)): raise ValueError("provider artifact identity is required")

def validate_span(span,text):
    if not isinstance(span,dict) or set(span)!={"start","end","text"}: raise ValueError("invalid provenance span fields")
    start,end=span["start"],span["end"]
    if not isinstance(start,int) or not isinstance(end,int) or not 0<=start<=end<=len(text) or span["text"]!=text[start:end]: raise ValueError("provenance span does not match source input")
    return (start,end)

def validate_content(text,content,kg: KnowledgeLayer):
    if not isinstance(content,dict) or set(content)!={"schema_version","action","arguments","topical","provenance","ambiguity"}: raise ValueError("invalid structured interpretation fields")
    if content["schema_version"]!=SCHEMA_VERSION: raise ValueError("unsupported interpretation schema version")
    if content["action"] not in set(kg.actions)|{"unknown"} or not isinstance(content["arguments"],dict): raise ValueError("invalid action or arguments")
    topical=content["topical"]
    if not isinstance(topical,dict) or set(topical)!={"query","entities","attributes","constraints"} or not isinstance(topical["query"],str) or not topical["query"].strip() or not isinstance(topical["entities"],list) or not isinstance(topical["attributes"],list) or not isinstance(topical["constraints"],dict): raise ValueError("invalid topical fields")
    ambiguity=content["ambiguity"]
    if not isinstance(ambiguity,dict) or set(ambiguity)!={"status","candidates","reason"} or ambiguity["status"] not in AMBIGUITY or not isinstance(ambiguity["candidates"],list) or not set(ambiguity["candidates"])<=set(kg.actions): raise ValueError("invalid ambiguity fields")
    provenance=content["provenance"]
    if not isinstance(provenance,dict) or set(provenance)!={"topic_spans","action_spans","argument_spans"} or not isinstance(provenance["argument_spans"],dict): raise ValueError("invalid provenance fields")
    if set(provenance["argument_spans"])!=set(content["arguments"]): raise ValueError("every argument requires provenance")
    spans=[]
    for group in (provenance["topic_spans"],provenance["action_spans"]):
        if not isinstance(group,list): raise ValueError("invalid provenance span group")
        spans.extend(validate_span(span,text) for span in group)
    for key,group in provenance["argument_spans"].items():
        if key not in content["arguments"] or not isinstance(group,list) or not group: raise ValueError("invalid argument provenance")
        spans.extend(validate_span(span,text) for span in group)
    return tuple(spans)
