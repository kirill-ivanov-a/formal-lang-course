from itertools import product

import pytest
from pyformlang.regular_expression import PythonRegex

from project import (
    generate_two_cycles_graph,
    rpq,
    FABooleanMatricesDok,
    FABooleanMatricesCB,
)


@pytest.fixture(params=[FABooleanMatricesDok, FABooleanMatricesCB])
def fabm(request):
    return request.param


@pytest.fixture
def graph():
    return generate_two_cycles_graph(3, 2, ("x", "y"))


@pytest.fixture
def all_nodes_rpq():
    res = set(product(range(4), range(4)))
    return res.union({(0, 4), (4, 5), (5, 0)})


def test_all_nodes_s_and_f(graph, fabm, all_nodes_rpq):
    # All nodes are start and final
    actual_rpq = rpq(graph, PythonRegex("x*|y"), fabm=fabm)

    assert actual_rpq == all_nodes_rpq


@pytest.mark.parametrize(
    "pattern,start_nodes,final_nodes,expected_rpq",
    [
        ("x*|y", {0}, {1, 2, 3, 4}, {(0, 1), (0, 2), (0, 3), (0, 4)}),
        ("x*|y", {4}, {4, 5}, {(4, 5)}),
        ("xx", {0, 1, 2, 3}, {0, 1, 2, 3}, {(0, 2), (1, 3), (2, 0), (3, 1)}),
        ("y", {0}, {0, 1, 2, 3}, set()),
        ("y*", {0}, {5, 4}, {(0, 5), (0, 4)}),
    ],
)
def test_querying(graph, fabm, pattern, start_nodes, final_nodes, expected_rpq):
    regex = PythonRegex(pattern)
    actual_rpq = rpq(graph, regex, start_nodes, final_nodes, fabm)

    assert actual_rpq == expected_rpq
