"""Versioned table serialization contracts for first-stage retrieval."""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json,yaml
from intention.contracts import Table

@dataclass(frozen=True)
class SerializationContract:
    serialization_id: str
    version: str
    visible_components: tuple[str,...]
    excluded_components: tuple[str,...]
    column_policy: str
    format: str

@dataclass(frozen=True)
class RetrievalPolicy:
    version: str
    primary_k: int
    development_k: tuple[int,...]
    sensitivity_k: tuple[int,...]
    serializations: dict[str,SerializationContract]
    input_scopes: dict[str,dict]

@dataclass(frozen=True)
class SerializedTable:
    table_id: str
    serialization_id: str
    text: str
    checksum: str

def load_retrieval_policy(path: Path|None=None) -> RetrievalPolicy:
    path=path or Path(__file__).resolve().parents[3]/"configs/retrieval/contracts.yaml"
    raw=yaml.safe_load(path.read_text()); required={"version","candidate_depth","serializations","input_scopes"}
    if not isinstance(raw,dict) or set(raw)!=required: raise ValueError("invalid retrieval policy root")
    depths=raw["candidate_depth"]
    if not isinstance(depths,dict) or set(depths)!={"primary","development","sensitivity"}: raise ValueError("invalid candidate-depth policy")
    groups=(depths["development"],depths["sensitivity"])
    if not isinstance(depths["primary"],int) or depths["primary"]<=0 or any(not isinstance(group,list) or group!=sorted(set(group)) or any(not isinstance(k,int) or k<=0 for k in group) for group in groups) or depths["primary"] not in groups[0] or not set(groups[0])<=set(groups[1]):
        raise ValueError("invalid candidate-depth values")
    contracts={}
    expected_components=("title","description","column_names")
    forbidden={"rows","cell_values","metadata","capability_profiles","grounded_action","action_arguments","full_user_input"}
    for name,item in raw["serializations"].items():
        if not isinstance(item,dict) or set(item)!={"version","visible_components","excluded_components","column_policy","format"}: raise ValueError("invalid serialization contract")
        if tuple(item["visible_components"])!=expected_components or not forbidden<=set(item["excluded_components"]) or item["column_policy"]!="first_row_insertion_order" or item["format"]!="ordered_space_join": raise ValueError("serialization visibility contract changed")
        contracts[name]=SerializationContract(name,item["version"],tuple(item["visible_components"]),tuple(item["excluded_components"]),item["column_policy"],item["format"])
    scopes=raw["input_scopes"]
    if set(scopes)!={"topical_only","full_input_baseline"} or scopes["topical_only"]!={"query_field":"topical_query","permits_full_user_input":False} or scopes["full_input_baseline"]!={"query_field":"full_user_input","permits_full_user_input":True}: raise ValueError("invalid retrieval input scopes")
    return RetrievalPolicy(raw["version"],depths["primary"],tuple(depths["development"]),tuple(depths["sensitivity"]),contracts,scopes)

class TableSerializer:
    def __init__(self,contract: SerializationContract): self.contract=contract
    def serialize(self,table: Table) -> SerializedTable:
        columns=list(table.rows[0]) if table.rows else []
        text=" ".join((table.title,table.description,*columns))
        checksum=sha256(json.dumps({"serialization_id":self.contract.serialization_id,"text":text},sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return SerializedTable(table.table_id,self.contract.serialization_id,text,checksum)
