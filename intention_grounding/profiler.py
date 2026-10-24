"""Table Profiler: Phi(T), reusable table capability profiles from observable evidence.

Works on any CSV with optional documentation (title, description, column
descriptions). Every profile is computed by a full scan and cached by content
hash and profiler version. Profiles describe evidence only; they do not decide
whether a table is useful for an intention (that is the Aligner's job).
"""
import hashlib
import os
import json
import math
import re
import time
from collections import OrderedDict
from pathlib import Path

PROFILER_VERSION = "3.0.0"
MISSING = {"", "na", "n/a", "nan", "null", "none", "-", ".", "?", "#n/a", "missing"}
_GAZETTEER = None

# Declared measure-kind rules: (kind, regex over name + description). Order matters.
KIND_RULES = [
    ("cumulative", r"\b(cumulative|cumulated|to date|up to the date|running total|since 20\d\d)\b|^cum_|^cumulative"),
    ("mean", r"\b(mean|average|avg|smoothed|rolling)\b"),
    ("rate", r"\b(per (hundred|thousand|million|100|1,?000|10,?000|100,?000|capita|cent)|percent(age)?|proportion|share of|fraction|ratio|p-scores?|pct|prevalence|incidence)\b|_per_|%|(?<!wage )(?<!hourly )(?<!interest )(?<!exchange )(?<!heart )(?<!tax )\brates?\b"),
    ("count", r"\b(number of|count|counts|frequency|freq|tally|new cases|new deaths|patients|admissions|rented|rentals)\b|^(n|cnt|count|freq|num_.*|n_.*|new_.*|daily_.*|weekly_.*|biweekly_.*)$"),
    ("amount", r"\b(amount|expenditure|spending|income|revenue|sales|cost|price|wage|salary|earnings|dollars|usd|euros?|pounds|gdp)\b|\$"),
]
_TOTAL_RULE = r"^total_|\btotal (number|count)\b"


def gazetteer():
    global _GAZETTEER
    if _GAZETTEER is None:
        path = Path(__file__).parent / "resources" / "gazetteer.json"
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"country_continent": {}, "continents": [], "aggregates": [], "us_states": []}
        _GAZETTEER = {
            "country": {k.casefold() for k in data["country_continent"]},
            "continent": {k.casefold() for k in data["continents"]},
            "aggregate": {k.casefold() for k in data["aggregates"]},
            "us_state": {k.casefold() for k in data["us_states"]},
            "country_continent": {k.casefold(): v for k, v in data["country_continent"].items()},
        }
    return _GAZETTEER


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ------------------------------------------------------------------ data loading
class FrameCache:
    """Small LRU of loaded tables (string-typed DataFrames) for scoped scans."""
    def __init__(self, capacity=24):
        self.capacity, self.items = capacity, OrderedDict()

    def get(self, path):
        import pandas as pd
        path = str(path)
        if path in self.items:
            self.items.move_to_end(path)
            return self.items[path]
        try:
            df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="latin-1")
        df.columns = [str(c) for c in df.columns]
        df.attrs["_derived"] = {}
        self.items[path] = df
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)
        return df


FRAMES = FrameCache()


def derived(df, key, fn):
    """Memoise per-table derived series (numeric parses, missing masks, dates)."""
    store = df.attrs.setdefault("_derived", {})
    if key not in store:
        store[key] = fn()
    return store[key]


def col_missing(df, name):
    return derived(df, ("missing", name), lambda: missing_mask(df[name].astype(str)))


_BOOL = {"yes": 1.0, "true": 1.0, "t": 1.0, "y": 1.0, "no": 0.0, "false": 0.0, "f": 0.0, "n": 0.0}


def _numeric_or_boolean(df, name):
    values = numeric_values(df[name].astype(str)).where(~col_missing(df, name))
    if values.notna().any():
        return values
    folded = col_folded(df, name)
    present = folded[~col_missing(df, name)]
    if len(present) and present.isin(list(_BOOL)).all():
        return folded.map(_BOOL)
    return values


def col_numeric(df, name):
    return derived(df, ("numeric", name), lambda: _numeric_or_boolean(df, name))


def col_dates(df, name):
    return derived(df, ("dates", name), lambda: parse_dates(df[name].astype(str)).dt.strftime("%Y-%m-%d"))


def col_folded(df, name):
    return derived(df, ("folded", name), lambda: df[name].astype(str).str.strip().str.casefold())


def missing_mask(series):
    return series.str.strip().str.casefold().isin(MISSING)


def numeric_values(series):
    import pandas as pd
    return pd.to_numeric(series.str.strip().str.replace(",", "", regex=False), errors="coerce")


def _looks_like_date(sample):
    return sum(bool(re.match(r"^\d{4}-\d{1,2}(-\d{1,2})?([ T]\d{1,2}:\d{2}.*)?$|^\d{1,2}/\d{1,2}/\d{2,4}$", s)) for s in sample) >= 0.9 * max(1, len(sample))


def parse_dates(series):
    import pandas as pd
    try:
        return pd.to_datetime(series.str.strip(), errors="coerce", format="mixed", dayfirst=False)
    except (ValueError, TypeError):
        return pd.to_datetime(series.str.strip(), errors="coerce")


def tokens(text):
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(text))
    return [t for t in re.split(r"[^a-z0-9]+", text.casefold()) if t]


def measure_kind(name, description, *, panel_time=False):
    text = f"{' '.join(tokens(name))} {description or ''}".casefold()
    raw = name.casefold()
    desc = (description or "").strip().casefold()
    if panel_time and (re.search(r"^(total|cum)", raw) or re.match(r"total\b", desc)) and not re.search(KIND_RULES[2][1], text + " " + raw):
        return {"kind": "cumulative", "rule": "total_in_time_series", "documented": bool(description)}
    for kind, pattern in KIND_RULES:
        if re.search(pattern, text) or re.search(pattern, raw):
            return {"kind": kind, "rule": pattern[:40], "documented": bool(description)}
    if re.search(_TOTAL_RULE, raw) or re.search(_TOTAL_RULE, text):
        return {"kind": "cumulative" if panel_time else "amount", "rule": "total", "documented": bool(description)}
    return {"kind": "level", "rule": "default_numeric", "documented": bool(description)}


def _grain(days):
    if days is None or not math.isfinite(days):
        return None
    for limit, name in ((0.5, "hour"), (1.5, "day"), (8, "week"), (32, "month"), (93, "quarter"), (367, "year")):
        if days <= limit:
            return name
    return "multi-year"


GRAIN_ORDER = ["hour", "day", "week", "month", "quarter", "year", "multi-year"]


def profile_frame(df, record, *, max_top=60):
    import pandas as pd
    rows = len(df)
    docs = {c["name"]: c.get("description", "") for c in record.get("columns", [])}
    gaz = gazetteer()
    columns = []
    for name in df.columns:
        s = df[name]
        miss = missing_mask(s)
        present = s[~miss].str.strip()
        n_valid = int(len(present))
        distinct = present.value_counts()
        col = {"name": name, "description": docs.get(name, ""), "n_valid": n_valid,
               "missing_fraction": round(1 - n_valid / rows, 6) if rows else None, "n_distinct": int(len(distinct))}
        nums = numeric_values(present) if n_valid else pd.Series(dtype=float)
        numeric_share = float(nums.notna().mean()) if n_valid else 0.0
        lowered = set(distinct.index.str.casefold()[:50]) if len(distinct) else set()
        if n_valid and len(distinct) <= 2 and lowered <= {"true", "false", "yes", "no", "t", "f", "y", "n", "0", "1"}:
            ctype = "binary"
        elif n_valid and numeric_share >= 0.98:
            ctype = "numeric"
        elif n_valid and _looks_like_date(list(present.head(50))):
            dates = parse_dates(present)
            ctype = "datetime" if dates.notna().mean() >= 0.98 else "categorical"
        elif n_valid and (len(distinct) <= 60 or len(distinct) <= 0.5 * n_valid) and present.str.len().mean() <= 60:
            ctype = "categorical"
        else:
            ctype = "text"
        col["type"] = ctype
        if ctype in ("numeric", "binary") and nums.notna().any():
            v = nums.dropna()
            col["numeric"] = {"min": float(v.min()), "max": float(v.max()), "mean": float(v.mean()),
                              "std": float(v.std()) if len(v) > 1 else 0.0,
                              "integer": bool((v % 1 == 0).all()), "nonnegative": bool((v >= 0).all())}
            if col["numeric"]["integer"] and 1700 <= col["numeric"]["min"] and col["numeric"]["max"] <= 2100 and \
                    re.search(r"\b(year|yr|yyyy)\b", " ".join(tokens(name)) + " " + col["description"].casefold()):
                col["temporal"] = {"kind": "year", "min": str(int(col["numeric"]["min"])), "max": str(int(col["numeric"]["max"])), "grain": "year"}
        if ctype == "datetime":
            dates = parse_dates(present).dropna()
            unique = dates.drop_duplicates().sort_values()
            diffs = unique.diff().dropna().dt.total_seconds() / 86400 if len(unique) > 1 else pd.Series(dtype=float)
            col["temporal"] = {"kind": "datetime", "min": str(unique.min().date()) if len(unique) else None,
                               "max": str(unique.max().date()) if len(unique) else None,
                               "grain": _grain(float(diffs.median())) if len(diffs) else None, "distinct_times": int(len(unique))}
        if ctype in ("categorical", "binary", "text") or (ctype == "numeric" and len(distinct) <= max_top):
            col["top_values"] = [[str(k), int(v)] for k, v in distinct.head(max_top).items()]
            col["values_complete"] = len(distinct) <= max_top
        if ctype in ("categorical", "text") and len(distinct):
            values = {v.casefold() for v in distinct.index}
            counts = {level: len(values & gaz[level]) for level in ("country", "continent", "aggregate", "us_state")}
            matched = sum(counts.values())
            if matched >= max(2, 0.5 * len(values)):
                level = max(("country", "continent", "us_state"), key=lambda k: counts[k] if k != "continent" else counts[k] + counts["aggregate"])
                col["geo"] = {"level": level, "counts": counts, "distinct": len(values)}
        col["identifier"] = bool(n_valid == rows and len(distinct) == rows and rows > 1 and
                                 (ctype in ("text", "categorical") or re.search(r"(^|_)(id|rownames|instant|index|key|code)$", name.casefold())))
        columns.append(col)
    temporal = [c for c in columns if c.get("temporal")]
    entity = [c for c in columns if c["type"] == "categorical" and not c["identifier"] and c.get("n_distinct", 0) > 1]
    panel = None
    entity = sorted(entity, key=lambda c: (not c.get("geo"), c["name"]))
    for t in temporal:
        for e in entity:
            if t["n_distinct"] < rows and e["n_distinct"] < rows and df.duplicated([e["name"], t["name"]]).sum() == 0:
                panel = {"entity": e["name"], "time": t["name"]}
                break
        if panel:
            break
    for c in columns:
        if c["type"] in ("numeric", "binary"):
            c["measure_kind"] = measure_kind(c["name"], c["description"], panel_time=bool(panel or temporal))
    cat_like = [c for c in columns if c["type"] in ("categorical", "binary") and not c["identifier"]]
    count_cols = [c for c in columns if c["type"] == "numeric" and re.fullmatch(r"(freq|frequency|count|n|number|counts)", c["name"].casefold())]
    aggregated = bool(count_cols) and rows <= 5000 and len(cat_like) >= 1 and \
        all(c["type"] in ("categorical", "binary") or c["identifier"] or c in count_cols for c in columns)
    geo_named = sum(1 for c in columns if c["name"].casefold() in gaz["country"] | gaz["continent"] | gaz["aggregate"] | gaz["us_state"])
    date_named = sum(1 for c in columns if re.match(r"^\d{4}[-_]\d{2}", c["name"]))
    return {"rows": rows, "n_columns": len(columns), "columns": columns,
            "structure": {"panel": panel, "aggregated_cells": aggregated,
                          "count_column": count_cols[0]["name"] if aggregated else None,
                          "wide_format": geo_named >= 10 or date_named >= 10,
                          "identifiers": [c["name"] for c in columns if c["identifier"]],
                          "temporal_columns": [c["name"] for c in temporal],
                          "geo_columns": [c["name"] for c in columns if c.get("geo")]}}


def profile(record, *, cache_dir=None, frames=FRAMES):
    """Phi(T) for one corpus record ({table_id, title, description, abs_path, columns})."""
    start = time.perf_counter()
    path = Path(record["abs_path"])
    digest = record.get("sha256") or sha256(path)
    doc_hash = hashlib.sha256(json.dumps([record.get("title"), record.get("description"), record.get("columns")],
                                         sort_keys=True).encode()).hexdigest()[:12]
    cache = Path(cache_dir) / f"{digest[:24]}-{doc_hash}-{PROFILER_VERSION}.json" if cache_dir else None
    if cache and cache.exists():
        result = json.loads(cache.read_text(encoding="utf-8"))
        result["cache_hit"] = True
        result["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 3)
        return result
    df = frames.get(path)
    body = profile_frame(df, record)
    result = {"table_id": record["table_id"], "title": record.get("title", ""), "description": record.get("description", ""),
              "sha256": digest, "profiler_version": PROFILER_VERSION, **body,
              "scan": {"scope": "full_table", "complete": True}, "cache_hit": False}
    result["compute_ms"] = round((time.perf_counter() - start) * 1000, 3)
    if cache:
        cache.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache.with_name(f"{cache.name}.{os.getpid()}.tmp")  # atomic: parallel workers may profile the same table
        tmp.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, cache)
    result["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 3)
    return result


def column(profile_, name):
    for c in profile_["columns"]:
        if c["name"] == name:
            return c
    return None
