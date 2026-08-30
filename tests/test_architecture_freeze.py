import json
from pathlib import Path
import pytest
import yaml
from intention.architecture import (
    ArtifactManifest,CollectionConfig,EmbeddingIdentity,EmbeddingProvider,EmbeddingResult,
    InMemoryVectorStore,NeuralTableSerializer,QdrantVectorStore,SemanticRetriever,
    VectorRecord,load_embedding_registry,load_llm_registry,load_neural_serialization_policy,
    reciprocal_rank_fusion,validate_artifact_manifest,
)
from intention.contracts import Capability,Provenance,Table
from intention.evaluation import evaluate_paper_ranking
from intention.profiling import SemanticEnrichment,merge_enrichments
from intention.retrieval import RetrieverIdentity,RetrievalRequest,ScoreNormalization

HASH="0"*64
ROOT=Path(__file__).parents[1]

class RecordingEncoder(EmbeddingProvider):
    def __init__(self): self.queries=[]; self.documents=[]; self._identity=EmbeddingIdentity("test","test","revision","tokenizer",2,"l2","cosine","query","document",128,"fail","cpu",HASH)
    @property
    def identity(self): return self._identity
    def encode_queries(self,texts): self.queries.extend(texts); return EmbeddingResult("success",self.identity,tuple((1.0,0.0) for _ in texts),0)
    def encode_documents(self,texts): self.documents.extend(texts); return EmbeddingResult("success",self.identity,tuple((0.0,1.0) for _ in texts),0)

def collection(): return CollectionConfig("tables","1",2,"cosine",HASH,HASH,"dataset-v1","profiles-v1")

def test_embedding_and_llm_registries_are_versioned_verified_and_fail_closed():
    registry=load_embedding_registry()
    assert registry.primary_architecture=="provider_independent_dense" and len(registry.digest)==64
    assert {record.record["category"] for record in registry.models.values()}>={"proprietary_strong","open_weight_strong","open_weight_lightweight","lexical_reference"}
    assert "TABERTA" not in " ".join(registry.models)
    assert registry.models["Qwen3-Embedding-8B"].record["revision"]=="1d8ad4ca9b3dd8059ad90a75d4983776a23d44af"
    with pytest.raises(RuntimeError,match="blocked"): registry.require_available("gemini-embedding-2")
    llms=load_llm_registry(); assert len(llms.digest)==64 and len(llms.providers["gemini-3.7-flash"].schema_hash)==64
    with pytest.raises(RuntimeError,match="blocked"): llms.require_available("gemini-3.7-flash")

def test_neural_serialization_is_deterministic_bounded_and_leakage_free():
    table=Table("t","Title","Caption",({"b":2,"a":"x"},{"b":3,"a":"y"}),{"grounded_action":"COMPARE","usefulness_label":3,"gold":"SECRET"})
    serializer=NeuralTableSerializer(); first=serializer.serialize(table); second=serializer.serialize(table)
    assert first==second and len(first.checksum)==64 and first.serialization_id=="neural_table_evidence_v1"
    payload=json.loads(first.text); assert [column["name"] for column in payload["columns"]]==["b","a"]
    assert "COMPARE" not in first.text and "SECRET" not in first.text and "usefulness" not in first.text
    policy=load_neural_serialization_policy(); assert len(first.text)<=policy.maximum_characters

def test_vector_store_enforces_collection_identity_and_qdrant_fails_explicitly():
    store=InMemoryVectorStore(); store.create_or_validate_collection(collection())
    store.upsert([VectorRecord("b",(1.0,0.0),{"source":"manifest-b"}),VectorRecord("a",(1.0,0.0),{"source":"manifest-a"})])
    assert [hit.table_id for hit in store.search((1.0,0.0),2)]==["a","b"] and store.get("a").payload["source"]=="manifest-a"
    with pytest.raises(ValueError,match="identity mismatch"): store.create_or_validate_collection(CollectionConfig("tables","2",2,"cosine",HASH,HASH,"dataset-v1","profiles-v1"))
    qdrant=QdrantVectorStore(); assert qdrant.availability[0]=="unavailable"
    with pytest.raises(RuntimeError,match="not configured"): qdrant.create_or_validate_collection(collection())

def test_semantic_retriever_encodes_only_topical_q_u_not_action_bearing_input():
    encoder=RecordingEncoder(); store=InMemoryVectorStore(); store.create_or_validate_collection(collection()); store.upsert([VectorRecord("t",(1.0,0.0),{})])
    identity=RetrieverIdentity("Dense","test","revision","1","neural_table_evidence_v1","1.0.0","topical_only","1",HASH,HASH)
    retriever=SemanticRetriever(encoder,store,identity)
    full="vaccine safety compare measure=rate by country"; topical="vaccine safety"
    result=retriever.retrieve(RetrievalRequest(topical,5,"topical_only"))
    assert result.status=="success" and encoder.queries==[topical] and full not in encoder.queries
    rejected=retriever.retrieve(RetrievalRequest(full,5,"full_input_baseline")); assert rejected.status=="failure" and encoder.queries==[topical]

def test_artifact_manifest_links_authoritative_storage_index_and_profile():
    identity={"id":"x","version":"1","hash":HASH}; artifact={"path":"artifacts/x.parquet","version":"1","hash":HASH}
    manifest=ArtifactManifest("1.0.0","table",{"id":"wiki","version":"v1","hash":HASH},artifact,identity,identity,identity,artifact)
    assert validate_artifact_manifest(manifest)["table_id"]=="table"
    broken=validate_artifact_manifest(manifest); broken["serialization"]["hash"]="bad"
    with pytest.raises(ValueError,match="manifest"): validate_artifact_manifest(broken)

def test_semantic_enrichment_cannot_silently_overwrite_observed_evidence():
    observed=(Capability("row_granularity","str","country","observed",1,Provenance("table","deterministic")),)
    inferred=SemanticEnrichment("row_granularity","str","person","inferred",.7,"model",HASH,HASH,("caption",),("title",))
    merged=merge_enrichments(observed,(inferred,)); assert not merged["inferred"] and merged["rejected_overwrites"]==(inferred,)

def test_hybrid_rrf_is_deterministic_and_alignment_independent():
    fused=reciprocal_rank_fusion({"dense":["b","a"],"bm25":["a","c"]})
    assert [item["table_id"] for item in fused]==["a","b","c"] and all(set(item)=={"table_id","raw_score"} for item in fused)
    selection=yaml.safe_load((ROOT/"configs/architecture/retrieval_selection.yaml").read_text())
    assert selection["split"]=="development_only" and not selection["test_labels_permitted"]
    assert selection["forbidden_selection_metric"]=="final_intended_action_usefulness"

def test_storage_contract_keeps_qdrant_a_rebuildable_non_authoritative_index():
    storage=yaml.safe_load((ROOT/"configs/architecture/storage.yaml").read_text())
    assert storage["authoritative_tables"]["format"]=="parquet" and storage["authoritative_tables"]["analytical_engine"]=="duckdb"
    assert storage["vector_index"]["provider"]=="qdrant" and storage["vector_index"]["role"]=="rebuildable_index_not_authority"
    assert storage["vector_index"]["future_sparse_vector_name"]=="topical_sparse"

def test_normative_paper_evaluator_requires_scored_ids_and_complete_qrels():
    qrels={"a":{"topical_label":2,"usefulness_label":3},"b":{"topical_label":1,"usefulness_label":0}}
    assert evaluate_paper_ranking([{"table_id":"a","score":1.0}],qrels,["a","b"])["usefulness_ndcg@5"]==1
    with pytest.raises((ValueError,AttributeError)): evaluate_paper_ranking([3,0],qrels,["a","b"])
