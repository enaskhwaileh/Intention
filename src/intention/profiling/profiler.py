"""Deterministic evidence extraction for small/complete in-memory tables."""
from __future__ import annotations
from collections import Counter
from intention.contracts import Capability, Provenance, Table

def _norm(value: object) -> str:
    return str(value).strip().lower().replace("_", " ")

def profile_table(table: Table) -> tuple[Capability, ...]:
    if not table.rows:
        return ()
    columns = tuple(table.rows[0])
    values = {c: [row.get(c) for row in table.rows] for c in columns}
    caps: list[Capability] = []
    for col in columns:
        nonmissing = [v for v in values[col] if v not in (None, "")]
        base = Provenance(f"column:{col}", "complete_table_scan", f"n={len(table.rows)}")
        caps.append(Capability("has_field", "sem", _norm(col), "observed", 1.0, base))
        numeric = nonmissing and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in nonmissing)
        if numeric:
            caps.append(Capability("numeric_measure", "sem", _norm(col), "observed", 1.0, base))
            caps.append(Capability("adequate_variation", "qual", len(set(nonmissing)) > 1, "observed", 1.0, base))
        if nonmissing and not numeric and 1 < len(set(map(str, nonmissing))) <= len(table.rows):
            caps.append(Capability("grouping_field", "str", _norm(col), "inferred", .8, Provenance(f"column:{col}", "cardinality_grouping_heuristic")))
        miss = 1 - len(nonmissing) / len(table.rows)
        caps.append(Capability("missingness_at_most", "qual", miss, "observed", 1.0, base))
    id_like = [c for c in columns if _norm(c) == "id" or _norm(c).endswith(" id")]
    features = [c for c in columns if c not in id_like]
    if features:
        caps.append(Capability("non_identifier_features", "aff", tuple(map(_norm, features)), "inferred", .9, Provenance("schema", "identifier_name_heuristic")))
    caps.append(Capability("identifier_only", "aff", bool(columns) and not features, "inferred", .9, Provenance("schema", "identifier_name_heuristic")))
    temporal = [c for c in columns if any(k in _norm(c) for k in ("date", "year", "time"))]
    if temporal:
        c = temporal[0]; vals = sorted(str(v) for v in values[c] if v not in (None, ""))
        if vals:
            caps.append(Capability("temporal_coverage", "cov", (vals[0], vals[-1]), "observed", 1.0, Provenance(f"column:{c}", "complete_min_max")))
            counts = Counter(str(v) for v in vals)
            caps.append(Capability("repeated_observations", "aff", len(vals) > len(counts), "inferred", .8, Provenance(f"column:{c}", "repetition_heuristic")))
    if "geographic_coverage" in table.metadata:
        caps.append(Capability("geographic_coverage", "cov", tuple(map(_norm, table.metadata["geographic_coverage"])), "observed", 1.0, Provenance("metadata:geographic_coverage", "declared_metadata")))
    if "row_granularity" in table.metadata:
        caps.append(Capability("row_granularity", "str", _norm(table.metadata["row_granularity"]), "observed", 1.0, Provenance("metadata:row_granularity", "declared_metadata")))
    return tuple(caps)
