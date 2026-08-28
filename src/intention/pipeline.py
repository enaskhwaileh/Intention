from intention.interpretation import DeterministicInterpreter, ground, requirements
from intention.knowledge import load_knowledge
from intention.profiling import profile_table
from intention.retrieval import BM25Retriever
from intention.ranking import rank

def run(text,tables,k=20,provider=None,**ranking):
    kg=load_knowledge(); provider=provider or DeterministicInterpreter(); artifact=provider.interpret(text); interp=ground(text,artifact,kg); req=requirements(interp,kg)
    profiles={t.table_id:profile_table(t) for t in tables}
    candidates=BM25Retriever().retrieve(interp.topical_query,tables,k)
    return {"provider_artifact":artifact,"interpretation":interp,"requirements":req,"profiles":profiles,"ranking":rank(candidates,profiles,req,kg,**ranking),"knowledge_hash":kg.digest}
