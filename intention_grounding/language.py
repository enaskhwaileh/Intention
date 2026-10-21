"""Evidence-preserving adapter from the existing Interpreter to discovery.

No table metadata, gold, dataset IDs or column bindings enter interpretation.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import time

from .interpreter.core import interpret, validate, parse_response
from .interpreter.providers import GroqProvider, SYSTEM_PROMPT

VERSION='discovery-literal-adapter-v1'
PROMPT=SYSTEM_PROMPT+'''
Discovery adapter conventions: extract one literal argument per value. Use method for
an explicit statistic (mean/average/documented values), unit only for an explicitly
stated unit, population for the named population, measure for the named measurement,
time_grain for explicit daily/hourly wording, time_points for each exact ISO date,
time_range for an explicit ISO range or four-digit calendar year, groups for each
named group and group_dimension for an explicit grouping dimension. Do not invent
units, statistics, population codes, IDs, columns or unstated dates. Retain subject,
place, time and other restrictions in query_profile and arguments. Put unsupported
restrictions in constraints/other; they must not disappear. Missing statistic is
insufficient, not an instruction to compute a mean. Preserve competing candidates.
'''


def adapt(envelope):
    if envelope['failure']:
        raise ValueError('INTERPRETER_'+envelope['failure'])
    doc=envelope['interpretation'];text=doc['original_input']
    roles={};issues=[];origins={}
    intentions=doc['intentions']
    kind='unsupported'
    if len(intentions)==1:
        expression=intentions[0]['expression']['literal'].casefold()
        if re.search(r'\b(compare|contrast|comparison|difference|differ|versus)\b',expression):kind='compare'
        elif re.search(r'\b(predict|forecast|estimate)\b',expression):kind='predict'
    else:issues.append('SINGLE_INTENTION_REQUIRED')
    args=intentions[0]['arguments'] if len(intentions)==1 else []
    values={}
    for arg in args:values.setdefault(arg['role'],[]).append(arg['value'])
    for source,target in [('population','population'),('measure','measure_concept'),('unit','unit'),('time_grain','grain'),('group_dimension','group_role')]:
        candidates=values.get(source,[])
        if len(candidates)==1:
            roles[target]=candidates[0]['literal'];origins[target]=candidates[0]['evidence']
        elif candidates:issues.append('MULTIPLE_'+source.upper())
    method=values.get('method',[])
    method_map={'mean':'mean','average':'mean','arithmetic mean':'mean','documented values':'documented','documented':'documented','recorded values':'documented','observed values':'documented'}
    if len(method)==1 and method[0]['literal'].casefold() in method_map:
        roles['statistic']=method_map[method[0]['literal'].casefold()];origins['statistic']=method[0]['evidence']
    else:issues.append('STATISTIC_UNRESOLVED')
    dates=[v['literal'] for v in values.get('time_points',[])]
    ranges=values.get('time_range',[])
    if dates and all(re.fullmatch(r'\d{4}-\d{2}-\d{2}',d) for d in dates):
        roles['period']=[min(dates),max(dates)];origins['period']=[e for v in values['time_points'] for e in v['evidence']]
        if len(set(dates))>=2 and not values.get('groups'):
            roles['groups']=dates;roles['group_role']='date';origins['groups']=origins['period'];origins['group_role']=origins['period']
    if ranges:
        if len(ranges)!=1 or dates:issues.append('CONFLICTING_TIME_SCOPE')
        else:
            literal=ranges[0]['literal']
            if re.fullmatch(r'\d{4}',literal):roles['period']=[literal+'-01-01',literal+'-12-31']
            elif re.fullmatch(r'\d{4}-\d{2}-\d{2} (?:to|through) \d{4}-\d{2}-\d{2}',literal):roles['period']=[literal[:10],literal[-10:]]
            else:issues.append('TIME_SCOPE_UNRESOLVED')
            origins['period']=ranges[0]['evidence']
    groups=values.get('groups',[])
    if len(groups)>=2:
        roles['groups']=[v['literal'] for v in groups];origins['groups']=[e for v in groups for e in v['evidence']]
    # Every scope constraint must be represented by a consumed argument span.
    consumed={e for refs in origins.values() for e in refs}
    if any(not set(a['value']['evidence'])<=consumed for a in args):issues.append('UNCONSUMED_ARGUMENT')
    if intentions and (len(intentions[0]['candidates'])!=1 or intentions[0]['candidates'][0]['arguments']!=args):issues.append('CANDIDATE_ARGUMENTS_REQUIRE_REVIEW')
    restrictions=doc['query_profile']['constraints']
    if any(not set(v['evidence'])<=consumed for v in restrictions) or values.get('other') or values.get('threshold'):
        issues.append('UNSUPPORTED_SCOPE_RESTRICTION')
    required={'population','measure_concept','unit','grain','group_role','groups','period','statistic'}
    issues.extend('MISSING_'+k.upper() for k in sorted(required-roles.keys()))
    if len(roles.get('groups',[]))!=len(set(roles.get('groups',[]))):issues.append('DUPLICATE_GROUPS')
    # Retain exact subject and scope fragments, ordered by source offset. No model rewrite.
    refs={e for entries in doc['query_profile'].values() for v in entries for e in v['evidence']}
    refs.update(e for a in args if a['role']!='method' for e in a['value']['evidence'])
    spans=sorted((e for e in doc['evidence'] if e['id'] in refs),key=lambda e:(e['start'],e['end']))
    topical=' '.join(dict.fromkeys(e['text'] for e in spans)) or text
    status='ready' if doc['status']=='unambiguous' and not issues else 'ambiguous'
    if kind!='compare':status='unsupported'
    record={'schema_version':'1.0','request_id':doc['input_id'],'text':text,'input_mode':'validated_natural_language',
            'status':status,'intention_type':kind,'roles':roles,'topic':topical,
            'purpose':'Authored mock contract test; not measured LLM accuracy' if envelope['metadata'].get('provider')=='manual-replay' else 'Validated model extraction; semantic accuracy requires review'}
    # Invalid calendar dates and contradictory roles are explicit failures, never defaults.
    from .contracts import validate_request
    validate_request(record)
    return record,{'topical_query':topical,'scope_restrictions':restrictions,'argument_candidates':intentions,
                   'role_evidence':origins,'unresolved':issues,'adapter_version':VERSION,
                   'normalizations':['explicit ISO dates to inclusive bounds','explicit calendar year to inclusive bounds','explicit statistic lexical map'],
                   'table_bindings':None}


def interpret_input(text, input_id, *, model=None, provider=None, cache_dir=None, allow_live=False):
    provider=provider or GroqProvider(model=model, system_prompt=PROMPT, prompt_version=VERSION, max_retries=0)
    metadata={k:v for k,v in provider.metadata.items() if k not in ("usage", "actual_model")}
    key=hashlib.sha256(json.dumps([input_id,text,metadata,VERSION,PROMPT],sort_keys=True).encode()).hexdigest()
    path=Path(cache_dir)/ (key+'.json') if cache_dir else None
    start=time.perf_counter();cached=bool(path and path.exists())
    if cached:
        envelope=json.loads(path.read_text())
        if envelope.get('failure') is None:
            # Revalidate stored raw evidence; cached interpretation cannot bypass validation.
            envelope['interpretation']=validate(parse_response(envelope['raw_response']),input_id,text)
    else:
        if metadata.get('provider')=='groq' and not allow_live:
            raise ValueError('LIVE_VERIFICATION_BLOCKED_NO_APPROVED_SPENDING_BUDGET; cached response unavailable')
        envelope=interpret(input_id,text,provider)
        if path:
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('x') as handle:json.dump(envelope,handle,indent=2)
    envelope=copy.deepcopy(envelope)
    envelope['execution']={'response_cache_hit':cached,'cache_key':key,'elapsed_ms':round((time.perf_counter()-start)*1000,2),
                           'live_generation_attempts':int(not cached and metadata.get('provider')=='groq')}
    return envelope
