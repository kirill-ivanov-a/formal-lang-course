"""Utilities for working with graphs"""
from typing import Tuple, AnyStr

import os
import cfpq_data
import networkx as nx

from project.graphs.graph_info import GraphInfo

__all__ = ["get_graph_info", "generate_two_cycles_graph", "write_graph_to_dot"]


def get_graph_info(graph: nx.MultiDiGraph) -> GraphInfo:
    """Returns graph information
    with number of nodes, number of edges, set of labels.

    Parameters
    ----------
    graph : MultiDiGraph
        The graph to describe.

    Returns
    -------
    GraphInfo
        Information about the graph.
    """
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        {l for _, _, l in graph.edges(data="label")},
    )


def generate_two_cycles_graph(
    first_cycle_nodes_num: int,
    second_cycle_nodes_num: int,
    edge_labels: Tuple[str, str],
) -> nx.MultiDiGraph:
    """Returns a labeled two cycles graph.

    Parameters
    ----------
    first_cycle_nodes_num : int
        Number of nodes in the first cycle.

    second_cycle_nodes_num : int
        Number of nodes in the second cycle.

    edge_labels : Tuple[str, str]
        Graph edge labels.

    Returns
    -------
    g : MultiDiGraph
        A graph with two cycles.
    """
    return cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes_num,
        second_cycle_nodes_num,
        labels=edge_labels,
    )


def write_graph_to_dot(
    graph: nx.MultiDiGraph,
    path: str,
) -> AnyStr:
    """Writes a graph of two cycles to the file.

    Parameters
    ----------
    graph : MultiDiGraph
        The graph to be written.
    path : str
        Path to the file where the graph will be written.

    Returns
    -------
    str
        Path to the file where the graph is written.
    """
    nx.drawing.nx_pydot.write_dot(graph, path)
    return os.path.abspath(path)
