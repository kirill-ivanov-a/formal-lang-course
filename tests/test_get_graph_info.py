import pytest
import cfpq_data
from project import get_graph_info, GraphInfo


def test_cycle():
    nodes_number = 5
    edge_label = "a"
    cycle = cfpq_data.labeled_cycle_graph(nodes_number, label=edge_label)

    actual_info = get_graph_info(cycle)
    expected_info = GraphInfo(nodes_number, nodes_number, set(edge_label))

    assert actual_info == expected_info


def test_two_cycles():
    n, m = 5, 10
    edge_labels = ("a", "b")
    two_cycles = cfpq_data.labeled_two_cycles_graph(n, m, labels=edge_labels)

    actual_info = get_graph_info(two_cycles)
    expected_info = GraphInfo(n + m + 1, n + m + 2, set(edge_labels))

    assert actual_info == expected_info
