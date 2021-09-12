"""Utilities for working with regular expressions"""
from typing import Union

from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["regex_to_min_dfa"]


def regex_to_min_dfa(regex: Union[str, Regex]) -> DeterministicFiniteAutomaton:
    """Returns the equivalent minimal dfa for a given regular expression

    Parameters
    ----------
    regex : Union[str, Regex]
        A string representation of a regular expression or
        a regular expression.

    Returns
    -------
    dfa_minimal : DeterministicFiniteAutomaton
        Equivalent minimal dfa.
    """
    if isinstance(regex, str):
        regex = Regex(regex)
    enfa = regex.to_epsilon_nfa()
    dfa_minimal = enfa.to_deterministic().minimize()
    return dfa_minimal
