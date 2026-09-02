from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json,yaml
from intention.contracts import Table
from intention.retrieval.serialization import SerializedTable
from intention.table_evidence import ordered_serialization_columns

@dataclass(frozen=True)
class NeuralSerializationPolicy:
    version:str; serialization_id:str; visible_components:tuple[str,...]; forbidden_components:tuple[str,...]; maximum_rows:int; maximum_values_per_column:int; maximum_characters:int; truncation:str; digest:str

def load_neural_serialization_policy(path:Path|None=None):
    path=path or Path(__file__).resolve().parents[3]/"configs/architecture/table_serialization.yaml"; raw=yaml.safe_load(path.read_text())
    required={"version","serialization_id","visible_components","forbidden_components","ordering","sampling","budget","format"}
    if not isinstance(raw,dict) or set(raw)!=required or raw["serialization_id"]!="neural_table_evidence_v1" or raw["ordering"]!="source_row_and_column_order" or raw["format"]!="canonical_json": raise ValueError("invalid neural serialization contract")
    forbidden={"grounded_action","action_arguments","requirements","capability_profiles","usefulness_labels","topical_labels","benchmark_labels","system_output","gold_information","full_user_input"}
    if not forbidden<=set(raw["forbidden_components"]) or set(raw["visible_components"])&forbidden: raise ValueError("neural serialization leakage")
    sampling=raw["sampling"]; budget=raw["budget"]
    if sampling!={"method":"stable_head","seed":2026,"maximum_rows":sampling.get("maximum_rows"),"maximum_values_per_column":sampling.get("maximum_values_per_column")} or any(not isinstance(sampling[key],int) or sampling[key]<=0 for key in ("maximum_rows","maximum_values_per_column")): raise ValueError("invalid deterministic sampling")
    if set(budget)!={"maximum_characters","truncation"} or not isinstance(budget["maximum_characters"],int) or budget["maximum_characters"]<=32 or budget["truncation"]!="right_boundary_with_marker": raise ValueError("invalid serialization budget")
    digest=sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return NeuralSerializationPolicy(raw["version"],raw["serialization_id"],tuple(raw["visible_components"]),tuple(raw["forbidden_components"]),sampling["maximum_rows"],sampling["maximum_values_per_column"],budget["maximum_characters"],budget["truncation"],digest)

def _kind(values):
    present=[value for value in values if value is not None]
    if not present:return "null"
    if all(isinstance(value,bool) for value in present):return "boolean"
    if all(isinstance(value,(int,float)) and not isinstance(value,bool) for value in present):return "number"
    return "string"

class NeuralTableSerializer:
    def __init__(self,policy:NeuralSerializationPolicy|None=None): self.policy=policy or load_neural_serialization_policy()
    def serialize(self,table:Table)->SerializedTable:
        columns=ordered_serialization_columns(table)
        payload={"title":table.title,"description":table.description,"columns":[{"name":name,"type":_kind([row.get(column_id) for row in table.rows]),"representative_values":[row.get(column_id) for row in table.rows[:self.policy.maximum_values_per_column]]} for column_id,name in columns],"representative_rows":[[row.get(column_id) for column_id,_ in columns] for row in table.rows[:self.policy.maximum_rows]]}
        text=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False)
        if len(text)>self.policy.maximum_characters: text=text[:self.policy.maximum_characters-15]+"...[TRUNCATED]"
        checksum=sha256(json.dumps({"serialization_id":self.policy.serialization_id,"version":self.policy.version,"policy_hash":self.policy.digest,"text":text},sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return SerializedTable(table.table_id,self.policy.serialization_id,text,checksum)
