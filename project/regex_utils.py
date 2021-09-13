"""Utilities for working with regular expressions"""
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["regex_to_min_dfa"]


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
