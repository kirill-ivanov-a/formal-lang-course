import sys

import pytest
from functools import partial
from pyformlang.cfg import CFG
from cfpq_data import labeled_cycle_graph


if not sys.platform.startswith("linux"):
    pytest.skip("skipping ubuntu-only tests", allow_module_level=True)
else:
    from project import (
        cf_graph_recognizer,
        generate_two_cycles_graph,
        FABooleanMatricesCB,
    )


@pytest.fixture(
    params=[
        cf_graph_recognizer.hellings,
        cf_graph_recognizer.matrix_based,
        cf_graph_recognizer.tensor_based,
        partial(cf_graph_recognizer.matrix_based, fabm=FABooleanMatricesCB),
        partial(cf_graph_recognizer.tensor_based, fabm=FABooleanMatricesCB),
    ]
)
def graph_recognizer(request):
    return request.param


@pytest.mark.parametrize(
    "cfg, graph, exp_ans",
    [
        (
            """
            S -> epsilon
            """,
            labeled_cycle_graph(3, "a"),
            {(1, "S", 1), (2, "S", 2), (0, "S", 0)},
        ),
        (
            """
                S -> b | epsilon
                """,
            labeled_cycle_graph(4, "b"),
            {
                (1, "S", 1),
                (2, "S", 2),
                (0, "S", 0),
                (3, "S", 3),
                (0, "S", 1),
                (1, "S", 2),
                (2, "S", 3),
                (3, "S", 0),
            },
        ),
        (
            """
                S -> A B
                S -> A S1
                S1 -> S B
                A -> a
                B -> b
                """,
            generate_two_cycles_graph(2, 1, ("a", "b")),
            {
                (0, "S1", 3),
                (2, "S1", 0),
                (2, "S", 3),
                (2, "S1", 3),
                (3, "B", 0),
                (1, "S", 0),
                (0, "S", 0),
                (1, "S", 3),
                (1, "A", 2),
                (0, "S", 3),
                (0, "B", 3),
                (1, "S1", 3),
                (2, "A", 0),
                (1, "S1", 0),
                (0, "S1", 0),
                (0, "A", 1),
                (2, "S", 0),
            },
        ),
    ],
)
def test_recognizer_answer(graph_recognizer, cfg, graph, exp_ans):
    assert graph_recognizer(graph, CFG.from_text(cfg)) == exp_ans
