from hashlib import sha256
import json,math,time
from .embedding import EmbeddingFailure,EmbeddingIdentity,EmbeddingProvider,EmbeddingResult

class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    """Generic pinned SentenceTransformers adapter; model loading is opt-in."""
    def __init__(self,registration,dimension=None,device="cpu",model_factory=None,tokenizer_factory=None,clock=None):
        record=registration.record if hasattr(registration,"record") else registration
        if not record.get("tokenizer_revision") or len(record["revision"])!=40 or len(record["tokenizer_revision"])!=40: raise ValueError("exact model and tokenizer revisions required")
        allowed=record["dimensions"]; dimension=dimension or max(allowed)
        bounds=record.get("dimension_range")
        if bounds and not bounds[0]<=dimension<=bounds[1] or not bounds and dimension not in allowed: raise ValueError("unsupported embedding dimension")
        config={"model":record["model"],"revision":record["revision"],"tokenizer_revision":record["tokenizer_revision"],"dimension":dimension,"device":device,"query_instruction":record["query_instruction"],"document_instruction":record["document_instruction"],"maximum_input_tokens":record["maximum_input_tokens"],"truncation_policy":record["truncation_policy"]}
        digest=sha256(json.dumps(config,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        self._identity=EmbeddingIdentity(record["provider"],record["model"],record["revision"],record["tokenizer_revision"],dimension,record["normalization"],record["similarity"],record["query_instruction"],record["document_instruction"],record["maximum_input_tokens"],record["truncation_policy"],device,digest)
        self.record=record; self.clock=clock or time.perf_counter; self.model=None; self.tokenizer=None; self.failure=None
        try:
            if model_factory is None:
                from sentence_transformers import SentenceTransformer
                model_factory=lambda **kwargs:SentenceTransformer(kwargs.pop("model_name"),**kwargs)
            if tokenizer_factory is None:
                from transformers import AutoTokenizer
                tokenizer_factory=lambda **kwargs:AutoTokenizer.from_pretrained(kwargs.pop("model_name"),**kwargs)
            self.model=model_factory(model_name=record["model"],revision=record["revision"],device=device,truncate_dim=dimension)
            self.tokenizer=tokenizer_factory(model_name=record["model"],revision=record["tokenizer_revision"])
        except Exception as error: self.failure=f"model unavailable: {error}"
    @property
    def identity(self): return self._identity
    def _format(self,text,mode):
        instruction=self.identity.query_instruction if mode=="query" else self.identity.document_instruction
        return instruction.replace("{content}",text) if instruction and "{content}" in instruction else f"{instruction}{text}" if instruction else text
    def _encode(self,texts,mode):
        if self.failure:return EmbeddingResult("failure",self.identity,(),0,EmbeddingFailure("unavailable",self.failure))
        if not texts or any(not isinstance(text,str) or not text.strip() for text in texts): return EmbeddingResult("failure",self.identity,(),0,EmbeddingFailure("invalid_input","non-empty text batch required"))
        formatted=[self._format(text,mode) for text in texts]
        try:
            lengths=[len(self.tokenizer(text,add_special_tokens=True,truncation=False)["input_ids"]) for text in formatted]
            if any(length>self.identity.maximum_input_length for length in lengths): return EmbeddingResult("failure",self.identity,(),0,EmbeddingFailure("input_too_long","input exceeds frozen token limit"))
            started=self.clock(); output=self.model.encode(formatted,batch_size=len(formatted),normalize_embeddings=True,convert_to_numpy=False); elapsed=(self.clock()-started)*1000
            vectors=[]
            for vector in output:
                values=vector.tolist() if hasattr(vector,"tolist") else list(vector); values=values[:self.identity.dimension]
                norm=math.sqrt(sum(value*value for value in values))
                if not norm or any(not math.isfinite(value) for value in values): raise ValueError("non-finite or zero embedding")
                vectors.append(tuple(value/norm for value in values))
            return EmbeddingResult("success",self.identity,tuple(vectors),elapsed)
        except Exception as error:
            code="out_of_memory" if "out of memory" in str(error).lower() else "provider_error"
            return EmbeddingResult("failure",self.identity,(),0,EmbeddingFailure(code,str(error),code=="out_of_memory"))
    def encode_queries(self,texts): return self._encode(texts,"query")
    def encode_documents(self,texts): return self._encode(texts,"document")
