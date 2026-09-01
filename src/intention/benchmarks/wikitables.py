from __future__ import annotations
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
from collections import Counter
from dataclasses import asdict,dataclass,replace
from time import monotonic
from typing import Any,Iterable,Iterator
import json,os,resource,shutil,urllib.request,zipfile
from .corpus import DATASET_ID,NORMALIZATION_VERSION,NormalizationMetadata,NormalizedCorpusTable,PartitionedCorpusStore,RejectedCorpusRecord,_digest,load_corpus_contract,normalize_source_record,qrel_resolution

EXPECTED_ARCHIVE_BYTES=687186284
PINNED_REVISION="ae156771cacc252031d74d61380e09bc1e838bc3"
SOURCE_FIELDS=frozenset({"title","numCols","numericColumns","pgTitle","numDataRows","secondTitle","numHeaderRows","caption","data"})

@dataclass(frozen=True)
class WikiTablesSourceRecord:
    member_name:str; table_id:str; payload:dict[str,Any]

def file_sha256(path:Path,chunk_size:int=8*1024*1024)->str:
    digest=sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(chunk_size),b""):digest.update(chunk)
    return digest.hexdigest()

def verify_zip(path:Path)->dict:
    try:
        with zipfile.ZipFile(path) as archive:
            bad=archive.testzip(); members=len(archive.infolist())
        return {"status":"verified" if bad is None else "failed","member_count":members,"first_bad_member":bad}
    except (OSError,zipfile.BadZipFile) as error:return {"status":"failed","member_count":None,"reason":type(error).__name__,"detail":str(error)}

def _stable_manifest(path:Path,final_url:str|None,zip_result:dict)->dict:
    return {"dataset_id":DATASET_ID,"normalization_version":NORMALIZATION_VERSION,"canonical_url":load_corpus_contract()["acquisition"]["canonical_download_url"],"final_url":final_url,"archive_filename":path.name,"archive_size_bytes":path.stat().st_size,"archive_sha256":file_sha256(path),"zip_integrity_status":zip_result["status"],"archive_member_count":zip_result["member_count"],"acquisition_status":"verified","pinned_repository_revision":PINNED_REVISION}

def acquire_archive(data_root:Path,network:bool=False,opener=urllib.request.urlopen,expected_bytes:int=EXPECTED_ARCHIVE_BYTES,expected_sha256:str|None=None)->dict:
    data_root=Path(data_root); raw=data_root/"raw"/"wikitables-www2018"; archive_path=raw/"WP_tables.zip"; manifest_path=raw/"archive_manifest.json"
    expected_sha256=expected_sha256 or load_corpus_contract()["acquisition"]["archive_sha256"]
    if archive_path.exists():
        if archive_path.stat().st_size!=expected_bytes:raise ValueError("existing archive has unexpected size and will not be overwritten")
        actual_sha256=file_sha256(archive_path)
        if actual_sha256!=expected_sha256:raise ValueError("existing archive SHA-256 does not match the frozen canonical archive and will not be overwritten")
        integrity=verify_zip(archive_path)
        if integrity["status"]!="verified":raise ValueError("existing archive failed ZIP integrity and will not be overwritten")
        previous=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}; stable=_stable_manifest(archive_path,previous.get("stable_identity",previous).get("final_url"),integrity)
        return {"classification":"corpus_acquisition","network_used":False,"reused":True,"stable_identity":stable,"evidence":{"status":"existing_verified"},"archive_path":str(archive_path),"manifest_path":str(manifest_path)}
    if not network:return {"classification":"corpus_acquisition","network_used":False,"reused":False,"status":"blocked","reason":"network acquisition requires explicit --network","archive_path":str(archive_path)}
    usage=shutil.disk_usage(data_root if data_root.exists() else data_root.parent); required=expected_bytes*3
    if usage.free<required:raise RuntimeError(f"insufficient disk space: available={usage.free}, required={required}")
    raw.mkdir(parents=True,exist_ok=True); incomplete=raw/"WP_tables.zip.incomplete"
    if incomplete.exists():incomplete.unlink()
    contract=load_corpus_contract(); url=contract["acquisition"]["canonical_download_url"]; request=urllib.request.Request(url,headers={"User-Agent":"intention-wikitables-acquisition/1.0"})
    try:
        with opener(request,timeout=120) as response,incomplete.open("xb") as output:
            while True:
                chunk=response.read(8*1024*1024)
                if not chunk:break
                output.write(chunk)
            output.flush(); os.fsync(output.fileno()); final_url=response.geturl(); headers={key.lower():value for key,value in response.headers.items()}
        if incomplete.stat().st_size!=expected_bytes:raise ValueError(f"downloaded archive size mismatch: {incomplete.stat().st_size} != {expected_bytes}")
        actual_sha256=file_sha256(incomplete)
        if actual_sha256!=expected_sha256:raise ValueError("downloaded archive SHA-256 does not match the frozen canonical archive")
        integrity=verify_zip(incomplete)
        if integrity["status"]!="verified":raise ValueError(f"downloaded archive failed ZIP integrity: {integrity}")
        incomplete.replace(archive_path); stable=_stable_manifest(archive_path,final_url,integrity)
        evidence={"observed_at":datetime.now(timezone.utc).isoformat(),"http_headers":headers,"disk_total":usage.total,"disk_used":usage.used,"disk_available_before":usage.free}
        manifest={"stable_identity":stable,"acquisition_evidence":evidence}; manifest_path.write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
        return {"classification":"corpus_acquisition","network_used":True,"reused":False,"stable_identity":stable,"evidence":evidence,"archive_path":str(archive_path),"manifest_path":str(manifest_path)}
    except Exception:
        if incomplete.exists():incomplete.unlink()
        raise

def archive_inventory(path:Path)->dict:
    with zipfile.ZipFile(path) as archive:
        items=archive.infolist(); files=[item for item in items if not item.is_dir()]; json_files=[item for item in files if item.filename.endswith(".json")]
        return {"member_count":len(items),"file_count":len(files),"json_member_count":len(json_files),"top_level":sorted({item.filename.split("/",1)[0] for item in items}),"compressed_bytes":sum(item.compress_size for item in items),"uncompressed_bytes":sum(item.file_size for item in items),"largest_member_bytes":max((item.file_size for item in files),default=0),"layout":"single_top_level_directory_with_json_object_members","record_container":"JSON object keyed by canonical table ID","encoding":"UTF-8"}

def _unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError(f"duplicate JSON object key: {key}")
        result[key]=value
    return result

def iter_source_records(path:Path,limit:int|None=None)->Iterator[WikiTablesSourceRecord]:
    emitted=0
    with zipfile.ZipFile(path) as archive:
        names=sorted(item.filename for item in archive.infolist() if not item.is_dir() and item.filename.endswith(".json"))
        for name in names:
            with archive.open(name) as stream:
                collection=json.load(stream,object_pairs_hook=_unique_object)
            if not isinstance(collection,dict):raise ValueError(f"archive member is not a JSON object: {name}")
            for table_id in sorted(collection):
                payload=collection[table_id]
                if not isinstance(payload,dict):raise ValueError(f"source table payload is not an object: {name}#{table_id}")
                yield WikiTablesSourceRecord(name,table_id,payload); emitted+=1
                if limit is not None and emitted>=limit:return

def _raw_checksum(record:WikiTablesSourceRecord)->str:return _digest({"member_name":record.member_name,"table_id":record.table_id,"payload":record.payload})

def adapt_source_record(record:WikiTablesSourceRecord)->NormalizedCorpusTable|RejectedCorpusRecord:
    raw_checksum=_raw_checksum(record); source_id=f"{record.member_name}#{record.table_id}"; payload=record.payload; fields=set(payload)
    if fields!=SOURCE_FIELDS:return RejectedCorpusRecord(source_id,"source_field_contract_mismatch",f"missing={sorted(SOURCE_FIELDS-fields)}, unexpected={sorted(fields-SOURCE_FIELDS)}",raw_checksum)
    headers=payload["title"]; rows=payload["data"]
    if not isinstance(payload["numCols"],int) or not isinstance(payload["numDataRows"],int) or not isinstance(payload["numHeaderRows"],int) or not isinstance(payload["numericColumns"],list):return RejectedCorpusRecord(source_id,"source_metadata_type_mismatch","declared shape/numeric fields have unexpected types",raw_checksum)
    if isinstance(headers,list) and payload["numCols"]!=len(headers):return RejectedCorpusRecord(source_id,"declared_column_count_mismatch",f"numCols={payload['numCols']}, headers={len(headers)}",raw_checksum)
    if isinstance(rows,list) and payload["numDataRows"]!=len(rows):return RejectedCorpusRecord(source_id,"declared_row_count_mismatch",f"numDataRows={payload['numDataRows']}, rows={len(rows)}",raw_checksum)
    mapped={"table_id":record.table_id,"source_record_id":source_id,"page_id":None,"source_table_id":record.table_id,"page_title":payload["pgTitle"],"section_title":payload["secondTitle"],"table_caption":payload["caption"],"headers":headers,"rows":rows}
    normalized=normalize_source_record(mapped,PINNED_REVISION)
    if isinstance(normalized,RejectedCorpusRecord):return replace(normalized,source_checksum=raw_checksum)
    source=replace(normalized.source,source_record_checksum=raw_checksum); provisional=replace(normalized,source=source,normalization=replace(normalized.normalization,logical_checksum="pending")); logical=asdict(provisional); logical["normalization"].pop("logical_checksum")
    return replace(provisional,normalization=replace(provisional.normalization,logical_checksum=_digest(logical)))

def resolve_batch_size(limit:int|None,requested:int|None,contract:dict|None=None)->int:
    if limit is None:
        authoritative=(contract or load_corpus_contract())["verified_corpus"]["batch_size"]
        if requested is not None and requested!=authoritative:raise ValueError(f"full normalization batch size must equal frozen contract value {authoritative}")
        return authoritative
    resolved=10000 if requested is None else requested
    if resolved<1:raise ValueError("batch_size must be positive")
    return resolved

def validate_full_corpus_identity(report:dict,contract:dict|None=None)->None:
    expected=(contract or load_corpus_contract())["verified_corpus"]
    checks={"source_records_attempted":expected["source_records_attempted"],"accepted_tables":expected["accepted_tables"],"rejected_records":expected["rejected_records"],"logical_corpus_digest":expected["logical_corpus_digest"]}
    mismatches={field:{"expected":value,"actual":report.get(field)} for field,value in checks.items() if report.get(field)!=value}
    if mismatches:raise ValueError(f"full corpus reproducibility identity mismatch: {mismatches}")

def normalize_archive(archive_path:Path,store_root:Path,limit:int|None,batch_size:int|None=None,report_path:Path|None=None,store_factory=PartitionedCorpusStore)->dict:
    batch_size=resolve_batch_size(limit,batch_size)
    store=store_factory(store_root,DATASET_ID,NORMALIZATION_VERSION); status,reason=store.availability
    if status!="available":raise RuntimeError(reason)
    started=monotonic(); accepted=[]; rejected=[]; manifests=[]; attempted=0; reasons=Counter(); rows=[]; columns=[]
    def flush():
        nonlocal accepted,rejected
        if accepted or rejected:manifests.append(store.write_batch(accepted,rejected)); accepted=[]; rejected=[]
    for source in iter_source_records(archive_path,limit):
        attempted+=1; item=adapt_source_record(source)
        if isinstance(item,RejectedCorpusRecord):rejected.append(item); reasons[item.reason_code]+=1
        else:accepted.append(item); rows.append(item.row_count); columns.append(item.column_count)
        if len(accepted)+len(rejected)>=batch_size:flush()
    flush(); corpus=store.finalize(manifests); elapsed=monotonic()-started; base=Path(store_root)/DATASET_ID/"normalized"/f"v{NORMALIZATION_VERSION}"; physical=sum(path.stat().st_size for path in base.rglob("*") if path.is_file()); files=list(base.rglob("*")); maximum_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report={"classification":"corpus_normalization","paper_result":False,"dataset_id":DATASET_ID,"normalization_version":NORMALIZATION_VERSION,"limit":limit,"batch_size":batch_size,"source_records_attempted":attempted,"accepted_tables":corpus["table_count"],"rejected_records":corpus["rejection_count"],"rejection_reason_distribution":dict(sorted(reasons.items())),"row_count":{"minimum":min(rows) if rows else 0,"maximum":max(rows) if rows else 0,"sum":sum(rows)},"column_count":{"minimum":min(columns) if columns else 0,"maximum":max(columns) if columns else 0,"sum":sum(columns)},"normalized_physical_bytes":physical,"parquet_table_parts":sum(path.suffix==".parquet" and "tables" in path.parts for path in files),"index_files":sum(path.suffix==".parquet" and "index" in path.parts for path in files),"rejection_files":sum(path.suffix==".parquet" and "rejects" in path.parts for path in files),"batch_manifests":len(manifests),"runtime_seconds":elapsed,"throughput_records_per_second":attempted/elapsed if elapsed else None,"maximum_rss_kb":maximum_rss_kb,"logical_corpus_digest":corpus["logical_corpus_digest"],"corpus_manifest":str(base/"corpus_manifest.json")}
    if limit is None:validate_full_corpus_identity(report)
    if report_path:report_path=Path(report_path); report_path.parent.mkdir(parents=True,exist_ok=True); report_path.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    return report

def audit_qrel_resolution(qrels_path:Path,index_paths:Iterable[Path])->dict:
    import pyarrow.parquet as pq
    resolved=set()
    for path in index_paths:resolved.update(pq.read_table(path,columns=["table_id"]).column("table_id").to_pylist())
    return qrel_resolution_report(qrels_path,resolved)

def qrel_resolution_report(qrels_path:Path,resolved_table_ids:Iterable[str])->dict:
    judgments=[]
    for line in Path(qrels_path).read_text().splitlines():
        query_id,_,table_id,label=line.split(); judgments.append((int(query_id),table_id,int(label)))
    expected={item[1] for item in judgments}; resolution=qrel_resolution(expected,resolved_table_ids); missing=set(resolution["missing_table_ids"]); affected=[item for item in judgments if item[1] in missing]
    return {**resolution,"canonical_judgment_count":len(judgments),"judgments_referencing_missing_tables":len(affected),"missing_judgment_label_distribution":dict(sorted(Counter(item[2] for item in affected).items())),"affected_query_ids":sorted({item[0] for item in affected}),"canonical_qrels_unchanged":True}
