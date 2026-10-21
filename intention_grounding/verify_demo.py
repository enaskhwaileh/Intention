"""Offline verification against acquired originals, not independent usefulness evaluation."""
import argparse
import csv
from decimal import Decimal
import io
import json
from pathlib import Path
import zipfile
from .discovery import ROOT, run
from .contracts import load_corpus, validate_splits


def verify(root=ROOT):
    root=Path(root)
    cases=json.loads((root/'data/requests/demo-v1.json').read_text())['cases']
    corpus=load_corpus(root/'data/manifests/uci-bikes-v1.json',root)
    split=json.loads((root/'data/splits/development-v1.json').read_text())
    validate_splits(split,corpus,[c['request'] for c in cases])
    results={c['request']['request_id']:run(c['request'],root=root,**c['run_options']) for c in cases}
    with zipfile.ZipFile(root/'data/raw/uci-275.zip') as archive:
        days=list(csv.DictReader(io.StringIO(archive.read('day.csv').decode())))
        hours=list(csv.DictReader(io.StringIO(archive.read('hour.csv').decode())))
    direct=results['dc_daily']['ranking'][0]
    assert direct['table_id']=='uci-275-day' and direct['overall_state']=='supported'
    actual=direct['procedures'][0]['execution']['rows']
    independent=[int(r['cnt']) for r in days if r['dteday'] in ('2011-01-01','2011-01-02')]
    assert independent==[985,801] and [r['value'] for r in actual]==independent
    means={}
    for rid,rows in [('dc_hourly_mean',hours),('dc_daily_mean',days)]:
        sql=results[rid]['ranking'][0]['procedures'][0]['execution']['rows']
        by_group={r['workingday']:r['value'] for r in sql}
        means[rid]={}
        for group in ['0','1']:
            values=[Decimal(r['cnt']) for r in rows if r['dteday'].startswith('2011-') and r['workingday']==group]
            mean=sum(values)/len(values)
            assert abs(by_group[group]-float(mean))<1e-9
            means[rid][group]={'n':len(values),'sum':str(sum(values)),'mean':str(mean)}
    assert all(t['overall_state']=='unresolved' for t in results['metadata_gap']['ranking'])
    assert results['metadata_gap']['abstained'] and results['no_population_match']['abstained']
    assert results['statistic_ambiguous']['grounded_intention']['status']=='ambiguous'
    assert results['predict_pending']['grounded_intention']['status']=='unsupported'
    return {'status':'passed','origin':'execution diagnostics verified against original archive rows',
            'effectiveness_metrics':None,'independent_usefulness_judgments':False,
            'direct_values':independent,'difference_second_minus_first':-184,'independent_decimal_means':means,
            'cases':{key:{'top_table':value['ranking'][0]['table_id'],'abstained':value['abstained'],
                          **value['diagnostics']} for key,value in results.items()},
            'normalized_hashes':{t['table_id']:t['normalized_sha256'] for t in corpus['tables']}}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
