from intention.retrieval import BM25Retriever

EXTERNAL={"EDBT25-Semantic","TABERTA-Hybrid","TABERTA-FullInput","Birdie","Qwen3-Embedding-8B","Qwen3-Reranker-8B"}
def baseline(name,config=None):
    if name=="BM25": return BM25Retriever()
    if name in EXTERNAL: raise RuntimeError(f"{name} unavailable: configure an exact model revision and adapter; no approximation substituted")
    if name=="Ours": raise ValueError("Ours is the complete pipeline, not a first-stage retriever")
    raise ValueError(f"unknown baseline {name}")
