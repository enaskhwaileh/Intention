"""Deterministic interpretation evaluation with action and argument diagnostics."""
import json,re
from pathlib import Path
from intention.evaluation.metrics import action_metrics
from intention.knowledge import load_knowledge
from .interpreter import DeterministicInterpreter,ground
from .normalization import load_normalization

def load_interpretation_gold(path=None):
    path=Path(path) if path else Path(__file__).resolve().parents[3]/"fixtures/synthetic_interpretation_gold.json"; raw=json.loads(path.read_text())
    if not isinstance(raw,dict) or set(raw)!={"version","normalization_version","cases"}: raise ValueError("invalid interpretation gold root")
    ids=set(); required={"case_id","input","topical_query","gold_action","gold_arguments","ambiguity","grounding","gold_span_texts"}
    for case in raw["cases"]:
        if set(case)!=required or case["case_id"] in ids or case["gold_action"] not in {"COMPARE","AGGREGATE","PREDICT","EXPLAIN","MONITOR","unknown"} or case["ambiguity"] not in {"unambiguous","ambiguous","insufficient"}: raise ValueError("invalid interpretation gold case")
        if not isinstance(case["gold_span_texts"],list) or any(not isinstance(label,str) and not (isinstance(label,dict) and set(label)=={"text","occurrence"} and isinstance(label["text"],str) and isinstance(label["occurrence"],int) and label["occurrence"]>0) for label in case["gold_span_texts"]): raise ValueError("invalid interpretation gold spans")
        ids.add(case["case_id"])
    return raw

def evaluate_interpreter(path=None):
    kg=load_knowledge(); catalogue=load_normalization(); gold=load_interpretation_gold(path)
    if gold["normalization_version"]!=catalogue.version: raise ValueError("interpretation gold normalization version mismatch")
    provider=DeterministicInterpreter(catalogue); outputs=[]; gold_actions=[]; predictions=[]; gold_pairs=set(); predicted_pairs=set(); joint=[]; span_scores=[]
    for case in gold["cases"]:
        artifact=provider.interpret(case["input"]); interp=ground(case["input"],artifact,kg,catalogue); predicted=interp.validated_output.get("action","unknown") if interp.validated_output else "unknown"; args=interp.grounding.arguments if interp.grounding else interp.validated_output.get("arguments",{}) if interp.validated_output else {}
        gold_actions.append(case["gold_action"]); predictions.append(predicted); gold_pairs.update((case["case_id"],k,str(v)) for k,v in case["gold_arguments"].items()); predicted_pairs.update((case["case_id"],k,str(v)) for k,v in args.items())
        frame_correct=predicted==case["gold_action"] and args==case["gold_arguments"]
        joint.append(frame_correct)
        predicted_spans=set(interp.provenance); gold_spans=set()
        for label in case["gold_span_texts"]:
            surface=label["text"] if isinstance(label,dict) else label
            occurrence=label.get("occurrence",1) if isinstance(label,dict) else 1
            starts=[match.start() for match in re.finditer(re.escape(surface),case["input"])]
            start=starts[occurrence-1] if 0 < occurrence <= len(starts) else -1
            if start < 0: raise ValueError(f"gold span text missing from input: {case['case_id']}")
            gold_spans.add((start,start+len(surface)))
        union=predicted_spans|gold_spans
        span_scores.append(len(predicted_spans&gold_spans)/len(union) if union else 1.0)
        passed=frame_correct and interp.topical_query==case["topical_query"] and interp.ambiguity==case["ambiguity"] and (interp.grounding is not None)==case["grounding"] and predicted_spans==gold_spans
        outputs.append({"case_id":case["case_id"],"predicted_action":predicted,"grounded":interp.grounding is not None,"status":interp.status,"passed":passed})
    tp=len(gold_pairs&predicted_pairs); precision=tp/len(predicted_pairs) if predicted_pairs else 0; recall=tp/len(gold_pairs) if gold_pairs else 0
    return {"version":gold["version"],"case_count":len(outputs),"passed":all(x["passed"] for x in outputs),"action":action_metrics(gold_actions,predictions),"arguments":{"precision":precision,"recall":recall,"f1":2*precision*recall/(precision+recall) if precision+recall else 0},"joint_frame_accuracy":sum(joint)/len(joint),"provenance_span_accuracy":sum(span_scores)/len(span_scores),"grounding_accuracy":sum(x["grounded"]==case["grounding"] for x,case in zip(outputs,gold["cases"]))/len(outputs),"cases":outputs}
