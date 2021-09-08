"""GraphInfo class for storing graph information"""
from dataclasses import dataclass

__all__ = ["GraphInfo"]


@dataclass
class GraphInfo:
    """Information about a graph.

    Attributes
    ----------
    num_nodes : int
        The number of nodes in the graph.

    num_edges : int
        The number of edges in the graph.

    edge_labels : set
        The set of edge labels in the graph.
    """

    num_nodes: int
    num_edges: int
    edge_labels: set

    def __repr__(self):
        return (
            f"Number of nodes: {self.num_nodes}\n"
            f"Number of edges: {self.num_edges}\n"
            f"Set of edge labels: {self.edge_labels}"
        )
