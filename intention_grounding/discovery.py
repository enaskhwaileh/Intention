"""One end-to-end development discovery path, reusing grounding/profiling/assessment."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import uuid

from .contracts import validate_request, load_corpus
from .grounder import ground_request
from .interpreter.core import interpret_structured
from .profiler import profile_table, sha256
from .retrieval import retrieve
from .aligner import assess_table

ROOT=Path(__file__).resolve().parent.parent


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def run(request, *, root=ROOT, manifest_path=None, execute=True, withhold_semantics=False, candidate_limit=None, retrieval_method="bm25", topical_query=None, encoder=None, interpreter_envelope=None):
    start=time.perf_counter();root=Path(root)
    validate_request(request)
    manifest_path=Path(manifest_path or root/'data/manifests/uci-bikes-v1.json')
    corpus=load_corpus(manifest_path,root)
    # Public request + metadata only. No judgment path or annotation loader exists here.
    interpreted=interpreter_envelope or interpret_structured(request)
    grounding=ground_request(request)
    query=request['text'] if retrieval_method in ('bm25','sbert-full') else topical_query
    if retrieval_method=='bm25':
        candidates=retrieve(query,corpus['tables'],limit=candidate_limit)
    elif retrieval_method in ('sbert','sbert-full'):
        from .semantic_retrieval import retrieve as semantic_retrieve
        if not query:raise ValueError('TOPICAL_QUERY_REQUIRED_FOR_SBERT')
        candidates=semantic_retrieve(query,corpus['tables'],root,encoder=encoder,limit=candidate_limit,
                                    query_mode='full_request' if retrieval_method=='sbert-full' else 'topical')
    else:raise ValueError('UNKNOWN_RETRIEVAL_METHOD')
    tables={t['table_id']:t for t in corpus['tables']}
    ranking=[]
    for candidate in candidates:
        table=tables[candidate['table_id']]
        try:
            profile=profile_table(root/table['path'],dataset_id=table['table_id'],source_metadata=table,
                                  cache_dir=root/'data/runtime/profiles')
            assessment=assess_table(table,profile,grounding,root,execute=execute,withhold_semantics=withhold_semantics)
            ranking.append({**candidate,**assessment,'profile':profile,'title':table['table_id'],'failure':None})
        except (ValueError,OSError) as exc:
            ranking.append({**candidate,'overall_state':'unresolved','procedures':[],
                            'failure':type(exc).__name__,'reason':'Table inspection or execution failed; no suitability asserted.'})
    policy_path=ROOT/'configs/pilot-ranking-v1.json'
    policy=json.loads(policy_path.read_text())
    if policy['policy_id']!='procedure_state_then_bm25_v1' or policy['state_order']!=['supported','unresolved','violated']:
        raise ValueError('UNSUPPORTED_RANKING_POLICY')
    policy={**policy,'retrieval_method':retrieval_method,'within_state_score':'BM25' if retrieval_method=='bm25' else 'SBERT cosine similarity','status':'pilot policy; not final paper scoring'}
    if retrieval_method!='bm25':
        policy.update(policy_id='procedure_state_then_sbert_v1',within_state=['sbert_cosine_descending','table_id_ascending'])
    state_order={s:i for i,s in enumerate(policy['state_order'])}
    ranking.sort(key=lambda x:(state_order[x['overall_state']],-x['retrieval_score'],x['table_id']))
    for index,table in enumerate(ranking,1):
        table['rank']=index
        table['tie_key']=[table['overall_state'],table['retrieval_score']]
        table['tied_on_evidence_and_retrieval']=[r['table_id'] for r in ranking if r['table_id']!=table['table_id'] and r['overall_state']==table['overall_state'] and r['retrieval_score']==table['retrieval_score']]
        table['ranking_explanation']='Evidence state first; '+policy['within_state_score']+' descending; exact ties by table ID. Not a probability.'
    abstain=grounding['status']!='grounded' or not any(r['overall_state']=='supported' for r in ranking)
    return {'schema_version':'1.0','run_id':'discovery-'+uuid.uuid4().hex[:12],
            'created_at':datetime.now(timezone.utc).isoformat(),'request':request,
            'interpreter':interpreted,
            'grounded_intention':grounding,'candidates':candidates,'ranking':ranking,'abstained':abstain,
            'retrieval_query':query,'retrieval_method':retrieval_method,'ranking_policy':policy,'ranking_policy_sha256':digest(policy),'ranking_policy_config_sha256':sha256(policy_path),
            'corpus_id':corpus['corpus_id'],'corpus_sha256':sha256(manifest_path),'request_sha256':digest(request),
            'il_version':grounding['il_version'],'il_sha256':sha256(ROOT/'intention_grounding/library/compare-procedures-v1.json'),
            'diagnostics':{'elapsed_ms':round((time.perf_counter()-start)*1000,2),
                           'candidate_count':len(candidates),'table_failures':sum(bool(t['failure']) for t in ranking),
                           'supported_tables':sum(t['overall_state']=='supported' for t in ranking),
                           'withheld_semantics':withhold_semantics,'live_model_calls':interpreted.get('execution',{}).get('live_generation_attempts',0)},
            'effectiveness':{'status':'pending_independent_judgments','metrics':None},
            'limitations':['Input mode: '+request['input_mode']+'; language accuracy not independently evaluated. Manual semantic mappings remain in use.',
                           'Development-only corpus: two source families, one topic; no held-out claim.',
                           'Predict, Qwen, semantic matching, TABERTA and LLM usefulness comparisons are not implemented.']}


def save_report(report, output):
    from .dashboard import identity
    report['code_identity']=identity()
    directory=Path(output)/report['run_id'];directory.mkdir(parents=True,exist_ok=False)
    path=directory/'predictions.json'
    # Exclusive creation: evaluation never rewrites this artifact.
    with path.open('x',encoding='utf-8') as handle:json.dump(report,handle,indent=2,ensure_ascii=False)
    digest_path=directory/'predictions.sha256'
    digest_path.write_text(sha256(path)+'\n')
    return path


def run_text(text, *, input_id='live-input-1', model=None, provider=None, allow_live=False,
             root=ROOT, retrieval_method='sbert', encoder=None, execute=False, **kwargs):
    """One validated generation, deterministic grounding, then the existing pipeline."""
    from .language import interpret_input, adapt
    from .provider_errors import provider_diagnostic
    start=time.perf_counter()
    envelope=None
    try:
        envelope=interpret_input(text,input_id,model=model,provider=provider,allow_live=allow_live,
                                 cache_dir=Path(root)/'data/runtime/responses')
        request,adapter=adapt(envelope)
        envelope['adapter']=adapter
        envelope['structured_intention_record']=request
        report=run(request,root=root,retrieval_method=retrieval_method,topical_query=adapter['topical_query'],
                   encoder=encoder,interpreter_envelope=envelope,execute=execute,**kwargs)
        report['diagnostics']['end_to_end_ms']=round((time.perf_counter()-start)*1000,2)
        return report
    except (ValueError,RuntimeError,ImportError,OSError) as exc:
        # Only our fixed diagnostic prefixes are printable; provider messages are never copied.
        message=str(exc)
        allowed=('INTERPRETER_','LIVE_VERIFICATION_BLOCKED','SBERT_UNAVAILABLE','INVALID_','MISSING_','TOPICAL_QUERY_')
        return {'schema_version':'1.0','run_id':'discovery-'+uuid.uuid4().hex[:12],
                'created_at':datetime.now(timezone.utc).isoformat(),'input':text,'input_id':input_id,
                'status':'failed','failure':message if message.startswith(allowed) else type(exc).__name__,
                'provider_error':provider_diagnostic(exc),'interpreter':envelope,'ranking':[],
                'abstained':True,'retrieval_method':retrieval_method,
                'diagnostics':{'end_to_end_ms':round((time.perf_counter()-start)*1000,2)},
                'effectiveness':{'status':'pending_independent_judgments','metrics':None}}
