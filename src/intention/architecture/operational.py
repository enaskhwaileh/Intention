from dataclasses import asdict
from hashlib import sha256
import json
from intention.retrieval import RetrievalRequest
from .manifest import ArtifactManifest
from .vector_store import VectorRecord

def identity_hash(value):return sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

class OfflineTableIndexer:
    def __init__(self,table_store,serializer,encoder,vector_store,profile_builder,profile_store,manifest_store,collection_config,source_id,source_version):
        self.table_store=table_store; self.serializer=serializer; self.encoder=encoder; self.vector_store=vector_store; self.profile_builder=profile_builder; self.profile_store=profile_store; self.manifest_store=manifest_store; self.collection_config=collection_config; self.source_id=source_id; self.source_version=source_version
    def index(self,table,source_hash):
        stored=self.table_store.write(table); serialized=self.serializer.serialize(table); profile=self.profile_builder(table); profile_payload=profile.to_dict() if hasattr(profile,"to_dict") else profile; profile_artifact=self.profile_store.save(table.table_id,profile_payload)
        expected={"source_hash":source_hash,"table_hash":stored["hash"],"serialization_hash":serialized.checksum,"encoder_hash":self.encoder.identity.config_hash,"profile_hash":profile_artifact["hash"]}
        self.vector_store.create_or_validate_collection(self.collection_config)
        try:
            current=self.manifest_store.load(table.table_id)
            actual={"source_hash":current["source"]["hash"],"table_hash":current["normalized_table"]["hash"],"serialization_hash":current["serialization"]["hash"],"encoder_hash":current["encoder"]["hash"],"profile_hash":current["capability_profile"]["hash"]}
            if actual==expected and self.vector_store.get(table.table_id) is not None:return {"status":"reused","manifest":current}
        except FileNotFoundError:pass
        encoded=self.encoder.encode_document(serialized.text)
        if encoded.status!="success":raise RuntimeError(f"document embedding failed: {encoded.failure.message}")
        collection_hash=identity_hash(asdict(self.collection_config)); payload={"source_id":self.source_id,"source_version":self.source_version,"table_artifact_hash":stored["hash"],"serialization_hash":serialized.checksum,"encoder_hash":self.encoder.identity.config_hash,"profile_hash":profile_artifact["hash"]}
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

def operational_smoke_status(blockers):
    return {"classification":"operational_smoke","paper_result":False,"status":"blocked" if blockers else "ready","blockers":sorted(blockers),"final_encoder_selected":False}
