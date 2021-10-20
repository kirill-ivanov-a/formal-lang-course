"""Utilities for working with CFG"""
from pyformlang.cfg import CFG, Production

__all__ = ["cfg_to_wcnf", "cfg_from_file"]


def cfg_to_wcnf(cfg: CFG) -> CFG:
    """Converts a CFG to the Chomsky Normal Form"""
    wcnf = cfg.to_normal_form()
    if cfg.generate_epsilon():
        productions = set(wcnf.productions)
        productions.add(Production(wcnf.start_symbol, []))
        wcnf = CFG(
            variables=wcnf.variables,
            terminals=wcnf.terminals,
            start_symbol=wcnf.start_symbol,
            productions=productions,
        )
    return wcnf


def cfg_from_file(path: str, start_symbol: str = "S") -> CFG:
    """Reads a CFG from a file"""
    with open(path) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
