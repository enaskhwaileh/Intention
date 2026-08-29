from intention.retrieval.contracts import RetrievalCandidate,RetrievalFailure,RetrieverIdentity,RetrievalRequest,RetrievalResult,RetrievalTiming,ScoreNormalization
from .embedding import EmbeddingProvider
from .calibration import CosineEngineeringMapping,RelevanceCalibrator
from .vector_store import VectorStore

class SemanticRetriever:
    """Topical-only semantic retrieval: E_query(q_u), never E_query(u)."""
    def __init__(self,encoder:EmbeddingProvider,store:VectorStore,identity:RetrieverIdentity,normalization:ScoreNormalization|None=None,calibrator:RelevanceCalibrator|None=None):
        self.encoder=encoder; self.store=store; self.identity=identity; self.calibrator=calibrator or CosineEngineeringMapping(); calibrated_identity=self.calibrator.normalization
        if normalization is not None and normalization!=calibrated_identity: raise ValueError("semantic normalization must match the active calibrator")
        self.normalization=calibrated_identity
    def retrieve(self,request:RetrievalRequest,tables=None):
        if request.input_scope!="topical_only" or self.identity.input_scope!="topical_only": return RetrievalResult("failure",self.identity,RetrievalTiming(0,0,0,"provider"),self.normalization,failure=RetrievalFailure("invalid_request","semantic primary retriever accepts q_u only",False))
        encoded=self.encoder.encode_query(request.query)
        if encoded.status=="failure": return RetrievalResult("failure",self.identity,RetrievalTiming(0,encoded.elapsed_ms,encoded.elapsed_ms,"provider"),self.normalization,failure=RetrievalFailure("provider_error",encoded.failure.message,encoded.failure.retryable))
        hits=self.store.search(encoded.vectors[0],request.k)
        raw=[hit.score for hit in hits]; calibrated=self.calibrator.transform(raw)
        candidates=tuple(RetrievalCandidate(hit.table_id,hit.score,relevance,rank) for rank,(hit,relevance) in enumerate(zip(hits,calibrated),1))
        return RetrievalResult("success",self.identity,RetrievalTiming(0,encoded.elapsed_ms,encoded.elapsed_ms,"provider"),self.normalization,candidates)
