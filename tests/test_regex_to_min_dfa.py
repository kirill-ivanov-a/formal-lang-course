import pytest
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol
from pyformlang.regular_expression import Regex

from project import regex_to_min_dfa


@pytest.fixture
def regex():
    pattern = "(a|$) (b a)* (b|$)"
    return Regex(pattern)


def test_deterministic(regex):
    assert regex_to_min_dfa(regex).is_deterministic()


def test_equivalence(regex):
    min_dfa = regex_to_min_dfa(regex)

    dfa = DeterministicFiniteAutomaton()

    state0 = State(0)
    state1 = State(1)
    state2 = State(2)

    symb_a = Symbol("a")
    symb_b = Symbol("b")

    dfa.add_start_state(state0)

    dfa.add_final_state(state0)
    dfa.add_final_state(state1)
    dfa.add_final_state(state2)

    dfa.add_transition(state0, symb_b, state1)
    dfa.add_transition(state0, symb_a, state2)
    dfa.add_transition(state2, symb_b, state1)
    dfa.add_transition(state1, symb_a, state2)

    assert min_dfa.is_equivalent_to(dfa)


def test_minimal(regex):
    min_dfa = regex_to_min_dfa(regex)
    expected_num_states = 3
    actual_num_states = len(min_dfa.states)

    assert actual_num_states == expected_num_states
