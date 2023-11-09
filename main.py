import argparse
import logging
from pprint import pformat
from diverse_lcs_graph import DiverseLCSGraph
from lcs import LCS
from lcs_graph import LCSGraph

# argparseをセットアップ
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Enable debug logging")
args = parser.parse_args()

# loggingのレベルをセットアップ
level = logging.INFO
if args.debug:
    level = logging.DEBUG

# Loggingの基本設定を行う。INFOレベル以上のログをコンソールに出力
logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    logging.info("Starting LCS computation.")

    S = "ABACB"
    T = "BABBCAB"
    lcs = LCS(S, T)

    logging.info(f"LCS computed")
    logging.info(f"LCS length = {lcs.length}")
    logging.debug(f"DP table:\n{pformat(lcs.dp_table)}")
    logging.debug(
        f"Previous position dict:\n{pformat({k: [e.name for e in v] for k, v in lcs.previous_position_dict.items()})}"
    )

    lcs_graph = LCSGraph(lcs.previous_position_dict, S, T, lcs.length)
    logging.info("LCS graph computed.")

    logging.debug(f"Epsilon-free V_G:\n{pformat(lcs_graph.eps_free_V_G)}")
    logging.debug(f"Epsilon-free E_G:\n{pformat(lcs_graph.eps_free_E_G)}")
    logging.debug(f"Leveled_eps_free V_G:\n{pformat(lcs_graph.leveled_eps_free_V_G)}")
    logging.debug(f"Leveled_eps_free E_G:\n{pformat(lcs_graph.leveled_eps_free_E_G)}")

    diverse_lcs_graph = DiverseLCSGraph(
        lcs_graph.leveled_eps_free_V_G, lcs_graph.leveled_eps_free_E_G
    )
    logging.info("Diverse LCS graph computed.")

    logging.debug(f"DP table for diverse LCS graph:\n{pformat(diverse_lcs_graph.L)}")
    logging.debug(f"V_H:\n{pformat(diverse_lcs_graph.V_H)}")
    logging.debug(f"E_H:\n{pformat(diverse_lcs_graph.E_H)}")
    logging.info(f"max hamming distance = {diverse_lcs_graph.hamming_distance}")
