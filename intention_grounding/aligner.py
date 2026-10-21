"""Conservative axis comparison; unsupported evidence is always unknown."""


def compare_card(card, profiles):
    if card is None:
        return {"status": "not_run", "reason": "NO_GROUNDED_CARD", "tables": []}
    tables = []
    for profile in profiles:
        evidence_ids = {item.get("id") for item in profile.get("evidence", [])
                        if isinstance(item, dict) and item.get("source")}
        results = []
        for requirement in card["requirements"]:
            reason = "PROFILE_DOES_NOT_MEASURE_PREDICATE"
            if not evidence_ids:
                reason = "PROFILE_MISSING_EVIDENCE"
            results.append({"requirement_id": requirement["id"], "predicate": requirement["predicate"],
                            "axis": requirement["axis"], "modality": requirement["modality"],
                            "state": "unresolved", "reason": reason, "profile_evidence_refs": []})
        tables.append({"table_id": profile.get("table_id", "unresolved"), "overall_state": "unresolved",
                       "requirements": results})
    return {"status": "completed", "policy": "all_of_three_valued_v1", "tables": tables,
            "notice": "Observable schema statistics do not establish semantic or relational suitability."}


def assess_table(table, profile, grounding, root, **kwargs):
    """Assess each grounded procedure separately; no evidence is shared as a verdict."""
    from .procedures import assess_procedure
    procedures=[assess_procedure(table,profile,p,root,**kwargs) for p in grounding['procedures']]
    states=[p['outcome'] for p in procedures]
    overall=('supported' if 'supported' in states else 'violated' if states and all(s=='violated' for s in states) else 'unresolved')
    return {'table_id':table['table_id'],'overall_state':overall,'procedures':procedures}
