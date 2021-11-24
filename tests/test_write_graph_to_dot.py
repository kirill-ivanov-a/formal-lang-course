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
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n, m, edge_labels=edge_labels, verbose=False
    )
    expected_graph_string = nx.drawing.nx_pydot.to_pydot(expected_graph).to_string()

    with open(file, "r") as f:
        actual_graph_string = f.read()

    assert actual_graph_string == expected_graph_string
