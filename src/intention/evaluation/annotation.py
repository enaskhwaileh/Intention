def quadratic_weighted_kappa(left,right,minimum=0,maximum=3):
    if len(left)!=len(right) or not left: raise ValueError("paired ordinal labels required")
    if any(value not in range(minimum,maximum+1) for value in (*left,*right)): raise ValueError("ordinal label outside scale")
    n=len(left); size=maximum-minimum+1; observed=[[0]*size for _ in range(size)]
    for a,b in zip(left,right): observed[a-minimum][b-minimum]+=1
    left_counts=[sum(row) for row in observed]; right_counts=[sum(observed[i][j] for i in range(size)) for j in range(size)]
    weighted_observed=sum(((i-j)/(size-1))**2*observed[i][j]/n for i in range(size) for j in range(size))
    weighted_expected=sum(((i-j)/(size-1))**2*(left_counts[i]*right_counts[j]/n**2) for i in range(size) for j in range(size))
    return 1-weighted_observed/weighted_expected if weighted_expected else 1.0

def require_complete_judgments(records,expected_keys):
    by_key={tuple(record[key] for key in ("topic_id","variant_id","table_id","annotator_id")):record for record in records}
    if len(by_key)!=len(records) or set(by_key)!=set(expected_keys) or any(record.get("usefulness_label") is None for record in records):
        raise ValueError("missing, duplicate, or incomplete judgments")
    return True
