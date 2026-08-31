from __future__ import annotations
from collections import defaultdict
from dataclasses import asdict,dataclass,replace
from hashlib import sha256
from pathlib import Path
from typing import Any,Iterable
import json,urllib.request
import yaml
from jsonschema import Draft202012Validator
from intention.contracts import Table

DATASET_ID="wikitables_www2018"
NORMALIZATION_VERSION="1.0.0"
FORBIDDEN_SOURCE_FIELDS=frozenset({"topical_label","qrel","qrels","usefulness_label","action","action_arguments","requirements","candidate_pool","split","system_output","gold"})
SOURCE_FIELDS=frozenset({"table_id","source_record_id","page_id","source_table_id","page_title","section_title","table_caption","headers","rows"})

CONFIG_SCHEMA={"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","additionalProperties":False,
 "required":["contract_version","dataset_id","normalization_version","source_contract","acquisition","licensing","normalization","storage","separation"],
 "properties":{
  "contract_version":{"const":"1.0.0"},"dataset_id":{"const":DATASET_ID},"normalization_version":{"const":NORMALIZATION_VERSION},
  "source_contract":{"type":"object","additionalProperties":False,"required":["path","audit_version","repository_revision"],"properties":{"path":{"const":"configs/benchmarks/ia_wikitables_source.yaml"},"audit_version":{"const":"1.0.0"},"repository_revision":{"const":"ae156771cacc252031d74d61380e09bc1e838bc3"}}},
  "acquisition":{"type":"object","additionalProperties":False,"required":["canonical_download_url","advertised_filename","full_corpus_status","network_default","format_status","recorded_head_evidence"],"properties":{"canonical_download_url":{"const":"http://iai.group/downloads/smart_table/WP_tables.zip"},"advertised_filename":{"const":"WP_tables.zip"},"full_corpus_status":{"const":"not_acquired"},"network_default":{"const":"disabled"},"format_status":{"const":"requires_full_archive_acquisition"},"recorded_head_evidence":{"type":"object","additionalProperties":False,"required":["inspected_at","final_url","redirect_statuses","http_status","content_length","content_type","etag","last_modified","accept_ranges"],"properties":{"inspected_at":{"type":"string"},"final_url":{"type":"string","format":"uri"},"redirect_statuses":{"type":"array","items":{"type":"integer"},"minItems":1},"http_status":{"type":"integer"},"content_length":{"type":"integer","minimum":1},"content_type":{"type":"string"},"etag":{"type":"string"},"last_modified":{"type":"string"},"accept_ranges":{"type":"string"}}}}},
  "licensing":{"type":"object","additionalProperties":False,"required":["source_use_evidence","redistribution_status"],"properties":{"source_use_evidence":{"type":"string","minLength":1},"redistribution_status":{"const":"requires_verification"}}},
  "normalization":{"type":"object","additionalProperties":False,"required":["cell_type","row_order","column_order","header_policy","ragged_row_policy","cleaning","type_coercion"],"properties":{"cell_type":{"const":"source_text_or_null"},"row_order":{"const":"source_preserved"},"column_order":{"const":"source_preserved"},"header_policy":{"const":"positional_duplicates_preserved"},"ragged_row_policy":{"const":"pad_absent_positions_with_null_and_flag"},"cleaning":{"const":"none"},"type_coercion":{"const":"none"}}},
  "storage":{"type":"object","additionalProperties":False,"required":["implementation","format","partition_count","partition_method","compression","logical_checksum","corpus_digest"],"properties":{"implementation":{"const":"PartitionedCorpusStore"},"format":{"const":"partitioned_parquet"},"partition_count":{"const":256},"partition_method":{"const":"deterministic_sha256"},"compression":{"const":"zstd"},"logical_checksum":{"const":"sha256_canonical_json"},"corpus_digest":{"const":"sha256_sorted_table_id_logical_checksum_pairs"}}},
  "separation":{"type":"object","additionalProperties":False,"required":["qrel_membership_in_corpus","benchmark_labels_in_corpus","actions_in_corpus","requirements_in_corpus"],"properties":{"qrel_membership_in_corpus":{"const":"forbidden"},"benchmark_labels_in_corpus":{"const":"forbidden"},"actions_in_corpus":{"const":"forbidden"},"requirements_in_corpus":{"const":"forbidden"}}}
 }}
Draft202012Validator.check_schema(CONFIG_SCHEMA); CONFIG_VALIDATOR=Draft202012Validator(CONFIG_SCHEMA)

def _canonical(value:Any)->bytes:return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")
def _digest(value:Any)->str:return sha256(_canonical(value)).hexdigest()

@dataclass(frozen=True)
class CorpusSource:
    dataset_id:str; source_record_id:str; page_id:str|None; source_table_id:str|None; source_revision:str; source_record_checksum:str

@dataclass(frozen=True)
class CorpusContext:
    page_title:str|None; section_title:str|None; table_caption:str|None

@dataclass(frozen=True)
class CorpusColumn:
    column_id:str; ordinal:int; header_text:str|None

@dataclass(frozen=True)
class NormalizationMetadata:
    version:str; flags:tuple[str,...]; logical_checksum:str

@dataclass(frozen=True)
class NormalizedCorpusTable:
    table_id:str; source:CorpusSource; context:CorpusContext; columns:tuple[CorpusColumn,...]; rows:tuple[tuple[str|None,...],...]; row_count:int; column_count:int; normalization:NormalizationMetadata
    def __post_init__(self):
        if not self.table_id or self.row_count!=len(self.rows) or self.column_count!=len(self.columns):raise ValueError("normalized table shape mismatch")
        if tuple(column.ordinal for column in self.columns)!=tuple(range(self.column_count)):raise ValueError("column ordinals must be positional")
        if any(len(row)!=self.column_count for row in self.rows):raise ValueError("normalized rows must match column count")
        if any(cell is not None and not isinstance(cell,str) for row in self.rows for cell in row):raise TypeError("cells must be source text or null")

@dataclass(frozen=True)
class RejectedCorpusRecord:
    source_record_id:str; reason_code:str; detail:str; source_checksum:str|None

@dataclass(frozen=True)
class TableIndexEntry:
    table_id:str; source_record_id:str; page_id:str|None; source_table_id:str|None; page_title:str|None; section_title:str|None; table_caption:str|None; row_count:int; column_count:int; shard:int; logical_checksum:str; normalization_flags:tuple[str,...]

def load_corpus_contract(path:Path|None=None)->dict:
    path=path or Path(__file__).resolve().parents[3]/"configs/benchmarks/wikitables_corpus.yaml"
    raw=yaml.safe_load(path.read_text()); errors=sorted(CONFIG_VALIDATOR.iter_errors(raw),key=lambda error:list(error.path))
    if errors:raise ValueError("invalid WikiTables corpus contract: "+"; ".join(error.message for error in errors))
    return raw

def normalize_source_record(record:dict[str,Any],source_revision:str)->NormalizedCorpusTable|RejectedCorpusRecord:
    table_id=str(record.get("table_id","")).strip(); source_id=str(record.get("source_record_id","")).strip(); checksum=_digest(record)
    unknown=set(record)-SOURCE_FIELDS
    if unknown:
        forbidden=sorted(unknown&FORBIDDEN_SOURCE_FIELDS); reason="forbidden_benchmark_fields" if forbidden else "unknown_source_fields"
        return RejectedCorpusRecord(source_id,reason,",".join(forbidden or sorted(unknown)),checksum)
    if not source_id:return RejectedCorpusRecord(source_id,"missing_source_record_id","source_record_id must be non-empty",checksum)
    if not table_id:return RejectedCorpusRecord(source_id,"missing_table_id","table_id must be non-empty",checksum)
    context_values=[record.get(key) for key in ("page_title","section_title","table_caption")]
    if any(value is not None and not isinstance(value,str) for value in context_values):return RejectedCorpusRecord(source_id,"invalid_context_type","context values must be source text or null",checksum)
    headers=record.get("headers"); rows=record.get("rows")
    if not isinstance(headers,list) or not isinstance(rows,list):return RejectedCorpusRecord(source_id,"invalid_structure","headers and rows must be lists",checksum)
    if any(item is not None and not isinstance(item,str) for item in headers):return RejectedCorpusRecord(source_id,"invalid_header_type","headers must be source text or null",checksum)
    if any(not isinstance(row,list) for row in rows):return RejectedCorpusRecord(source_id,"invalid_row_type","every row must be an ordered list",checksum)
    if any(cell is not None and not isinstance(cell,str) for row in rows for cell in row):return RejectedCorpusRecord(source_id,"invalid_cell_type","cells must be source text or null",checksum)
    width=max([len(headers),*(len(row) for row in rows)],default=0); flags=[]
    if len(headers)<width:headers=[*headers,*([None]*(width-len(headers)))]; flags.append("missing_headers_padded")
    if any(len(row)<width for row in rows):flags.append("ragged_rows_padded")
    padded=tuple(tuple([*row,*([None]*(width-len(row)))]) for row in rows)
    columns=tuple(CorpusColumn(f"c{ordinal:04d}",ordinal,header) for ordinal,header in enumerate(headers))
    source=CorpusSource(DATASET_ID,source_id,None if record.get("page_id") is None else str(record["page_id"]),None if record.get("source_table_id") is None else str(record["source_table_id"]),source_revision,checksum)
    context=CorpusContext(*context_values)
    provisional=NormalizedCorpusTable(table_id,source,context,columns,padded,len(padded),width,NormalizationMetadata(NORMALIZATION_VERSION,tuple(flags),"pending"))
    payload=asdict(provisional); payload["normalization"].pop("logical_checksum")
    return replace(provisional,normalization=replace(provisional.normalization,logical_checksum=_digest(payload)))

def shard_for(table_id:str,partition_count:int=256)->int:
    if partition_count<1:raise ValueError("partition_count must be positive")
    return int.from_bytes(sha256(table_id.encode("utf-8")).digest()[:8],"big")%partition_count

def logical_corpus_digest(tables:Iterable[NormalizedCorpusTable])->str:
    pairs=sorted((table.table_id,table.normalization.logical_checksum) for table in tables)
    if len({pair[0] for pair in pairs})!=len(pairs):raise ValueError("duplicate table IDs in logical corpus")
    return _digest(pairs)

def to_runtime_table(table:NormalizedCorpusTable)->Table:
    rows=tuple({column.column_id:cell for column,cell in zip(table.columns,row)} for row in table.rows)
    metadata={"source":asdict(table.source),"context":asdict(table.context),"columns":[asdict(column) for column in table.columns],"normalization":asdict(table.normalization)}
    return Table(table.table_id,table.context.page_title or "",table.context.table_caption or "",rows,metadata)

def qrel_resolution(qrel_table_ids:Iterable[str],resolved_table_ids:Iterable[str])->dict:
    expected=set(qrel_table_ids); resolved=expected&set(resolved_table_ids); missing=sorted(expected-resolved)
    return {"expected_count":len(expected),"resolved_count":len(resolved),"resolution_ratio":len(resolved)/len(expected) if expected else 1.0,"missing_table_ids":missing}

class PartitionedCorpusStore:
    """Generic bounded-batch Parquet corpus store; distinct from the runtime table store."""
    def __init__(self,root:Path,dataset_id:str,normalization_version:str,partition_count:int=256,compression:str="zstd",backend=None):
        self.root=Path(root); self.dataset_id=dataset_id; self.normalization_version=normalization_version; self.partition_count=partition_count; self.compression=compression; self.failure=None; self.backend=backend
        if backend is None:
            try:
                import pyarrow as pa,pyarrow.parquet as pq
                self.backend=_ArrowCorpusBackend(pa,pq)
            except ImportError as error:self.failure=f"pyarrow unavailable: {error}"
    @property
    def availability(self):return ("available",None) if self.backend else ("unavailable",self.failure)
    def write_source_manifest(self,payload:dict)->Path:
        forbidden=set(payload)&FORBIDDEN_SOURCE_FIELDS
        if forbidden:raise ValueError(f"benchmark fields forbidden in source manifest: {sorted(forbidden)}")
        path=self.root/self.dataset_id/"raw"/"source_manifest.json"; content={"dataset_id":self.dataset_id,**payload}; text=json.dumps(content,sort_keys=True,indent=2)+"\n"
        if path.exists() and path.read_text()!=text:raise FileExistsError("source manifest identity changed")
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text); return path
    def write_batch(self,tables:Iterable[NormalizedCorpusTable],rejects:Iterable[RejectedCorpusRecord]=())->dict:
        if self.backend is None:raise RuntimeError(self.failure)
        tables=tuple(tables); rejects=tuple(rejects)
        for table in tables:
            if table.source.dataset_id!=self.dataset_id:raise ValueError(f"table dataset identity mismatch: {table.table_id}")
            if table.normalization.version!=self.normalization_version:raise ValueError(f"table normalization version mismatch: {table.table_id}")
        logical_digest=logical_corpus_digest(tables); logical_pairs=sorted((table.table_id,table.normalization.logical_checksum) for table in tables); rejection_records=sorted((asdict(item) for item in rejects),key=_canonical); rejection_digest=_digest(rejection_records); artifact_digest=_digest({"accepted":logical_pairs,"rejected":rejection_records})
        base=self.root/self.dataset_id/"normalized"/f"v{self.normalization_version}"; grouped=defaultdict(list); index=[]
        for table in tables:
            shard=shard_for(table.table_id,self.partition_count); grouped[shard].append(asdict(table)); index.append(asdict(TableIndexEntry(table.table_id,table.source.source_record_id,table.source.page_id,table.source.source_table_id,table.context.page_title,table.context.section_title,table.context.table_caption,table.row_count,table.column_count,shard,table.normalization.logical_checksum,table.normalization.flags)))
        paths=[]
        for shard,records in sorted(grouped.items()):
            path=base/"tables"/f"shard={shard:03d}"/f"part-{artifact_digest}.parquet"; self._write_new(path,records); paths.append(path)
        index_path=None
        if index:index_path=base/"index"/f"table_index-{artifact_digest}.parquet"; self._write_new(index_path,sorted(index,key=lambda row:row["table_id"]))
        reject_path=None
        if rejects:reject_path=base/"rejects"/f"rejected_records-{artifact_digest}.parquet"; self._write_new(reject_path,rejection_records)
        manifest={"dataset_id":self.dataset_id,"normalization_version":self.normalization_version,"partition_count":self.partition_count,"partition_method":"deterministic_sha256","compression":self.compression,"table_count":len(tables),"rejection_count":len(rejects),"logical_batch_digest":logical_digest,"batch_artifact_digest":artifact_digest,"rejection_digest":rejection_digest,"logical_pairs":logical_pairs,"table_files":[str(path.relative_to(base)) for path in paths],"index_file":None if index_path is None else str(index_path.relative_to(base)),"reject_file":None if reject_path is None else str(reject_path.relative_to(base))}
        manifest_path=base/"manifests"/f"batch-{artifact_digest}.json"; manifest_path.parent.mkdir(parents=True,exist_ok=True); text=json.dumps(manifest,sort_keys=True,indent=2)+"\n"
        if manifest_path.exists():raise FileExistsError(f"batch manifest already exists: {manifest_path}")
        manifest_path.write_text(text); return {**manifest,"manifest_path":str(manifest_path)}
    def finalize(self,batch_manifests:Iterable[dict])->dict:
        manifests=tuple(batch_manifests); pairs=[tuple(pair) for manifest in manifests for pair in manifest["logical_pairs"]]
        if len({pair[0] for pair in pairs})!=len(pairs):raise ValueError("duplicate table IDs across corpus batches")
        digest=_digest(sorted(pairs)); base=self.root/self.dataset_id/"normalized"/f"v{self.normalization_version}"
        corpus={"dataset_id":self.dataset_id,"normalization_version":self.normalization_version,"partition_count":self.partition_count,"partition_method":"deterministic_sha256","compression":self.compression,"table_count":sum(item["table_count"] for item in manifests),"rejection_count":sum(item["rejection_count"] for item in manifests),"logical_corpus_digest":digest,"batch_artifact_digests":sorted(item["batch_artifact_digest"] for item in manifests)}
        path=base/"corpus_manifest.json"; text=json.dumps(corpus,sort_keys=True,indent=2)+"\n"
        if path.exists() and path.read_text()!=text:raise FileExistsError("corpus manifest identity changed")
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text); return corpus
    def _write_new(self,path:Path,records:list[dict]):
        if path.exists():raise FileExistsError(f"corpus artifact already exists: {path}")
        self.backend.write(path,records,self.compression)

class _ArrowCorpusBackend:
    def __init__(self,pa,pq):self.pa=pa; self.pq=pq
    def write(self,path:Path,records:list[dict],compression:str):path.parent.mkdir(parents=True,exist_ok=True); self.pq.write_table(self.pa.Table.from_pylist(records),path,compression=compression)

def inspect_archive(url:str)->dict:
    try:
        request=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"intention-corpus-preflight/1.0"})
        with urllib.request.urlopen(request,timeout=30) as response:
            headers=response.headers
            return {"status":"reachable","http_status":response.status,"final_url":response.url,"content_length":int(headers["Content-Length"]) if headers.get("Content-Length") else None,"content_type":headers.get_content_type(),"etag":headers.get("ETag"),"last_modified":headers.get("Last-Modified"),"accept_ranges":headers.get("Accept-Ranges")}
    except Exception as error:return {"status":"blocked","reason":type(error).__name__,"detail":str(error)}

def corpus_preflight(network:bool=False)->dict:
    contract=load_corpus_contract(); acquisition=contract["acquisition"]; net=inspect_archive(acquisition["canonical_download_url"]) if network else {"status":"not_requested","reason":"network checks require explicit --network"}
    blockers=[{"component":"full_archive","reason":"full corpus is not acquired","next_action":"acquire and checksum the canonical archive in M7A.2b"},{"component":"archive_format","reason":"archive internals are not safely verified by HEAD metadata","next_action":"verify after full archive acquisition"},{"component":"redistribution","reason":"redistribution permission requires verification","next_action":"obtain authoritative licensing evidence before redistribution"}]
    if network and net["status"]!="reachable":blockers.append({"component":"network","reason":"canonical archive endpoint could not be reached","detail":net})
    return {"classification":"corpus_preflight","paper_result":False,"benchmark_frozen":False,"corpus_normalized":False,"annotation_started":False,"final_encoder_selected":False,"source_identity":{"dataset_id":contract["dataset_id"],"source_contract":contract["source_contract"]},"acquisition_status":{"full_corpus_status":acquisition["full_corpus_status"],"canonical_download_url":acquisition["canonical_download_url"],"advertised_filename":acquisition["advertised_filename"]},"network_status":net,"archive_metadata":acquisition["recorded_head_evidence"],"format_status":acquisition["format_status"],"license_status":contract["licensing"],"normalization_contract":contract["normalization"],"storage_contract":contract["storage"],"blockers":blockers,"next_gate":"M7A.2b full acquisition and normalization after review"}
