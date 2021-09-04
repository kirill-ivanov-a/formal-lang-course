"""Basic utilities for working with graphs"""
from typing import Tuple

import cfpq_data
import networkx as nx


def get_graph_description(graph: nx.MultiDiGraph) -> Tuple[int, int, set]:
    """Returns number of nodes, number of edges, set of labels"""
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def write_two_cycles_graph(
    first_cycle_nodes: int,
    second_cycle_nodes: int,
    edge_labels: Tuple[str, str],
    path: str,
) -> None:
    """Creates and writes a graph of two cycles to the file"""
    two_cycles_graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes, second_cycle_nodes, edge_labels=edge_labels, verbose=False
    )
    nx.drawing.nx_pydot.write_dot(two_cycles_graph, path)
