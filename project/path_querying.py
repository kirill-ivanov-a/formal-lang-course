import networkx as nx
from pyformlang.regular_expression import Regex

from project import regex_to_min_dfa, graph_to_nfa, FABooleanMatrices


def make_rpq(
    graph: nx.MultiDiGraph,
    query: Regex,
    start_nodes: set = None,
    final_nodes: set = None,
) -> set:

    graph_bm = FABooleanMatrices.from_automaton(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )
    query_bm = FABooleanMatrices.from_automaton(regex_to_min_dfa(query))

    intersected_bm = FABooleanMatrices.intersect(graph_bm, query_bm)
    start_states = intersected_bm.start_states
    final_states = intersected_bm.final_states
    tc = intersected_bm.get_transitive_closure()
    res = set()

    for s_from, s_to in zip(*tc.nonzero()):
        if s_from in start_states and s_to in final_states:
            res.add((s_from // query_bm.num_states, s_to // query_bm.num_states))

    return res
