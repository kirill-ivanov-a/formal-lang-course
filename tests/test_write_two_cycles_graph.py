import pytest
import cfpq_data
import networkx as nx
from project.basic_graph_utils import write_two_cycles_graph


def test_graph_isomorphism(tmpdir):
    n, m = 52, 48
    edge_labels = ("a", "b")
    file = tmpdir.mkdir("test_dir").join("example.dot")
    write_two_cycles_graph(n, m, edge_labels, file)
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )
    unexpected_graph = cfpq_data.labeled_two_cycles_graph(
        n, m + 1, edge_labels=edge_labels, verbose=False
    )
    actual_graph = nx.drawing.nx_pydot.read_dot(file)
    assert nx.is_isomorphic(expected_graph, actual_graph)
    assert not nx.is_isomorphic(unexpected_graph, actual_graph)
