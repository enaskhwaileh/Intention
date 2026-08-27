from abc import ABC, abstractmethod
import math, re
from collections import Counter
from intention.contracts import Table

def tokens(text: str): return re.findall(r"[a-z0-9]+", text.lower())
class Retriever(ABC):
    @abstractmethod
    def retrieve(self, topical_query: str, tables: list[Table], k: int) -> list[tuple[Table,float]]: ...
class BM25Retriever(Retriever):
    def retrieve(self, topical_query, tables, k):
        docs=[tokens(t.title+" "+t.description+" "+" ".join(t.rows[0].keys() if t.rows else ())) for t in tables]; q=tokens(topical_query); n=len(docs)
        df=Counter(w for d in docs for w in set(d)); avg=sum(map(len,docs))/n if n else 1
        raw=[]
        for table,doc in zip(tables,docs):
            tf=Counter(doc); score=sum(math.log(1+(n-df[w]+.5)/(df[w]+.5))*tf[w]*2.2/(tf[w]+1.2*(.25+.75*len(doc)/avg)) for w in q)
            raw.append((table,score))
        maximum=max((s for _,s in raw),default=0); ranked=[(t,s/maximum if maximum else 0.0) for t,s in raw]
        return sorted(ranked,key=lambda x:(-x[1],x[0].table_id))[:k]
