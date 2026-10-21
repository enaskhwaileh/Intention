"""Full-request BM25, with explicit tokenization and deterministic ties."""
from collections import Counter
import math
import re

VERSION='bm25_full_request_v1'


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.casefold())


def retrieve(request, tables, *, limit=None, k1=1.2, b=.75):
    documents=[tokens(t['retrieval_text']) for t in tables]
    n=len(documents)
    average=sum(map(len,documents))/n if n else 0
    terms=sorted(set(tokens(request)))
    df={term:sum(term in doc for doc in documents) for term in terms}
    results=[]
    for table,doc in zip(tables,documents):
        counts=Counter(doc);score=0.
        for term in terms:
            f=counts[term]
            if f:
                idf=math.log(1+(n-df[term]+.5)/(df[term]+.5))
                score+=idf*f*(k1+1)/(f+k1*(1-b+b*len(doc)/average))
        results.append({'table_id':table['table_id'],'retrieval_score':score,'method':VERSION})
    results.sort(key=lambda x:(-x['retrieval_score'],x['table_id']))
    # In the small pilot, all tables remain candidates, including lexical zero matches.
    return results if limit is None else results[:limit]
