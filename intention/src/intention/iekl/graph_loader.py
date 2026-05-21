from pathlib import Path

import yaml

from intention.iekl.graph_store import IEKLGraph
from intention.schemas.iekl import IEKLEdge, IEKLNode


def load_graph(path: str | Path) -> IEKLGraph:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    nodes = [IEKLNode(**node) for node in data.get("nodes", [])]
    edges = [IEKLEdge(**edge) for edge in data.get("edges", [])]
    return IEKLGraph(nodes=nodes, edges=edges)
