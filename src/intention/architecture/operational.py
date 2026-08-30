from dataclasses import asdict
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
from intention.retrieval import RetrievalRequest
from .embedding import load_embedding_registry
from .manifest import ArtifactManifest
from .vector_store import VectorRecord

def identity_hash(value):return sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

class OfflineTableIndexer:
    def __init__(self,table_store,serializer,encoder,vector_store,profile_builder,profile_store,manifest_store,collection_config,source_id,source_version):
        self.table_store=table_store; self.serializer=serializer; self.encoder=encoder; self.vector_store=vector_store; self.profile_builder=profile_builder; self.profile_store=profile_store; self.manifest_store=manifest_store; self.collection_config=collection_config; self.source_id=source_id; self.source_version=source_version
    def index(self,table,source_hash):
        if self.collection_config.encoder_hash!=self.encoder.identity.config_hash:raise ValueError("vector collection encoder identity does not match embedding provider")
        if hasattr(self.profile_store,"profile_version") and self.collection_config.profile_version!=self.profile_store.profile_version:raise ValueError("vector collection profile identity does not match profile store")
        stored=self.table_store.write(table); serialized=self.serializer.serialize(table); profile=self.profile_builder(table); profile_payload=profile.to_dict() if hasattr(profile,"to_dict") else profile; profile_artifact=self.profile_store.save(table.table_id,profile_payload)
        collection_hash=identity_hash(asdict(self.collection_config))
        expected={"source_hash":source_hash,"table_hash":stored["hash"],"serialization_hash":serialized.checksum,"encoder_hash":self.encoder.identity.config_hash,"profile_hash":profile_artifact["hash"],"collection_hash":collection_hash}
        self.vector_store.create_or_validate_collection(self.collection_config)
        try:
            current=self.manifest_store.load(table.table_id)
            actual={"source_hash":current["source"]["hash"],"table_hash":current["normalized_table"]["hash"],"serialization_hash":current["serialization"]["hash"],"encoder_hash":current["encoder"]["hash"],"profile_hash":current["capability_profile"]["hash"],"collection_hash":current["vector_collection"]["hash"]}
            vector=self.vector_store.get(table.table_id)
            expected_payload={"source_id":self.source_id,"source_version":self.source_version,"table_artifact_hash":stored["hash"],"serialization_hash":serialized.checksum,"encoder_hash":self.encoder.identity.config_hash,"profile_hash":profile_artifact["hash"],"collection_hash":collection_hash}
            if actual==expected and vector is not None and vector.payload==expected_payload:return {"status":"reused","manifest":current}
        except FileNotFoundError:pass
        encoded=self.encoder.encode_document(serialized.text)
        if encoded.status!="success":raise RuntimeError(f"document embedding failed: {encoded.failure.message}")
        payload={"source_id":self.source_id,"source_version":self.source_version,"table_artifact_hash":stored["hash"],"serialization_hash":serialized.checksum,"encoder_hash":self.encoder.identity.config_hash,"profile_hash":profile_artifact["hash"],"collection_hash":collection_hash}
        self.vector_store.upsert([VectorRecord(table.table_id,encoded.vectors[0],payload)])
        manifest_payload={"manifest_version":"1.0.0","table_id":table.table_id,"source":{"id":self.source_id,"version":self.source_version,"hash":source_hash},"normalized_table":{"path":stored["path"],"version":self.source_version,"hash":stored["hash"]},"serialization":{"id":serialized.serialization_id,"version":self.serializer.policy.version,"hash":serialized.checksum},"encoder":{"id":self.encoder.identity.model,"version":self.encoder.identity.revision,"hash":self.encoder.identity.config_hash},"vector_collection":{"id":self.collection_config.name,"version":self.collection_config.version,"hash":collection_hash},"capability_profile":{"path":profile_artifact["path"],"version":profile_artifact["version"],"hash":profile_artifact["hash"]}}
        manifest=ArtifactManifest(**manifest_payload); path=self.manifest_store.save(manifest)
        return {"status":"indexed","manifest":manifest_payload,"manifest_path":str(path),"build_identity":expected}

class OnlineSemanticPipeline:
    def __init__(self,interpreter,semantic_retriever):self.interpreter=interpreter; self.semantic_retriever=semantic_retriever
    def run(self,user_input,k=20):
        interpretation=self.interpreter.interpret(user_input)
        if interpretation.topical_query is None:return {"interpretation":interpretation,"retrieval":None}
        retrieval=self.semantic_retriever.retrieve(RetrievalRequest(interpretation.topical_query,k,"topical_only"))
        return {"interpretation":interpretation,"grounding":interpretation.grounding,"retrieval":retrieval}

def _record(component,status,reason=None,required_action=None,**details):
    return {"component":component,"status":status,"reason":reason,"required_action":required_action,**details}

class OperationalReadinessProbe:
    """Read-only runtime readiness detection; never downloads or starts services."""
    DEPENDENCIES=("pyarrow","duckdb","qdrant_client","sentence_transformers","transformers","huggingface_hub","torch")
    def __init__(self,registry=None,environ=None,module_available=None,artifact_available=None,qdrant_factory=None,path_writable=None,device_available=None):
        self.registry=registry or load_embedding_registry(); self.environ=dict(os.environ if environ is None else environ)
        self.module_available=module_available or (lambda name:importlib.util.find_spec(name) is not None)
        self.artifact_available=artifact_available or self._local_hf_artifact
        self.qdrant_factory=qdrant_factory or self._qdrant_client
        self.path_writable=path_writable or self._path_writable
        self.device_available=device_available or self._device_available
    def _local_hf_artifact(self,model,revision):
        try:
            from huggingface_hub import try_to_load_from_cache
            required=("modules.json","config_sentence_transformers.json","1_Pooling/config.json","config.json","tokenizer.json","tokenizer_config.json","model.safetensors")
            values=(try_to_load_from_cache(model,name,revision=revision) for name in required)
            return all(isinstance(value,str) and Path(value).is_file() for value in values)
        except (ImportError,OSError,ValueError):return False
    def _qdrant_client(self,url):
        from qdrant_client import QdrantClient
        return QdrantClient(url=url,timeout=2)
    def _path_writable(self,path):
        candidate=Path(path).expanduser().resolve()
        existing=next((item for item in (candidate,*candidate.parents) if item.exists()),None)
        return bool(existing and existing.is_dir() and os.access(existing,os.W_OK))
    def _device_available(self,device):
        if device=="cpu":return True
        if device.startswith("cuda"):
            try:
                import torch
                return torch.cuda.is_available()
            except ImportError:return False
        return False
    def inspect(self):
        checks=[]
        for dependency in self.DEPENDENCIES:
            available=self.module_available(dependency)
            checks.append(_record(dependency,"ready" if available else "blocked",None if available else "required dependency is unavailable",None if available else f"install the operational extra providing {dependency}"))
        name=self.registry.operational_smoke_encoder; record=self.registry.models[name].record
        local=self.artifact_available(record["model"],record["revision"]); device=self.environ.get("INTENTION_EMBEDDING_DEVICE","cpu"); runtime=self.device_available(device)
        encoder_ready=local and runtime; reason=None if encoder_ready else ("exact pinned model artifacts are not available locally" if not local else "configured embedding device is unavailable")
        action=None if encoder_ready else (f"download {record['model']} at revision {record['revision']} outside deterministic CI" if not local else f"configure an available runtime device instead of {device}")
        checks.append(_record("encoder","ready" if encoder_ready else "blocked",reason,action,encoder=name,model=record["model"],revision=record["revision"],tokenizer_revision=record["tokenizer_revision"],registry_status=record["availability"],device=device,hardware_requirements=record["hardware"],operational_role=record["operational_role"]))
        root=self.environ.get("INTENTION_ARTIFACT_ROOT")
        writable=bool(root and self.path_writable(root))
        checks.append(_record("authoritative_storage","ready" if writable else "blocked",None if writable else ("INTENTION_ARTIFACT_ROOT is not configured" if not root else "configured artifact path is not writable"),None if writable else "configure INTENTION_ARTIFACT_ROOT to a writable persistent path",path=root))
        url=self.environ.get("INTENTION_QDRANT_URL"); collection=self.environ.get("INTENTION_QDRANT_COLLECTION","intention-operational-smoke")
        expected_collection={"name":collection,"version":self.environ.get("INTENTION_COLLECTION_VERSION","operational-smoke-v1"),"named_vector":"topical_dense","dimension":int(self.environ.get("INTENTION_EMBEDDING_DIMENSION","1024")),"metric":"cosine","dataset_version":self.environ.get("INTENTION_DATASET_VERSION","operational-smoke-v1"),"profile_version":self.environ.get("INTENTION_PROFILE_VERSION","operational-smoke-v1")}
        qdrant_ready=False; reason="INTENTION_QDRANT_URL is not configured"
        if url and self.module_available("qdrant_client"):
            try:self.qdrant_factory(url).get_collections(); qdrant_ready=True; reason=None
            except Exception as error:reason=f"configured Qdrant service is unreachable: {type(error).__name__}"
        checks.append(_record("vector_store","ready" if qdrant_ready else "blocked",reason,None if qdrant_ready else "configure a reachable Qdrant service; it will not be started automatically",url=url,expected_collection=expected_collection))
        return checks

def operational_smoke_status(checks):
    blockers=sorted((item for item in checks if item["status"]!="ready"),key=lambda item:item["component"])
    return {"classification":"operational_smoke","paper_result":False,"status":"blocked" if blockers else "ready","checks":checks,"blockers":blockers,"final_encoder_selected":False}
