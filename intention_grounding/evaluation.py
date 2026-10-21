"""Evaluator-only usefulness metrics. Runtime discovery never imports this module."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from .contracts import validate
from .profiler import sha256


def request_metrics(ranking, candidates, labels, *, k=10):
    """Strict complete-judgment eligibility; unresolved/unjudged is never a zero gain."""
    if len(ranking)!=len(set(ranking)) or len(candidates)!=len(set(candidates)):
        raise ValueError('DUPLICATE_PREDICTION_ID')
    if not set(ranking)<=labels.keys() or not set(candidates)<=labels.keys():
        raise ValueError('PREDICTION_OUTSIDE_JUDGMENT_UNIVERSE')
    if any(v not in ('useful','not_useful','unresolved','unjudged') for v in labels.values()):
        raise ValueError('INVALID_JUDGMENT')
    positives={t for t,v in labels.items() if v=='useful'}
    if any(v in ('unresolved','unjudged') for v in labels.values()):
        return {'eligible':False,'reason':'incomplete_or_unresolved_judgments','ndcg_at_10':None,
                'success_at_1':None,'recall_at_10':None,'candidate_recall':None}
    if not positives:
        return {'eligible':False,'reason':'fully_judged_no_positive','ndcg_at_10':None,
                'success_at_1':None,'recall_at_10':None,'candidate_recall':None}
    dcg=sum((t in positives)/math.log2(i+2) for i,t in enumerate(ranking[:k]))
    ideal=sum(1/math.log2(i+2) for i in range(min(k,len(positives))))
    return {'eligible':True,'reason':None,'ndcg_at_10':dcg/ideal,
            'success_at_1':int(bool(ranking) and ranking[0] in positives),
            'recall_at_10':len(set(ranking[:k]) & positives)/len(positives),
            'candidate_recall':len(set(candidates)&positives)/len(positives)}


def evaluate(predictions_path, judgments_path, corpus_ids):
    path=Path(predictions_path)
    recorded=(path.parent/'predictions.sha256').read_text().strip()
    if sha256(path)!=recorded:
        raise ValueError('IMMUTABLE_PREDICTION_HASH_MISMATCH')
    report=json.loads(path.read_text())
    judgment=validate('judgments',json.loads(Path(judgments_path).read_text()))
    if not judgment['independently_reviewed'] or judgment['origin']!='independent_human_review':
        return {'status':'pending_independent_review','metrics':None}
    if judgment['corpus_sha256']!=report['corpus_sha256']:
        raise ValueError('JUDGMENT_CORPUS_MISMATCH')
    if judgment['request_sha256']!=report['request_sha256']:
        raise ValueError('JUDGMENT_REQUEST_MISMATCH')
    records=judgment['judgments']
    if any(r['request_id']!=report['request']['request_id'] for r in records):
        raise ValueError('JUDGMENT_REQUEST_ID_MISMATCH')
    if len({r['table_id'] for r in records})!=len(records):raise ValueError('DUPLICATE_JUDGMENT')
    if not {r['table_id'] for r in records}<=set(corpus_ids):raise ValueError('UNKNOWN_JUDGMENT_TABLE')
    labels={tid:'unjudged' for tid in corpus_ids}
    for row in records:
        if row['usefulness'] in ('useful','not_useful') and (not row['reviewer'] or not row['evidence']):
            raise ValueError('DECISIVE_LABEL_WITHOUT_REVIEW_EVIDENCE')
        labels[row['table_id']]=row['usefulness']
    ranking=[t['table_id'] for t in report['ranking']]
    metrics=request_metrics(ranking,[t['table_id'] for t in report['candidates']],labels)
    metrics.update({'request_grounded':report['grounded_intention']['status']=='grounded',
                    'recommendation_coverage':int(not report['abstained']),
                    'table_failure_count':report['diagnostics']['table_failures'],
                    'request_failure_count':int(report['grounded_intention']['status'] not in ('grounded','ambiguous','unsupported')),
                    'abstained':report['abstained']})
    if metrics['reason']=='fully_judged_no_positive':
        metrics['correct_abstention']=report['abstained']
        metrics['false_recommendation']=not report['abstained']
    verdicts=[v for t in report['ranking'] for p in t['procedures'] for v in p['requirements']]
    metrics['verdict_decision_coverage']=sum(v['verdict']!='unresolved' for v in verdicts)/len(verdicts) if verdicts else None
    # This evaluator computes one request; aggregate only eligible requests with denominators disclosed.
    return {'status':'evaluated' if metrics['eligible'] else 'ineligible', 'metrics':metrics,
            'prediction_sha256':recorded,'judgment_sha256':sha256(judgments_path),
            'notice':'Reviewer declarations and evidence require external audit; this program cannot authenticate human independence.'}


def annotation_template(report, corpus_ids):
    return {'schema_version':'1.0','origin':'annotation_candidate','independently_reviewed':False,
            'corpus_sha256':report['corpus_sha256'],'request_sha256':report['request_sha256'],
            'judgments':[{'request_id':report['request']['request_id'],'table_id':tid,
                          'topical':'unjudged','usefulness':'unjudged','reviewer':None,'evidence':[]}
                         for tid in corpus_ids]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--predictions',type=Path,required=True)
    parser.add_argument('--corpus',type=Path,default=Path('data/manifests/uci-bikes-v1.json'))
    parser.add_argument('--judgments',type=Path)
    parser.add_argument('--prepare-annotations',type=Path)
    args=parser.parse_args()
    corpus=json.loads(args.corpus.read_text());ids=[t['table_id'] for t in corpus['tables']]
    report=json.loads(args.predictions.read_text())
    if sha256(args.corpus)!=report['corpus_sha256']:parser.error('Corpus differs from prediction corpus')
    if args.prepare_annotations:
        with args.prepare_annotations.open('x') as handle:json.dump(annotation_template(report,ids),handle,indent=2)
        print('Unjudged annotation candidates written; no independent gold generated.')
    elif args.judgments:
        print(json.dumps(evaluate(args.predictions,args.judgments,ids),indent=2))
    else:parser.error('Choose --judgments or --prepare-annotations')


if __name__=='__main__':main()
