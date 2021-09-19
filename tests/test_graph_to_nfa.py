import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from project import generate_two_cycles_graph, graph_to_nfa


@pytest.fixture
def synt_graph():
    return generate_two_cycles_graph(3, 2, ("a", "b"))


@pytest.fixture
def expected_nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [
            (1, "a", 2),
            (2, "a", 3),
            (3, "a", 0),
            (0, "a", 1),
            (0, "b", 4),
            (4, "b", 5),
            (5, "b", 0),
        ]
    )
    return nfa


def test_nondeterministic(synt_graph):
    nfa = graph_to_nfa(synt_graph)
    assert not nfa.is_deterministic()


@pytest.mark.parametrize("start_nodes,final_nodes", [(None, None), ({0, 1}, {2, 3})])
def test_equivalence(synt_graph, expected_nfa, start_nodes, final_nodes):
    if not start_nodes:
        start_nodes = set(synt_graph.nodes)
    if not final_nodes:
        final_nodes = set(synt_graph.nodes)

    for state in start_nodes:
        expected_nfa.add_start_state(State(state))

    for state in final_nodes:
        expected_nfa.add_final_state(State(state))

    actual_nfa = graph_to_nfa(synt_graph, start_nodes, final_nodes)

    assert actual_nfa.is_equivalent_to(expected_nfa)
