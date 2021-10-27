import cfpq_data
import networkx as nx
from project import write_graph_to_dot


def test_graph_isomorphism(tmpdir):
    n, m = 52, 48
    edge_labels = ("a", "b")
    file = tmpdir.mkdir("test_dir").join("two_cycles.dot")

    graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )
    write_graph_to_dot(graph, file)

    actual_graph = nx.drawing.nx_pydot.read_dot(file)
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )

    assert nx.is_isomorphic(actual_graph, expected_graph)
