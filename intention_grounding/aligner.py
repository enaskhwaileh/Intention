"""Aligner: A(T, iota_u) = Assess(Phi(T), Psi_u).

For each candidate table the Aligner (1) binds the symbolic slots of the grounded
requirements (measure, group, target, partner, time) to the table's attributes,
(2) evaluates every instantiated requirement with a registered predicate under its
evidence rule, producing supported / violated / unresolved with evidence, and
(3) combines verdicts per procedure and across alternative procedures.

Binding uses only table evidence: attribute names, documented descriptions and
observed values (no LLM). Absence of a concept never yields violation; violation
needs evidence of a negation (e.g. a full scan, a documented measure kind or a
geographic level that cannot provide the requested distinction).
"""
import math
import re
import time

from . import profiler as P

SUPPORTED, VIOLATED, UNRESOLVED = "supported", "violated", "unresolved"
ALIGNER_VERSION = "aligner-v1.0"

# General-purpose lexical normalisation for binding (documented, domain-independent).
SYNONYMS = {
    "salary": "wage", "salaries": "wage", "earning": "wage", "earnings": "wage", "pay": "wage", "wages": "wage",
    "nation": "country", "nations": "country", "countries": "country", "continents": "continent",
    "state": "state", "states": "state", "region": "region", "regions": "region",
    "sex": "gender", "genders": "gender", "male": "gender", "female": "gender",
    "yr": "year", "years": "year", "annual": "year", "yearly": "year", "mnth": "month", "monthly": "month",
    "hr": "hour", "hourly": "hour", "daily": "day", "days": "day", "weekly": "week", "dteday": "date",
    "temp": "temperature", "hum": "humidity", "cnt": "count", "num": "number", "no": "number",
    "mortality": "death", "deaths": "death", "died": "death", "dead": "death", "fatalities": "death",
    "survived": "survive", "survival": "survive", "survivor": "survive", "survivors": "survive",
    "rentals": "rent", "rental": "rent", "rented": "rent", "renting": "rent", "rides": "rent",
    "vaccination": "vaccin", "vaccinations": "vaccin", "vaccinated": "vaccin", "vaccine": "vaccin", "vaccines": "vaccin",
    "hospitalisation": "hospital", "hospitalization": "hospital", "hospitalizations": "hospital", "hospitalised": "hospital",
    "hospitalized": "hospital", "hospitals": "hospital", "admission": "admission", "admissions": "admission",
    "percentage": "percent", "pct": "percent", "share": "percent", "proportion": "percent", "%": "percent",
    "avg": "average", "mean": "average", "prices": "price", "costs": "cost", "houses": "house", "housing": "house",
    "passengers": "passenger", "people": "people", "persons": "people", "person": "people", "individuals": "people",
    "tests": "test", "testing": "test", "tested": "test", "cases": "case", "infections": "case", "infection": "case",
    "doses": "dose", "booster": "booster", "boosters": "booster", "educational": "education", "schooling": "education",
    "employees": "employee", "workers": "worker", "occupations": "occupation", "jobs": "occupation", "job": "occupation",
    "diabetic": "diabetes", "income": "wage", "incomes": "wage", "smoker": "smoke", "smoking": "smoke", "smokers": "smoke", "ages": "age", "aged": "age",
}
STOP = {"the", "of", "a", "an", "in", "on", "for", "and", "or", "to", "by", "per", "with", "at", "from", "as", "is", "are",
        "data", "dataset", "table", "value", "values", "number", "level", "levels", "group", "groups", "each", "different",
        "their", "its", "who", "which", "that", "this", "these", "covid", "19", "s", "how", "what", "all", "any",
        "against", "about", "among", "between", "into", "during", "over", "under", "within", "without", "across", "versus",
        "has", "have", "had", "whether", "does", "did", "do", "be", "been", "being", "was", "were", "per"}
GENERIC_HEADS_RAW = {"status", "level", "value", "amount", "concentration", "measurement", "measure", "figure", "quantity",
                 "indicator", "information", "record", "statistic", "data"}
KIND_WORDS = {"rate": "rate", "rates": "rate", "percent": "rate", "ratio": "rate", "share": "rate",
              "average": "mean", "mean": "mean", "total": "cumulative", "cumulative": "cumulative",
              "count": "count", "counts": "count", "number": "count"}
UNIT_WORDS = {"hundred", "thousand", "million", "capita", "cent", "percent", "day", "week", "month", "year", "hour"}
GEO_WORDS = {"country": "country", "continent": "continent", "state": "us_state", "region": "continent"}


def stem(tok):
    tok = SYNONYMS.get(tok, tok)
    for suffix, repl in (("ies", "y"), ("sses", "ss"), ("ations", "ate"), ("ation", "ate"), ("ing", ""), ("s", "")):
        if suffix == "s" and tok.endswith(("ss", "us", "is")):
            continue
        if tok.endswith(suffix) and len(tok) - len(suffix) >= 3:
            tok = tok[: len(tok) - len(suffix)] + repl
            break
    return SYNONYMS.get(tok, tok)


GENERIC_HEADS = GENERIC_HEADS_RAW | {stem(t) for t in GENERIC_HEADS_RAW}


def norm_tokens(text, *, keep_stop=False):
    return [stem(t) for t in P.tokens(text) if keep_stop or t not in STOP]


# ------------------------------------------------------------------ binding
class Binder:
    def __init__(self, prof, record, threshold=0.5):
        self.prof, self.record, self.threshold = prof, record, threshold
        self.head = None
        self.table_tokens = set(norm_tokens(f"{record.get('title', '')} {record.get('description', '')}"))
        self.col_tokens = {c["name"]: (set(norm_tokens(c["name"])), set(norm_tokens(c.get("description", ""))))
                           for c in prof["columns"]}
        self.value_tokens = {c["name"]: {t for v, _ in c.get("top_values", [])[:2] for t in norm_tokens(v)}
                             for c in prof["columns"] if c["type"] in ("binary", "categorical") and c["n_distinct"] == 2}

    @staticmethod
    def head_of(text):
        """Head concept of a noun phrase: the last content word before 'of', or after it when the
        pre-modifier is only a quantity word ('share of people vaccinated' -> vaccinated)."""
        def content(toks):
            return [t for t in toks if t not in KIND_WORDS and t not in UNIT_WORDS and t not in GENERIC_HEADS]
        pre, _, post = text.partition(" of ")
        for part in ((pre, post) if post else (pre,)):
            toks = content(norm_tokens(part))
            if toks:
                return toks[-1]
        return None

    def _score(self, concept_toks, col):
        """Score = 0.6 * head evidence + 0.4 * mean evidence of the other concept words.
        Evidence weights: attribute name 1.0, attribute description 0.8, documented measure kind 0.8,
        binary value labels 0.6, table documentation 0.5 (context only, never sufficient alone)."""
        name_t, desc_t = self.col_tokens[col["name"]]
        if not concept_toks:
            return 0.0, []
        value_t = self.value_tokens.get(col["name"], set())

        def weight(t):
            if t in name_t:
                return 1.0, "name", True
            if t in desc_t:
                return 0.8, "description", True
            if t in KIND_WORDS and col.get("measure_kind", {}).get("kind") == KIND_WORDS[t]:
                return 0.8, "measure_kind", False
            if t in value_t:
                return 0.6, "values", True
            if t in self.table_tokens:
                return 0.5, "table_documentation", False
            return 0.0, None, False

        matched, own = [], False
        weights = {}
        for t in concept_toks:
            w, source, is_own = weight(t)
            weights[t] = w
            own |= is_own
            if source:
                matched.append((t, source))
        if not own:
            return 0.0, matched
        head = self.head if self.head in weights else None
        if head is not None:
            h_w, _, h_own = weight(head)
            if not h_own:
                return 0.0, matched  # the head concept must be evidenced by the attribute itself
            rest = [weights[t] for t in concept_toks if t != head]
            return 0.6 * h_w + 0.4 * (sum(rest) / len(rest) if rest else 1.0), matched
        return sum(weights.values()) / len(concept_toks), matched

    def bind(self, concept, kind="measure", values=None, exclude=()):
        """Return a binding dict or None. kind in measure|target|dimension|any|time."""
        if concept is None and not values:
            return None
        text = concept if isinstance(concept, str) else " ".join(concept or [])
        toks = norm_tokens(text)
        self.head = self.head_of(text)
        geo_level = next((GEO_WORDS[t] for t in toks if t in GEO_WORDS), None)
        candidates = []
        for col in self.prof["columns"]:
            if col["name"] in exclude:
                continue
            if col["identifier"] and not (kind == "dimension" and (col.get("geo") or col["type"] in ("text", "categorical"))
                                          and col["name"].casefold() != "rownames"):
                continue
            ctype = col["type"]
            if kind == "measure" and ctype not in ("numeric", "binary"):
                continue
            if kind == "dimension" and not (ctype in ("categorical", "binary") or col.get("temporal") or
                                            (ctype == "numeric" and col["n_distinct"] <= 60) or col.get("geo")):
                continue
            if kind == "time" and not col.get("temporal"):
                continue
            if kind == "target" and ctype == "text" and not col.get("geo"):
                continue
            score, matched = self._score(toks, col)
            source = "lexical"
            if values:
                present = {v.casefold() for v, _ in col.get("top_values", [])}
                hit = sum(1 for v in values if v.casefold() in present)
                if hit == len(values):
                    score, source = max(score, 0.95), "values"
                elif hit:
                    score = max(score, 0.5 + 0.4 * hit / len(values))
                    source = "values"
            level_filter = None
            if geo_level and col.get("geo"):
                counts = col["geo"]["counts"]
                n_level = counts.get(geo_level, 0)
                if col["geo"]["level"] == geo_level and n_level >= 2:
                    score, source = max(score, 0.9), "geo_level"
                    if sum(counts.values()) > n_level:
                        level_filter = geo_level
                elif n_level >= 2:
                    score, source, level_filter = max(score, 0.85), "geo_level_subset", geo_level
            item = {"column": col["name"], "score": round(score, 4), "matched": matched, "source": source}
            if level_filter:
                item["level_filter"] = level_filter
            candidates.append(item)
        candidates.sort(key=lambda c: (-c["score"], c["column"]))
        best = candidates[0] if candidates and candidates[0]["score"] >= self.threshold else None
        result = {"concept": text, "kind": kind, "binding": best, "alternatives": candidates[1:4]}
        if best is None and kind in ("measure", "target"):
            long = self._long_format(toks)
            if long:
                result["binding"] = long
        if kind == "dimension" and geo_level:
            geo_cols = [c for c in self.prof["columns"] if c.get("geo")]
            has_level = any(c["geo"]["counts"].get(geo_level, 0) >= 2 for c in geo_cols)
            if geo_cols and not has_level and not (result["binding"] and not result["binding"]["source"].startswith("geo")):
                result["geo_mismatch"] = {"requested": geo_level, "available": sorted({c["geo"]["level"] for c in geo_cols})}
                result["binding"] = None
        return result

    def _long_format(self, toks):
        """Measure stored as (indicator, value) rows: match the concept to indicator values."""
        numeric = [c for c in self.prof["columns"] if c["type"] == "numeric" and not c["identifier"]]
        if len(numeric) != 1:
            return None
        best = None
        for col in self.prof["columns"]:
            if col["type"] != "categorical":
                continue
            for value, count in col.get("top_values", []):
                vt = set(norm_tokens(value))
                if not vt:
                    continue
                hit = sum(1 for t in toks if t in vt) / max(1, len(toks))
                exact_bonus = 0.1 if vt == set(toks) else 0.0
                score = hit + exact_bonus - 0.05 * len(vt - set(toks))
                if best is None or score > best[0]:
                    best = (score, col["name"], value)
        if best and best[0] >= 0.6:
            return {"column": numeric[0]["name"], "score": round(min(best[0], 1.0), 4), "source": "long_format",
                    "row_filter": {"column": best[1], "value": best[2]},
                    "measure_kind": P.measure_kind(best[2], best[2], panel_time=True)}
        return None


# ------------------------------------------------------------------ assessment context
class Context:
    def __init__(self, record, prof, theta, frames=P.FRAMES, binding_threshold=0.5):
        self.record, self.prof, self.theta, self.frames = record, prof, theta, frames
        self.binder = Binder(prof, record, binding_threshold)
        self.slots, self.evidence = {}, {}
        self._df, self._scope = None, None
        self.scans = 0

    # lazy full-table access for scoped evidence
    @property
    def df(self):
        if self._df is None:
            self._df = self.frames.get(self.record["abs_path"])
            self.scans += 1
        return self._df

    def col(self, name):
        return P.column(self.prof, name)

    def slot_column(self, slot):
        b = self.slots.get(slot)
        if isinstance(b, list):
            b = b[0] if b else None
        return b["binding"]["column"] if b and b.get("binding") else None

    def row_filter(self, slot):
        b = self.slots.get(slot)
        if b and b.get("binding") and b["binding"].get("row_filter"):
            rf = b["binding"]["row_filter"]
            return self.df[rf["column"]].str.strip() == rf["value"]
        return None

    def kind_of(self, slot):
        b = self.slots.get(slot)
        if b and b.get("binding"):
            if b["binding"].get("measure_kind"):
                return b["binding"]["measure_kind"]
            c = self.col(b["binding"]["column"])
            return c.get("measure_kind") if c else None
        return None

    def add_evidence(self, eid, fact):
        self.evidence[eid] = fact
        return eid

    # scope
    def scope_mask(self):
        if self._scope is None:
            self._scope = scope_evaluation(self)
        return self._scope


def _period_bounds(value):
    years = re.findall(r"(?:19|20)\d{2}", value)
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", value)
    if dates:
        return min(dates), max(dates)
    if years:
        return f"{min(years)}-01-01", f"{max(years)}-12-31"
    return None


def scope_evaluation(ctx):
    """Evaluate every scope restriction; returns dict(verdict, mask, details)."""
    import pandas as pd
    scope = ctx.theta.get("scope") or []
    details, mask = [], None
    gaz = P.gazetteer()
    doc_text = " ".join(P.tokens(f"{ctx.record.get('title', '')} {ctx.record.get('description', '')}"))
    for entry in scope:
        label, value = entry["label"], entry["value"].strip()
        v = value.casefold()
        v_core = re.sub(r"^the\s+", "", v)
        v_doc = " ".join(P.tokens(v_core))
        outcome = {"label": label, "value": value, "verdict": UNRESOLVED, "evidence": None}
        if label == "period":
            bounds = _period_bounds(value)
            temporal = [c for c in ctx.prof["columns"] if c.get("temporal")]
            if bounds and temporal:
                c = temporal[0]
                lo, hi = c["temporal"]["min"], c["temporal"]["max"]
                lo_s, hi_s = bounds
                if c["temporal"]["kind"] == "year":
                    lo, hi, lo_s, hi_s = lo[:4], hi[:4], lo_s[:4], hi_s[:4]
                overlap = not (hi_s < lo[: len(hi_s)] or lo_s > hi[: len(lo_s)])
                outcome.update(verdict=SUPPORTED if overlap else VIOLATED,
                               evidence={"column": c["name"], "observed": [lo, hi], "requested": [lo_s, hi_s], "rule": "temporal_overlap"})
                if overlap:
                    s = ctx.df[c["name"]].str.strip()
                    if c["temporal"]["kind"] == "year":
                        m = (s >= lo_s) & (s <= hi_s)
                    else:
                        d = P.col_dates(ctx.df, c["name"])
                        m = (d >= lo_s) & (d <= hi_s)
                    mask = m if mask is None else (mask & m)
            elif bounds and any(y in doc_text for y in re.findall(r"(?:19|20)\d{2}", value)):
                outcome.update(verdict=SUPPORTED, evidence={"rule": "documented_table_scope", "matched": value})
        elif label == "geography":
            hit = None
            for c in ctx.prof["columns"]:
                if c["type"] in ("categorical", "text", "binary") and any(val.casefold() == v_core for val, _ in c.get("top_values", [])):
                    hit = c["name"]
                    break
            if hit is None:
                for c in ctx.prof["columns"]:
                    if c["type"] in ("categorical", "text") and c.get("values_complete") is False:
                        if (P.col_folded(ctx.df, c["name"]) == v_core).any():
                            hit = c["name"]
                            break
            members = None
            if v_core in gaz["continent"] or v_core in ("europe",):
                members = {k for k, cont in gaz["country_continent"].items() if cont.casefold() == v_core}
            country_cols = [c for c in ctx.prof["columns"] if c.get("geo", {}).get("level") == "country"]
            member_rows = 0
            if members and country_cols:
                member_rows = int(P.col_folded(ctx.df, country_cols[0]["name"]).isin(members).sum())
            if hit and not member_rows:
                m = P.col_folded(ctx.df, hit) == v_core
                mask = m if mask is None else (mask & m)
                outcome.update(verdict=SUPPORTED, evidence={"rule": "value_present", "column": hit, "rows": int(m.sum())})
            elif members and country_cols:
                c = country_cols[0]["name"]
                m = P.col_folded(ctx.df, c).isin(members)
                n = int(m.sum())
                outcome.update(verdict=SUPPORTED if n else VIOLATED,
                               evidence={"rule": "declared_membership_mapping(gazetteer)", "column": c, "member_rows": n})
                if n:
                    mask = m if mask is None else (mask & m)
            elif v_doc and re.search(r"\b" + re.escape(v_doc) + r"\b", doc_text):
                outcome.update(verdict=SUPPORTED, evidence={"rule": "documented_table_scope", "matched": value})
            else:
                geo_cols = [c for c in ctx.prof["columns"] if c.get("geo")]
                known = v_core in gaz["country"] | gaz["continent"] | gaz["us_state"] | gaz["aggregate"]
                if geo_cols and known:
                    outcome.update(verdict=VIOLATED, evidence={"rule": "full_scan_no_member", "columns": [c["name"] for c in geo_cols]})
        else:  # population / condition
            for c in ctx.prof["columns"]:
                vals = {val.casefold() for val, _ in c.get("top_values", [])}
                if v_core in vals or stem(v_core) in {stem(x) for x in vals}:
                    m = ctx.df[c["name"]].str.strip().str.casefold().map(stem) == stem(v_core)
                    mask = m if mask is None else (mask & m)
                    outcome.update(verdict=SUPPORTED, evidence={"rule": "value_present", "column": c["name"], "rows": int(m.sum())})
                    break
            else:
                if v_doc and re.search(r"\b" + re.escape(v_doc) + r"\b", doc_text):
                    outcome.update(verdict=SUPPORTED, evidence={"rule": "documented_table_scope"})
        details.append(outcome)
    verdicts = [d["verdict"] for d in details]
    verdict = VIOLATED if VIOLATED in verdicts else SUPPORTED if all(v == SUPPORTED for v in verdicts) else UNRESOLVED
    if mask is None:
        mask = pd.Series(True, index=ctx.df.index) if scope else None
    return {"verdict": verdict, "details": details, "mask": mask}


# ------------------------------------------------------------------ predicates
PREDICATES = {}


def predicate(name):
    def register(fn):
        PREDICATES[name] = fn
        return fn
    return register


def _valid_numeric(ctx, slot, mask=None):
    c = ctx.slot_column(slot)
    if c is None:
        return None
    valid = P.col_numeric(ctx.df, c).notna()
    rf = ctx.row_filter(slot)
    if rf is not None:
        valid &= rf
    if mask is not None:
        valid &= mask
    return valid


def _scoped_mask(ctx):
    sc = ctx.scope_mask() if ctx.theta.get("scope") else None
    return sc["mask"] if sc else None


@predicate("concept_bound")
def p_concept_bound(ctx, params):
    slot, kind = params["slot"], params.get("kind", "measure")
    concept = params.get("concept")
    values = params.get("values")
    if slot == "target":
        kind = "target"
    if isinstance(concept, list):
        results = [ctx.binder.bind(c, "any" if kind == "any" else kind) for c in concept]
        ctx.slots[slot] = results
        bound = [r for r in results if r["binding"]]
        if not concept:
            return UNRESOLVED, {"reason": "no concept"}
        return (SUPPORTED if len(bound) == len(results) else UNRESOLVED), {"bindings": results}
    if concept is None and not values:
        return UNRESOLVED, {"reason": "concept not specified"}
    result = ctx.binder.bind(concept, kind, values=values if isinstance(values, list) else None)
    ctx.slots[slot] = result
    if result.get("geo_mismatch"):
        return VIOLATED, {"binding": result, "rule": "geographic_level_mismatch(full scan)"}
    if result["binding"]:
        return SUPPORTED, {"binding": result}
    return UNRESOLVED, {"binding": result, "rule": "no attribute denotes the concept"}


@predicate("scope_satisfiable")
def p_scope(ctx, params):
    if not params.get("scope"):
        return SUPPORTED, {"rule": "no scope restriction"}
    sc = ctx.scope_mask()
    return sc["verdict"], {"restrictions": sc["details"]}


@predicate("single_definition")
def p_single_definition(ctx, params):
    b = ctx.slots.get(params["slot"])
    if not b or not b.get("binding"):
        return UNRESOLVED, {"reason": "measure unbound"}
    col = ctx.col(b["binding"]["column"])
    if b["binding"].get("row_filter"):
        return SUPPORTED, {"rule": "single indicator selected", "filter": b["binding"]["row_filter"]}
    if ctx.prof["structure"]["wide_format"]:
        return UNRESOLVED, {"rule": "wide format: one column per entity"}
    return (SUPPORTED, {"rule": "one documented attribute"}) if col and col.get("description") else (UNRESOLVED, {"rule": "undocumented attribute"})


@predicate("observation_level")
def p_observation(ctx, params):
    kind = ctx.kind_of(params["slot"])
    if not kind:
        return UNRESOLVED, {"reason": "measure unbound"}
    units = _unit_count_column(ctx, exclude=(ctx.slot_column(params["slot"]),))
    if units and not ctx.prof["structure"]["panel"]:
        return VIOLATED, {"measure_kind": kind, "rule": f"rows aggregate several units (unit-count attribute {units}); per-row values are not unit observations"}
    if kind["kind"] == "mean" and not units:
        return SUPPORTED, {"measure_kind": kind, "rule": "per-unit average with no aggregation-size attribute: rows treated as observations"}
    if kind["kind"] in ("rate", "mean", "cumulative"):
        return VIOLATED, {"measure_kind": kind, "rule": "existing summary cannot be averaged as observations"}
    if ctx.prof["structure"]["aggregated_cells"]:
        return VIOLATED, {"rule": "rows are aggregated cells"}
    return (SUPPORTED if kind["documented"] else UNRESOLVED), {"measure_kind": kind}


def _unit_count_column(ctx, exclude=()):
    """An attribute counting the units behind each row (number of workers, cases, population, n)."""
    for c in ctx.prof["columns"]:
        if c["name"] in exclude:
            continue
        text = (c["name"] + " " + c.get("description", "")).casefold()
        if c["type"] == "numeric" and re.search(r"\b(number of (workers|people|persons|individuals|patients|passengers|cases|observations|respondents)|population|^n$|cases|sample size|freq)\b", text):
            return c["name"]
    return None


@predicate("summary_kind")
def p_summary_kind(ctx, params):
    kind = ctx.kind_of(params["slot"])
    if not kind:
        return UNRESOLVED, {"reason": "measure unbound"}
    if kind["kind"] in params["kinds"]:
        return SUPPORTED, {"measure_kind": kind}
    if kind["documented"]:
        return VIOLATED, {"measure_kind": kind, "rule": "documented kind differs from requested summary"}
    return UNRESOLVED, {"measure_kind": kind}


@predicate("additive_measure")
def p_additive(ctx, params):
    kind = ctx.kind_of(params["slot"])
    if not kind:
        return UNRESOLVED, {"reason": "measure unbound"}
    if kind["kind"] in ("count", "amount"):
        return SUPPORTED, {"measure_kind": kind}
    col = ctx.col(ctx.slot_column(params["slot"]))
    if col and col["type"] == "binary":
        return SUPPORTED, {"rule": "binary indicator: its sum counts positive rows"}
    if kind["kind"] in ("rate", "mean", "cumulative"):
        return VIOLATED, {"measure_kind": kind, "rule": "non-additive values"}
    return UNRESOLVED, {"measure_kind": kind}


def _group_ok(c):
    return c and (c["type"] in ("categorical", "binary") or c.get("temporal") or c.get("geo") or
                  (c["type"] == "numeric" and c["n_distinct"] <= 60))


@predicate("categorical_membership")
def p_membership(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "group unbound"}
    c = ctx.col(name)
    if _group_ok(c):
        return SUPPORTED, {"column": name, "type": c["type"], "n_distinct": c["n_distinct"]}
    return VIOLATED, {"column": name, "type": c["type"], "n_distinct": c["n_distinct"], "rule": "continuous or unique-valued attribute"}


@predicate("co_located")
def p_co_located(ctx, params):
    cols = [ctx.slot_column(s) for s in params["slots"]]
    if any(c is None for c in cols):
        return UNRESOLVED, {"reason": "slot unbound"}
    if ctx.prof["structure"]["wide_format"]:
        return UNRESOLVED, {"rule": "wide format"}
    return SUPPORTED, {"columns": cols, "rule": "same row of one table"}


def _group_series(ctx, slot):
    name = ctx.slot_column(slot)
    if name is None:
        return None, None
    series = ctx.df[name].str.strip()
    b = ctx.slots.get(slot)
    level = b["binding"].get("level_filter") if isinstance(b, dict) and b.get("binding") else None
    if level:  # mixed geographic column: keep only values of the requested level
        members = P.gazetteer()[level]
        series = series.where(P.col_folded(ctx.df, name).isin(members))
    return name, series


def _match_groups(series_values, requested):
    present = {v.casefold(): v for v in series_values if isinstance(v, str)}
    matched, missing = {}, []
    for g in requested:
        key = g.casefold().strip()
        if key in present:
            matched[g] = present[key]
        else:
            alt = next((v for k, v in present.items() if key == stem(k) or stem(key) == stem(k)), None)
            if alt is not None:
                matched[g] = alt
            else:
                missing.append(g)
    return matched, missing


@predicate("groups_covered")
def p_groups_covered(ctx, params):
    name, groups = _group_series(ctx, params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "group unbound"}
    valid = _valid_numeric(ctx, params.get("valid_slot", "measure"), _scoped_mask(ctx))
    if valid is None:
        return UNRESOLVED, {"reason": "measure unbound"}
    counts = groups[valid].value_counts()
    requested = params.get("groups") or []
    if isinstance(requested, str):
        requested = [requested]
    if requested:
        matched, missing = _match_groups(list(groups.dropna().unique()), requested)
        per = {g: int(counts.get(v, 0)) for g, v in matched.items()}
        if missing:
            c = ctx.col(name)
            same_kind = bool(c.get("geo"))  # requested values of the same geographic level
            return (VIOLATED if same_kind else UNRESOLVED), {"column": name, "missing_groups": missing, "counts": per}
        ok = all(n > 0 for n in per.values()) and len(per) >= params.get("min_groups", 2)
        return (SUPPORTED if ok else VIOLATED), {"column": name, "counts": per, "rule": "scoped valid counts (full scan)"}
    n_groups = int((counts > 0).sum())
    return (SUPPORTED if n_groups >= params.get("min_groups", 2) else VIOLATED), \
        {"column": name, "groups_with_valid_values": n_groups, "rule": "scoped valid counts (full scan)"}


@predicate("valid_per_group")
def p_valid_per_group(ctx, params):
    valid = _valid_numeric(ctx, params["slot"], _scoped_mask(ctx))
    if valid is None:
        return UNRESOLVED, {"reason": "measure unbound"}
    name, groups = _group_series(ctx, params["group_slot"])
    if name is None:
        if params.get("group_optional") and not ctx.theta.get("group_dimension"):
            n = int(valid.sum())
            return (SUPPORTED if n >= params.get("min_valid", 1) else VIOLATED), {"valid_rows": n}
        return UNRESOLVED, {"reason": "group unbound"}
    counts = groups[valid].value_counts()
    requested = params.get("groups") or []
    if requested:
        matched, missing = _match_groups(list(groups.unique()), requested)
        if missing:
            return UNRESOLVED, {"missing_groups": missing}
        per = {g: int(counts.get(v, 0)) for g, v in matched.items()}
        return (SUPPORTED if all(n >= params.get("min_valid", 1) for n in per.values()) else VIOLATED), {"counts": per}
    n_groups = int((counts >= params.get("min_valid", 1)).sum())
    return (SUPPORTED if n_groups >= 1 else VIOLATED), {"groups_with_valid_values": n_groups, "valid_rows": int(valid.sum())}


@predicate("completeness")
def p_completeness(ctx, params):
    valid = _valid_numeric(ctx, params["slot"])
    if valid is None:
        return None, {"reason": "unavailable"}
    rf = ctx.row_filter(params["slot"])
    base = rf.sum() if rf is not None else len(valid)
    mask = _scoped_mask(ctx)
    if mask is not None:
        base = int((mask & (rf if rf is not None else True)).sum())
        valid = valid & mask
    if not base:
        return None, {"reason": "empty denominator"}
    return round(float(valid.sum()) / float(base), 4), {"valid": int(valid.sum()), "selected": int(base)}


@predicate("size_indicator")
def p_size(ctx, params):
    valid = _valid_numeric(ctx, params["slot"], _scoped_mask(ctx))
    n = int(valid.sum()) if valid is not None else ctx.prof["rows"]
    ref = params.get("reference_rows", 1000)
    return round(min(1.0, math.log1p(n) / math.log1p(ref)), 4), {"rows": n}


@predicate("keys_bound")
def p_keys_bound(ctx, params):
    groups = params.get("groups") or []
    if isinstance(groups, str):
        groups = [groups]
    dim = params.get("dimension")
    if groups and all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", g) for g in groups):
        temporal = [c for c in ctx.prof["columns"] if c.get("temporal") and c["temporal"]["kind"] == "datetime"]
        if temporal:
            ctx.slots["key"] = {"binding": {"column": temporal[0]["name"], "source": "temporal", "dates": True}}
            return SUPPORTED, {"column": temporal[0]["name"], "rule": "datetime key"}
        return UNRESOLVED, {"rule": "no date attribute"}
    result = ctx.binder.bind(dim, "dimension", values=groups or None) if (dim or groups) else None
    if result is None:
        return UNRESOLVED, {"reason": "no key concept"}
    ctx.slots["key"] = result
    ctx.slots.setdefault("group", result)
    if result.get("geo_mismatch"):
        return VIOLATED, {"binding": result, "rule": "geographic_level_mismatch(full scan)"}
    return (SUPPORTED if result["binding"] else UNRESOLVED), {"binding": result}


def _key_series(ctx):
    b = ctx.slots.get("key")
    if not b or not b.get("binding"):
        return None, None
    name = b["binding"]["column"]
    s = P.col_dates(ctx.df, name) if b["binding"].get("dates") else ctx.df[name].str.strip()
    return name, s


@predicate("keys_present")
def p_keys_present(ctx, params):
    groups = params.get("groups") or []
    if isinstance(groups, str):
        groups = [groups]
    if not groups:
        if params.get("optional"):
            return SUPPORTED, {"rule": "no subject requested"}
        name, s = _key_series(ctx)
        if name is None:
            return UNRESOLVED, {"reason": "key unbound"}
        mask = _scoped_mask(ctx)
        n = int(s[mask].nunique()) if mask is not None else int(s.nunique())
        return (SUPPORTED if n >= 2 else VIOLATED), {"distinct_keys": n}
    if "key" not in ctx.slots:
        p_keys_bound(ctx, {"groups": groups, "dimension": ctx.theta.get("group_dimension")})
    name, s = _key_series(ctx)
    if name is None:
        return UNRESOLVED, {"reason": "key unbound"}
    mask = _scoped_mask(ctx)
    present = s[mask] if mask is not None else s
    matched, missing = _match_groups(list(present.dropna().unique()), groups)
    if missing:
        c = ctx.col(name)
        decisive = bool(c.get("geo")) or bool(c.get("temporal"))
        return (VIOLATED if decisive else UNRESOLVED), {"column": name, "missing": missing}
    return SUPPORTED, {"column": name, "matched": matched}


@predicate("valid_per_key")
def p_valid_per_key(ctx, params):
    groups = params.get("groups") or []
    name, s = _key_series(ctx)
    valid = _valid_numeric(ctx, params["slot"], _scoped_mask(ctx))
    if name is None or valid is None:
        return UNRESOLVED, {"reason": "key or measure unbound"}
    counts = s[valid].value_counts()
    if not groups:
        n = int((counts > 0).sum())
        return (SUPPORTED if n >= 2 else VIOLATED), {"keys_with_valid_values": n}
    matched, missing = _match_groups(list(s.dropna().unique()), groups)
    if missing:
        return UNRESOLVED, {"missing": missing}
    per = {g: int(counts.get(v, 0)) for g, v in matched.items()}
    return (SUPPORTED if all(per.values()) else VIOLATED), {"counts": per}


@predicate("unique_per_key")
def p_unique_per_key(ctx, params):
    name, s = _key_series(ctx)
    valid = _valid_numeric(ctx, params["slot"], _scoped_mask(ctx))
    if name is None or valid is None:
        return None, {"reason": "unavailable"}
    counts = s[valid].value_counts()
    groups = params.get("groups") or []
    if groups:
        matched, _ = _match_groups(list(s.dropna().unique()), groups)
        values = [counts.get(v, 0) for v in matched.values()]
    else:
        values = list(counts.values)
    if not values:
        return None, {"reason": "no keys"}
    return round(sum(1 for n in values if n == 1) / len(values), 4), {"keys": len(values)}


@predicate("optional_grouping")
def p_optional_grouping(ctx, params):
    concept, groups = params.get("concept"), params.get("groups")
    if not concept and not groups:
        return SUPPORTED, {"rule": "no grouping requested"}
    result = ctx.binder.bind(concept, "dimension", values=groups if isinstance(groups, list) else None)
    ctx.slots["group"] = result
    if result.get("geo_mismatch"):
        return VIOLATED, {"binding": result, "rule": "geographic_level_mismatch(full scan)"}
    if result["binding"]:
        return p_membership(ctx, {"slot": "group"})[0], {"binding": result}
    return UNRESOLVED, {"binding": result}


@predicate("target_type")
def p_target_type(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "target unbound"}
    c = ctx.col(name)
    if params["type"] == "categorical":
        ok = c["type"] in ("binary", "categorical") or (c["type"] == "numeric" and c["n_distinct"] <= 30 and c.get("numeric", {}).get("integer"))
        ok = ok and 2 <= c["n_distinct"] <= 30
        return (SUPPORTED if ok else VIOLATED), {"column": name, "type": c["type"], "n_distinct": c["n_distinct"]}
    ok = c["type"] == "numeric" and c["n_distinct"] > 2
    return (SUPPORTED if ok else VIOLATED), {"column": name, "type": c["type"], "n_distinct": c["n_distinct"]}


@predicate("row_level_target")
def p_row_level(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "target unbound"}
    if ctx.prof["structure"]["aggregated_cells"]:
        return VIOLATED, {"rule": "rows are aggregated cells (count column " + str(ctx.prof["structure"]["count_column"]) + ")"}
    return SUPPORTED, {"rows": ctx.prof["rows"], "rule": "one outcome per row (rows are not aggregated cells)"}


def _features(ctx, target):
    return [c for c in ctx.prof["columns"] if c["name"] != target and not c["identifier"] and c["type"] != "text"
            and c["n_valid"] > 0 and c["n_distinct"] > 1]


@predicate("features_available")
def p_features(ctx, params):
    target = ctx.slot_column(params["slot"])
    if target is None:
        return UNRESOLVED, {"reason": "target unbound"}
    feats = _features(ctx, target)
    predictors = params.get("predictors") or []
    if isinstance(predictors, str):
        predictors = [predictors]
    bound = []
    for p_ in predictors:
        r = ctx.binder.bind(p_, "any", exclude=(target,))
        if r["binding"]:
            bound.append(r["binding"]["column"])
    detail = {"candidate_features": len(feats), "requested_predictors": predictors, "bound_predictors": bound}
    if predictors and not bound:
        return UNRESOLVED, detail
    return (SUPPORTED if len(feats) >= params.get("min_features", 2) else VIOLATED), detail


@predicate("label_variation")
def p_label_variation(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "target unbound"}
    s = ctx.df[name].str.strip()
    s = s[~P.missing_mask(s)]
    counts = s.value_counts()
    ok = int((counts >= params.get("min_per_class", 5)).sum()) >= 2
    return (SUPPORTED if ok else VIOLATED), {"class_counts": {str(k): int(v) for k, v in counts.head(10).items()}}


@predicate("numeric_variation")
def p_numeric_variation(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "target unbound"}
    c = ctx.col(name)
    std = c.get("numeric", {}).get("std", 0)
    return (SUPPORTED if std and std > 0 else VIOLATED), {"std": std}


@predicate("min_valid_rows")
def p_min_valid_rows(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "target unbound"}
    valid = ~P.col_missing(ctx.df, name)
    mask = _scoped_mask(ctx)
    if mask is not None:
        valid &= mask
    n = int(valid.sum())
    return (SUPPORTED if n >= params["min_rows"] else VIOLATED), {"labelled_rows": n}


@predicate("feature_completeness")
def p_feature_completeness(ctx, params):
    target = ctx.slot_column(params["slot"])
    if target is None:
        return None, {"reason": "unavailable"}
    feats = _features(ctx, target)
    if not feats:
        return None, {"reason": "no features"}
    return round(sum(1 - c["missing_fraction"] for c in feats) / len(feats), 4), {"features": len(feats)}


@predicate("class_balance")
def p_class_balance(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return None, {"reason": "unavailable"}
    counts = ctx.df[name].str.strip().value_counts()
    counts = counts[[not P.missing_mask(__import__("pandas").Series([k])).iloc[0] for k in counts.index]]
    if len(counts) < 2:
        return 0.0, {"classes": len(counts)}
    p = counts / counts.sum()
    h = -float((p * p.apply(math.log)).sum()) / math.log(len(counts))
    return round(h, 4), {"classes": int(len(counts))}


@predicate("numeric_measure")
def p_numeric_measure(ctx, params):
    name = ctx.slot_column(params["slot"])
    if name is None:
        return UNRESOLVED, {"reason": "unbound"}
    c = ctx.col(name)
    return (SUPPORTED if c["type"] in ("numeric", "binary") else VIOLATED), {"column": name, "type": c["type"]}


def _partner_columns(ctx):
    b = ctx.slots.get("partner")
    if isinstance(b, list):
        return [x["binding"]["column"] for x in b if x.get("binding")]
    if b and b.get("binding"):
        return [b["binding"]["column"]]
    return []


@predicate("co_observed")
def p_co_observed(ctx, params):
    m = ctx.slot_column("measure")
    partners = _partner_columns(ctx)
    if m is None or not partners:
        return UNRESOLVED, {"reason": "slot unbound"}
    base = ~P.col_missing(ctx.df, m)
    mask = _scoped_mask(ctx)
    if mask is not None:
        base &= mask
    counts = {p_: int((base & ~P.col_missing(ctx.df, p_)).sum()) for p_ in partners}
    ok = all(n >= params.get("min_rows", 10) for n in counts.values())
    return (SUPPORTED if ok else VIOLATED), {"co_observed_rows": counts}


@predicate("both_vary")
def p_both_vary(ctx, params):
    cols = [ctx.slot_column("measure")] + _partner_columns(ctx)
    if None in cols or len(cols) < 2:
        return UNRESOLVED, {"reason": "slot unbound"}
    distinct = {c: ctx.col(c)["n_distinct"] for c in cols}
    return (SUPPORTED if all(n > 1 for n in distinct.values()) else VIOLATED), {"distinct": distinct}


@predicate("time_bound")
def p_time_bound(ctx, params):
    temporal = [c for c in ctx.prof["columns"] if c.get("temporal")]
    if not temporal:
        return VIOLATED, {"rule": "no parseable time attribute (all attributes profiled)"}
    concept = ctx.theta.get("time_dimension")
    choice = temporal[0]
    if concept:
        r = ctx.binder.bind(concept, "time")
        if r["binding"]:
            choice = ctx.col(r["binding"]["column"])
    ctx.slots["time"] = {"binding": {"column": choice["name"], "source": "temporal"}}
    return SUPPORTED, {"column": choice["name"], "temporal": choice["temporal"]}


@predicate("distinct_times")
def p_distinct_times(ctx, params):
    name = ctx.slot_column("time")
    valid = _valid_numeric(ctx, "measure", _scoped_mask(ctx))
    if name is None or valid is None:
        return UNRESOLVED, {"reason": "unbound"}
    n = int(ctx.df[name][valid].nunique())
    return (SUPPORTED if n >= params.get("min_points", 3) else VIOLATED), {"distinct_times": n}


@predicate("grain_compatible")
def p_grain(ctx, params):
    requested = params.get("grain")
    name = ctx.slot_column("time")
    if not requested or name is None:
        return None, {"reason": "unavailable"}
    want = {"hourly": "hour", "daily": "day", "weekly": "week", "monthly": "month", "quarterly": "quarter",
            "yearly": "year", "annual": "year", "annually": "year"}.get(str(requested).casefold(), str(requested).casefold())
    c = ctx.col(name)
    have = c["temporal"].get("grain")
    if want == "hour" and any(x["name"].casefold() in ("hr", "hour") for x in ctx.prof["columns"]):
        have = "hour"
    if have not in P.GRAIN_ORDER or want not in P.GRAIN_ORDER:
        return 0.5, {"observed": have, "requested": want}
    return (1.0 if P.GRAIN_ORDER.index(have) <= P.GRAIN_ORDER.index(want) else 0.0), {"observed": have, "requested": want}


# ------------------------------------------------------------------ combination
FIRST = {"concept_bound": 0, "keys_bound": 1, "time_bound": 1, "optional_grouping": 1}


def combine(states):
    if VIOLATED in states:
        return VIOLATED
    return SUPPORTED if states and all(s == SUPPORTED for s in states) else UNRESOLVED


def assess(record, prof, grounding, *, soft_weight=0.2, use_soft=True, binding_threshold=0.5, frames=P.FRAMES):
    """Assess one table against Psi_u. Returns verdicts, per-procedure states and A(T, iota)."""
    start = time.perf_counter()
    theta = grounding["g_u"]["theta"]
    procedures = []
    for proc in grounding["psi_u"]:
        ctx = Context(record, prof, theta, frames=frames, binding_threshold=binding_threshold)
        verdicts = []
        ordered = sorted(proc["hard"], key=lambda r: FIRST.get(r["predicate"], 2))
        for req in ordered:
            fn = PREDICATES[req["predicate"]]
            try:
                verdict, evidence = fn(ctx, req["params"])
            except Exception as exc:  # evidence evaluation failure: never a verdict of violation
                verdict, evidence = UNRESOLVED, {"error": type(exc).__name__}
            verdicts.append({"id": req["id"], "axis": req["axis"], "origin": req["origin"], "predicate": req["predicate"],
                             "verdict": verdict, "evidence": _compact(evidence)})
        soft = []
        for req in proc["soft"]:
            try:
                value, evidence = PREDICATES[req["predicate"]](ctx, req["params"])
            except Exception as exc:
                value, evidence = None, {"error": type(exc).__name__}
            soft.append({"id": req["id"], "axis": req["axis"], "value": value, "evidence": _compact(evidence)})
        states = [v["verdict"] for v in verdicts]
        state = combine(states)
        n_sup = states.count(SUPPORTED)
        a = 0.0 if state == VIOLATED else n_sup / len(states)
        soft_vals = [s["value"] for s in soft if s["value"] is not None]
        if use_soft and soft_vals and a > 0:
            a = a * (1 - soft_weight + soft_weight * sum(soft_vals) / len(soft_vals))
        bindings = {k: (v.get("binding") if isinstance(v, dict) else [x.get("binding") for x in v]) for k, v in ctx.slots.items()}
        procedures.append({"procedure_id": proc["procedure_id"], "state": state, "score": round(a, 6),
                           "counts": {s: states.count(s) for s in (SUPPORTED, VIOLATED, UNRESOLVED)},
                           "requirements": verdicts, "soft": soft, "bindings": bindings, "full_scans": ctx.scans})
    states = [p["state"] for p in procedures]
    overall = SUPPORTED if SUPPORTED in states else VIOLATED if states and all(s == VIOLATED for s in states) else UNRESOLVED
    best = max(procedures, key=lambda p: p["score"]) if procedures else None
    return {"table_id": record["table_id"], "state": overall, "A": best["score"] if best else 0.0,
            "best_procedure": best["procedure_id"] if best else None, "procedures": procedures,
            "aligner_version": ALIGNER_VERSION, "elapsed_ms": round((time.perf_counter() - start) * 1000, 3)}


def _compact(evidence):
    """Drop bulky objects (masks, frames) from evidence before reporting."""
    import pandas as pd
    if isinstance(evidence, dict):
        return {k: _compact(v) for k, v in evidence.items() if not isinstance(v, (pd.Series, pd.DataFrame))}
    if isinstance(evidence, list):
        return [_compact(v) for v in evidence]
    return evidence
