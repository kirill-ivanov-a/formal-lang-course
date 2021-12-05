import pytest
import cfpq_data
import networkx as nx
from project import generate_two_cycles_graph


def test_graph_creation():
    n, m = 15, 5
    edge_labels = ("a", "b")

    expected_two_cycles = cfpq_data.labeled_two_cycles_graph(n, m, labels=edge_labels)
    actual_two_cycles = generate_two_cycles_graph(n, m, edge_labels=edge_labels)

    assert nx.is_isomorphic(actual_two_cycles, expected_two_cycles)
