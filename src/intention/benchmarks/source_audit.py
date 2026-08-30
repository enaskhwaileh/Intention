from __future__ import annotations
from collections import Counter,defaultdict
from dataclasses import asdict,dataclass
from hashlib import sha256
from pathlib import Path
from statistics import mean,median
import re
import yaml

def _hash(path:Path)->str:return sha256(path.read_bytes()).hexdigest()

@dataclass(frozen=True)
class SourceIdentity:
    lineage_name:str; paper_title:str; venue:str; year:int; repository_url:str; repository_revision:str; audit_version:str

@dataclass(frozen=True)
class QueryAudit:
    file_sha256:str; physical_line_count:int; record_count:int; unique_query_ids:tuple[int,...]; duplicate_query_ids:tuple[int,...]; malformed_lines:tuple[dict,...]; missing_ids:tuple[int,...]; qs1_ids:tuple[int,...]; qs2_ids:tuple[int,...]; outside_declared_ids:tuple[int,...]; empty_query_ids:tuple[int,...]
    @property
    def valid(self):return not (self.duplicate_query_ids or self.malformed_lines or self.missing_ids or self.outside_declared_ids or self.empty_query_ids)

@dataclass(frozen=True)
class QrelAudit:
    file_sha256:str; physical_line_count:int; parsed_judgment_count:int; unique_pair_count:int; exact_duplicate_lines:tuple[dict,...]; duplicate_pairs:tuple[dict,...]; conflicting_duplicate_judgments:tuple[dict,...]; malformed_rows:tuple[dict,...]; query_ids:tuple[int,...]; missing_query_ids:tuple[int,...]; table_id_examples:tuple[str,...]; unique_table_count:int; label_distribution:dict[int,int]; labels_outside_scale:tuple[int,...]; judgments_per_query:dict[str,float]; table_id_pattern:str; table_id_suffix_width_distribution:dict[int,int]; table_ids_matching_pattern:bool
    @property
    def valid(self):return not (self.duplicate_pairs or self.conflicting_duplicate_judgments or self.malformed_rows or self.missing_query_ids or self.labels_outside_scale) and self.table_ids_matching_pattern

@dataclass(frozen=True)
class SourceAuditReport:
    classification:str; paper_result:bool; benchmark_frozen:bool; annotation_started:bool; final_encoder_selected:bool; source_identity:dict; source_manifest:dict; query_audit:dict|None; qrel_audit:dict|None; discrepancy_audit:dict; blockers:tuple[dict,...]; audit_status:str
    def to_dict(self):return asdict(self)

def load_source_contract(path:Path|None=None)->dict:
    path=path or Path(__file__).resolve().parents[3]/"configs/benchmarks/ia_wikitables_source.yaml"
    raw=yaml.safe_load(path.read_text())
    required={"audit_version","lineage_name","source_paper","repository","resources","query_contract","qrel_contract","table_id_contract","acquisition_status"}
    if not isinstance(raw,dict) or set(raw)!=required:raise ValueError("invalid WikiTables source contract")
    revision=raw["repository"]["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}",revision):raise ValueError("source repository revision must be an immutable SHA")
    return raw

def audit_queries(path:Path,expected_ids=range(1,61),qs1=range(1,31),qs2=range(31,61))->QueryAudit:
    lines=path.read_text(encoding="utf-8").splitlines(); records=[]; malformed=[]; empty=[]
    for number,line in enumerate(lines,1):
        parts=line.split(maxsplit=1)
        if not parts:
            malformed.append({"line_number":number,"raw":line,"reason":"empty physical line"}); continue
        try:query_id=int(parts[0])
        except ValueError:
            malformed.append({"line_number":number,"raw":line,"reason":"query ID is not an integer"}); continue
        text=parts[1].strip() if len(parts)==2 else ""; records.append((query_id,text))
        if not text:empty.append(query_id)
    counts=Counter(query_id for query_id,_ in records); unique=sorted(counts); expected=set(expected_ids)
    return QueryAudit(_hash(path),len(lines),len(records),tuple(unique),tuple(sorted(query_id for query_id,count in counts.items() if count>1)),tuple(malformed),tuple(sorted(expected-set(unique))),tuple(sorted(set(unique)&set(qs1))),tuple(sorted(set(unique)&set(qs2))),tuple(sorted(set(unique)-expected)),tuple(sorted(set(empty))))

def audit_qrels(path:Path,expected_query_ids=range(1,61),label_scale=(0,1,2),table_id_pattern=r"^table-[0-9]{4}-[0-9]{1,4}$")->QrelAudit:
    lines=path.read_text(encoding="utf-8").splitlines(); parsed=[]; malformed=[]
    for number,line in enumerate(lines,1):
        fields=line.split()
        if len(fields)!=4:
            malformed.append({"line_number":number,"raw":line,"reason":"expected four TREC qrels fields"}); continue
        try:query_id=int(fields[0]); label=int(fields[3])
        except ValueError:
            malformed.append({"line_number":number,"raw":line,"reason":"query ID and label must be integers"}); continue
        if not fields[2]:
            malformed.append({"line_number":number,"raw":line,"reason":"empty table ID"}); continue
        parsed.append((number,query_id,fields[2],label,line))
    grouped=defaultdict(list); raw_groups=defaultdict(list)
    for number,query_id,table_id,label,line in parsed:grouped[(query_id,table_id)].append((number,label,line))
    for number,_,_,_,line in parsed:raw_groups[line].append(number)
    exact=tuple({"raw":line,"line_numbers":numbers} for line,numbers in sorted(raw_groups.items()) if len(numbers)>1)
    duplicates=[]; conflicts=[]
    for (query_id,table_id),items in sorted(grouped.items()):
        if len(items)>1:
            entry={"query_id":query_id,"table_id":table_id,"line_numbers":[item[0] for item in items],"labels":[item[1] for item in items]}; duplicates.append(entry)
            if len({item[1] for item in items})>1:conflicts.append(entry)
    judgments={(query_id,table_id):items[0][1] for (query_id,table_id),items in grouped.items()}; query_ids=sorted({key[0] for key in judgments}); table_ids=sorted({key[1] for key in judgments}); per_query=Counter(key[0] for key in judgments)
    values=sorted(per_query.values()); stats={"minimum":min(values) if values else 0,"maximum":max(values) if values else 0,"mean":mean(values) if values else 0,"median":median(values) if values else 0}
    labels=Counter(judgments.values()); pattern=re.compile(table_id_pattern)
    widths=Counter(len(table_id.rsplit("-",1)[-1]) for table_id in table_ids)
    examples=sorted({table_ids[0],table_ids[-1],*(next((item for item in table_ids if len(item.rsplit('-',1)[-1])==width),table_ids[0]) for width in sorted(widths))}) if table_ids else []
    return QrelAudit(_hash(path),len(lines),len(parsed),len(judgments),exact,tuple(duplicates),tuple(conflicts),tuple(malformed),tuple(query_ids),tuple(sorted(set(expected_query_ids)-set(query_ids))),tuple(examples),len(table_ids),dict(sorted(labels.items())),tuple(sorted(set(labels)-set(label_scale))),stats,table_id_pattern,dict(sorted(widths.items())),all(pattern.fullmatch(table_id) for table_id in table_ids))

def _identity(contract):
    paper=contract["source_paper"]; repository=contract["repository"]
    return SourceIdentity(contract["lineage_name"],paper["title"],paper["venue"],paper["year"],repository["url"],repository["commit"],contract["audit_version"])

def discrepancy_audit(qrels:QrelAudit|None)->dict:
    checks=["canonical qrel physical and parsed counts","exact/duplicate query-table pairs","conflicting duplicate labels","malformed qrel rows","missing query IDs","canonical label distribution","EDBT 2025 paper statement and linked public implementation search for qrel/split/preprocessing artifacts"]
    evidence={"WWW2018_reported_pairs":3120,"EDBT2025_reported_pairs":3117,"difference":3,"canonical_physical_records":None if qrels is None else qrels.physical_line_count,"canonical_unique_pairs":None if qrels is None else qrels.unique_pair_count,"authoritative_removal_artifact_found":False}
    return {"discrepancy_status":"unresolved","verified_cause":None,"hypotheses":[],"evidence":evidence,"checked":checks,"conclusion":"No authoritative artifact inspected identifies the three removed judgments; canonical qrels remain unchanged."}

def audit_source(source_root:Path,contract_path:Path|None=None)->SourceAuditReport:
    contract=load_source_contract(contract_path); qrange=contract["query_contract"]["expected_ids"]; qs1=contract["query_contract"]["qs1"]; qs2=contract["query_contract"]["qs2"]
    queries_path=source_root/contract["resources"]["queries"]["path"]; qrels_path=source_root/contract["resources"]["qrels"]["path"]
    missing=[path for path in (queries_path,qrels_path) if not path.is_file()]
    if missing:return blocked_source_audit(contract,[{"component":"source_files","reason":"required canonical metadata file is unavailable","required_action":f"place pinned files under {source_root}","missing":[str(path) for path in missing]}])
    queries=audit_queries(queries_path,range(qrange[0],qrange[1]+1),range(qs1[0],qs1[1]+1),range(qs2[0],qs2[1]+1)); qrels=audit_qrels(qrels_path,range(qrange[0],qrange[1]+1),tuple(contract["qrel_contract"]["original_topical_label_scale"]),contract["table_id_contract"]["observed_pattern"])
    blockers=[]
    for name,audit in (("queries",queries),("qrels",qrels)):
        expected=contract["resources"][name]["sha256"]
        if audit.file_sha256!=expected:blockers.append({"component":name,"reason":"SHA-256 does not match pinned source contract","required_action":"acquire the exact file from the pinned repository revision","expected":expected,"actual":audit.file_sha256})
        if not audit.valid:blockers.append({"component":name,"reason":"source file violates the declared canonical contract","required_action":"do not repair silently; investigate source identity"})
    status="blocked" if blockers else "verified_with_unresolved_discrepancy"
    return SourceAuditReport("source_audit",False,False,False,False,asdict(_identity(contract)),contract,asdict(queries),asdict(qrels),discrepancy_audit(qrels),tuple(blockers),status)

def blocked_source_audit(contract:dict,blockers:list[dict])->SourceAuditReport:
    return SourceAuditReport("source_audit",False,False,False,False,asdict(_identity(contract)),contract,None,None,discrepancy_audit(None),tuple(blockers),"blocked")
