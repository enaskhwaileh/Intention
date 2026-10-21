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


def run(request, *, root=ROOT, manifest_path=None, execute=True, withhold_semantics=False, candidate_limit=None):
    start=time.perf_counter();root=Path(root)
    validate_request(request)
    manifest_path=Path(manifest_path or root/'data/manifests/uci-bikes-v1.json')
    corpus=load_corpus(manifest_path,root)
    # Public request + metadata only. No judgment path or annotation loader exists here.
    interpreted=interpret_structured(request)
    grounding=ground_request(interpreted['structured_intention_record'])
    candidates=retrieve(request['text'],corpus['tables'],limit=candidate_limit)
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
    state_order={s:i for i,s in enumerate(policy['state_order'])}
    ranking.sort(key=lambda x:(state_order[x['overall_state']],-x['retrieval_score'],x['table_id']))
    for index,table in enumerate(ranking,1):
        table['rank']=index
        table['tie_key']=[table['overall_state'],table['retrieval_score']]
        table['tied_on_evidence_and_retrieval']=[r['table_id'] for r in ranking if r['table_id']!=table['table_id'] and r['overall_state']==table['overall_state'] and r['retrieval_score']==table['retrieval_score']]
        table['ranking_explanation']='Evidence state first; full-request BM25 descending; exact ties by table ID. Not a probability.'
    abstain=grounding['status']!='grounded' or not any(r['overall_state']=='supported' for r in ranking)
    return {'schema_version':'1.0','run_id':'discovery-'+uuid.uuid4().hex[:12],
            'created_at':datetime.now(timezone.utc).isoformat(),'request':request,
            'interpreter':interpreted,
            'grounded_intention':grounding,'candidates':candidates,'ranking':ranking,'abstained':abstain,
            'ranking_policy':policy,'ranking_policy_sha256':sha256(policy_path),
            'corpus_id':corpus['corpus_id'],'corpus_sha256':sha256(manifest_path),'request_sha256':digest(request),
            'il_version':grounding['il_version'],'il_sha256':sha256(ROOT/'intention_grounding/library/compare-procedures-v1.json'),
            'diagnostics':{'elapsed_ms':round((time.perf_counter()-start)*1000,2),
                           'candidate_count':len(candidates),'table_failures':sum(bool(t['failure']) for t in ranking),
                           'supported_tables':sum(t['overall_state']=='supported' for t in ranking),
                           'withheld_semantics':withhold_semantics,'live_model_calls':0},
            'effectiveness':{'status':'pending_independent_judgments','metrics':None},
            'limitations':['Authored structured demonstration, not measured language interpretation.',
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
