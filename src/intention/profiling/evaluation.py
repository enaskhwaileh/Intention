"""Profiler diagnostics against independently stored capability gold."""
from __future__ import annotations
from statistics import mean
from intention.contracts import Capability
from .annotations import GoldDataset

SET_PREDICATES={"has_field","numeric_measure","grouping_field","geographic_coverage","non_identifier_features"}

def _f1(gold,pred):
    gold,pred=set(gold),set(pred); tp=len(gold&pred); precision=tp/len(pred) if pred else float(not gold); recall=tp/len(gold) if gold else float(not pred); return precision,recall,2*precision*recall/(precision+recall) if precision+recall else 0.0
def _predicted_values(caps):
    out=[]
    for cap in caps:
        if isinstance(cap.value,(list,tuple,set)): out.extend(str(x) for x in cap.value)
        else: out.append(str(cap.value))
    return out

def evaluate_profiles(gold: GoldDataset,profiles: dict[str,tuple[Capability,...]]) -> dict:
    per={}; value_scores=[]; provenance=[]; row_kind=[]; row_agg=[]; row_exact=[]; field_scores=[]; excluded={"unknown":0,"not_applicable":0}
    for table in gold.tables:
        if table.table_id not in profiles: raise ValueError(f"missing profile: {table.table_id}")
        capabilities=profiles[table.table_id]
        by={};
        for cap in capabilities: by.setdefault(cap.predicate,[]).append(cap); provenance.append(bool(cap.provenance.source and cap.provenance.procedure))
        for item in table.capabilities:
            if item.judgment in excluded: excluded[item.judgment]+=1; continue
            positive=item.judgment=="supported"; predicted=bool(by.get(item.predicate)); stats=per.setdefault(item.predicate,{"tp":0,"fp":0,"fn":0,"tn":0})
            stats["tp" if positive and predicted else "fn" if positive else "fp" if predicted else "tn"]+=1
            if positive and predicted:
                caps=by[item.predicate]
                if item.predicate in SET_PREDICATES:
                    _,_,score=_f1([str(x) for x in item.value],_predicted_values(caps)); value_scores.append(score)
                elif item.predicate=="temporal_coverage": value_scores.append(float(tuple(map(str,item.value))==tuple(map(str,caps[0].value))))
                elif item.predicate=="missingness_at_most":
                    predicted_map={cap.provenance.source.split(":",1)[-1].replace("_"," "):cap.value for cap in caps}; value_scores.append(mean(float(abs(predicted_map.get(k,2)-v)<1e-12) for k,v in item.value.items()))
                else: value_scores.append(float(any(cap.value==item.value for cap in caps)))
        row=table.row_granularity; predicted_rows=by.get("row_granularity",[])
        if row.judgment=="supported" and predicted_rows:
            value=predicted_rows[0].value; gold_value=row.value; row_kind.append(value.get("kind")==gold_value["kind"]); row_agg.append(value.get("aggregation_status")==gold_value["aggregation_status"])
            structural_fields={"kind","entity_fields","entity_type","time_fields","time_unit","grouping_fields","aggregation_status"}; row_exact.append(all(value.get(field)==gold_value[field] for field in structural_fields))
            for field in ("entity_fields","time_fields","grouping_fields"): field_scores.append(_f1(gold_value[field],value.get(field,[]))[2])
    predicate_metrics={}
    for predicate,stats in per.items():
        precision=stats["tp"]/(stats["tp"]+stats["fp"]) if stats["tp"]+stats["fp"] else 0; recall=stats["tp"]/(stats["tp"]+stats["fn"]) if stats["tp"]+stats["fn"] else 0
        positive_support=stats["tp"]+stats["fn"]
        predicate_metrics[predicate]={**stats,"positive_support":positive_support,"precision":precision,"recall":recall,"f1":2*precision*recall/(precision+recall) if precision+recall else None}
    macro_values=[x["f1"] for x in predicate_metrics.values() if x["f1"] is not None]
    return {"table_count":len(gold.tables),"predicate_metrics":predicate_metrics,"predicate_macro_f1":mean(macro_values),"macro_predicate_count":len(macro_values),"value_macro_score":mean(value_scores) if value_scores else 0,"provenance_validity":mean(provenance) if provenance else 0,"excluded_judgments":excluded,"row_granularity":{"kind_accuracy":mean(row_kind) if row_kind else 0,"aggregation_accuracy":mean(row_agg) if row_agg else 0,"field_macro_f1":mean(field_scores) if field_scores else 0,"exact_accuracy":mean(row_exact) if row_exact else 0}}
