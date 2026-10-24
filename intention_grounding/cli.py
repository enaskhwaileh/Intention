"""Command line: run one request through the framework and explain every stage.

  python -m intention_grounding.cli "Compare the average hourly wage across genders"
  python -m intention_grounding.cli "..." --interpreter llm --resolver llm --allow-live --html out.html
  python -m intention_grounding.cli --describe compare.group_means
"""
import argparse
import html
import json
import sys
from pathlib import Path

from . import corpus, il
from .context import ContextMatcher
from .grounder import IndexResolver, LLMResolver
from .interpreter import LLMInterpreter, RuleInterpreter
from .pipeline import Pipeline


def build(args):
    manifest, library = corpus.load_manifest(), il.load()
    interp = LLMInterpreter(allow_live=args.allow_live) if args.interpreter == "llm" else RuleInterpreter()
    resolver = LLMResolver(allow_live=args.allow_live) if args.resolver == "llm" else IndexResolver(library)
    return Pipeline(manifest, library=library, interpreter=interp, resolver=resolver,
                    matcher=ContextMatcher(manifest, args.context, sbert_model=args.sbert_model, vector_store=args.vector_store), k_candidates=args.k, k_out=args.top,
                    combination=args.combination)


def explain_text(report, top):
    lines = []
    i, g = report["interpretation"], report["grounding"]
    lines.append(f"Interpreter [{i['status']}]  q_u = {report['context_query']!r}")
    if i.get("intention"):
        lines.append(f"  expression: {i['intention']['expression']!r}")
        for e in i["intention"]["arguments"] + i["intention"]["scope"]:
            lines.append(f"  {e['id']:>3} {e['label']:<16} {e['value']}")
    lines.append(f"Grounder [{g['status']}] " + (f"variant {g['g_u']['variant_id']} procedures {[p['procedure_id'] for p in g['psi_u']]}" if g["g_u"] else str(g["diagnostics"])))
    lines.append(f"Ranking ({report['mode']}):")
    for item in report["ranking"][:top]:
        a = report["assessments"].get(item["table_id"])
        extra = ""
        if a:
            best = next(p for p in a["procedures"] if p["procedure_id"] == a["best_procedure"])
            extra = f"  {a['state']:<10} A={a['A']:.2f} via {a['best_procedure']} " + "".join(v["verdict"][0].upper() for v in best["requirements"])
        lines.append(f"  {item['rank']:>2}. {item['table_id']:<48} U={item['U']:.3f} r={item['r']:.3f}{extra}")
    t = report["timing"]
    lines.append("Timing (ms): " + ", ".join(f"{k.replace('_ms', '')}={v}" for k, v in t.items()))
    return "\n".join(lines)


def explain_html(report, top, tables):
    esc = html.escape
    i, g = report["interpretation"], report["grounding"]
    rows = []
    for item in report["ranking"][:top]:
        a = report["assessments"].get(item["table_id"])
        detail = ""
        if a:
            for p in a["procedures"]:
                reqs = "".join(f"<tr class='{v['verdict']}'><td>{esc(v['id'])}</td><td>{v['axis']}</td><td>{v['verdict']}</td>"
                               f"<td><code>{esc(json.dumps(v['evidence'], ensure_ascii=False)[:400])}</code></td></tr>" for v in p["requirements"])
                soft = ", ".join(f"{s['id'].split('/')[1]}={s['value']}" for s in p["soft"])
                detail += f"<details><summary>{esc(p['procedure_id'])}: {p['state']} (score {p['score']:.2f})</summary><table>{reqs}</table><p>soft: {esc(soft)}</p></details>"
        title = tables[item["table_id"]].get("title", "")
        rows.append(f"<tr><td>{item['rank']}</td><td><b>{esc(item['table_id'])}</b><br><small>{esc(title)}</small>{detail}</td>"
                    f"<td>{item['U']:.3f}</td><td>{item['r']:.3f}</td><td>{'' if item['A'] is None else f'{item['A']:.2f}'}</td>"
                    f"<td class='{item['state'] or ''}'>{item['state'] or 'context only'}</td></tr>")
    args_ = "".join(f"<li><code>{esc(e['label'])}</code>: {esc(e['value'])}</li>" for e in (i.get("intention") or {}).get("arguments", []) + (i.get("intention") or {}).get("scope", []))
    psi = "".join(f"<li><b>{esc(p['procedure_id'])}</b> <code>{esc(p['expression'])}</code>: " + ", ".join(esc(r['requirement_id']) for r in p["hard"]) + "</li>" for p in g["psi_u"])
    timing = "".join(f"<tr><td>{esc(k)}</td><td>{v}</td></tr>" for k, v in report["timing"].items())
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Intention grounding run</title><style>
:root{{--bg:#fff;--fg:#1d1d1f;--muted:#666;--line:#e3e3e3;--sup:#e7f6ec;--vio:#fbe9e9;--unr:#f6f3e6}}
@media (prefers-color-scheme: dark){{:root{{--bg:#16171a;--fg:#ececec;--muted:#aaa;--line:#333;--sup:#1d3326;--vio:#3a1f1f;--unr:#35321f}}}}
body{{font:14px/1.5 system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:1100px;margin:auto;padding:16px}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid var(--line);padding:6px;vertical-align:top;text-align:left}}
.supported{{background:var(--sup)}}.violated{{background:var(--vio)}}.unresolved{{background:var(--unr)}}code{{font-size:12px;word-break:break-word}}
small{{color:var(--muted)}}</style></head><body>
<h1>{esc(report['input'])}</h1>
<h2>1. Interpreter: {esc(i['status'])}</h2><p>Context query q<sub>u</sub>: <b>{esc(report['context_query'])}</b>; expression: <b>{esc(str((i.get('intention') or {}).get('expression')))}</b></p><ul>{args_}</ul>
<h2>2. Grounder: {esc(g['status'])}</h2><p>{esc(g['g_u']['variant_id'] if g['g_u'] else json.dumps(g['diagnostics']))}</p><ul>{psi}</ul>
<h2>3–6. Context matching, profiling, alignment and ranking ({esc(report['mode'])})</h2>
<table><tr><th>#</th><th>Table and requirement verdicts</th><th>U</th><th>r</th><th>A</th><th>State</th></tr>{''.join(rows)}</table>
<h2>Timing (ms)</h2><table>{timing}</table></body></html>"""


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("request", nargs="?")
    p.add_argument("--interpreter", choices=["rule", "llm"], default="rule")
    p.add_argument("--resolver", choices=["index", "llm"], default="index")
    p.add_argument("--context", default="bm25", choices=["bm25", "tfidf", "lsa", "sbert", "hybrid"])
    p.add_argument("--sbert-model", default=None)
    p.add_argument("--vector-store", default="chroma", choices=["chroma", "faiss", "numpy"])
    p.add_argument("--k", type=int, default=50, help="candidates retrieved by context matching")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--combination", default="product", choices=["product", "linear", "lexicographic"])
    p.add_argument("--allow-live", action="store_true", help="permit new LLM calls")
    p.add_argument("--json", type=Path)
    p.add_argument("--html", type=Path)
    p.add_argument("--describe", help="print one Intention Library variant with its procedures and requirements")
    p.add_argument("--list", action="store_true", help="list Intention Library variants")
    args = p.parse_args(argv)
    if args.list or args.describe:
        library = il.load()
        out = il.describe(library, args.describe) if args.describe else {v: x["outcome"] for v, x in library["variants"].items()}
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    if not args.request:
        p.error("a request is required")
    pipe = build(args)
    report = pipe.run(args.request)
    print(explain_text(report, args.top))
    if args.json:
        args.json.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str))
    if args.html:
        args.html.write_text(explain_html(report, args.top, pipe.tables), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
