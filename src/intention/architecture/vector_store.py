from abc import ABC,abstractmethod
from dataclasses import dataclass
import math
from uuid import NAMESPACE_URL,uuid5

@dataclass(frozen=True)
class CollectionConfig:
    name:str; version:str; dimension:int; metric:str; encoder_hash:str; serialization_hash:str; dataset_version:str; profile_version:str
    def __post_init__(self):
        if not self.name or not self.version or self.dimension<=0 or self.metric not in {"cosine","dot","euclidean"} or any(len(value)!=64 for value in (self.encoder_hash,self.serialization_hash)): raise ValueError("invalid vector collection configuration")

@dataclass(frozen=True)
class VectorRecord:
    table_id:str; vector:tuple[float,...]; payload:dict

@dataclass(frozen=True)
class SearchHit:
    table_id:str; score:float; payload:dict

class VectorStore(ABC):
    @abstractmethod
    def create_or_validate_collection(self,config:CollectionConfig): ...
    @abstractmethod
    def upsert(self,records:list[VectorRecord]): ...
    @abstractmethod
    def get(self,table_id:str)->VectorRecord|None: ...
    @abstractmethod
    def search(self,vector:tuple[float,...],limit:int)->list[SearchHit]: ...
    @abstractmethod
    def delete_collection(self): ...
    @abstractmethod
    def rebuild_collection(self,config:CollectionConfig,records:list[VectorRecord]): ...
    @abstractmethod
    def collection_config(self)->CollectionConfig|None: ...
    @property
    @abstractmethod
    def availability(self)->tuple[str,str|None]: ...

class InMemoryVectorStore(VectorStore):
    """Deterministic contract adapter for CI; never an experiment backend."""
    def __init__(self): self.config=None; self.records={}
    @property
    def availability(self): return ("available",None)
    def create_or_validate_collection(self,config):
        if self.config is not None and self.config!=config: raise ValueError("vector collection identity mismatch")
        self.config=config; return config
    def upsert(self,records):
        if self.config is None: raise RuntimeError("collection unavailable")
        for record in records:
            if len(record.vector)!=self.config.dimension or any(not math.isfinite(value) for value in record.vector): raise ValueError("vector identity mismatch")
            self.records[record.table_id]=record
    def get(self,table_id): return self.records.get(table_id)
    def search(self,vector,limit):
        if self.config is None or len(vector)!=self.config.dimension or limit<=0: raise ValueError("invalid vector search")
        def cosine(left,right):
            denominator=math.sqrt(sum(x*x for x in left))*math.sqrt(sum(x*x for x in right))
            return sum(x*y for x,y in zip(left,right))/denominator if denominator else 0.0
        hits=[SearchHit(record.table_id,cosine(vector,record.vector),record.payload) for record in self.records.values()]
        return sorted(hits,key=lambda hit:(-hit.score,hit.table_id))[:limit]
    def delete_collection(self): self.config=None; self.records={}
    def rebuild_collection(self,config,records): self.delete_collection(); self.create_or_validate_collection(config); self.upsert(records)
    def collection_config(self): return self.config

class QdrantVectorStore(VectorStore):
    """Preferred production adapter boundary. Qdrant is a rebuildable index."""
    IDENTITY_ID=str(uuid5(NAMESPACE_URL,"intention:qdrant:collection-identity"))
    def __init__(self,client=None,models_module=None): self.client=client; self.models_module=models_module; self.config=None
    @property
    def availability(self): return ("available",None) if self.client is not None else ("unavailable","qdrant client/service is not configured")
    def _require(self):
        if self.client is None: raise RuntimeError(self.availability[1])
    def create_or_validate_collection(self,config):
        self._require(); models=self._models(); exists=self.client.collection_exists(config.name)
        if not exists:
            self.client.create_collection(collection_name=config.name,vectors_config={"topical_dense":models.VectorParams(size=config.dimension,distance=self._distance(models,config.metric))})
            self.config=config
            self.client.upsert(collection_name=config.name,points=[models.PointStruct(id=self.IDENTITY_ID,vector={"topical_dense":[0.0]*config.dimension},payload={"record_type":"collection_identity","identity":self._identity_payload(config)})])
        else:
            info=self.client.get_collection(config.name); vectors=info.config.params.vectors
            dense=vectors.get("topical_dense") if hasattr(vectors,"get") else None
            if dense is None or dense.size!=config.dimension or str(dense.distance).lower().split(".")[-1]!=config.metric: raise ValueError("Qdrant vector schema mismatch")
            points=self.client.retrieve(collection_name=config.name,ids=[self.IDENTITY_ID],with_payload=True,with_vectors=False)
            if len(points)!=1 or points[0].payload.get("identity")!=self._identity_payload(config): raise ValueError("Qdrant collection identity mismatch")
            self.config=config
        return config
    def _models(self):
        if self.models_module is not None:return self.models_module
        try:
            from qdrant_client import models
            return models
        except ImportError as error: raise RuntimeError("qdrant-client dependency unavailable") from error
    def _distance(self,models,metric): return {"cosine":models.Distance.COSINE,"dot":models.Distance.DOT,"euclidean":models.Distance.EUCLID}[metric]
    def _identity_payload(self,config): return {"version":config.version,"dimension":config.dimension,"metric":config.metric,"encoder_hash":config.encoder_hash,"serialization_hash":config.serialization_hash,"dataset_version":config.dataset_version,"profile_version":config.profile_version}
    def _point_id(self,table_id): return str(uuid5(NAMESPACE_URL,f"intention:table:{table_id}"))
    def upsert(self,records):
        self._require(); models=self._models()
        if self.config is None: raise RuntimeError("Qdrant collection is not validated")
        points=[]
        for record in records:
            if len(record.vector)!=self.config.dimension or any(not math.isfinite(value) for value in record.vector): raise ValueError("vector identity mismatch")
            payload={**record.payload,"table_id":record.table_id,"record_type":"table"}; points.append(models.PointStruct(id=self._point_id(record.table_id),vector={"topical_dense":list(record.vector)},payload=payload))
        self.client.upsert(collection_name=self.config.name,points=points,wait=True)
    def get(self,table_id):
        self._require(); points=self.client.retrieve(collection_name=self.config.name,ids=[self._point_id(table_id)],with_payload=True,with_vectors=True)
        if not points:return None
        point=points[0]; vector=point.vector["topical_dense"] if isinstance(point.vector,dict) else point.vector
        payload={key:value for key,value in point.payload.items() if key not in {"table_id","record_type"}}
        return VectorRecord(table_id,tuple(vector),payload)
    def search(self,vector,limit):
        self._require()
        if self.config is None or len(vector)!=self.config.dimension or limit<=0: raise ValueError("invalid vector search")
        models=self._models(); response=self.client.query_points(collection_name=self.config.name,query=list(vector),using="topical_dense",limit=limit,with_payload=True,query_filter=models.Filter(must=[models.FieldCondition(key="record_type",match=models.MatchValue(value="table"))]))
        points=response.points if hasattr(response,"points") else response
        hits=[SearchHit(point.payload["table_id"],float(point.score),{key:value for key,value in point.payload.items() if key not in {"table_id","record_type"}}) for point in points]
        return sorted(hits,key=lambda hit:(-hit.score,hit.table_id))
    def delete_collection(self):
        self._require()
        if self.config:self.client.delete_collection(collection_name=self.config.name)
        self.config=None
    def rebuild_collection(self,config,records): self.delete_collection(); self.create_or_validate_collection(config); self.upsert(records)
    def collection_config(self): return self.config
