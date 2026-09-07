from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from time import perf_counter
from typing import Any,Callable,Iterable
import importlib.metadata
import json
import math
import os
import platform
import shutil
import subprocess

import yaml

from intention.architecture.embedding import load_embedding_registry
from intention.architecture.serialization import NeuralTableSerializer,load_neural_serialization_policy
from intention.benchmarks.corpus import FORBIDDEN_SOURCE_FIELDS,logical_index_digest,runtime_table_from_normalized_record
from intention.benchmarks.source_audit import load_source_contract
from intention.evaluation.m7b_pilot import SUPPORTED_MODELS,TorchHardwareDetector,_module_contract
from intention.evaluation.topical_bakeoff import evaluate_development_rankings,load_bakeoff_contract,require_exact_search,select_encoder
from intention.retrieval.serialization import select_candidate_depth

ROOT=Path(__file__).resolve().parents[3]
CONFIG_PATH=ROOT/"configs/benchmarks/m7b_full_execution.yaml"
EXECUTION_ORDER_ID="normalized_shard_then_table_id_v1"
EXPECTED_CORPUS_DIGEST="27b811722376d38aa2b37986dc3ff713869e7ae76fa5c399929905b8b31c589c"
EXPECTED_TABLE_COUNT=1_652_771
EXPECTED_SERIALIZATION_HASH="1b37ffbfb3b0a47ea053f315d064427a0c61bdcac2ec8413bdd593ee46507290"
MODEL_ORDER=("Qwen3-Embedding-0.6B","Nemotron-3-Embed-1B-BF16","Qwen3-Embedding-4B")

def _sha(path:Path)->str:
    digest=sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):digest.update(block)
    return digest.hexdigest()

def _ids_digest(table_ids:Iterable[str])->str:
    digest=sha256()
    for table_id in table_ids:digest.update(table_id.encode("utf-8")+b"\n")
    return digest.hexdigest()

def _finite_nonnegative(value):return isinstance(value,(int,float)) and math.isfinite(value) and value>=0

def load_full_execution_contract(path:Path|None=None)->dict:
    raw=yaml.safe_load((path or CONFIG_PATH).read_text())
    required={"version","execution_id","corpus_iteration","partition_count","vector_dtype","vector_format","normalization","resume_policy","exact_backend","exact_compute_dtype","allow_tf32","top_k","maximum_exact_search_seconds_per_model","minimum_free_disk_gib_before_full_execution","batch_sizes","oom_policy","minimum_batch_size"}
    expected={"version":"1.0.0","execution_id":"m7b-full-corpus-v1","corpus_iteration":EXECUTION_ORDER_ID,"partition_count":256,"vector_dtype":"float32","vector_format":"npy","normalization":"l2","resume_policy":"checksum_verified_atomic_shards","exact_backend":"sharded_torch_matmul","exact_compute_dtype":"float32","allow_tf32":False,"top_k":100,"maximum_exact_search_seconds_per_model":7200,"minimum_free_disk_gib_before_full_execution":100,"batch_sizes":{"Qwen3-Embedding-0.6B":64,"Nemotron-3-Embed-1B-BF16":128,"Qwen3-Embedding-4B":32},"oom_policy":"halve_batch_and_continue","minimum_batch_size":1}
    if not isinstance(raw,dict) or set(raw)!=required or raw!=expected:raise ValueError("invalid M7B full-execution contract")
    return raw

def _normalized_roots(data_root:Path)->list[Path]:
    return sorted(Path(data_root).glob("normalized/*/wikitables_www2018/normalized/v1.0.0"))

def resolve_normalized_root(data_root:Path)->Path:
    valid=[]
    for root in _normalized_roots(data_root):
        manifest=root/"corpus_manifest.json"
        if manifest.is_file():
            payload=json.loads(manifest.read_text())
            if payload.get("table_count")==EXPECTED_TABLE_COUNT and payload.get("logical_corpus_digest")==EXPECTED_CORPUS_DIGEST and payload.get("partition_count")==256:valid.append(root)
    if not valid:raise FileNotFoundError("verified normalized WikiTables corpus unavailable")
    authoritative=[root for root in valid if "authoritative" in root.parts[-4]]
    return (authoritative or valid)[0]

def _read_index(root:Path,index_reader=None)->list[dict]:
    paths=sorted((root/"index").glob("*.parquet"))
    if not paths:raise FileNotFoundError("normalized lightweight index unavailable")
    if index_reader is not None:return list(index_reader(paths))
    import pyarrow.dataset as ds
    return ds.dataset([str(path) for path in paths],format="parquet").to_table(columns=["table_id","shard","logical_checksum"]).to_pylist()

def inspect_corpus_identity(data_root:Path,index_reader=None,normalized_root:Path|None=None,expected_count=EXPECTED_TABLE_COUNT,expected_digest=EXPECTED_CORPUS_DIGEST,partition_count=256)->dict:
    root=Path(normalized_root) if normalized_root else resolve_normalized_root(Path(data_root))
    records=_read_index(root,index_reader)
    ids=[row.get("table_id") for row in records]
    if len(records)!=expected_count:raise ValueError(f"corpus count mismatch: {len(records)} != {expected_count}")
    if any(not isinstance(table_id,str) or not table_id for table_id in ids):raise ValueError("invalid table ID in normalized index")
    if len(ids)!=len(set(ids)):raise ValueError("duplicate table IDs in normalized index")
    if any(not isinstance(row.get("logical_checksum"),str) or len(row["logical_checksum"])!=64 for row in records):raise ValueError("missing logical checksum in normalized index")
    shards={row.get("shard") for row in records}
    if shards!=set(range(partition_count)):raise ValueError("normalized index does not declare exactly 256 shards")
    logical=logical_index_digest((row["table_id"],row["logical_checksum"]) for row in records)
    if logical!=expected_digest:raise ValueError("logical corpus digest mismatch")
    grouped={shard:[] for shard in range(partition_count)}
    for row in records:grouped[row["shard"]].append(row["table_id"])
    ordered=[]; shard_identities={}
    for shard in range(partition_count):
        shard_ids=sorted(grouped[shard]); ordered.extend(shard_ids)
        shard_identities[str(shard)]={"expected_table_count":len(shard_ids),"expected_ordered_table_id_digest":_ids_digest(shard_ids)}
    return {"normalized_root":str(root),"count":len(ordered),"logical_digest":logical,"partition_count":partition_count,"execution_order_id":EXECUTION_ORDER_ID,"full_table_id_digest":_ids_digest(ordered),"shards":shard_identities}

def _version(distribution):
    try:return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:return None

def _repository_commit():
    try:return subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    except Exception:return None

def full_preflight(data_root:Path,artifact_root:Path,index_reader=None,normalized_root:Path|None=None,hardware_detector=None)->dict:
    operational=load_full_execution_contract(); bakeoff=load_bakeoff_contract(); corpus=inspect_corpus_identity(data_root,index_reader,normalized_root)
    policy=load_neural_serialization_policy()
    if (policy.serialization_id,policy.version,policy.digest)!=("neural_table_evidence_v1","1.1.0",EXPECTED_SERIALIZATION_HASH):raise ValueError("serialization identity mismatch")
    registry=load_embedding_registry(); models=[]
    for name in MODEL_ORDER:
        record=registry.models[name].record; declared=bakeoff["models"][name]
        if max(record["dimensions"])!=declared["dimension"] or record.get("trust_remote_code_required") is not False:raise ValueError(f"model contract mismatch: {name}")
        models.append({"name":name,"model":record["model"],"revision":record["revision"],"tokenizer_revision":record["tokenizer_revision"],"expected_dimension":declared["dimension"],"configured_full_batch":operational["batch_sizes"][name],"runtime_availability":record["availability"],"trust_remote_code":False})
    try:
        import torch
        hardware=(hardware_detector or TorchHardwareDetector(torch)).detect()
        environment={"python":platform.python_version(),"torch":torch.__version__,"torch_cuda":torch.version.cuda,"transformers":_version("transformers"),"sentence_transformers":_version("sentence-transformers"),"huggingface_hub":_version("huggingface-hub")}
    except ImportError:
        hardware=TorchHardwareDetector(type("T",(),{"cuda":type("C",(),{"is_available":lambda _:False})()})()).detect()
        environment={"python":platform.python_version(),"torch":None,"torch_cuda":None,"transformers":_version("transformers"),"sentence_transformers":_version("sentence-transformers"),"huggingface_hub":_version("huggingface-hub")}
    artifact_root=Path(artifact_root); nearest=artifact_root
    while not nearest.exists() and nearest!=nearest.parent:nearest=nearest.parent
    usage=shutil.disk_usage(nearest); minimum=operational["minimum_free_disk_gib_before_full_execution"]*1024**3
    return {"classification":"m7b_full_corpus_preflight","paper_result":False,"repository_commit":_repository_commit(),"operational_contract":{"version":operational["version"],"execution_id":operational["execution_id"],"sha256":_sha(CONFIG_PATH)},"corpus":corpus,"serialization":{"id":policy.serialization_id,"version":policy.version,"hash":policy.digest},"models":models,"environment":environment,"hardware":{"cuda_available":hardware.cuda_available,"device":hardware.gpu_name,"vram_bytes":hardware.total_vram_bytes,"bf16_supported":hardware.bf16_supported},"storage":{"artifact_root":str(artifact_root),"free_bytes":usage.free,"free_gib":usage.free/1024**3,"minimum_required_gib":operational["minimum_free_disk_gib_before_full_execution"],"passed":usage.free>=minimum},"external_api_spend_usd":0,"holdout":"locked_not_evaluated","holdout_qrels_materialized":False}

def _vector_checks(vectors,dimension:int,tolerance=.01)->dict:
    import numpy as np
    if not isinstance(vectors,np.ndarray) or vectors.dtype!=np.float32 or vectors.ndim!=2 or vectors.shape[1]!=dimension:raise ValueError("persisted vectors must be 2D float32 with the declared dimension")
    finite=bool(np.isfinite(vectors).all()); norms=np.linalg.norm(vectors,axis=1); nonzero=bool((norms>0).all()); deviation=float(np.max(np.abs(norms-1))) if len(norms) else 0.0; l2=bool(deviation<=tolerance)
    if not (finite and nonzero and l2):raise ValueError("vector finite/nonzero/L2 validation failed")
    return {"finite":finite,"nonzero":nonzero,"l2":l2,"maximum_norm_deviation":deviation}

def _expected_shard_identity(model_name:str,source_shard:int,corpus:dict,batch_size:int|None)->dict:
    operational=load_full_execution_contract(); registry=load_embedding_registry(); record=registry.models[model_name].record; policy=load_neural_serialization_policy()
    result={"execution_id":operational["execution_id"],"corpus_digest":corpus["logical_digest"],"execution_order_id":corpus["execution_order_id"],"full_table_id_digest":corpus["full_table_id_digest"],"source_shard":source_shard,"model":record["model"],"model_revision":record["revision"],"tokenizer_revision":record["tokenizer_revision"],"dimension":max(record["dimensions"]),"dtype":"float32","serialization_id":policy.serialization_id,"serialization_version":policy.version,"serialization_hash":policy.digest}
    shard_expectation=corpus.get("shards",{}).get(str(source_shard))
    if not isinstance(shard_expectation,dict):raise ValueError(f"missing verified index identity for source shard {source_shard}")
    result.update({"table_count":shard_expectation.get("expected_table_count"),"ordered_table_id_digest":shard_expectation.get("expected_ordered_table_id_digest")})
    if batch_size is not None:result["selected_batch_size"]=batch_size
    return result

def validate_complete_shard(shard_dir:Path,expected:dict|None=None)->dict:
    shard_dir=Path(shard_dir); manifest_path=shard_dir/"shard-manifest.json"; vector_path=shard_dir/"vectors.npy"; ids_path=shard_dir/"table_ids.txt"
    if not all(path.is_file() for path in (manifest_path,vector_path,ids_path)):raise FileNotFoundError("complete shard artifacts are missing")
    manifest=json.loads(manifest_path.read_text())
    required={"execution_id","corpus_digest","execution_order_id","full_table_id_digest","source_shard","table_count","ordered_table_id_digest","model","model_revision","tokenizer_revision","dimension","dtype","serialization_id","serialization_version","serialization_hash","selected_batch_size","vector_sha256","table_id_sha256","finite_check","nonzero_check","l2_check","serialization_seconds","embedding_inference_seconds","artifact_write_seconds","total_shard_wall_seconds","status"}
    if set(manifest)!=required or manifest["status"]!="complete":raise ValueError("invalid complete shard manifest")
    if expected and any(manifest.get(key)!=value for key,value in expected.items()):raise ValueError("complete shard identity mismatch")
    if manifest["vector_sha256"]!=_sha(vector_path) or manifest["table_id_sha256"]!=_sha(ids_path):raise ValueError("complete shard checksum mismatch")
    table_ids=ids_path.read_text().splitlines()
    if len(table_ids)!=manifest["table_count"] or len(table_ids)!=len(set(table_ids)) or table_ids!=sorted(table_ids) or _ids_digest(table_ids)!=manifest["ordered_table_id_digest"]:raise ValueError("complete shard table-ID mapping mismatch")
    import numpy as np
    vectors=np.load(vector_path,mmap_mode="r",allow_pickle=False); checks=_vector_checks(vectors,manifest["dimension"])
    if vectors.shape[0]!=len(table_ids) or not all((manifest["finite_check"]==checks["finite"],manifest["nonzero_check"]==checks["nonzero"],manifest["l2_check"]==checks["l2"])):raise ValueError("complete shard vector alignment mismatch")
    if any(not _finite_nonnegative(manifest[key]) for key in ("serialization_seconds","embedding_inference_seconds","artifact_write_seconds","total_shard_wall_seconds")):raise ValueError("invalid shard timing")
    return manifest

def promote_complete_shard(shard_dir:Path,table_ids:list[str],vectors,identity:dict,embedding_seconds:float,total_seconds:float,serialization_seconds=0.0)->dict:
    import numpy as np
    shard_dir=Path(shard_dir); tmp=shard_dir.with_name("."+shard_dir.name+".tmp")
    if tmp.exists():shutil.rmtree(tmp)
    if shard_dir.exists():return validate_complete_shard(shard_dir,identity)
    tmp.mkdir(parents=True)
    ids_tmp=tmp/"table_ids.txt.tmp"; vector_tmp=tmp/"vectors.npy.tmp"; manifest_tmp=tmp/"shard-manifest.json.tmp"
    if table_ids!=sorted(table_ids) or len(table_ids)!=len(set(table_ids)):raise ValueError("shard table IDs must be unique canonical order")
    vectors=np.asarray(vectors,dtype=np.float32); checks=_vector_checks(vectors,identity["dimension"])
    if vectors.shape[0]!=len(table_ids):raise ValueError("vector rows do not align with table IDs")
    write_started=perf_counter()
    with ids_tmp.open("w",encoding="utf-8") as stream:
        stream.write("".join(table_id+"\n" for table_id in table_ids)); stream.flush(); os.fsync(stream.fileno())
    with vector_tmp.open("wb") as stream:
        np.save(stream,vectors,allow_pickle=False); stream.flush(); os.fsync(stream.fileno())
    artifact_seconds=perf_counter()-write_started
    manifest={**identity,"table_count":len(table_ids),"ordered_table_id_digest":_ids_digest(table_ids),"vector_sha256":_sha(vector_tmp),"table_id_sha256":_sha(ids_tmp),"finite_check":checks["finite"],"nonzero_check":checks["nonzero"],"l2_check":checks["l2"],"serialization_seconds":float(serialization_seconds),"embedding_inference_seconds":float(embedding_seconds),"artifact_write_seconds":artifact_seconds,"total_shard_wall_seconds":float(total_seconds)+artifact_seconds,"status":"complete"}
    with manifest_tmp.open("w",encoding="utf-8") as stream:
        stream.write(json.dumps(manifest,sort_keys=True,indent=2)+"\n"); stream.flush(); os.fsync(stream.fileno())
    os.replace(ids_tmp,tmp/"table_ids.txt"); os.replace(vector_tmp,tmp/"vectors.npy"); os.replace(manifest_tmp,tmp/"shard-manifest.json")
    validate_complete_shard(tmp,identity); shard_dir.parent.mkdir(parents=True,exist_ok=True); os.replace(tmp,shard_dir)
    return validate_complete_shard(shard_dir,identity)

def encode_with_oom_retry(texts:list[str],encode_batch:Callable[[list[str],int],Any],initial_batch_size:int,minimum_batch_size=1,cuda=None):
    import numpy as np
    offset=0; batch_size=initial_batch_size; pieces=[]; events=[]; inference_seconds=0.0
    while offset<len(texts):
        batch=texts[offset:offset+batch_size]; started=perf_counter()
        try:
            vectors=encode_batch(batch,batch_size); elapsed=perf_counter()-started; inference_seconds+=elapsed
            if len(vectors)!=len(batch):raise ValueError("encoder dropped records")
            pieces.append(np.asarray(vectors,dtype=np.float32)); offset+=len(batch)
        except Exception as error:
            elapsed=perf_counter()-started; inference_seconds+=elapsed
            oom=error.__class__.__name__=="OutOfMemoryError" or "out of memory" in str(error).lower()
            if not oom:raise
            if batch_size<=minimum_batch_size:raise RuntimeError(json.dumps({"status":"failed","code":"cuda_oom_at_minimum_batch","batch_size":batch_size,"record_offset":offset})) from error
            reduced=max(minimum_batch_size,batch_size//2); events.append({"record_offset":offset,"failed_batch_size":batch_size,"new_batch_size":reduced,"same_records_retried":True}); batch_size=reduced
            if cuda is not None:
                try:cuda.empty_cache()
                except Exception:pass
    return np.concatenate(pieces,axis=0) if pieces else np.empty((0,0),dtype=np.float32),batch_size,events,inference_seconds

def _atomic_json(path:Path,payload:dict):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp")
    with tmp.open("w",encoding="utf-8") as stream:
        stream.write(json.dumps(payload,sort_keys=True,indent=2)+"\n"); stream.flush(); os.fsync(stream.fileno())
    os.replace(tmp,path)

def _load_source_shard(normalized_root:Path,shard:int)->list[dict]:
    import pyarrow.dataset as ds
    path=normalized_root/"tables"/f"shard={shard:03d}"
    if not path.is_dir():raise FileNotFoundError(f"normalized source shard missing: {shard}")
    return sorted(ds.dataset(str(path),format="parquet").to_table().to_pylist(),key=lambda row:row["table_id"])

def _verify_physical_source_shard(records:Iterable[dict],source_shard:int,corpus:dict)->list[dict]:
    records=list(records); expectation=corpus.get("shards",{}).get(str(source_shard),{})
    expected_count=expectation.get("expected_table_count"); expected_digest=expectation.get("expected_ordered_table_id_digest")
    raw_ids=[record.get("table_id") if isinstance(record,dict) else None for record in records]
    valid_ids=all(isinstance(table_id,str) and bool(table_id) for table_id in raw_ids)
    unique=valid_ids and len(raw_ids)==len(set(raw_ids)); canonical=valid_ids and raw_ids==sorted(raw_ids)
    actual_digest=_ids_digest(raw_ids) if valid_ids else None
    if not (isinstance(expected_count,int) and isinstance(expected_digest,str) and len(expected_digest)==64 and len(records)==expected_count and unique and canonical and actual_digest==expected_digest):
        raise RuntimeError(json.dumps({"status":"failed","code":"physical_source_shard_identity_mismatch","source_shard":source_shard,"expected_table_count":expected_count,"actual_table_count":len(records),"expected_ordered_table_id_digest":expected_digest,"actual_ordered_table_id_digest":actual_digest},sort_keys=True))
    return records

def serialize_normalized_records(records:Iterable[dict],serializer=None)->tuple[list[str],list[str]]:
    serializer=serializer or NeuralTableSerializer(); records=list(records)
    if any(set(record)&FORBIDDEN_SOURCE_FIELDS for record in records):raise ValueError("normalized source contains structurally forbidden benchmark metadata")
    table_ids=[]; texts=[]
    for record in records:
        table=runtime_table_from_normalized_record(record); table_ids.append(table.table_id); texts.append(serializer.serialize(table).text)
    if table_ids!=sorted(table_ids) or len(table_ids)!=len(set(table_ids)):raise ValueError("normalized shard is not in unique canonical table-ID order")
    return table_ids,texts

def _load_runtime_model(model_name:str,device:str,model_factory=None,torch_module=None):
    if model_name not in SUPPORTED_MODELS:raise ValueError(f"unsupported M7B model: {model_name}")
    import torch
    torch=torch_module or torch; record=load_embedding_registry().models[model_name].record
    if device not in {"cuda","cuda:0"}:raise ValueError("full M7B encoding requires CUDA")
    if not TorchHardwareDetector(torch).detect().cuda_available:raise RuntimeError("CUDA accelerator unavailable; no substitution allowed")
    if model_factory is None:
        from sentence_transformers import SentenceTransformer
        model_factory=SentenceTransformer
    started=perf_counter(); model=model_factory(record["model"],revision=record["revision"],device="cuda:0",trust_remote_code=False,model_kwargs={"torch_dtype":torch.bfloat16}); load_seconds=perf_counter()-started
    model_commit=getattr(getattr(getattr(model,"_first_module",lambda:None)(),"auto_model",None),"config",None); model_commit=getattr(model_commit,"_commit_hash",None)
    tokenizer=getattr(model,"tokenizer",None); tokenizer_commit=getattr(tokenizer,"init_kwargs",{}).get("_commit_hash")
    if tokenizer_commit is None:
        from huggingface_hub import try_to_load_from_cache
        cached=try_to_load_from_cache(record["model"],"tokenizer_config.json",revision=record["tokenizer_revision"]); parts=Path(cached).parts if isinstance(cached,str) else ()
        tokenizer_commit=next((part for part in parts if part==record["tokenizer_revision"]),None)
    if model_commit!=record["revision"] or tokenizer_commit!=record["tokenizer_revision"]:raise RuntimeError("pinned model/tokenizer revision verification failed")
    pooling=_module_contract(model,model_name)
    return model,record,torch,load_seconds,pooling

def full_encode(model_name:str,data_root:Path,artifact_root:Path,device="cuda",confirm_full_corpus=False,model_factory=None,torch_module=None,preflight_fn=full_preflight,shard_reader=None)->dict:
    if not confirm_full_corpus:raise PermissionError("--confirm-full-corpus is required before model loading")
    if model_name not in MODEL_ORDER:raise ValueError(f"unsupported M7B model: {model_name}")
    operational=load_full_execution_contract(); preflight=preflight_fn(Path(data_root),Path(artifact_root))
    if not preflight["storage"]["passed"]:raise RuntimeError("minimum free-disk gate failed before model loading")
    corpus=preflight["corpus"]; normalized_root=Path(corpus["normalized_root"]); model,record,torch,load_seconds,pooling=_load_runtime_model(model_name,device,model_factory,torch_module)
    model_root=Path(artifact_root)/model_name; identity={"execution_id":operational["execution_id"],"model_name":model_name,"model":record["model"],"revision":record["revision"],"tokenizer_revision":record["tokenizer_revision"],"dimension":max(record["dimensions"]),"precision":"bfloat16","persisted_dtype":"float32","quantization":False,"trust_remote_code":False,"pooling":pooling,"corpus":corpus,"serialization":preflight["serialization"]}
    identity_path=model_root/"identity.json"
    if identity_path.exists() and json.loads(identity_path.read_text())!=identity:raise ValueError("model execution identity mismatch")
    if not identity_path.exists():_atomic_json(identity_path,identity)
    serializer=NeuralTableSerializer(); selected_batch=operational["batch_sizes"][model_name]; oom_events=[]; manifests=[]
    for shard in range(operational["partition_count"]):
        expected=_expected_shard_identity(model_name,shard,corpus,None); shard_dir=model_root/"shards"/f"shard-{shard:03d}"
        if shard_dir.exists():
            manifest=validate_complete_shard(shard_dir,expected); selected_batch=manifest["selected_batch_size"]; manifests.append(manifest); continue
        shard_started=perf_counter(); records=(shard_reader or _load_source_shard)(normalized_root,shard)
        records=_verify_physical_source_shard(records,shard,corpus)
        serialization_started=perf_counter(); table_ids,texts=serialize_normalized_records(records,serializer)
        serialization_seconds=perf_counter()-serialization_started
        formatted=[record["document_instruction"].replace("{content}",text) if record["document_instruction"] else text for text in texts]
        def encode_batch(batch,size):
            tokenizer=getattr(model,"tokenizer",None)
            if tokenizer is not None:
                lengths=[len(tokens) for tokens in tokenizer(batch,add_special_tokens=True,truncation=False)["input_ids"]]
                if any(length>record["maximum_input_tokens"] for length in lengths):raise RuntimeError("truncation-policy violation")
            with torch.inference_mode():return model.encode(batch,batch_size=size,normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
        vectors,used_batch,events,inference=encode_with_oom_retry(formatted,encode_batch,selected_batch,operational["minimum_batch_size"],torch.cuda); selected_batch=used_batch; oom_events.extend({"source_shard":shard,**event} for event in events)
        expected=_expected_shard_identity(model_name,shard,corpus,selected_batch); manifest=promote_complete_shard(shard_dir,table_ids,vectors,expected,inference,perf_counter()-shard_started,serialization_seconds); manifests.append(manifest)
        _atomic_json(model_root/"encode-progress.json",{"status":"in_progress","completed_shards":len(manifests),"partition_count":256,"selected_batch_size":selected_batch,"oom_events":oom_events})
    vector_bytes=sum((model_root/"shards"/f"shard-{shard:03d}"/"vectors.npy").stat().st_size for shard in range(256)); id_bytes=sum((model_root/"shards"/f"shard-{shard:03d}"/"table_ids.txt").stat().st_size for shard in range(256))
    totals={key:sum(item[key] for item in manifests) for key in ("serialization_seconds","embedding_inference_seconds","artifact_write_seconds","total_shard_wall_seconds")}
    report={"classification":"m7b_full_corpus_encoding","paper_result":False,"status":"complete","model":model_name,"corpus":corpus,"serialization":preflight["serialization"],"model_load_seconds":load_seconds,**totals,"embedding_wall_seconds":totals["embedding_inference_seconds"],"total_wall_seconds":load_seconds+totals["total_shard_wall_seconds"],"selected_batch_size":selected_batch,"batch_changes":oom_events,"raw_vector_payload_bytes":sum(item["table_count"]*item["dimension"]*4 for item in manifests),"physical_index_bytes":vector_bytes+id_bytes,"physical_index_byte_definition":"vectors.npy plus table_ids.txt across all 256 shards; manifests, reports, and logs excluded","external_api_spend_usd":0,"holdout":"locked_not_evaluated"}
    _atomic_json(model_root/"full-encode-report.json",report); _atomic_json(model_root/"encode-progress.json",{"status":"complete","completed_shards":256,"partition_count":256,"selected_batch_size":selected_batch,"oom_events":oom_events}); return report

def validate_full_index(model_name:str,artifact_root:Path)->dict:
    model_root=Path(artifact_root)/model_name; identity_path=model_root/"identity.json"; report_path=model_root/"full-encode-report.json"
    if not identity_path.is_file() or not report_path.is_file():raise FileNotFoundError("complete full-corpus encoding is unavailable")
    identity=json.loads(identity_path.read_text()); report=json.loads(report_path.read_text())
    if report.get("status")!="complete" or report.get("model")!=model_name:raise ValueError("full encoding report is incomplete")
    corpus=identity.get("corpus",{}); manifests=[]; digest=sha256(); observed=set(); physical_index_bytes=0
    for shard in range(256):
        shard_root=model_root/"shards"/f"shard-{shard:03d}"; manifests.append(validate_complete_shard(shard_root,_expected_shard_identity(model_name,shard,corpus,None)))
        physical_index_bytes+=(shard_root/"vectors.npy").stat().st_size+(shard_root/"table_ids.txt").stat().st_size
        for table_id in shard_root.joinpath("table_ids.txt").read_text().splitlines():
            if table_id in observed:raise ValueError("duplicate table ID across exact-index shards")
            observed.add(table_id); digest.update(table_id.encode("utf-8")+b"\n")
    if sum(item["table_count"] for item in manifests)!=EXPECTED_TABLE_COUNT:raise ValueError("validated full index table count mismatch")
    if digest.hexdigest()!=corpus.get("full_table_id_digest"):raise ValueError("full exact-index execution-order digest mismatch")
    embedding_wall_seconds=sum(item["embedding_inference_seconds"] for item in manifests)
    reported_seconds=report.get("embedding_wall_seconds"); reported_bytes=report.get("physical_index_bytes")
    if not _finite_nonnegative(reported_seconds) or not math.isclose(reported_seconds,embedding_wall_seconds,rel_tol=1e-12,abs_tol=1e-12):raise ValueError("full encoding report embedding wall time does not match validated shard manifests")
    if not isinstance(reported_bytes,int) or isinstance(reported_bytes,bool) or reported_bytes!=physical_index_bytes:raise ValueError("full encoding report physical index bytes do not match validated shard files")
    return {"model_root":model_root,"identity":identity,"report":report,"manifests":manifests,"validated_embedding_wall_seconds":embedding_wall_seconds,"validated_physical_index_bytes":physical_index_bytes}

def load_development_sources(source_root:Path,contract=None)->dict:
    contract=contract or load_bakeoff_contract(); source=load_source_contract(); queries_path=Path(source_root)/source["resources"]["queries"]["path"]; qrels_path=Path(source_root)/source["resources"]["qrels"]["path"]
    for name,path in (("queries",queries_path),("qrels",qrels_path)):
        if not path.is_file():raise FileNotFoundError(f"canonical {name} unavailable")
        if _sha(path)!=source["resources"][name]["sha256"]:raise ValueError(f"canonical {name} SHA-256 mismatch")
    development=set(contract["split"]["development_ids"]); holdout=set(contract["split"]["holdout_ids"]); queries={}
    for line in queries_path.read_text(encoding="utf-8").splitlines():
        fields=line.split(maxsplit=1); query_id=int(fields[0])
        if query_id in holdout:continue
        if query_id not in development or len(fields)!=2 or not fields[1].strip():raise ValueError("invalid canonical development query")
        queries[query_id]=fields[1].strip()
    qrels={query_id:{} for query_id in development}; parsed_total=0
    for line in qrels_path.read_text(encoding="utf-8").splitlines():
        query_id=int(line.split(maxsplit=1)[0]); parsed_total+=1
        if query_id in holdout:continue
        fields=line.split()
        if query_id not in development or len(fields)!=4:raise ValueError("invalid canonical development qrel")
        table_id=fields[2]; label=int(fields[3])
        if table_id in qrels[query_id]:raise ValueError("duplicate canonical qrel")
        qrels[query_id][table_id]=label
    if set(queries)!=development or set(qrels)!=development or parsed_total!=contract["qrels"]["judgment_count"]:raise ValueError("canonical development source completeness mismatch")
    return {"queries":dict(sorted(queries.items())),"qrels":dict(sorted(qrels.items())),"query_sha256":_sha(queries_path),"qrels_sha256":_sha(qrels_path),"canonical_qrel_judgments":parsed_total,"holdout_qrels_materialized":False,"holdout":"locked_not_evaluated"}

def exact_search_shards(query_vectors,shards:Iterable[tuple[list[str],Any]],top_k=100,device="cpu",torch_module=None,maximum_seconds=7200)->dict:
    import numpy as np
    if torch_module is None:import torch as torch_module
    torch=torch_module; queries=np.asarray(query_vectors,dtype=np.float32); _vector_checks(queries,queries.shape[1])
    if top_k<1:raise ValueError("top_k must be positive")
    if hasattr(torch.backends,"cuda") and hasattr(torch.backends.cuda,"matmul"):torch.backends.cuda.matmul.allow_tf32=False
    if hasattr(torch.backends,"cudnn"):torch.backends.cudnn.allow_tf32=False
    candidates=[[] for _ in range(len(queries))]; all_ids=set(); searched=0; started=perf_counter()
    query_tensor=torch.as_tensor(queries,dtype=torch.float32,device=device)
    for table_ids,vectors in shards:
        vectors=np.asarray(vectors)
        if vectors.dtype!=np.float32:raise ValueError("exact index vectors must be persisted float32")
        _vector_checks(vectors,queries.shape[1])
        if len(table_ids)!=len(vectors) or len(table_ids)!=len(set(table_ids)) or all_ids.intersection(table_ids):raise ValueError("exact index table-ID alignment/uniqueness failure")
        all_ids.update(table_ids); searched+=len(table_ids); scores=(query_tensor@torch.as_tensor(vectors,dtype=torch.float32,device=device).T).detach().cpu().numpy()
        for query_index,row in enumerate(scores):
            local=sorted(zip(table_ids,(float(value) for value in row)),key=lambda item:(-item[1],item[0]))[:top_k]
            candidates[query_index]=sorted([*candidates[query_index],*local],key=lambda item:(-item[1],item[0]))[:top_k]
        if perf_counter()-started>maximum_seconds:raise TimeoutError("exact development search exceeded two-hour model limit")
    elapsed=perf_counter()-started; require_exact_search(True,elapsed)
    rankings=[]
    for ranking in candidates:
        ids=[item[0] for item in ranking]
        if len(ids)!=len(set(ids)):raise ValueError("duplicate exact top-k table ID")
        rankings.append([{"rank":rank,"table_id":table_id,"score":score} for rank,(table_id,score) in enumerate(ranking,1)])
    return {"rankings":rankings,"searched_table_count":searched,"exact_search_seconds":elapsed,"backend":"sharded_torch_matmul","compute_dtype":"float32","allow_tf32":False,"tie_policy":"score_descending_then_table_id_ascending"}

def _artifact_shards(model_root:Path):
    import numpy as np
    for shard in range(256):
        root=model_root/"shards"/f"shard-{shard:03d}"
        yield root.joinpath("table_ids.txt").read_text().splitlines(),np.load(root/"vectors.npy",mmap_mode="r",allow_pickle=False)

def _atomic_npy(path:Path,vectors):
    import numpy as np
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp")
    with tmp.open("wb") as stream:
        np.save(stream,np.asarray(vectors,dtype=np.float32),allow_pickle=False); stream.flush(); os.fsync(stream.fileno())
    os.replace(tmp,path)

def exact_development_evaluate(model_name:str,source_root:Path,artifact_root:Path,device="cuda",model_factory=None,torch_module=None,index_validator=validate_full_index,source_loader=load_development_sources,search_fn=exact_search_shards)->dict:
    validated=index_validator(model_name,Path(artifact_root)); sources=source_loader(Path(source_root)); model,record,torch,load_seconds,pooling=_load_runtime_model(model_name,device,model_factory,torch_module)
    query_ids=list(sources["queries"]); raw=[sources["queries"][query_id] for query_id in query_ids]; formatted=[record["query_instruction"].replace("{content}",text) if record["query_instruction"] else text for text in raw]
    tokenizer=getattr(model,"tokenizer",None)
    if tokenizer is not None and any(len(tokens)>record["maximum_input_tokens"] for tokens in tokenizer(formatted,add_special_tokens=True,truncation=False)["input_ids"]):raise RuntimeError("query truncation-policy violation")
    started=perf_counter()
    with torch.inference_mode():vectors=model.encode(formatted,batch_size=len(formatted),normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
    query_seconds=perf_counter()-started
    import numpy as np
    vectors=np.asarray(vectors,dtype=np.float32); _vector_checks(vectors,max(record["dimensions"])); query_vector_path=validated["model_root"]/"development-query-vectors.npy"; _atomic_npy(query_vector_path,vectors)
    search=search_fn(vectors,_artifact_shards(validated["model_root"]),top_k=100,device=device,maximum_seconds=load_full_execution_contract()["maximum_exact_search_seconds_per_model"])
    if search["searched_table_count"]!=EXPECTED_TABLE_COUNT or any(len(row)!=100 for row in search["rankings"]):raise ValueError("exact full-corpus top-100 completeness failure")
    rankings={query_id:[item["table_id"] for item in search["rankings"][index]] for index,query_id in enumerate(query_ids)}
    evaluation=evaluate_development_rankings(rankings,sources["qrels"],query_ids)
    ranking_report={"classification":"m7b_exact_development_rankings","paper_result":False,"model":model_name,"model_identity":validated["identity"],"query_ids":query_ids,"query_sha256":sources["query_sha256"],"qrels_sha256":sources["qrels_sha256"],"canonical_qrel_judgments":sources["canonical_qrel_judgments"],"holdout":"locked_not_evaluated","holdout_qrels_materialized":False,"query_vector_dtype":"float32","query_vector_sha256":_sha(query_vector_path),"model_load_seconds":load_seconds,"query_embedding_seconds":query_seconds,**search}
    _atomic_json(validated["model_root"]/"exact-development-rankings.json",ranking_report); _atomic_json(validated["model_root"]/"development-evaluation.json",evaluation); return {"rankings":ranking_report,"evaluation":evaluation}

def provisional_select(artifact_root:Path,index_validator=validate_full_index)->dict:
    results=[]; missing=[]; evaluations={}
    for model_name in MODEL_ORDER:
        root=Path(artifact_root)/model_name; encode_path=root/"full-encode-report.json"; ranking_path=root/"exact-development-rankings.json"; evaluation_path=root/"development-evaluation.json"
        if not encode_path.is_file() or not ranking_path.is_file() or not evaluation_path.is_file():missing.append(model_name); continue
        try:validated=index_validator(model_name,Path(artifact_root))
        except Exception:missing.append(model_name); continue
        encode=json.loads(encode_path.read_text()); ranking=json.loads(ranking_path.read_text()); evaluation=json.loads(evaluation_path.read_text())
        ranking_rows=ranking.get("rankings",[])
        rankings_valid=ranking.get("classification")=="m7b_exact_development_rankings" and ranking.get("searched_table_count")==EXPECTED_TABLE_COUNT and ranking.get("holdout_qrels_materialized") is False and len(ranking.get("query_ids",[]))==30 and len(ranking_rows)==30 and all(len(row)==100 and len({item["table_id"] for item in row})==100 for row in ranking_rows)
        if encode.get("status")!="complete" or evaluation.get("classification")!="development_topical_retrieval" or evaluation.get("topic_count")!=30 or not rankings_valid:missing.append(model_name); continue
        metrics=evaluation["metrics"]; results.append({"model":model_name,"status":"complete","known_relevant_recall_at_100":metrics["known_relevant_recall_at_100"]["all"],"bpref":metrics["bpref"]["all"],"embedding_wall_seconds":validated["validated_embedding_wall_seconds"],"physical_index_bytes":validated["validated_physical_index_bytes"]}); evaluations[model_name]=evaluation
    if missing:return {"classification":"provisional_development_selection","paper_result":False,"status":"blocked","winner":None,"missing_or_failed_models":missing,"encoder_frozen":False,"candidate_depth_frozen":False}
    selected=select_encoder(results,set(MODEL_ORDER)); winner=selected["winner"]; curve={k:evaluations[winner]["metrics"][f"known_relevant_recall_at_{k}"]["all"] for k in (5,10,20,50,100)}; depth=select_candidate_depth(curve)
    return {"classification":"provisional_development_selection","paper_result":False,"status":"complete","selection":selected,"provisional_k":depth,"encoder_frozen":False,"candidate_depth_frozen":False,"external_api_spend_usd":0,"holdout":"locked_not_evaluated"}
