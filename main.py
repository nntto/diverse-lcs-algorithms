import argparse
import logging
from pprint import pformat
import time
from lcs import LCS
from lcs_graph import LCSGraph
from path_k_tuple_graph import PathKTupleGraph
from path_tuple_graph import PathTupleGraph


def setup_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("X", type=str, help="First string for LCS computation")
    parser.add_argument("Y", type=str, help="Second string for LCS computation")
    parser.add_argument("k", type=int, help="k for k-diverse LCS computation")
    return parser.parse_args()


def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    # 現在時刻をファイル名とするログファイルを作成する
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=f"logs/{time.strftime('%Y%m%d_%H%M%S')}.log",
    )


def compute_lcs(X, Y):
    lcs = LCS(X, Y)
    logging.info(f"LCS computed for strings '{X}' and '{Y}'")
    logging.info(f"LCS length = {lcs.length}")
    logging.debug(f"DP table:\n{pformat(lcs.dp_table)}")
    logging.debug(
        f"Previous position dict:\n{pformat({k: [e.name for e in v] for k, v in lcs.previous_position_dict.items()})}"
    )
    return lcs


def compute_lcs_graph(lcs, X, Y):
    lcs_graph = LCSGraph(lcs.previous_position_dict, X, Y, (0, 0), (len(X), len(Y)))
    logging.info("LCS graph computed.")
    logging.info(f"LCS set:\n{pformat(lcs_graph.LCS_set)}")
    logging.debug(f"Epsilon-free V_G:\n{pformat(lcs_graph.eps_free_V_G)}")
    logging.debug(f"Epsilon-free E_G:\n{pformat(lcs_graph.eps_free_E_G)}")
    logging.debug(f"Leveled_eps_free V_G:\n{pformat(lcs_graph.leveled_eps_free_V_G)}")
    logging.debug(f"Leveled_eps_free E_G:\n{pformat(lcs_graph.leveled_eps_free_E_G)}")
    return lcs_graph


def compute_path_tuple_graph(lcs_graph):
    path_tuple_graph = PathTupleGraph(
        lcs_graph.leveled_eps_free_V_G, lcs_graph.leveled_eps_free_E_G
    )
    logging.info("2-Diverse LCS graph computed.")
    logging.debug(f"DP table for diverse LCS graph:\n{pformat(path_tuple_graph.L)}")
    logging.debug(f"V_H:\n{pformat(path_tuple_graph.V_H)}")
    logging.debug(f"E_H:\n{pformat(path_tuple_graph.E_H)}")
    logging.info(f"2-Diverse LCS set:\n{pformat(path_tuple_graph.diverse_LCS_set)}")
    logging.info(f"max hamming distance = {path_tuple_graph.hamming_distance}")
    return path_tuple_graph


def compute_path_k_tuple_graph(lcs_graph, k):
    path_k_tuple_graph = PathKTupleGraph(
        lcs_graph.leveled_eps_free_V_G, lcs_graph.leveled_eps_free_E_G, k
    )
    logging.info("mutual hamming weight matrix computed.")
    logging.debug(
        f"mutual hamming weight matrix of k LCSs:\n{pformat(path_k_tuple_graph.mathcal_H)}"
    )
    logging.info(f"Diversity min = {path_k_tuple_graph.Diversity_min}")
    return path_k_tuple_graph


if __name__ == "__main__":
    args = setup_argparse()
    setup_logging(args.debug)

    lcs = compute_lcs(args.X, args.Y)
    lcs_graph = compute_lcs_graph(lcs, args.X, args.Y)
    path_tuple_graph = compute_path_tuple_graph(lcs_graph)
    path_k_tuple_graph = compute_path_k_tuple_graph(lcs_graph, args.k)
