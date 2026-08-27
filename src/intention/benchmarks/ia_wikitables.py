"""Leakage-safe benchmark utilities; human judgments remain external inputs."""
from __future__ import annotations
import random

def split_topics(topic_ids, seed=2026, fractions=(.6,.2,.2)):
    if abs(sum(fractions)-1)>1e-9: raise ValueError("split fractions must sum to one")
    ids=sorted(set(topic_ids)); random.Random(seed).shuffle(ids); a=int(len(ids)*fractions[0]); b=a+int(len(ids)*fractions[1])
    result={"train":tuple(ids[:a]),"dev":tuple(ids[a:b]),"test":tuple(ids[b:])}; check_topic_leakage(result); return result
def check_topic_leakage(splits):
    seen=set()
    for name,topics in splits.items():
        overlap=seen & set(topics)
        if overlap: raise ValueError(f"topic leakage in {name}: {sorted(overlap)}")
        seen.update(topics)
def pool_results(system_results, depth):
    if depth<=0 or "Ours" not in system_results: raise ValueError("pool requires positive depth and Ours")
    return tuple(sorted({table for ranking in system_results.values() for table in ranking[:depth]}))
def validate_annotations(rows, expected_annotators=2):
    keys=set(); groups={}
    for row in rows:
        required={"topic_id","variant_id","table_id","annotator_id","topical_label","usefulness_label"}
        if set(row)!=required or row["topical_label"] not in {0,1,2} or row["usefulness_label"] not in {0,1,2,3}:
            raise ValueError("invalid annotation record")
        key=tuple(row[x] for x in ("variant_id","table_id","annotator_id"))
        if key in keys: raise ValueError("duplicate annotation")
        keys.add(key); groups.setdefault(key[:2],set()).add(row["annotator_id"])
    if any(len(v)!=expected_annotators for v in groups.values()): raise ValueError("incomplete annotator coverage")
    return True
