from __future__ import annotations
from dataclasses import asdict,dataclass
from hashlib import sha256
from pathlib import Path
from statistics import median
from time import perf_counter
import importlib.metadata,json,math,platform,resource

from intention.architecture.embedding import load_embedding_registry
from intention.architecture.serialization import NeuralTableSerializer
from intention.benchmarks.corpus import runtime_table_from_normalized_record
from intention.evaluation.topical_bakeoff import load_bakeoff_contract

SUPPORTED_MODELS=("Qwen3-Embedding-0.6B","Nemotron-3-Embed-1B-BF16","Qwen3-Embedding-4B")

@dataclass(frozen=True)
class GPUInfo:
    cuda_available:bool; visible_device_count:int; gpu_index:int|None; gpu_name:str|None
    total_vram_bytes:int|None; free_vram_bytes:int|None; compute_capability:str|None
    bf16_supported:bool; selected_device:str|None

class TorchHardwareDetector:
    def __init__(self,torch_module=None):
        if torch_module is None:import torch as torch_module
        self.torch=torch_module
    def detect(self,index=0):
        torch=self.torch; available=bool(torch.cuda.is_available()); count=int(torch.cuda.device_count()) if available else 0
        if not available or count<=index:return GPUInfo(False,count,None,None,None,None,None,False,None)
        props=torch.cuda.get_device_properties(index)
        try:free,total=torch.cuda.mem_get_info(index)
        except Exception:free,total=None,int(props.total_memory)
        return GPUInfo(True,count,index,props.name,int(total or props.total_memory),None if free is None else int(free),f"{props.major}.{props.minor}",bool(torch.cuda.is_bf16_supported()),f"cuda:{index}")

def gpu_preflight(detector=None):
    import torch
    gpu=(detector or TorchHardwareDetector(torch)).detect()
    return {"classification":"m7b_gpu_preflight","python_version":platform.python_version(),"torch_version":torch.__version__,"torch_cuda_runtime":torch.version.cuda,**asdict(gpu)}

def _percentiles(values):
    ordered=sorted(values)
    def p(frac):return ordered[min(len(ordered)-1,math.ceil(frac*len(ordered))-1)]
    return {"minimum":ordered[0],"median":median(ordered),"p95":p(.95),"maximum":ordered[-1]}

def pilot_table_ids(data_root:Path,count=10000,index_reader=None,expected_total=1652771):
    if count!=10000:raise ValueError("M7B pilot requires exactly 10,000 tables")
    base=Path(data_root)/"normalized/wikitables-www2018/wikitables_www2018/normalized/v1.0.0"
    paths=sorted((base/"index").glob("*.parquet"))
    if index_reader is None:
        import pyarrow.dataset as ds
        if not paths:raise FileNotFoundError("normalized WikiTables index unavailable")
        index_reader=lambda _:ds.dataset([str(path) for path in paths],format="parquet").to_table(columns=["table_id"])["table_id"].to_pylist()
    ids=index_reader(paths)
    if len(ids)!=expected_total or len(ids)!=len(set(ids)):raise ValueError("normalized index identity mismatch")
    selected=tuple(sorted(ids)[:count]); digest=sha256(("\n".join(selected)+"\n").encode()).hexdigest()
    return selected,digest

def load_serialized_pilot(data_root:Path,expected_ids):
    import pyarrow.dataset as ds
    base=Path(data_root)/"normalized/wikitables-www2018/wikitables_www2018/normalized/v1.0.0/tables"
    dataset=ds.dataset(str(base),format="parquet",partitioning="hive")
    records=dataset.to_table(filter=ds.field("table_id").isin(list(expected_ids))).to_pylist()
    by_id={record["table_id"]:record for record in records}
    if set(by_id)!=set(expected_ids) or len(records)!=len(expected_ids):raise ValueError("pilot table resolution mismatch")
    serializer=NeuralTableSerializer(); serialized=[]
    for table_id in expected_ids:
        record=by_id[table_id]; table=runtime_table_from_normalized_record(record)
        serialized.append(serializer.serialize(table).text)
    return serialized,serializer.policy,{"status":"verified","table_count":len(serialized),"source":"canonical_normalized_column_metadata"}

def calibrate_batch_size(encode_probe,batch_sizes=(4,8,16,32,64,128),cuda=None,safety_fraction=.85):
    attempts=[]; successful=[]; ooms=0; chosen=None; peak_allocated=peak_reserved=0
    for size in batch_sizes:
        try:
            if cuda:cuda.reset_peak_memory_stats()
            encode_probe(size)
            allocated=int(cuda.max_memory_allocated()) if cuda else 0; reserved=int(cuda.max_memory_reserved()) if cuda else 0
            total=int(cuda.get_device_properties(0).total_memory) if cuda else max(allocated,1)
            attempts.append({"batch_size":size,"status":"success","peak_allocated_bytes":allocated,"peak_reserved_bytes":reserved})
            peak_allocated=max(peak_allocated,allocated); peak_reserved=max(peak_reserved,reserved)
            if reserved>safety_fraction*total:break
            successful.append(size); chosen=size
        except Exception as error:
            is_oom=error.__class__.__name__=="OutOfMemoryError" or "out of memory" in str(error).lower()
            if not is_oom:raise
            ooms+=1; attempts.append({"batch_size":size,"status":"oom"})
            if cuda:cuda.empty_cache()
            break
    if chosen is None:raise RuntimeError("no safe pilot batch size")
    return {"attempts":attempts,"successful_sizes":successful,"oom_events":ooms,"selected_batch_size":chosen,"calibration_peak_allocated_bytes":peak_allocated,"calibration_peak_reserved_bytes":peak_reserved}

def _module_contract(model,name):
    pooling=next((module for module in model.modules() if module.__class__.__name__=="Pooling"),None)
    if pooling is None:raise RuntimeError("model-defined SentenceTransformers pooling unavailable")
    configured=getattr(pooling,"pooling_mode",None)
    modes={"mean":configured in {"mean","mean_tokens"} or bool(getattr(pooling,"pooling_mode_mean_tokens",False)),"lasttoken":configured in {"lasttoken","last_token"} or bool(getattr(pooling,"pooling_mode_lasttoken",False))}
    expected="mean" if name=="Nemotron-3-Embed-1B-BF16" else "lasttoken"
    if not modes[expected]:raise RuntimeError(f"unexpected model-defined pooling: expected {expected}, observed {modes}")
    return {"expected":expected,"observed":modes}

def run_pilot(model_name,data_root:Path,artifact_root:Path,device="cuda",model_factory=None,torch_module=None):
    if model_name not in SUPPORTED_MODELS:raise ValueError(f"unsupported M7B model: {model_name}")
    import torch
    torch=torch_module or torch; hardware=TorchHardwareDetector(torch).detect()
    if not hardware.cuda_available:raise RuntimeError("CUDA accelerator unavailable; no substitution allowed")
    if device not in {"cuda","cuda:0"}:raise ValueError("M7B pilots require cuda:0")
    contract=load_bakeoff_contract(); registry=load_embedding_registry(); record=registry.models[model_name].record
    ids,id_digest=pilot_table_ids(data_root,contract["pilot"]["table_count"]); texts,policy,semantic_headers=load_serialized_pilot(data_root,ids)
    if model_factory is None:
        from sentence_transformers import SentenceTransformer
        model_factory=SentenceTransformer
    started_load=perf_counter()
    model=model_factory(record["model"],revision=record["revision"],device="cuda:0",trust_remote_code=False,model_kwargs={"torch_dtype":torch.bfloat16})
    load_seconds=perf_counter()-started_load
    model_commit=getattr(getattr(model,"_first_module",lambda:None)(),"auto_model",None)
    model_commit=getattr(getattr(model_commit,"config",None),"_commit_hash",None)
    tokenizer=getattr(model,"tokenizer",None); tokenizer_commit=getattr(tokenizer,"init_kwargs",{}).get("_commit_hash")
    if tokenizer_commit is None:
        from huggingface_hub import try_to_load_from_cache
        artifact=try_to_load_from_cache(record["model"],"tokenizer_config.json",revision=record["tokenizer_revision"])
        parts=Path(artifact).parts if isinstance(artifact,str) else ()
        tokenizer_commit=next((part for part in parts if part==record["tokenizer_revision"]),None)
    if model_commit!=record["revision"] or tokenizer_commit!=record["tokenizer_revision"]:raise RuntimeError(f"pinned revision verification failed: model={model_commit}, tokenizer={tokenizer_commit}")
    pooling=_module_contract(model,model_name)
    formatted=[record["document_instruction"].replace("{content}",text) if record["document_instruction"] else text for text in texts]
    token_lengths=[len(item) for item in tokenizer(formatted,add_special_tokens=True,truncation=False)["input_ids"]]
    violations=sum(length>record["maximum_input_tokens"] for length in token_lengths)
    if violations:raise RuntimeError(f"truncation-policy violations: {violations}")
    def encode(items,batch_size):
        with torch.inference_mode():return model.encode(items,batch_size=batch_size,normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
    longest=[text for _,text in sorted(zip(token_lengths,formatted),key=lambda item:item[0],reverse=True)]
    calibration=calibrate_batch_size(lambda size:encode(longest[:size],size),cuda=torch.cuda)
    timings=[]; peak_allocated=peak_reserved=0; vectors=None
    def timed_once():
        nonlocal vectors,peak_allocated,peak_reserved
        torch.cuda.reset_peak_memory_stats(); started=perf_counter(); vectors=encode(formatted,calibration["selected_batch_size"]); elapsed=perf_counter()-started
        peak_allocated=max(peak_allocated,int(torch.cuda.max_memory_allocated())); peak_reserved=max(peak_reserved,int(torch.cuda.max_memory_reserved())); return elapsed
    timings.append(timed_once()); first_projection=timings[0]/10000*contract["corpus"]["table_count"]/3600
    if 10.8<=first_projection<=13.2:timings.extend((timed_once(),timed_once()))
    wall=median(timings)
    import numpy as np
    finite=bool(np.isfinite(vectors).all()); norms=np.linalg.norm(vectors,axis=1); nonzero=bool((norms>0).all()); norm_max_deviation=float(np.max(np.abs(norms-1))); normalized=bool(norm_max_deviation<=.01)
    dimension_ok=vectors.ndim==2 and vectors.shape==(10000,max(record["dimensions"])); projected=wall/10000*contract["corpus"]["table_count"]
    checks={"dimension":dimension_ok,"finite":finite,"nonzero":nonzero,"l2_normalized":normalized,"no_truncation":violations==0,"projected_within_12_gpu_hours":projected/3600<=contract["pilot"]["maximum_projected_gpu_hours"]}
    failures=[name for name,value in checks.items() if not value]; passed=not failures
    timing_summary={"role":"boundary_stability_measurement" if len(timings)==3 else "single_measurement","aggregation":"median" if len(timings)==3 else "single","wall_seconds":timings,"tables_per_second":[10000/value for value in timings],"minimum_seconds":min(timings),"median_seconds":median(timings),"maximum_seconds":max(timings)}
    report={"classification":"m7b_real_10k_gpu_pilot","paper_result":False,"model":model_name,"model_id":record["model"],"revision":record["revision"],"tokenizer_revision":record["tokenizer_revision"],"license":record["license"],"trust_remote_code":False,"pilot_selection_version":contract["pilot"]["selection_version"],"pilot_table_count":len(ids),"pilot_table_id_digest":id_digest,"corpus_digest":contract["corpus"]["logical_digest"],"serialization_id":policy.serialization_id,"serialization_version":policy.version,"serialization_hash":policy.digest,"semantic_header_validation":semantic_headers,"environment":{"python":platform.python_version(),"torch":torch.__version__,"torch_cuda_runtime":torch.version.cuda,"transformers":importlib.metadata.version("transformers"),"sentence_transformers":importlib.metadata.version("sentence-transformers")},"hardware":asdict(hardware),"device":"cuda:0","precision":"bfloat16","dimension":max(record["dimensions"]),"pooling":pooling,"model_load_seconds":load_seconds,"batch_calibration":calibration,"embedding_timing":timing_summary,"embedding_wall_seconds":wall,"tables_per_second":10000/wall,"serialized_characters":_percentiles([len(text) for text in texts]),"token_lengths":_percentiles(token_lengths),"peak_host_ram_kb":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,"peak_cuda_allocated_bytes":peak_allocated,"peak_cuda_reserved_bytes":peak_reserved,"vector_checks":{"dimension":dimension_ok,"finite":finite,"nonzero":nonzero,"l2_normalized":normalized,"maximum_norm_deviation":norm_max_deviation,"bf16_tolerance":.01},"truncation_violations":violations,"projection":{"method":"projection_from_10k_pilot","projected_full_seconds":projected,"projected_full_hours":projected/3600},"gate_checks":checks,"pilot_status":"passed" if passed else "failed","failure":None if passed else {"code":"pilot_gate_failed","failed_checks":failures},"gate_12_gpu_hours":checks["projected_within_12_gpu_hours"]}
    artifact_root=Path(artifact_root); artifact_root.mkdir(parents=True,exist_ok=True); path=artifact_root/f"{model_name}-pilot-report.json"; path.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    return report
