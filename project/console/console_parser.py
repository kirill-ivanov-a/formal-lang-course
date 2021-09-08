"""Function for parsing console input"""
import argparse

from project.console.console_utils import (
    print_graph_info,
    check_non_negative,
    print_graphs_list,
    graphs,
    gen_graph_by_name,
    gen_two_cycles,
)


def parse_args() -> argparse.Namespace:
    """Parses console input when starting a module

    Returns
    -------
    Namespace with parsed arguments.
    """
    parser = argparse.ArgumentParser(prog="python -m project")
    parser.set_defaults(func=lambda args: parser.error("too few arguments"))
    subparsers = parser.add_subparsers(title="graph utilities", dest="")

    # print-graph-info
    parser_print_graph_info = subparsers.add_parser(
        "print-graph-info", help="prints graph info"
    )
    parser_print_graph_info.add_argument(
        "name", metavar="graph-name", choices=graphs, help="name of desired graph"
    )
    parser_print_graph_info.set_defaults(func=print_graph_info)

    # graphs-list
    parser_print_graphs = subparsers.add_parser(
        "graphs-list", help="prints list of available graphs"
    )
    parser_print_graphs.set_defaults(func=print_graphs_list)

    # gen-graph
    parser_gen_graph = subparsers.add_parser("gen-graph", help="generates graph")
    parser_gen_graph.set_defaults(
        func=lambda args: parser_gen_graph.error("too few arguments")
    )
    gen_graph_subparsers = parser_gen_graph.add_subparsers()

    # gen-graph by-name
    parser_gen_graph_by_name = gen_graph_subparsers.add_parser(
        "by-name", help="generates graph by name"
    )
    parser_gen_graph_by_name.add_argument("name", help="graph name")
    parser_gen_graph_by_name.add_argument(
        "--output", metavar="PATH", help="path to save"
    )
    parser_gen_graph_by_name.set_defaults(func=gen_graph_by_name)

    # gen-graph two-cycles
    parser_gen_graph_two_cycles = gen_graph_subparsers.add_parser(
        "two-cycles", help="generates two cycles graph"
    )
    parser_gen_graph_two_cycles.add_argument(
        "num_first_cycle_nodes",
        metavar="num-first-cycle-nodes",
        help="number of nodes in the first cycle",
        type=check_non_negative,
    )
    parser_gen_graph_two_cycles.add_argument(
        "num_second_cycle_nodes",
        metavar="num-second-cycle-nodes",
        help="number of nodes in the second cycle",
        type=check_non_negative,
    )
    parser_gen_graph_two_cycles.add_argument(
        "--edge-labels",
        dest="edge_labels",
        help='edge labels for the first and second cycle (default "a", "b")',
        metavar=("L1", "L2"),
        default=["a", "b"],
        nargs=2,
    )
    parser_gen_graph_two_cycles.add_argument(
        "--output", metavar="PATH", help="path to save"
    )
    parser_gen_graph_two_cycles.set_defaults(func=gen_two_cycles)

    return parser.parse_args()
