from dataclasses import dataclass

from intention.schemas.iekl import IEKLEdge, IEKLNode


@dataclass(frozen=True)
class IEKLGraph:
    nodes: list[IEKLNode]
    edges: list[IEKLEdge]

    def node_by_id(self, node_id: str) -> IEKLNode:
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise KeyError(f"unknown IEKL node: {node_id}")
