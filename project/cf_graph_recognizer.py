"""Context-free recognizers for graphs"""

from typing import Set, Tuple
import networkx as nx
from pyformlang.cfg import CFG

from project import (
    cfg_to_wcnf,
    ecfg_to_rsm,
    cfg_to_ecfg,
    FABooleanMatricesDok,
    FABooleanMatrices,
    graph_to_nfa,
)

__all__ = ["hellings", "matrix_based", "tensor_based"]


def hellings(graph: nx.MultiDiGraph, cfg: CFG) -> Set[Tuple[int, str, int]]:
    """Context-free recognizers for graph based on Hellings Algorithm"""
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


def matrix_based(
    graph: nx.MultiDiGraph, cfg: CFG, fabm: FABooleanMatrices = FABooleanMatricesDok
) -> Set[Tuple[int, str, int]]:
    """Context-free recognizers for graph based on matrix multiplication"""
    wcnf = cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}
    nodes_num = graph.number_of_nodes()
    matrices = {
        v.value: fabm.create_bool_matrix((nodes_num, nodes_num)) for v in wcnf.variables
    }

    for i, j, data in graph.edges(data=True):
        l = data["label"]
        for v in {p.head.value for p in term_productions if p.body[0].value == l}:
            matrices[v][i, j] = True

    for i in range(nodes_num):
        for v in eps_prod_heads:
            matrices[v][i, i] = True

    any_changing = True
    while any_changing:
        any_changing = False
        for p in var_productions:
            old_nnz = fabm.get_nnz(matrices[p.head.value])
            fabm.mxm(
                matrices[p.body[0].value],
                matrices[p.body[1].value],
                bm_out=(matrices[p.head.value]),
            )
            new_nnz = fabm.get_nnz(matrices[p.head.value])
            any_changing = any_changing or old_nnz != new_nnz

    return {
        (u, variable, v)
        for variable, matrix in matrices.items()
        for u, v in fabm.get_nonzero(matrix)
    }


def tensor_based(
    graph: nx.MultiDiGraph, cfg: CFG, fabm: FABooleanMatrices = FABooleanMatricesDok
) -> Set[Tuple[int, str, int]]:
    """Context-free recognizers for graph based on Kronecker product"""
    graph_bm = fabm.from_automaton(graph_to_nfa(graph))
    rsm = ecfg_to_rsm(cfg_to_ecfg(cfg))
    rsm_vars = {box.variable.value for box in rsm.boxes}
    rsm_bm = fabm.from_rsm(rsm)

    for eps_state in rsm_bm.start_states & rsm_bm.final_states:
        variable = rsm_bm.get_nonterminals(eps_state, eps_state)
        if variable not in graph_bm.bool_matrices:
            graph_bm.bool_matrices[variable] = fabm.create_bool_matrix(
                (graph_bm.num_states, graph_bm.num_states)
            )
        for i in range(graph_bm.num_states):
            graph_bm.bool_matrices[variable][i, i] = True

    intersected_bm = graph_bm.intersect(rsm_bm)
    if not intersected_bm.num_states:
        return set()
    tc = intersected_bm.get_transitive_closure()

    prev_nnz = fabm.get_nnz(tc)
    new_nnz = 0

    while prev_nnz != new_nnz:
        for i, j in fabm.get_nonzero(tc):
            rsm_from = i % rsm_bm.num_states
            rsm_to = j % rsm_bm.num_states
            variable = rsm_bm.get_nonterminals(rsm_from, rsm_to)
            if not variable:
                continue
            graph_from = i // rsm_bm.num_states
            graph_to = j // rsm_bm.num_states
            if variable not in graph_bm.bool_matrices:
                graph_bm.bool_matrices[variable] = fabm.create_bool_matrix(
                    (graph_bm.num_states, graph_bm.num_states)
                )
            graph_bm.bool_matrices[variable][graph_from, graph_to] = True

        tc = graph_bm.intersect(rsm_bm).get_transitive_closure()

        prev_nnz, new_nnz = new_nnz, fabm.get_nnz(tc)

    return {
        (u, label, v)
        for label, bm in graph_bm.bool_matrices.items()
        if label in rsm_vars
        for u, v in fabm.get_nonzero(bm)
    }
