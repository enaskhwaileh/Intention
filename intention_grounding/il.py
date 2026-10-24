"""Intention Library (IL): loading and registration checks.

The IL is the finite, versioned structure L = (J, O, P, R, E, v) of the paper:
families and variants (J), operator contracts (O), procedure templates (P),
requirement records (R), an expression index (E) and the release (v).
"""
import hashlib
import json
from pathlib import Path

IL_PATH = Path(__file__).parent / "library" / "intention-library-v1.0.json"
AXES = ("sem", "str", "cov", "qual", "aff")


class LibraryError(ValueError):
    pass


def load(path=IL_PATH, *, check=True):
    path = Path(path)
    library = json.loads(path.read_text(encoding="utf-8"))
    library["_path"] = str(path)
    library["_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    if check:
        problems = registration_problems(library)
        if problems:
            raise LibraryError("IL registration failed: " + "; ".join(problems))
    return library


def version(library):
    return library["release"]["il_version"]


def registration_problems(library, predicates=None):
    """Structural review: reference integrity, roles, kinds, axes and predicates."""
    problems = []
    families, variants = library["families"], library["variants"]
    procedures, requirements = library["procedures"], library["requirements"]
    operators = library["operators"]
    labels = set(library["vocabulary"]["argument_labels"])
    for fid, family in families.items():
        for vid in family["variants"]:
            if vid not in variants:
                problems.append(f"{fid}: unknown variant {vid}")
            elif variants[vid]["family"] != fid:
                problems.append(f"{vid}: family mismatch")
    for vid, variant in variants.items():
        if not variant.get("procedures"):
            problems.append(f"{vid}: no procedures")
        for role, contract in variant["roles"].items():
            unknown = set(contract["labels"]) - labels
            if unknown:
                problems.append(f"{vid}.{role}: unknown labels {sorted(unknown)}")
        for pid in variant["procedures"]:
            if pid not in procedures:
                problems.append(f"{vid}: unknown procedure {pid}")
            elif procedures[pid]["variant"] != vid:
                problems.append(f"{pid}: variant mismatch")
    for pid, procedure in procedures.items():
        if not procedure["hard"]:
            problems.append(f"{pid}: empty hard-requirement set")
        for op in procedure["operators"]:
            if op not in operators:
                problems.append(f"{pid}: unknown operator {op}")
        roles = set(variants[procedure["variant"]]["roles"]) | {"scope"}
        for kind in ("hard", "soft"):
            for rid in procedure[kind]:
                record = requirements.get(rid)
                if record is None:
                    problems.append(f"{pid}: unknown requirement {rid}")
                    continue
                declared = record.get("kind", "hard")
                if declared != kind:
                    problems.append(f"{pid}: {rid} declared {declared}, listed {kind}")
                for value in record["params"].values():
                    for item in value if isinstance(value, list) else [value]:
                        if isinstance(item, str) and item.startswith("$") and item[1:] not in roles:
                            problems.append(f"{pid}: {rid} references unknown role {item}")
    for rid, record in requirements.items():
        if record["axis"] not in AXES:
            problems.append(f"{rid}: unknown axis {record['axis']}")
        if record["evidence_rule"] not in library["evidence_rules"]:
            problems.append(f"{rid}: unknown evidence rule")
        if predicates is not None and record["predicate"] not in predicates:
            problems.append(f"{rid}: unregistered predicate {record['predicate']}")
    for entry in library["expression_index"]:
        if entry["family"] not in families:
            problems.append(f"index phrase {entry['phrase']}: unknown family")
    return problems


def definitions(library):
    """D_u: family meanings, variant outcomes, role contracts and applicability (no requirements)."""
    return {
        "il_version": version(library),
        "families": {fid: {"meaning": f["meaning"], "variants": f["variants"]} for fid, f in library["families"].items()},
        "variants": {vid: {"family": v["family"], "outcome": v["outcome"], "roles": v["roles"],
                           "procedures": {pid: {"applicability": library["procedures"][pid]["applicability"],
                                                "output": library["procedures"][pid]["output"]}
                                          for pid in v["procedures"]}}
                     for vid, v in library["variants"].items()},
        "argument_labels": library["vocabulary"]["argument_labels"],
        "scope_labels": library["vocabulary"]["scope_labels"],
    }


def describe(library, variant_id):
    """Human-readable view of one variant with its procedures and requirement records."""
    variant = library["variants"][variant_id]
    out = {"variant": variant_id, **variant, "procedures": {}}
    for pid in variant["procedures"]:
        p = library["procedures"][pid]
        out["procedures"][pid] = {**p, "requirements": {rid: library["requirements"][rid] for rid in p["hard"] + p["soft"]}}
    return out


def markdown(library):
    """Human-readable specification of the release (used for docs/INTENTION_LIBRARY.md)."""
    rel = library["release"]
    out = [f"# Intention Library {rel['il_version']}", "",
           f"Status: {rel['status']}; review: {rel['review_status']}. Generated from `intention_grounding/library/intention-library-v1.0.json` "
           "by `python -m intention_grounding.il`.", "", "## Assessment axes", ""]
    out += [f"- **{a}**: {d}" for a, d in library["axes"].items()]
    out += ["", "## Extraction vocabulary", "", "| Label | Meaning |", "|---|---|"]
    out += [f"| `{k}` | {v} |" for k, v in library["vocabulary"]["argument_labels"].items()]
    out += [f"| scope `{k}` | {v} |" for k, v in library["vocabulary"]["scope_labels"].items()]
    out += ["", "## Families, variants and procedures", ""]
    for fid, fam in library["families"].items():
        out += [f"### {fid}", "", fam["meaning"], ""]
        for vid in fam["variants"]:
            v = library["variants"][vid]
            out += [f"#### `{vid}`", "", v["outcome"], "", "| Role | Labels | Required | Cardinality | Admissible |", "|---|---|---|---|---|"]
            for role, c in v["roles"].items():
                out.append(f"| {role} | {', '.join(c['labels'])} | {'yes' if c['required'] else 'no'} | {c['min']}..{c['max'] or 'n'} | {', '.join(c.get('admissible', [])) or '–'} |")
            if v.get("requires_one_of"):
                out.append(f"\nAt least one of: {', '.join(' / '.join(g) for g in v['requires_one_of'])}.")
            for pid in v["procedures"]:
                p = library["procedures"][pid]
                out += ["", f"**Procedure `{pid}`**: `{p['expression']}` — {p['output']} Applicability: `{json.dumps(p['applicability'])}`.", "",
                        "| Requirement | Kind | Origin | Axis | Predicate | Evidence rule | Rationale |", "|---|---|---|---|---|---|---|"]
                for kind in ("hard", "soft"):
                    for rid in p[kind]:
                        r = library["requirements"][rid]
                        out.append(f"| `{rid}` | {kind} | {r['origin']} | {r['axis']} | `{r['predicate']}({', '.join(f'{k}={v}' for k, v in r['params'].items())})` | {r['evidence_rule']} | {r['rationale']} |")
            out.append("")
    out += ["## Operators", "", "| Operator | Inputs | Outputs | Preconditions | Missing values |", "|---|---|---|---|---|"]
    out += [f"| {o} | {d['inputs']} | {d['outputs']} | {' '.join(d['preconditions'])} | {d['missing_value_policy']} |" for o, d in library["operators"].items()]
    out += ["", "## Evidence rules", ""] + [f"- **{k}**: {v}" for k, v in library["evidence_rules"].items()]
    out += ["", "## Expression index", "", ", ".join(f"*{e['phrase']}* → {e['family']}" for e in library["expression_index"]), "",
            "## Release log", ""] + [f"- {c}" for c in rel["changes"]]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(markdown(load()))
