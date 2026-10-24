"""Import TARGET benchmark datasets (Ji et al., 2025) as corpora and benchmarks for this framework.

TARGET standardises table-retrieval evaluation over established datasets and publishes them on
the Hugging Face hub (namespace `target-benchmark`). This importer converts a dataset into
  data/corpus/target-<name>/manifest.json + tables/*.csv     (corpus, usable by every module)
  benchmarks/target/<name>.json                               (queries + gold tables)

  pip install datasets          # once, on a machine with internet access
  python -m intention_grounding.target_import --dataset bird-validation
  python -m intention_grounding.target_import --dataset spider-test --max-queries 500
  python -m intention_grounding.experiments --corpus data/corpus/target-bird-validation/manifest.json \\
      --benchmark benchmarks/target/bird-validation.json --systems target --context bm25,sbert

Relevance is TARGET's: the gold table(s) needed to answer the question get label 2; every other
table 0 (binary). For text-to-SQL datasets the analytical operation is derived from the gold SQL
(`sql_operation`: mean, total/count, extreme, lookup; `grouped`) so results can be stratified.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = {
    "bird-validation": ("target-benchmark/bird-corpus-validation", "target-benchmark/bird-queries-validation", "validation"),
    "spider-test": ("target-benchmark/spider-corpus-test", "target-benchmark/spider-queries-test", "test"),
    "spider-validation": ("target-benchmark/spider-corpus-validation", "target-benchmark/spider-queries-validation", "train"),
    "infiagentda": ("target-benchmark/infiagentda-corpus", "target-benchmark/infiagentda-queries", "test"),
    "fetaqa": ("target-benchmark/fetaqa-corpus", "target-benchmark/fetaqa-queries", "test"),
    "ottqa": ("target-benchmark/ottqa-corpus", "target-benchmark/ottqa-queries", "validation"),
}


def _read_file(f):
    """Rows of one data file, read without a shared schema (TARGET mixes cell types across files)."""
    name = f.name.lower()
    if name.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.read_table(f).to_pylist()
    if name.endswith(".jsonl") or name.endswith(".ndjson"):
        return [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]
    if name.endswith(".json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data and all(isinstance(v, (list, dict)) for v in data.values()):
            cols = {k: (list(v.values()) if isinstance(v, dict) else v) for k, v in data.items()}
            lengths = {len(v) for v in cols.values()}
            if len(lengths) == 1 and len(cols) <= 12 and not any(k in data for k in ("data", "rows", "examples")):
                n = lengths.pop()
                return [{k: cols[k][i] for k in cols} for i in range(n)]  # columnar (pandas / dict-of-lists) layout
        if isinstance(data, dict):
            for key in ("data", "rows", "examples", "tables", "queries"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        return data
    if name.endswith(".csv"):
        with open(f, newline="", encoding="utf-8", errors="replace") as fh:
            return list(csv.DictReader(fh))
    return []


def list_hub(author="target-benchmark"):
    from huggingface_hub import HfApi
    return sorted(d.id for d in HfApi().list_datasets(author=author, limit=500))


def _resolve_repo(path):
    """Exact repo id if it exists, else the closest target-benchmark dataset by name tokens."""
    from huggingface_hub import HfApi
    api = HfApi()
    try:
        api.dataset_info(path)
        return path
    except Exception:
        pass
    want = set(re.findall(r"[a-z0-9]+", path.split("/")[-1].lower()))
    best, score = None, 0
    for repo in list_hub(path.split("/")[0]):
        have = set(re.findall(r"[a-z0-9]+", repo.split("/")[-1].lower()))
        s = len(want & have) / max(len(want | have), 1)
        if s > score:
            best, score = repo, s
    if best is None or score < 0.5:
        raise SystemExit(f"dataset {path} not found; available: {list_hub(path.split('/')[0])}")
    print(f"using {best} for {path}")
    return best


def _load(path, split):
    """Hugging Face dataset id, or a local .jsonl file (offline use and tests).

    Hub datasets are downloaded as files and read file by file, so heterogeneous cell types
    (numbers and text in one column) do not break a shared Arrow schema."""
    local = Path(path)
    if local.exists():
        return _read_file(local) if local.is_file() else [r for f in sorted(local.rglob("*")) if f.is_file() for r in _read_file(f)]
    from huggingface_hub import snapshot_download
    repo = _resolve_repo(path)
    root = Path(snapshot_download(repo_id=repo, repo_type="dataset"))
    _ROOTS.append(root)
    files = [f for f in sorted(root.rglob("*")) if f.is_file() and f.suffix.lower() in {".parquet", ".jsonl", ".json", ".csv", ".ndjson"}
             and not f.name.lower().startswith(("dataset_info", "dataset_infos", "state", "readme"))]
    from collections import Counter
    print(f"{repo}: files by type {dict(Counter(f.suffix.lower() for f in files))}; e.g. {[str(f.relative_to(root)) for f in files[:6]]}")
    top = [f for f in files if len(f.relative_to(root).parts) == 1 or f.relative_to(root).parts[0] == "data"]
    files = top or files  # the dataset's own data files, not the raw databases shipped beside them
    with_split = [f for f in files if split and split.lower() in str(f.relative_to(root)).lower()]
    files = with_split or files
    for ext in (".parquet", ".jsonl", ".ndjson", ".json", ".csv"):  # one format only: the dataset's data files
        chosen = [f for f in files if f.suffix.lower() == ext]
        if chosen:
            files = chosen
            break
    rows = [r for f in files for r in _read_file(f)]
    print(f"{repo}: {len(rows)} rows from {len(files)} files; fields {sorted(rows[0]) if rows else []}")
    return rows


_ROOTS = []


def _bird_column_docs(db, tid):
    """BIRD ships per-table column documentation (database_description/<table>.csv); use it when present."""
    for root in _ROOTS:
        for f in root.glob(f"**/{db}/database_description/*.csv"):
            if f.stem.lower() != str(tid).lower():
                continue
            raw = f.read_bytes()
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = raw.decode("latin-1")
            docs = {}
            for row in csv.DictReader(text.splitlines()):
                row = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
                name = row.get("original_column_name")
                if name:
                    parts = [row.get("column_name"), row.get("column_description"), row.get("value_description")]
                    docs[name] = "; ".join(p for p in parts if p and p.lower() != name.lower())[:400]
            return docs
    return {}


def _get(row, *keys, default=None):
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return default


def _as_table(table):
    if isinstance(table, str):
        try:
            table = json.loads(table)
        except ValueError:
            rows = list(csv.reader(table.splitlines()))
            return rows[0], rows[1:]
    if isinstance(table, dict):
        if "header" in table and ("rows" in table or "data" in table):
            return [str(h) for h in table["header"]], table.get("rows") or table.get("data")
        header = list(table)
        return header, list(zip(*[table[c] for c in header]))
    return [str(h) for h in table[0]], table[1:]


def sql_operation(sql):
    """Analytical operation required by a gold SQL query (coarse, for stratified reporting)."""
    s = (sql or "").upper()
    grouped = " GROUP BY " in s
    if re.search(r"\bAVG\s*\(", s):
        op = "mean"
    elif re.search(r"\b(SUM|COUNT)\s*\(", s):
        op = "total_or_count"
    elif re.search(r"\b(MAX|MIN)\s*\(", s) or re.search(r"ORDER BY .* LIMIT\s+\d", s):
        op = "extreme"
    elif s:
        op = "lookup"
    else:
        op = None
    return {"sql_operation": op, "grouped": grouped}


def _slug(text):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(text)).strip("_")[:120] or "t"


def _describe(context):
    """Turn TARGET's per-table context into title/description/column documentation."""
    context = context or {}
    if isinstance(context, str):
        try:
            context = json.loads(context)
        except ValueError:
            context = {"context": context}
    if isinstance(context, list):
        merged, notes = {}, []
        for item in context:
            if isinstance(item, dict):
                merged.update(item)
            elif item not in (None, ""):
                notes.append(str(item))
        if notes:
            merged.setdefault("context", "; ".join(notes))
        context = merged
    if not isinstance(context, dict):
        context = {"context": str(context)}
    title_bits = [str(context[k]) for k in ("table_page_title", "page_title", "title", "table_section_title", "section_title") if context.get(k)]
    columns = {}
    for key in ("column_descriptions", "columns_description", "column_description"):
        value = context.get(key)
        if isinstance(value, dict):
            columns.update({str(k): str(v) for k, v in value.items()})
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and item.get("column_name"):
                    columns[str(item["column_name"])] = str(item.get("column_description") or item.get("value_description") or "")
    rest = {k: v for k, v in context.items() if k not in {"column_descriptions", "columns_description", "column_description"}}
    description = "; ".join(f"{k}: {v}" for k, v in rest.items() if v not in (None, "", [], {}))[:1500]
    return " — ".join(title_bits), description, columns


def import_dataset(name, *, corpus_path=None, queries_path=None, out_corpus=None, out_bench=None, max_rows=None, max_queries=None):
    hf_corpus, hf_queries, split = DATASETS.get(name, (corpus_path, queries_path, "test"))
    corpus_rows = _load(corpus_path or hf_corpus, split)
    query_rows = _load(queries_path or hf_queries, split)
    out_corpus = Path(out_corpus or ROOT / "data" / "corpus" / f"target-{name}")
    out_bench = Path(out_bench or ROOT / "benchmarks" / "target" / f"{name}.json")
    (out_corpus / "tables").mkdir(parents=True, exist_ok=True)
    tables, ids = [], {}
    for entry in corpus_rows:
        db = str(_get(entry, "database_id", "database_name", "db_id", "dataset_name", default="db"))
        tid = str(_get(entry, "table_id", "table_name", "table_title", "id"))
        raw_table = _get(entry, "table", "data", "table_content")
        if not raw_table or tid == "None":
            continue
        header, body = _as_table(raw_table)
        if max_rows:
            body = body[:max_rows]
        path = out_corpus / "tables" / _slug(db) / f"{_slug(tid)}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            w.writerows([["" if v is None else v for v in row] for row in body])
        title_ctx, description, col_docs = _describe(entry.get("context"))
        for col, doc in _bird_column_docs(db, tid).items():
            col_docs.setdefault(col, doc)
        table_id = f"{db}/{tid}"
        ids[(db, tid)] = table_id
        tables.append({"table_id": table_id, "title": f"{Path(tid).stem.replace('_', ' ')}" + (f" ({title_ctx})" if title_ctx else "") + f" [{db}]",
                       "description": description, "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                       "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size,
                       "source_family": f"target:{name}:{db}", "source": {"benchmark": "TARGET", "dataset": name, "database_id": db, "table_id": tid},
                       "license": "see TARGET / original dataset", "columns": [{"name": h, "description": col_docs.get(h, "")} for h in header]})
    manifest = {"corpus_id": f"target-{name}", "source": {"benchmark": "TARGET", "hf_corpus": hf_corpus, "split": split},
                "table_count": len(tables), "tables": tables}
    (out_corpus / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    queries = []
    for n, row in enumerate(query_rows):
        if max_queries and n >= max_queries:
            break
        db = str(_get(row, "database_id", "database_name", "db_id", "dataset_name", default="db"))
        gold = _get(row, "table_id", "table_ids", "table_name", "table_names", default=[])
        if isinstance(gold, str) and gold.startswith("["):
            try:
                gold = json.loads(gold)
            except ValueError:
                pass
        gold = gold if isinstance(gold, list) else [gold]
        labels = {ids[(db, str(t))]: 2 for t in gold if (db, str(t)) in ids}
        if not labels:
            continue
        answer = _get(row, "answer", "sql", "query_sql")
        q = {"query_id": f"{name}-{row.get('query_id', n)}", "topic": db, "pair_group": db, "text": str(_get(row, "query", "question", "utterance")),
             "gold_family": None, "gold_variant": None, "gold_grounding_status": None, "gold_interpretation": None,
             "gold_grounding": None, "labels": labels, "label_notes": {}, "answer": answer}
        if "sql" in name or name.startswith(("bird", "spider")):
            q.update(sql_operation(answer if isinstance(answer, str) else ""))
        queries.append(q)
    if not queries and query_rows:
        print("WARN: no query matched a corpus table; corpus keys e.g.", list(ids)[:3], "query row e.g.",
              {k: str(v)[:80] for k, v in query_rows[0].items()})
    out_bench.parent.mkdir(parents=True, exist_ok=True)
    bench = {"benchmark": f"target-{name}", "corpus_id": manifest["corpus_id"], "label_scale": {"2": "gold table", "0": "other"},
             "label_status": "established_benchmark_gold", "default_label": 0, "queries": queries}
    out_bench.write_text(json.dumps(bench, indent=1, ensure_ascii=False))
    return manifest, bench


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="list TARGET datasets on the Hugging Face hub")
    p.add_argument("--dataset", help="one of: " + ", ".join(DATASETS) + " (or a name with --corpus/--queries)")
    p.add_argument("--corpus", help="local corpus .jsonl or HF id (overrides the default)")
    p.add_argument("--queries", help="local queries .jsonl or HF id")
    p.add_argument("--max-rows", type=int, default=None, help="keep at most this many rows per table")
    p.add_argument("--max-queries", type=int, default=None)
    args = p.parse_args(argv)
    if args.list:
        print("\n".join(list_hub()))
        return
    if not args.dataset:
        p.error("--dataset is required")
    m, b = import_dataset(args.dataset, corpus_path=args.corpus, queries_path=args.queries, max_rows=args.max_rows, max_queries=args.max_queries)
    ops = {}
    for q in b["queries"]:
        ops[q.get("sql_operation")] = ops.get(q.get("sql_operation"), 0) + 1
    print(f"{m['corpus_id']}: {m['table_count']} tables; {len(b['queries'])} queries; operations {ops}")


if __name__ == "__main__":
    main()
