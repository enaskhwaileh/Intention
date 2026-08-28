from intention.contracts import RankedTable
from intention.alignment import align

def rank(candidates, profiles, requirement_profile, kg, lambda_r=.4, lambda_a=.6, **kwargs):
    if lambda_r<0 or lambda_a<0 or abs(lambda_r+lambda_a-1)>1e-9: raise ValueError("ranking weights must be nonnegative and sum to one")
    out=[]
    for table,relevance in candidates:
        if not 0 <= relevance <= 1:
            raise ValueError("retrieval relevance must be normalized to [0,1]")
        if requirement_profile is None: alignment=None; usefulness=relevance
        else:
            alignment,_=align(requirement_profile,profiles[table.table_id],kg,**kwargs); usefulness=lambda_r*relevance+lambda_a*alignment
        if not 0 <= usefulness <= 1:
            raise AssertionError("usefulness score escaped [0,1]")
        out.append(RankedTable(table.table_id,relevance,alignment,usefulness))
    return sorted(out,key=lambda x:(-x.usefulness,x.table_id))
