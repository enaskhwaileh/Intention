from intention.interpretation import DeterministicInterpreter, ground, requirements
from intention.knowledge import load_knowledge
from intention.profiling import profile_table
from intention.retrieval import BM25Retriever,RetrievalFailure,RetrievalRequest,RetrievalResult,RetrievalTiming,load_retrieval_policy
from intention.ranking import rank

def run(text,tables,k=None,provider=None,retriever=None,**ranking):
    kg=load_knowledge(); policy=load_retrieval_policy(); k=policy.default_k if k is None else k; provider=provider or DeterministicInterpreter(); retriever=retriever or BM25Retriever(); artifact=provider.interpret(text); interp=ground(text,artifact,kg); req=requirements(interp,kg)
    profiles={t.table_id:profile_table(t) for t in tables}
    if interp.topical_query is None:
        retrieval=RetrievalResult("failure",retriever.identity,RetrievalTiming(0,0,0,"not_started"),retriever.normalization,failure=RetrievalFailure("invalid_request","topical extraction failed; retrieval was not run",False))
    else: retrieval=retriever.retrieve(RetrievalRequest(interp.topical_query,k,"topical_only"),tables)
    by_id={table.table_id:table for table in tables}; candidates=[(by_id[item.table_id],item.relevance) for item in retrieval.candidates]
    return {"provider_artifact":artifact,"interpretation":interp,"requirements":req,"retrieval":retrieval,"profiles":profiles,"ranking":rank(candidates,profiles,req,kg,**ranking),"knowledge_hash":kg.digest}
