import pytest
import cfpq_data
from project.basic_graph_utils import get_graph_description


def test_cycle():
    nodes_number = 5
    edge_label = "a"
    cycle = cfpq_data.labeled_cycle_graph(nodes_number, edge_label=edge_label)
    assert (nodes_number, nodes_number, set(edge_label)) == get_graph_description(cycle)


def test_two_cycle():
    n, m = 5, 10
    edge_labels = ("a", "b")
    two_cycle = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )
    assert (n + m + 1, n + m + 2, set(edge_labels)) == get_graph_description(two_cycle)
