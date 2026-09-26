"""Deterministic, semantic-claim-free profiling of local CSV and JSON tables."""
import csv
import hashlib
import json
import math
from pathlib import Path

PROFILE_SCHEMA_VERSION = "1.0"


def _type(values):
    present = [v for v in values if v not in (None, "")]
    if not present:
        return "unknown"
    def all_parse(fn):
        try:
            for value in present:
                fn(value)
            return True
        except (TypeError, ValueError, OverflowError):
            return False
    if all_parse(lambda x: float(x)):
        return "number"
    if all_parse(lambda x: __import__("datetime").datetime.fromisoformat(str(x).replace("Z", "+00:00"))):
        return "datetime"
    if all(isinstance(x, bool) or str(x).lower() in {"true", "false"} for x in present):
        return "boolean"
    return "string"


def _read(path):
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle)), "csv"
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and isinstance(value.get("rows"), list):
            value = value["rows"]
        if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
            raise ValueError("JSON_TABLE_MUST_BE_ARRAY_OF_OBJECTS_OR_ROWS_OBJECT")
        return value, "json"
    raise ValueError("UNSUPPORTED_TABLE_FORMAT")


def profile_table(path, *, dataset_id="unknown", source_metadata=None):
    path = Path(path)
    rows, table_format = _read(path)
    names = list(dict.fromkeys(key for row in rows for key in row))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    columns = []
    evidence = []
    for index, name in enumerate(names):
        values = [row.get(name) for row in rows]
        missing = sum(value in (None, "") for value in values)
        inferred = _type(values)
        eid = f"column-{index}"
        claim = {"id": eid, "fact": "observed_column_profile", "column": name,
                 "method": "full_local_scan_v1", "scope": "entire_local_file", "complete": True,
                 "source": {"path": str(path), "sha256": digest}}
        evidence.append(claim)
        item = {"name": name, "observed_type": inferred, "null_count": missing,
                "missing_fraction": (missing / len(rows) if rows else None), "evidence_ref": eid}
        if inferred == "number":
            numeric = [float(v) for v in values if v not in (None, "") and math.isfinite(float(v))]
            item["numeric_statistics"] = {"finite_count": len(numeric),
                                           "minimum": min(numeric) if numeric else None,
                                           "maximum": max(numeric) if numeric else None}
        else:
            item["distinct_count"] = len({str(v) for v in values if v not in (None, "")})
        columns.append(item)
    row_evidence = {"id": "table-scan", "fact": "observed_table_identity_and_row_count",
                    "method": "full_local_scan_v1", "scope": "entire_local_file", "complete": True,
                    "source": {"path": str(path), "sha256": digest}}
    evidence.append(row_evidence)
    return {"schema_version": PROFILE_SCHEMA_VERSION, "dataset_id": dataset_id,
            "table_id": f"{dataset_id}:{digest[:16]}", "source_file": str(path),
            "format": table_format, "row_count": len(rows),
            "column_names": names, "columns": columns, "file_sha256": digest,
            "source_metadata": source_metadata or {"source_url": "unknown", "version": "unknown",
                                                   "license": "unknown", "acquisition_date": "unknown",
                                                   "archive_checksum": "unknown",
                                                   "selection_procedure": "explicit local path"},
            "evidence": evidence,
            "semantic_annotations": {"status": "unknown", "reason": "not inferred by local profiler"}}


def profile_paths(paths, **kwargs):
    return [profile_table(path, **kwargs) for path in sorted(map(Path, paths), key=lambda p: str(p))]
