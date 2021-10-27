"""Class representing a production of an ECFG"""
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

__all__ = ["ECFGProduction"]


class ECFGProduction:
    """A production of a ECFG"""

    def __init__(self, head: Variable, body: Regex):
        self._head = head
        self._body = body

    def __str__(self):
        return str(self.head) + " -> " + str(self.body)

    @property
    def head(self) -> Variable:
        """Get the head variable"""
        return self._head

    @property
    def body(self) -> Regex:
        """Get the body objects"""
        return self._body
