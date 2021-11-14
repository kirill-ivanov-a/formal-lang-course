from typing import Set, Tuple
import networkx as nx
from pyformlang.cfg import CFG, Variable

from project import cfg_to_wcnf

__all__ = ["hellings"]


def hellings(graph: nx.MultiDiGraph, cfg: CFG) -> Set[Tuple[int, str, int]]:
    wcnf = cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}

    r = {(v, h, v) for v in range(graph.number_of_nodes()) for h in eps_prod_heads} | {
        (u, p.head.value, v)
        for u, v, edge_data in graph.edges(data=True)
        for p in term_productions
        if p.body[0].value == edge_data["label"]
    }

    new = r.copy()
    while new:
        n, N, m = new.pop()
        r_temp = set()

        for u, M, v in r:
            if v == n:
                triplets = {
                    (u, p.head.value, m)
                    for p in var_productions
                    if p.body[0].value == M
                    and p.body[1].value == N
                    and (u, p.head.value, m) not in r
                }
                r_temp |= triplets
        r |= r_temp
        new |= r_temp
        r_temp.clear()

        for u, M, v in r:
            if u == m:
                triplets = {
                    (n, p.head.value, v)
                    for p in var_productions
                    if p.body[0].value == N
                    and p.body[1].value == M
                    and (n, p.head.value, v) not in r
                }
                r_temp |= triplets
        r |= r_temp
        new |= r_temp

    return r
