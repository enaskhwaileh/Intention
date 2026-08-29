from abc import ABC,abstractmethod
from dataclasses import dataclass
import math

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
    def __init__(self,client=None): self.client=client; self.config=None
    @property
    def availability(self): return ("available",None) if self.client is not None else ("unavailable","qdrant client/service is not configured")
    def _require(self):
        if self.client is None: raise RuntimeError(self.availability[1])
    def create_or_validate_collection(self,config):
        self._require(); existing=self.client.get_collection_config(config.name)
        if existing is None:self.client.create_collection(config)
        elif existing!=config:raise ValueError("Qdrant collection identity mismatch")
        self.config=config; return config
    def upsert(self,records): self._require(); self.client.upsert(self.config.name,records)
    def get(self,table_id): self._require(); return self.client.get(self.config.name,table_id)
    def search(self,vector,limit): self._require(); return self.client.search(self.config.name,vector,limit)
    def delete_collection(self):
        self._require()
        if self.config:self.client.delete_collection(self.config.name)
        self.config=None
    def rebuild_collection(self,config,records): self.delete_collection(); self.create_or_validate_collection(config); self.upsert(records)
    def collection_config(self): return self.config
