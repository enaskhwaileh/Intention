from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import yaml

@dataclass(frozen=True)
class EvaluationProtocol:
    version: str
    raw: dict
    digest: str

def load_evaluation_protocol(path: Path|None=None) -> EvaluationProtocol:
    path=path or Path(__file__).resolve().parents[3]/"configs/evaluation/protocol.yaml"
    raw=yaml.safe_load(path.read_text())
    required={"version","labels","ranking","aggregation","retrieval","annotation","statistics","tuning_guard"}
    if not isinstance(raw,dict) or set(raw)!=required: raise ValueError("invalid evaluation protocol root")
    if raw["labels"]!={"usefulness":[0,1,2,3],"useful_threshold":2}: raise ValueError("invalid usefulness labels")
    if raw["ranking"]!={"ndcg_cutoffs":[5,10],"mrr_threshold":2,"useful_recall_cutoffs":[5,10,20],"tie_break":"score_desc_table_id_asc"}: raise ValueError("invalid ranking protocol")
    if raw["aggregation"]!={"unit":"topic","corpus_operation":"arithmetic_mean_of_topic_metrics"}: raise ValueError("metrics must aggregate by topic first")
    if raw["retrieval"]!={"candidate_recall_cutoffs":[5,10,20],"upper_bound":"useful_items_present_in_candidates"}: raise ValueError("invalid retrieval evaluation protocol")
    if raw["annotation"]!={"agreement":"quadratic_weighted_kappa","missing_judgments":"fail"}: raise ValueError("invalid annotation evaluation protocol")
    expected_statistics={"bootstrap":{"iterations":2000,"seed":2026,"confidence":.95,"unit":"topic"},"paired_test":{"method":"paired_sign_permutation","iterations":10000,"seed":2026},"correction":{"method":"holm","alpha":.05,"family":"all_predeclared_primary_system_comparisons"}}
    if raw["statistics"]!=expected_statistics: raise ValueError("invalid statistical protocol")
    guard=raw["tuning_guard"]
    if guard["forbidden_split"]!="test" or "test" in guard["permitted_splits"] or set(guard["protected_parameters"])!={"usefulness_threshold","candidate_depth","fusion_weights","score_calibration","prompts"}: raise ValueError("invalid test-seal policy")
    digest=sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return EvaluationProtocol(raw["version"],raw,digest)

def assert_tuning_allowed(split: str,parameter: str,protocol: EvaluationProtocol|None=None):
    protocol=protocol or load_evaluation_protocol(); guard=protocol.raw["tuning_guard"]
    if parameter not in guard["protected_parameters"] or split not in guard["permitted_splits"]:
        raise ValueError(f"tuning {parameter} on {split} is forbidden")
