import json
from pathlib import Path

def generate_table(run_dirs,metrics,output):
    rows=[]
    for directory in run_dirs:
        path=Path(directory)/"metrics.json"
        if not path.exists(): raise FileNotFoundError(f"missing required run metrics: {path}")
        data=json.loads(path.read_text()); missing=[m for m in metrics if m not in data]
        if missing: raise ValueError(f"missing metrics in {directory}: {missing}")
        rows.append((Path(directory).name,[data[m] for m in metrics]))
    lines=["\\begin{tabular}{l"+"r"*len(metrics)+"}","System & "+" & ".join(metrics)+r" \\","\\hline"]
    lines += [name+" & "+" & ".join(f"{v:.3f}" for v in vals)+r" \\" for name,vals in rows]; lines.append("\\end{tabular}")
    Path(output).write_text("\n".join(lines)+"\n"); return Path(output)
