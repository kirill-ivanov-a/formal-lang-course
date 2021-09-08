"""Console utilities for running `project` as a module"""
import argparse
from argparse import Namespace
from itertools import chain

import networkx as nx
from cfpq_data import graph_from_dataset, DATASET
from project import graph_utils

graphs = list(chain.from_iterable(x.keys() for x in DATASET.values()))


def print_graph_info(args: Namespace) -> None:
    """Prints information about a graph by its name.

    Parameters
    ----------
    args: Namespace
        Parsed arguments.

    Returns
    -------
    None
    """
    graph = graph_from_dataset(args.name, verbose=False)
    print(f"Information about graph `{args.name}`")
    print(graph_utils.get_graph_info(graph))


def gen_two_cycles(args: Namespace) -> None:
    """Generates a graph of two cycles and prints
    its dot representation (if args contains the output path)
    or saves to a file (otherwise).

    Parameters
    ----------
    args: Namespace
        Parsed arguments.

    Returns
    -------
    None
    """
    graph = graph_utils.generate_two_cycles_graph(
        args.num_first_cycle_nodes, args.num_second_cycle_nodes, args.edge_labels
    )
    if args.output:
        print(
            f"The graph has been successfully written to "
            f"{graph_utils.write_graph_to_dot(graph, args.output)}"
        )
    else:
        print(nx.drawing.nx_pydot.to_pydot(graph).to_string())


def gen_graph_by_name(args: Namespace) -> None:
    """Generates a graph by its name and prints
    its dot representation (if args contains the output path)
    or saves to a file (otherwise).

    Parameters
    ----------
    args: Namespace
        Parsed arguments.

    Returns
    -------
    None
    """
    graph = graph_from_dataset(args.name, verbose=False)
    if args.output:
        print(
            f"The graph has been successfully written to "
            f"{graph_utils.write_graph_to_dot(graph, args.output)}"
        )
    else:
        print(nx.drawing.nx_pydot.to_pydot(graph).to_string())


def print_graphs_list(args: Namespace) -> None:
    """Prints a list of names of available graphs

    Parameters
    ----------
    args: Namespace
        Parsed arguments.

    Returns
    -------
    None
    """
    print("List of available graphs:")
    print(", ".join(graphs))


def check_non_negative(value: str) -> int:
    """Checks if the value is a non-negative integer.

    Parameters
    ----------
    value : str
        Value to check.

    Returns
    -------
    value : int
        Casted integer value.

    Raises
    ------
    ArgumentTypeError
        If the value cannot be converted to non-negative integer.
    """
    try:
        value = int(value)
        if value < 0:
            raise argparse.ArgumentTypeError(f"{value} is not a non-negative integer")
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"{value} is not an integer") from error
    return value
