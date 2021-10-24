"""Utilities for working with CFG"""
from pyformlang.cfg import CFG
from pyformlang.regular_expression import Regex

from project.grammars.ecfg import ECFG
from project.grammars.ecfg_production import ECFGProduction
from project.automatons.automaton_utils import regex_to_min_dfa
from project.automatons.rsm import RSM
from project.automatons.rsm_box import Box

__all__ = [
    "cfg_to_wcnf",
    "cfg_from_file",
    "cfg_to_ecfg",
    "ecfg_to_rsm",
    "ecfg_from_file",
]


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


def cfg_to_ecfg(cfg: CFG) -> ECFG:
    """Converts a CFG to an Extended CFG"""
    productions = dict()

    for p in cfg.productions:
        body = Regex(" ".join(cfg_obj.value for cfg_obj in p.body) if p.body else "$")
        if p.head not in productions:
            productions[p.head] = body
        else:
            productions[p.head] = productions.get(p.head).union(body)

    ecfg_productions = [
        ECFGProduction(head, body) for head, body in productions.items()
    ]

    return ECFG(
        variables=cfg.variables,
        start_symbol=cfg.start_symbol,
        productions=ecfg_productions,
    )


def ecfg_to_rsm(ecfg: ECFG) -> RSM:
    """Converts an ECFG to a Recursive State Machine"""
    boxes = [Box(p.head, regex_to_min_dfa(p.body)) for p in ecfg.productions]
    return RSM(start_symbol=ecfg.start_symbol, boxes=boxes)


def ecfg_from_file(path: str, start_symbol: str = "S") -> ECFG:
    """Reads an ECFG from a file"""
    with open(path) as f:
        return ECFG.from_text(f.read(), start_symbol=start_symbol)
