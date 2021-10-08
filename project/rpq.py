import networkx as nx
from pyformlang.regular_expression import Regex

from project import (
    regex_to_min_dfa,
    graph_to_nfa,
    FABooleanMatrices,
    FABooleanMatricesDok,
)


def rpq(
    graph: nx.MultiDiGraph,
    query: Regex,
    start_nodes: set = None,
    final_nodes: set = None,
    fabm: FABooleanMatrices = FABooleanMatricesDok,
) -> set:
    graph_bm = fabm.from_automaton(graph_to_nfa(graph, start_nodes, final_nodes))
    query_bm = fabm.from_automaton(regex_to_min_dfa(query))

    intersected_bm = graph_bm.intersect(query_bm)
    start_states = intersected_bm.get_start_states()
    final_states = intersected_bm.get_final_states()
    tc = intersected_bm.get_transitive_closure()
    res = set()

    for s_from, s_to in fabm._get_nonzero(tc):
        if s_from in start_states and s_to in final_states:
            res.add((s_from // query_bm.num_states, s_to // query_bm.num_states))

    return res
