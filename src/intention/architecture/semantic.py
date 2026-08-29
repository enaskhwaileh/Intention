from intention.retrieval.contracts import RetrievalCandidate,RetrievalFailure,RetrieverIdentity,RetrievalRequest,RetrievalResult,RetrievalTiming,ScoreNormalization
from .embedding import EmbeddingProvider
from .vector_store import VectorStore

class SemanticRetriever:
    """Topical-only semantic retrieval: E_query(q_u), never E_query(u)."""
    def __init__(self,encoder:EmbeddingProvider,store:VectorStore,identity:RetrieverIdentity,normalization:ScoreNormalization): self.encoder=encoder; self.store=store; self.identity=identity; self.normalization=normalization
    def retrieve(self,request:RetrievalRequest,tables=None):
        if request.input_scope!="topical_only" or self.identity.input_scope!="topical_only": return RetrievalResult("failure",self.identity,RetrievalTiming(0,0,0,"provider"),self.normalization,failure=RetrievalFailure("invalid_request","semantic primary retriever accepts q_u only",False))
        encoded=self.encoder.encode_query(request.query)
        if encoded.status=="failure": return RetrievalResult("failure",self.identity,RetrievalTiming(0,encoded.elapsed_ms,encoded.elapsed_ms,"provider"),self.normalization,failure=RetrievalFailure("provider_error",encoded.failure.message,encoded.failure.retryable))
        hits=self.store.search(encoded.vectors[0],request.k)
        raw=[hit.score for hit in hits]; low=min(raw,default=0); high=max(raw,default=0)
        relevance=lambda score:(score-low)/(high-low) if high>low else (1.0 if raw else 0.0)
        candidates=tuple(RetrievalCandidate(hit.table_id,hit.score,relevance(hit.score),rank) for rank,hit in enumerate(hits,1))
        return RetrievalResult("success",self.identity,RetrievalTiming(0,encoded.elapsed_ms,encoded.elapsed_ms,"provider"),self.normalization,candidates)
