import argparse
import logging
from pprint import pformat
from diverse_lcs_graph import DiverseLCSGraph
from lcs import LCS
from lcs_graph import LCSGraph


def setup_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("S", type=str, help="First string for LCS computation")
    parser.add_argument("T", type=str, help="Second string for LCS computation")
    return parser.parse_args()


def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def compute_lcs(S, T):
    lcs = LCS(S, T)
    logging.info(f"LCS computed for strings '{S}' and '{T}'")
    logging.info(f"LCS length = {lcs.length}")
    logging.debug(f"DP table:\n{pformat(lcs.dp_table)}")
    logging.debug(
        f"Previous position dict:\n{pformat({k: [e.name for e in v] for k, v in lcs.previous_position_dict.items()})}"
    )
    return lcs


def compute_lcs_graph(lcs, S, T):
    lcs_graph = LCSGraph(lcs.previous_position_dict, S, T, lcs.length)
    logging.info("LCS graph computed.")
    logging.debug(f"Epsilon-free V_G:\n{pformat(lcs_graph.eps_free_V_G)}")
    logging.debug(f"Epsilon-free E_G:\n{pformat(lcs_graph.eps_free_E_G)}")
    logging.debug(f"Leveled_eps_free V_G:\n{pformat(lcs_graph.leveled_eps_free_V_G)}")
    logging.debug(f"Leveled_eps_free E_G:\n{pformat(lcs_graph.leveled_eps_free_E_G)}")
    return lcs_graph


def compute_diverse_lcs_graph(lcs_graph):
    diverse_lcs_graph = DiverseLCSGraph(
        lcs_graph.leveled_eps_free_V_G, lcs_graph.leveled_eps_free_E_G
    )
    logging.info("Diverse LCS graph computed.")
    logging.debug(f"DP table for diverse LCS graph:\n{pformat(diverse_lcs_graph.L)}")
    logging.debug(f"V_H:\n{pformat(diverse_lcs_graph.V_H)}")
    logging.debug(f"E_H:\n{pformat(diverse_lcs_graph.E_H)}")
    logging.info(f"max hamming distance = {diverse_lcs_graph.hamming_distance}")
    return diverse_lcs_graph


if __name__ == "__main__":
    args = setup_argparse()
    setup_logging(args.debug)

    lcs = compute_lcs(args.S, args.T)
    lcs_graph = compute_lcs_graph(lcs, args.S, args.T)
    diverse_lcs_graph = compute_diverse_lcs_graph(lcs_graph)
