"""Class representing a box of RSM"""
from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["Box"]


class Box:
    """A box for RMS"""

    def __init__(
        self, variable: Variable = None, dfa: DeterministicFiniteAutomaton = None
    ):
        self._dfa = dfa
        self._variable = variable

    def __eq__(self, other: "Box"):
        return self._variable == other._variable and self._dfa.is_equivalent_to(
            other._dfa
        )

    def minimize(self):
        self._dfa = self._dfa.minimize()

    @property
    def dfa(self) -> DeterministicFiniteAutomaton:
        return self._dfa

    @property
    def variable(self) -> Variable:
        return self._variable
