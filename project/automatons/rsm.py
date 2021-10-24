from typing import Iterable

from pyformlang.cfg import Variable

from project.automatons.rsm_box import Box

__all__ = ["RSM"]


class RSM:
    """Recursive State Machine"""

    def __init__(
        self,
        start_symbol: Variable,
        boxes: Iterable[Box],
    ):
        self._start_symbol = start_symbol
        self._boxes = boxes

    def set_start_symbol(self, start_symbol: Variable):
        self._start_symbol = start_symbol

    def minimize(self):
        for box in self._boxes:
            box.minimize()
        return self

    @property
    def boxes(self):
        return self._boxes

    @property
    def start_symbol(self):
        return self._start_symbol
