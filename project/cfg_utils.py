"""Utilities for working with CFG"""
from pyformlang.cfg import CFG

__all__ = ["cfg_to_wcnf", "cfg_from_file"]


def cfg_to_wcnf(cfg: CFG) -> CFG:
    """Converts a CFG to the Weak Chomsky Normal Form"""
    cleared_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cleared_productions = cleared_cfg._get_productions_with_only_single_terminals()
    cleared_productions = cleared_cfg._decompose_productions(cleared_productions)
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=cleared_productions)


def cfg_from_file(path: str, start_symbol: str = "S") -> CFG:
    """Reads a CFG from a file"""
    with open(path) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
