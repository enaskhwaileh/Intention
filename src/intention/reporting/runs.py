from __future__ import annotations
from pathlib import Path
from hashlib import sha256
import csv,json,platform,subprocess
import yaml

def create_run(root,run_id,config,dataset_manifest,knowledge,metrics,per_query,predictions,timings):
    target=Path(root)/run_id
    if target.exists(): raise FileExistsError(f"immutable run already exists: {target}")
    target.mkdir(parents=True); (target/"logs").mkdir()
    canonical=yaml.safe_dump(config,sort_keys=True); (target/"config.yaml").write_text(canonical); (target/"config_hash.txt").write_text(sha256(canonical.encode()).hexdigest()+"\n")
    try: commit=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    except Exception: commit="unknown"
    (target/"git_commit.txt").write_text(commit+"\n"); (target/"environment.json").write_text(json.dumps({"python":platform.python_version(),"platform":platform.platform()},indent=2)); (target/"dataset_manifest.json").write_text(json.dumps(dataset_manifest,indent=2,sort_keys=True)); (target/"knowledge_version.json").write_text(json.dumps({"version":knowledge.version,"hash":knowledge.digest},indent=2)); (target/"metrics.json").write_text(json.dumps(metrics,indent=2,sort_keys=True)); (target/"timings.json").write_text(json.dumps(timings,indent=2,sort_keys=True))
    fields=sorted({k for row in per_query for k in row});
    with (target/"per_query_metrics.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(per_query)
    try:
        import pyarrow as pa, pyarrow.parquet as pq
    except ImportError as exc: raise RuntimeError("pyarrow is required to record predictions.parquet") from exc
    pq.write_table(pa.Table.from_pylist(predictions),target/"predictions.parquet")
    return target
