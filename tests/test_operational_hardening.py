from pathlib import Path
from types import SimpleNamespace
import importlib.util,json,math
import pytest
from intention.architecture import (
    CollectionConfig,GeminiEmbedding2Client,GeminiStructuredOutputClient,HuggingFaceEmbeddingProvider,
    InMemoryVectorStore,ManifestRepository,NeuralTableSerializer,OfflineTableIndexer,OnlineSemanticPipeline,
    ParquetDuckDBTableStore,QdrantVectorStore,SemanticRetriever,ValidatedExternalInterpreter,VersionedProfileStore,
    load_embedding_registry,load_llm_registry,
)
from intention.architecture.embedding import EmbeddingIdentity,EmbeddingProvider,EmbeddingResult
from intention.contracts import Grounding,Interpretation,Table
from intention.interpretation.interpreter import ExternalStructuredProvider
from intention.knowledge import load_knowledge
from intention.retrieval import RetrieverIdentity

HASH="0"*64

class FakeQdrantModels:
    class Distance: COSINE="Cosine"; DOT="Dot"; EUCLID="Euclidean"
    class VectorParams:
        def __init__(self,size,distance):self.size=size; self.distance=distance
    class PointStruct:
        def __init__(self,id,vector,payload):self.id=id; self.vector=vector; self.payload=payload
    class MatchValue:
        def __init__(self,value):self.value=value
    class FieldCondition:
        def __init__(self,key,match):self.key=key; self.match=match
    class Filter:
        def __init__(self,must):self.must=must

class FakeQdrantClient:
    def __init__(self):self.collections={}
    def collection_exists(self,name):return name in self.collections
    def create_collection(self,collection_name,vectors_config):self.collections[collection_name]={"vectors":vectors_config,"points":{}}
    def upsert(self,collection_name,points,**kwargs):self.collections[collection_name]["points"].update({point.id:point for point in points})
    def retrieve(self,collection_name,ids,**kwargs):return [self.collections[collection_name]["points"][point_id] for point_id in ids if point_id in self.collections[collection_name]["points"]]
    def get_collection(self,name):return SimpleNamespace(config=SimpleNamespace(params=SimpleNamespace(vectors=self.collections[name]["vectors"])))
    def query_points(self,collection_name,query,limit,**kwargs):
        points=[]
        for point in self.collections[collection_name]["points"].values():
            if point.payload.get("record_type")!="table":continue
            vector=point.vector["topical_dense"]; score=sum(a*b for a,b in zip(query,vector)); points.append(SimpleNamespace(payload=point.payload,score=score))
        return SimpleNamespace(points=sorted(points,key=lambda point:-point.score)[:limit])
    def delete_collection(self,collection_name):del self.collections[collection_name]

class FakeTokenizer:
    def __init__(self):self.inputs=[]
    def __call__(self,text,**kwargs):self.inputs.append((text,kwargs)); return {"input_ids":list(range(len(text.split())))}
class FakeModel:
    def __init__(self):self.calls=[]
    def encode(self,texts,**kwargs):self.calls.append((texts,kwargs)); return [[3.0,4.0]+[0.0]*30 for _ in texts]

def test_gemini_embedding_2_uses_current_prompt_contract_and_never_task_type():
    class Models:
        def __init__(self):self.calls=[]
        def embed_content(self,**kwargs):self.calls.append(kwargs); return {"embeddings":[]}
    models=Models(); adapter=GeminiEmbedding2Client(SimpleNamespace(models=models),output_dimension=768)
    adapter.embed_query("vaccine safety"); adapter.embed_document("serialized table","Rates")
    assert models.calls[0]["contents"][0]["parts"][0]["text"]=="task: search result | query: vaccine safety"
    assert models.calls[1]["contents"][0]["parts"][0]["text"]=="title: Rates | text: serialized table"
    assert all("task_type" not in call.get("config",{}) and "taskType" not in call.get("config",{}) for call in models.calls)
    record=load_embedding_registry().models["gemini-embedding-2"].record
    assert record["api_task_type_supported"] is False and record["maximum_input_tokens"]==8192

def test_gemini_llm_omits_deprecated_sampling_and_retains_raw_response():
    class Interactions:
        def __init__(self):self.calls=[]
        def create(self,**kwargs):self.calls.append(kwargs); return {"output_text":json.dumps({"schema_version":"1.0.0"})}
    interactions=Interactions(); registration=load_llm_registry().providers["gemini-3.7-flash"]
    client=GeminiStructuredOutputClient(SimpleNamespace(interactions=interactions),registration,"prompt-v1")
    raw=client("input",{"type":"object"}); call=interactions.calls[0]
    assert raw["content"]["schema_version"]=="1.0.0" and raw["raw_provider_response"]
    assert not {"temperature","top_p","top_k"}&set(call.get("generation_config") or {})
    assert registration.parameters["temperature"]["support"]=="deprecated_do_not_send" and registration.parameters["temperature"]["configured"] is None

def test_generic_huggingface_adapter_pins_revisions_batches_formats_and_normalizes():
    registration=load_embedding_registry().models["Qwen3-Embedding-0.6B"]; model=FakeModel(); tokenizer=FakeTokenizer(); seen={}
    def model_factory(**kwargs):seen["model"]=kwargs; return model
    def tokenizer_factory(**kwargs):seen["tokenizer"]=kwargs; return tokenizer
    provider=HuggingFaceEmbeddingProvider(registration,dimension=32,model_factory=model_factory,tokenizer_factory=tokenizer_factory,clock=iter((0,0.01)).__next__)
    result=provider.encode_queries(["topic one","topic two"])
    assert result.status=="success" and result.elapsed_ms==10 and result.vectors[0][:2]==pytest.approx((.6,.8))
    assert seen["model"]["revision"]==registration.record["revision"] and seen["tokenizer"]["revision"]==registration.record["tokenizer_revision"]
    assert model.calls[0][0][0].startswith("Instruct:") and "Query: topic one" in model.calls[0][0][0]
    assert all(math.isclose(sum(value*value for value in vector),1) for vector in result.vectors)

def test_huggingface_adapter_fails_closed_for_missing_model_and_long_input():
    registration=load_embedding_registry().models["Qwen3-Embedding-0.6B"]
    unavailable=HuggingFaceEmbeddingProvider(registration,dimension=32,model_factory=lambda **_:(_ for _ in ()).throw(RuntimeError("offline")),tokenizer_factory=lambda **_:FakeTokenizer())
    assert unavailable.encode_query("topic").failure.code=="unavailable"
    record=dict(registration.record); record["maximum_input_tokens"]=1; model=FakeModel(); provider=HuggingFaceEmbeddingProvider(record,dimension=32,model_factory=lambda **_:model,tokenizer_factory=lambda **_:FakeTokenizer())
    assert provider.encode_query("two tokens").failure.code=="input_too_long" and not model.calls

class FakeParquetBackend:
    def __init__(self):self.rows={}
    def write(self,path,rows):self.rows[str(path)]=rows; path.write_bytes(b"PAR1fake")
    def read(self,path):return self.rows[str(path)]
    def query(self,directory,sql):return [(str(directory),sql)]

class FixedEncoder(EmbeddingProvider):
    def __init__(self):self.queries=[]; self.documents=[]; self._identity=EmbeddingIdentity("mock","mock-embed","rev","tok",2,"l2","cosine",None,None,100,"fail","cpu",HASH)
    @property
    def identity(self):return self._identity
    def encode_queries(self,texts):self.queries.extend(texts); return EmbeddingResult("success",self.identity,tuple((1.0,0.0) for _ in texts),0)
    def encode_documents(self,texts):self.documents.extend(texts); return EmbeddingResult("success",self.identity,tuple((1.0,0.0) for _ in texts),0)

def test_parquet_store_indexing_manifest_and_restart_are_operational_with_injected_backends(tmp_path):
    backend=FakeParquetBackend(); tables=ParquetDuckDBTableStore(tmp_path/"tables","tiny","v1",backend); table=Table("rates","Rates","Vaccine rates",({"country":"A","rate":.8},),{})
    stored=tables.write(table); assert stored["path"].endswith(".parquet") and tables.read("rates")==table and tables.list_tables()==["rates"] and tables.validate("rates")
    encoder=FixedEncoder(); vectors=InMemoryVectorStore(); config=CollectionConfig("tiny-v1","1",2,"cosine",HASH,HASH,"v1","p1")
    indexer=OfflineTableIndexer(tables,NeuralTableSerializer(),encoder,vectors,lambda _: {"table_id":"rates","capabilities":[]},VersionedProfileStore(tmp_path/"profiles","p1"),ManifestRepository(tmp_path/"manifests"),config,"tiny","v1")
    first=indexer.index(table,HASH); second=indexer.index(table,HASH)
    assert first["status"]=="indexed" and second["status"]=="reused" and len(encoder.documents)==1
    manifest=ManifestRepository(tmp_path/"manifests").load("rates"); assert manifest["source"]["hash"]==HASH and vectors.get("rates").payload["profile_hash"]==manifest["capability_profile"]["hash"]

@pytest.mark.skipif(not importlib.util.find_spec("pyarrow") or not importlib.util.find_spec("duckdb"),reason="optional Parquet/DuckDB dependencies unavailable")
def test_real_parquet_duckdb_backend_round_trip(tmp_path):
    store=ParquetDuckDBTableStore(tmp_path,"tiny","v1"); table=Table("rates","Rates","Caption",({"country":"A","rate":.8},{"country":"B","rate":.6}),{})
    assert store.availability==( "available",None); store.write(table); assert store.read("rates")==table
    assert store.query("SELECT count(*) FROM normalized_tables")==[(2,)]

def test_real_qdrant_adapter_contract_uses_named_vectors_payload_identity_and_ties():
    from intention.architecture.vector_store import VectorRecord
    client=FakeQdrantClient(); config=CollectionConfig("tables","1",2,"cosine",HASH,HASH,"v1","p1"); store=QdrantVectorStore(client,FakeQdrantModels)
    store.create_or_validate_collection(config); store.upsert([VectorRecord("b",(1.0,0.0),{"manifest":"b"}),VectorRecord("a",(1.0,0.0),{"manifest":"a"})])
    assert store.get("a").payload=={"manifest":"a"} and [hit.table_id for hit in store.search((1.0,0.0),2)]==["a","b"]
    assert "topical_dense" in client.collections["tables"]["vectors"]
    QdrantVectorStore(client,FakeQdrantModels).create_or_validate_collection(config)
    store.delete_collection(); assert not client.collection_exists("tables")

def test_online_path_keeps_action_downstream_and_only_encodes_q_u():
    encoder=FixedEncoder(); vectors=InMemoryVectorStore(); vectors.create_or_validate_collection(CollectionConfig("x","1",2,"cosine",HASH,HASH,"v1","p1")); vectors.upsert([])
    identity=RetrieverIdentity("Dense","mock","rev","1","neural_table_evidence_v1","1","topical_only","1",HASH,HASH); retriever=SemanticRetriever(encoder,vectors,identity)
    interpretation=Interpretation("vaccine safety",Grounding("COMPARE",{"measure":"rate"}),(),{},topical_fields={})
    interpreter=SimpleNamespace(interpret=lambda _:interpretation); output=OnlineSemanticPipeline(interpreter,retriever).run("vaccine safety compare rates")
    assert encoder.queries==["vaccine safety"] and output["grounding"].action=="COMPARE" and output["retrieval"].normalization.calibration_status=="development_fit_pending"

def test_raw_cosine_survives_calibration_unchanged():
    encoder=FixedEncoder(); vectors=InMemoryVectorStore(); vectors.create_or_validate_collection(CollectionConfig("x","1",2,"cosine",HASH,HASH,"v1","p1")); from intention.architecture.vector_store import VectorRecord
    vectors.upsert([VectorRecord("a",(.5,math.sqrt(.75)),{}),VectorRecord("b",(-.5,math.sqrt(.75)),{})]); identity=RetrieverIdentity("Dense","mock","rev","1","s","1","topical_only","1",HASH,HASH)
    result=SemanticRetriever(encoder,vectors,identity).retrieve(__import__("intention.retrieval",fromlist=["RetrievalRequest"]).RetrievalRequest("topic",2))
    assert [candidate.raw_score for candidate in result.candidates]==pytest.approx([.5,-.5]) and [candidate.relevance for candidate in result.candidates]==pytest.approx([.75,.25])

def test_external_structured_provider_accepts_mocked_gemini_boundary():
    class Interactions:
        def create(self,**kwargs):return {"output_text":json.dumps({"schema_version":"1.0.0","action":"unknown","arguments":{},"topical":{"query":"topic","entities":[],"attributes":[],"constraints":{}},"provenance":{"topic_spans":[],"action_spans":[],"argument_spans":{}},"ambiguity":{"status":"insufficient","candidates":[],"reason":"none"}})}
    registration=load_llm_registry().providers["gemini-3.7-flash"]; callable_client=GeminiStructuredOutputClient(SimpleNamespace(interactions=Interactions()),registration,"prompt")
    artifact=ExternalStructuredProvider("google",registration.model,registration.revision,callable_client).interpret("topic")
    assert artifact.raw_response!=artifact.content and artifact.content["action"]=="unknown"
    interpreted=ValidatedExternalInterpreter(ExternalStructuredProvider("google",registration.model,registration.revision,callable_client),load_knowledge()).interpret("topic")
    assert interpreted.topical_query=="topic" and interpreted.grounding is None
