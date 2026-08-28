from intention.retrieval import BM25Retriever,load_retriever_registry

EXTERNAL={"EDBT25-Semantic","TABERTA-Hybrid","TABERTA-FullInput","Birdie","Qwen3-Embedding-8B","Qwen3-Reranker-8B"}
def baseline(name,config=None):
    registry=load_retriever_registry()
    if name=="BM25": return BM25Retriever()
    if name in EXTERNAL:
        record=registry.retrievers[name]
        raise RuntimeError(f"{name} unavailable: {record.failure_reason}; no approximation substituted")
    if name=="Ours": raise ValueError("Ours is the complete pipeline, not a first-stage retriever")
    raise ValueError(f"unknown baseline {name}")
