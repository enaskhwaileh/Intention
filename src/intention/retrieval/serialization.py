"""Versioned table serialization contracts for first-stage retrieval."""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json,yaml
from intention.contracts import Table
from intention.table_evidence import ordered_serialization_columns

@dataclass(frozen=True)
class SerializationContract:
    serialization_id: str
    version: str
    evidence_policy: str
    visible_components: tuple[str,...]
    excluded_components: tuple[str,...]
    column_policy: str
    format: str

@dataclass(frozen=True)
class RetrievalPolicy:
    version: str
    default_k: int
    final_k_status: str
    development_k: tuple[int,...]
    sensitivity_k: tuple[int,...]
    depth_selection: dict
    evidence_access: dict[str,dict]
    score_normalizations: dict[str,dict]
    serializations: dict[str,SerializationContract]
    input_scopes: dict[str,dict]
    digest: str

@dataclass(frozen=True)
class SerializedTable:
    table_id: str
    serialization_id: str
    text: str
    checksum: str

def load_retrieval_policy(path: Path|None=None) -> RetrievalPolicy:
    path=path or Path(__file__).resolve().parents[3]/"configs/retrieval/contracts.yaml"
    raw=yaml.safe_load(path.read_text()); required={"version","evidence_access","candidate_depth","score_normalizations","serializations","input_scopes"}
    if not isinstance(raw,dict) or set(raw)!=required: raise ValueError("invalid retrieval policy root")
    depths=raw["candidate_depth"]
    if not isinstance(depths,dict) or set(depths)!={"default","final_status","development","sensitivity","selection_rule"}: raise ValueError("invalid candidate-depth policy")
    groups=(depths["development"],depths["sensitivity"])
    if not isinstance(depths["default"],int) or depths["default"]<=0 or depths["final_status"]!="development_selection_pending" or any(not isinstance(group,list) or group!=sorted(set(group)) or any(not isinstance(k,int) or k<=0 for k in group) for group in groups) or depths["default"] not in groups[0] or not set(groups[0])<=set(groups[1]):
        raise ValueError("invalid candidate-depth values")
    selection=depths["selection_rule"]
    expected_selection={"split":"development_only","metric":"known_relevant_recall","reference_depth":100,"saturation_ratio":.98,"choice":"smallest_k_reaching_ratio_of_recall_at_100","test_labels_permitted":False}
    if selection!=expected_selection: raise ValueError("invalid development-only depth selection rule")
    evidence=raw["evidence_access"]
    if set(evidence)!={"retrieval_table_evidence_v1"}: raise ValueError("invalid evidence-access policy")
    allowed={"title","description","column_names","row_structure","cell_values"}; forbidden={"metadata","capability_profiles","grounded_action","action_arguments","full_user_input","gold_labels","usefulness_labels"}
    if set(evidence["retrieval_table_evidence_v1"]["allowed_components"])!=allowed or not forbidden<=set(evidence["retrieval_table_evidence_v1"]["forbidden_components"]): raise ValueError("invalid evidence visibility")
    contracts={}
    expected_components=("title","description","column_names")
    forbidden={"row_structure","cell_values","metadata","capability_profiles","grounded_action","action_arguments","full_user_input"}
    for name,item in raw["serializations"].items():
        if not isinstance(item,dict) or set(item)!={"version","evidence_policy","visible_components","excluded_components","column_policy","format"}: raise ValueError("invalid serialization contract")
        if item["evidence_policy"] not in evidence or not set(item["visible_components"])<=allowed or set(item["visible_components"])&forbidden: raise ValueError("serialization violates evidence-access policy")
        if tuple(item["visible_components"])!=expected_components or not forbidden<=set(item["excluded_components"]) or item["column_policy"]!="canonical_semantic_metadata_or_legacy_first_row" or item["format"]!="ordered_space_join": raise ValueError("serialization visibility contract changed")
        contracts[name]=SerializationContract(name,item["version"],item["evidence_policy"],tuple(item["visible_components"]),tuple(item["excluded_components"]),item["column_policy"],item["format"])
    scopes=raw["input_scopes"]
    if set(scopes)!={"topical_only","full_input_baseline"} or scopes["topical_only"]!={"query_field":"topical_query","permits_full_user_input":False} or scopes["full_input_baseline"]!={"query_field":"full_user_input","permits_full_user_input":True}: raise ValueError("invalid retrieval input scopes")
    normalizations=raw["score_normalizations"]
    if set(normalizations)!={"bm25_query_max_v1"} or normalizations["bm25_query_max_v1"]!={"version":"1.0.0","method":"query_max","fit_scope":"query_local","calibration_data":"none","future_calibration_fit_scope":"development_only","test_labels_permitted":False,"formula":"raw_score / max_query_raw_score; all_zero_maps_to_zero"}: raise ValueError("invalid score normalization")
    digest=sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return RetrievalPolicy(raw["version"],depths["default"],depths["final_status"],tuple(depths["development"]),tuple(depths["sensitivity"]),selection,evidence,normalizations,contracts,scopes,digest)

def select_candidate_depth(recall_by_k: dict[int,float],policy: RetrievalPolicy|None=None,split: str="development") -> int:
    policy=policy or load_retrieval_policy()
    if split!="development" or set(recall_by_k)!=set(policy.sensitivity_k): raise ValueError("candidate depth selection requires all frozen development-only sensitivity values")
    values=[recall_by_k[k] for k in policy.sensitivity_k]
    if any(not isinstance(value,(int,float)) or not 0<=value<=1 for value in values) or values!=sorted(values): raise ValueError("development recall curve must be bounded and monotonic")
    target=policy.depth_selection["saturation_ratio"]*recall_by_k[policy.depth_selection["reference_depth"]]
    for k in policy.sensitivity_k:
        if recall_by_k[k]>=target:return k
    return policy.sensitivity_k[-1]

class TableSerializer:
    def __init__(self,contract: SerializationContract): self.contract=contract
    def serialize(self,table: Table) -> SerializedTable:
        columns=ordered_serialization_columns(table); names=[name if isinstance(name,str) else "" for _,name in columns]
        text=" ".join((table.title,table.description,*names))
        checksum=sha256(json.dumps({"serialization_id":self.contract.serialization_id,"text":text},sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return SerializedTable(table.table_id,self.contract.serialization_id,text,checksum)
