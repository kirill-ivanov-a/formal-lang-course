"""Utilities for working with regular expressions"""
import networkx as nx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)

__all__ = ["regex_to_min_dfa", "graph_to_nfa"]


def regex_to_min_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """Returns the equivalent minimal dfa for a given regular expression.

    Parameters
    ----------
    regex : Regex
        Regular expression to be transformed into a minimal DFA.

    Returns
    -------
    dfa_minimal : DeterministicFiniteAutomaton
        Equivalent minimal dfa.
    """
    enfa = regex.to_epsilon_nfa()
    dfa_minimal = enfa.to_deterministic().minimize()
    return dfa_minimal


def graph_to_nfa(
    graph: nx.MultiDiGraph, start_nodes: set = None, final_nodes: set = None
) -> NondeterministicFiniteAutomaton:
    """Converts the given graph to NFA.

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to be converted.

    start_nodes : set
        Set of starting nodes.

    final_nodes : set
        Set of final nodes.

    Returns
    -------
    nfa : NondeterministicFiniteAutomaton
        NFA transformed from the graph.
    """
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    if not start_nodes:
        start_nodes = set(graph.nodes)
    if not final_nodes:
        final_nodes = set(graph.nodes)

    for state in start_nodes:
        nfa.add_start_state(State(state))

    for state in final_nodes:
        nfa.add_final_state(State(state))

    return nfa
