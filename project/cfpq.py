from typing import Set, Tuple, Callable
import networkx as nx
from pyformlang.cfg import CFG, Variable

from project import cf_graph_recognizer, cfg_to_wcnf

__all__ = ["hellings_cfpq", "matrix_cfpq"]


def hellings_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    """Context-Free Path Querying based on Hellings Algorithm"""
    return _cfpq(
        graph,
        cfg,
        start_nodes,
        final_nodes,
        start_var,
        recognizer=cf_graph_recognizer.hellings,
    )


def matrix_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    """Context-Free Path Querying based on matrix multiplication"""
    return _cfpq(
        graph,
        cfg,
        start_nodes,
        final_nodes,
        start_var,
        recognizer=cf_graph_recognizer.matrix_based,
    )


def _cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
    recognizer: Callable = cf_graph_recognizer.hellings,
) -> Set[Tuple[int, int]]:
    """Basic CFPQ function"""
    cfg._start_symbol = start_var
    wcnf = cfg_to_wcnf(cfg)
    reach_pairs = {
        (u, v) for u, h, v in recognizer(graph, wcnf) if h == wcnf.start_symbol.value
    }
    if start_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if u in start_nodes}
    if final_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if v in final_nodes}

    return reach_pairs
