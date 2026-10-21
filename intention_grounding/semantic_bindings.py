"""Small manually curated request vocabulary, applied only at table assessment.

Mappings do not establish suitability: source documentation, grain, scope and actual
values must still pass every existing requirement. Unknown terms stay unresolved.
"""
import copy

VERSION='uci-bike-request-vocabulary-v1'
VOCABULARY={
 'population':{'capital bikeshare washington dc':'capital_bikeshare_dc','capital bikeshare in washington dc':'capital_bikeshare_dc','seoul bike system':'seoul_bike_system'},
 'measure_concept':{'bike rental counts':'bike_rental_count','bike rental count':'bike_rental_count','rental counts':'bike_rental_count'},
 'unit':{'rentals':'rentals'},
 'grain':{'daily':'day','day':'day','hourly':'hour','hour':'hour'},
 'group_role':{'date':'date','working-day status':'workingday','working day status':'workingday'},
 'groups':{'working days':'1','working day':'1','weekends and holidays':'0','non-working days':'0'}
}


def bind(procedure):
    bound=copy.deepcopy(procedure)
    if procedure.get('input_mode')!='validated_natural_language':return bound,None
    original=copy.deepcopy(bound['bindings'])
    for role in ('population','measure_concept','unit','grain','group_role'):
        bound['bindings'][role]=VOCABULARY[role].get(str(original.get(role,'')).casefold())
    if bound['bindings']['group_role']!='date':
        bound['bindings']['groups']=[VOCABULARY['groups'].get(g.casefold(),g) for g in original.get('groups',[])]
    return bound,{'id':'request-vocabulary','fact':'manual_literal_to_semantic_mapping','version':VERSION,
                  'original_roles':original,'mapped_roles':bound['bindings'],
                  'limitation':'Curated terminology mapping; not inferred by similarity or independently evaluated.'}
