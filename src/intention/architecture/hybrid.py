def reciprocal_rank_fusion(rankings:dict[str,list[str]],k:int=60):
    if not rankings or not isinstance(k,int) or k<=0: raise ValueError("RRF requires rankings and positive k")
    scores={}
    for name,ranking in sorted(rankings.items()):
        if len(ranking)!=len(set(ranking)): raise ValueError(f"duplicate table in {name}")
        for rank,table_id in enumerate(ranking,1): scores[table_id]=scores.get(table_id,0)+1/(k+rank)
    return sorted(({"table_id":table_id,"raw_score":score} for table_id,score in scores.items()),key=lambda item:(-item["raw_score"],item["table_id"]))
