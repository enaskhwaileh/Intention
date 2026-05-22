from pathlib import Path

import yaml

from intention.iekl.graph_store import IEKLGraph, PredicateSpec


def load_iekl_graph(path: str | Path) -> IEKLGraph:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    predicate_specs = {
        predicate_id: PredicateSpec(
            id=predicate_id,
            axis=payload["axis"],
            definition=payload["definition"],
            testable_from=list(payload.get("testable_from", [])),
        )
        for predicate_id, payload in data.get("predicates", {}).items()
    }
    return IEKLGraph(
        intentions=dict(data.get("intentions", {})),
        predicates=predicate_specs,
    )


load_graph = load_iekl_graph
