"""Evidence-backed table binding and read-only SQLite comparison operators."""
import json
import math
from pathlib import Path
import sqlite3

from .profiler import read_table, sha256


def quote_identifier(name):
    if not isinstance(name,str) or not name or '\x00' in name:
        raise ValueError('INVALID_IDENTIFIER')
    return '"'+name.replace('"','""')+'"'


def build_sql(procedure, columns):
    bindings=procedure['bindings']
    group,measure,date=[quote_identifier(columns[k]) for k in ('group','measure','date')]
    placeholders=','.join('?' for _ in bindings['groups'])
    template=procedure['sql_template']
    sql=template.format(group=group,measure=measure,date=date,placeholders=placeholders)
    return sql,[*bindings['period'],*bindings['groups']]


def execute_readonly(rows, names, columns, procedure):
    connection=sqlite3.connect(':memory:')
    try:
        declaration=','.join(quote_identifier(n)+(' REAL' if n==columns['measure'] else ' TEXT') for n in names)
        connection.execute('CREATE TABLE observations ('+declaration+')')
        converted=[]
        for row in rows:
            values=[]
            for name in names:
                value=row.get(name)
                if name==columns['measure']:
                    try:value=float(value)
                    except (TypeError,ValueError):value=None
                    if value is not None and not math.isfinite(value):value=None
                values.append(value)
            converted.append(values)
        connection.executemany('INSERT INTO observations VALUES ('+','.join('?' for _ in names)+')',converted)
        connection.execute('PRAGMA query_only=ON')
        allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION}
        connection.set_authorizer(lambda op,*args: sqlite3.SQLITE_OK if op in allowed else sqlite3.SQLITE_DENY)
        traces=[];connection.set_trace_callback(traces.append)
        sql,parameters=build_sql(procedure,columns)
        cursor=connection.execute(sql,parameters)
        labels=[col[0] for col in cursor.description]
        result=[dict(zip(labels,row)) for row in cursor.fetchall()]
        group_name=columns['group']
        by_group={str(row[group_name]):row['value'] for row in result}
        groups=procedure['bindings']['groups']
        difference=by_group[groups[1]]-by_group[groups[0]] if len(groups)==2 and all(g in by_group for g in groups) else None
        return {'status':'executed','engine':'sqlite','engine_version':sqlite3.sqlite_version,
                'parameterized_sql':sql,'parameters':parameters,'instantiated_sql':traces[-1],
                'rows':result,'difference_second_minus_first':difference,'group_order':groups,
                'notice':'Descriptive scoped comparison; SQL success is not causal evidence or retrieval effectiveness.'}
    finally:
        connection.close()


def assess_procedure(table, profile, procedure, root, *, withhold_semantics=False, execute=True):
    """No header similarity is used as semantic proof. Every decision cites scoped evidence."""
    roles=procedure['bindings'];semantics={} if withhold_semantics else table.get('semantics',{})
    document=semantics.get('source_document')
    evidence={item['id']:item for item in profile['evidence']}
    evidence['metadata-inspection']={'id':'metadata-inspection','fact':'semantic_documentation_inspection',
                                    'present':bool(document),'withheld_for_diagnostic':withhold_semantics,
                                    'scope':table['table_id'],'source':{'table_sha256':profile['file_sha256'],
                                    'manifest_record':table['table_id']}}
    if document:
        evidence['source-document']={'id':'source-document','fact':'documented_table_semantics',
                                    'source':document,'semantics':semantics,'scope':table['table_id'],
                                    'limitation':'Project-authored source mapping, not independent usefulness gold.'}
    verdicts=[]
    def add(name,state,reason,refs):
        assert state in ('supported','violated','unresolved') and refs and all(r in evidence for r in refs)
        verdicts.append({'requirement_id':name,'verdict':state,'reason':reason,'evidence_refs':refs})
    add('documented_semantics','supported' if document else 'unresolved',
        'Source documentation and an explicit semantic mapping are available.' if document else 'Semantic documentation unavailable; column names do not prove meaning.',
        ['source-document'] if document else ['metadata-inspection'])
    for key in ('population','measure_concept','unit','grain'):
        value=semantics.get(key)
        state='unresolved' if not document or value is None else 'supported' if value==roles[key] else 'violated'
        add(key,state,f'Requested {roles[key]}; documented {value if document else "unresolved"}.',
            ['source-document'] if document else ['metadata-inspection'])
    kind=semantics.get('measure_kind')
    state='unresolved' if not document or kind is None else 'supported' if kind=='interval_count' else 'violated'
    add('observation_kind',state,'Only documented interval counts are implemented. Precomputed means cannot be averaged without weights.',
        ['source-document'] if document else ['metadata-inspection'])
    mapped=semantics.get('columns',{}) if document else {}
    columns={'measure':mapped.get('measure'),'date':mapped.get('date'),'group':mapped.get(roles['group_role'])}
    names=profile['column_names']
    bound=all(v in names for v in columns.values())
    add('role_binding','supported' if bound else 'unresolved','Explicit documented columns '+json.dumps(columns),
        ['source-document','table-scan'] if document else ['metadata-inspection','table-scan'])
    scoped=[]
    rows=[]
    if bound:
        if sha256(Path(root)/table['path']) != profile['file_sha256']:
            raise ValueError('TABLE_CHANGED_AFTER_PROFILE')
        rows,_,_=read_table(Path(root)/table['path'])
        dates=[str(r[columns['date']]) for r in rows if r.get(columns['date'])]
        # Only normalized ISO dates are accepted. The acquisition command records the transformation.
        from datetime import date
        try:
            for d in dates: date.fromisoformat(d)
            date_valid=bool(dates)
        except ValueError: date_valid=False
        start,end=roles['period']
        evidence['scope-scan']={'id':'scope-scan','fact':'full_table_date_and_group_scan',
                                'source':{'path':profile['source_file'],'sha256':profile['file_sha256']},
                                'scope':{'period':[start,end],'groups':roles['groups'],'columns':columns},
                                'complete':True,'date_range':[min(dates),max(dates)] if dates else None}
        state='unresolved' if not date_valid else 'supported' if min(dates)<=start<=end<=max(dates) else 'violated'
        add('period',state,'Requested date bounds versus full observed date extent; does not certify a complete time grid.',['scope-scan'])
        scoped=[row for row in rows if start<=str(row.get(columns['date'],''))<=end and str(row.get(columns['group'])) in roles['groups']] if date_valid else []
        counts={g:sum(str(r[columns['group']])==g for r in scoped) for g in roles['groups']}
        evidence['scope-scan']['group_counts']=counts
        evidence['scope-scan']['rows_scanned']=len(rows)
        add('group_coverage','supported' if all(counts.values()) else 'violated' if date_valid else 'unresolved',
            'Exact group counts in a full scoped scan: '+json.dumps(counts),['scope-scan'])
        invalid=0
        for row in scoped:
            value=row.get(columns['measure'])
            try:
                valid=not isinstance(value,bool) and math.isfinite(float(value))
            except (ValueError,TypeError):valid=False
            invalid+=not valid
        evidence['scope-scan']['invalid_or_missing_measure_count']=invalid
        add('usable_numeric_values','violated' if invalid else 'supported' if scoped else 'unresolved',
            f'{len(scoped)} scoped observations; {invalid} missing/nonfinite/non-numeric measures. No silent omission.', ['scope-scan'])
        if 'one_value_per_group' in procedure['requirements']:
            add('one_value_per_group','supported' if all(n==1 for n in counts.values()) else 'violated',
                'Direct comparison requires exactly one observation per group; duplicates are not silently aggregated.',['scope-scan'])
    else:
        for name in ('period','group_coverage','usable_numeric_values','one_value_per_group'):
            if name in procedure['requirements']:
                add(name,'unresolved','Cannot inspect requested scope without documented column bindings.',['metadata-inspection','table-scan'])
    states=[v['verdict'] for v in verdicts]
    outcome='violated' if 'violated' in states else 'supported' if all(s=='supported' for s in states) else 'unresolved'
    execution={'status':'not_executed','reason':'Suitability not established' if outcome!='supported' else 'Execution disabled'}
    if outcome=='supported' and execute:
        execution=execute_readonly(rows,names,columns,procedure)
    return {'procedure_id':procedure['procedure_id'],'description':procedure['description'],'bindings':columns,
            'outcome':outcome,'requirements':verdicts,'evidence':list(evidence.values()),'execution':execution,
            'sql_template':procedure['sql_template'],'applicability':procedure['applicability']}
