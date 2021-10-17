"""Utilities for working with CFG"""
from pyformlang.cfg import CFG

__all__ = ["cfg_to_cnf", "cfg_from_file"]


def cfg_to_cnf(cfg: CFG) -> CFG:
    """Converts a CFG to the Chomsky Normal Form"""
    return cfg.to_normal_form()


def cfg_from_file(path: str, start_symbol: str = "S") -> CFG:
    """Reads a CFG from a file"""
    with open(path) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
