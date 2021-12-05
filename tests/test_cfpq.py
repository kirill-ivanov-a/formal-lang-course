import sys

import pytest
from pyformlang.cfg import CFG
from itertools import product
from collections import namedtuple
from functools import partial
from cfpq_data import labeled_cycle_graph

if not sys.platform.startswith("linux"):
    pytest.skip("skipping ubuntu-only tests", allow_module_level=True)
else:
    from project import (
        generate_two_cycles_graph,
        matrix_cfpq,
        hellings_cfpq,
        tensor_cfpq,
        FABooleanMatricesCB,
    )

Config = namedtuple("Config", ["start_var", "start_nodes", "final_nodes", "exp_ans"])


@pytest.fixture(
    params=[
        hellings_cfpq,
        matrix_cfpq,
        tensor_cfpq,
        partial(matrix_cfpq, fabm=FABooleanMatricesCB),
        partial(tensor_cfpq, fabm=FABooleanMatricesCB),
    ]
)
def cfpq(request):
    return request.param


@pytest.mark.parametrize(
    "cfg, graph, confs",
    [
        (
            """
                        S -> A B
                        S -> A S1
                        S1 -> S B
                        A -> a
                        B -> b
                        """,
            generate_two_cycles_graph(2, 1, ("a", "b")),
            [
                Config(
                    "S", None, None, {(0, 0), (0, 3), (2, 0), (2, 3), (1, 0), (1, 3)}
                ),
                Config("S", {0}, {0}, {(0, 0)}),
                Config("A", None, None, {(0, 1), (1, 2), (2, 0)}),
                Config("B", None, None, {(3, 0), (0, 3)}),
            ],
        ),
        (
            """
                    A -> a A | epsilon
                    B -> b B | b
                    """,
            labeled_cycle_graph(3, "a", verbose=False),
            [
                Config("A", {0}, {0}, {(0, 0)}),
                Config("A", None, None, set(product(range(3), range(3)))),
                Config("B", None, None, set()),
            ],
        ),
        (
            """
                    S -> epsilon
                    """,
            labeled_cycle_graph(4, "b", verbose=False),
            [
                Config("S", {0, 1}, {0, 1}, {(0, 0), (1, 1)}),
                Config("S", None, None, set((v, v) for v in range(4))),
                Config("B", None, None, set()),
            ],
        ),
    ],
)
def test_cfpq_answer(cfpq, cfg, graph, confs):
    assert all(
        cfpq(
            graph,
            CFG.from_text(cfg),
            conf.start_nodes,
            conf.final_nodes,
            conf.start_var,
        )
        == conf.exp_ans
        for conf in confs
    )
