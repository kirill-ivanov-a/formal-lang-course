"""Utilities for working with CFG"""
from typing import AbstractSet, Iterable

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project.grammars.ecfg_exeptions import InvalidECFGFormatException
from project.grammars.ecfg_production import ECFGProduction

__all__ = ["ECFG"]


class ECFG:
    """Extended CFG"""

    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        start_symbol: Variable = None,
        productions: Iterable[ECFGProduction] = None,
    ):
        self._variables = variables or set()
        self._start_symbol = start_symbol
        self._productions = productions or set()

    @property
    def variables(self) -> AbstractSet[Variable]:
        return self._variables

    @property
    def productions(self) -> AbstractSet[ECFGProduction]:
        return self._productions

    @property
    def start_symbol(self) -> Variable:
        return self._start_symbol

    def to_text(self) -> str:
        """Returns a string representation of CFG"""
        return "\n".join(str(p) for p in self.productions)

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")) -> "ECFG":
        """Reads an ECFG from a text"""
        variables = set()
        productions = set()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise InvalidECFGFormatException(
                    "There should only be one production per line."
                )

            head_text, body_text = production_objects
            head = Variable(head_text.strip())

            if head in variables:
                raise InvalidECFGFormatException(
                    "There should only be one production for each variable."
                )

            variables.add(head)
            body = Regex(body_text.strip())
            productions.add(ECFGProduction(head, body))

        return ECFG(
            variables=variables, start_symbol=start_symbol, productions=productions
        )
