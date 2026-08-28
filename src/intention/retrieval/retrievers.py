"""Common retrieval interface and deterministic BM25 reference adapter."""
from abc import ABC,abstractmethod
import math,re,time
from collections import Counter
from collections.abc import Callable
from intention.contracts import Table
from .contracts import RetrievalCandidate,RetrievalFailure,RetrieverIdentity,RetrievalRequest,RetrievalResult,RetrievalTiming
from .serialization import TableSerializer,load_retrieval_policy

def tokens(text: str): return re.findall(r"[a-z0-9]+",text.lower())

class Retriever(ABC):
    @property
    @abstractmethod
    def identity(self) -> RetrieverIdentity: ...
    @abstractmethod
    def retrieve(self,request: RetrievalRequest,tables: list[Table]) -> RetrievalResult: ...

class BM25Retriever(Retriever):
    """Offline reference adapter over the frozen title/description/schema view."""
    def __init__(self,clock: Callable[[],float]|None=None,clock_name: str="perf_counter"):
        policy=load_retrieval_policy(); serialization_id="title_description_schema_v1"
        self.serializer=TableSerializer(policy.serializations[serialization_id])
        self._identity=RetrieverIdentity("BM25","1.0.0",serialization_id,"topical_only")
        self.clock=clock or time.perf_counter; self.clock_name=clock_name
    @property
    def identity(self): return self._identity
    def retrieve(self,request,tables):
        if request.input_scope!=self.identity.input_scope:
            return RetrievalResult("failure",self.identity,RetrievalTiming(0,0,0,self.clock_name),failure=RetrievalFailure("invalid_request","BM25 accepts topical_query only",False))
        started=self.clock()
        try: documents=[self.serializer.serialize(table) for table in tables]
        except Exception as error:
            elapsed=max(0,(self.clock()-started)*1000)
            return RetrievalResult("failure",self.identity,RetrievalTiming(elapsed,0,elapsed,self.clock_name),failure=RetrievalFailure("serialization_error",str(error),False))
        serialized=self.clock(); docs=[tokens(document.text) for document in documents]; query=tokens(request.query); count=len(docs)
        df=Counter(word for document in docs for word in set(document)); average=sum(map(len,docs))/count if count else 1
        raw=[]
        for table,document in zip(tables,docs):
            tf=Counter(document); score=sum(math.log(1+(count-df[word]+.5)/(df[word]+.5))*tf[word]*2.2/(tf[word]+1.2*(.25+.75*len(document)/average)) for word in query)
            raw.append((table.table_id,score))
        maximum=max((score for _,score in raw),default=0); ranked=sorted(((table_id,score/maximum if maximum else 0.0) for table_id,score in raw),key=lambda item:(-item[1],item[0]))[:request.k]
        finished=self.clock(); serialization_ms=max(0,(serialized-started)*1000); inference_ms=max(0,(finished-serialized)*1000)
        candidates=tuple(RetrievalCandidate(table_id,relevance,index) for index,(table_id,relevance) in enumerate(ranked,1))
        return RetrievalResult("success",self.identity,RetrievalTiming(serialization_ms,inference_ms,serialization_ms+inference_ms,self.clock_name),candidates)
