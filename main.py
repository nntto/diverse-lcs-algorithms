import argparse
import logging
from pprint import pformat, pprint
import time
from lcs import LCS
from lcs_graph import LCSGraph
from path_k_tuple_graph import PathKTupleGraph
from path_tuple_graph import PathTupleGraph


def setup_argparse():
    parser = argparse.ArgumentParser()
    # mode
    parser.add_argument(
        "--debug-level",
        type=str,
        default="None",
        help="Enable debug logging if 'debug' is specified, Enable info logging if 'info' is specified, Disable logging if 'None' is specified",
    )
    parser.add_argument("X", type=str, help="First string for LCS computation")
    parser.add_argument("Y", type=str, help="Second string for LCS computation")
    parser.add_argument("k", type=int, help="k for k-diverse LCS computation")
    return parser.parse_args()


class CustomFormatter(logging.Formatter):
    def __init__(self, debug_format, info_format):
        self.debug_format = debug_format
        self.info_format = info_format
        super().__init__(
            fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt=None, style="%"
        )

    def format(self, record):
        # ログレベルによってフォーマットを切り替え
        if record.levelno <= logging.DEBUG:
            self._style._fmt = self.debug_format
        else:
            self._style._fmt = self.info_format

        return super().format(record)


def setup_logging(debug_level: str = "info" or "debug" or "None"):
    if debug_level == "debug":
        level = logging.DEBUG
    elif debug_level == "info":
        level = logging.INFO
    else:
        # 出力しない
        level = logging.CRITICAL


    # カスタムフォーマッタを作成
    debug_format = "%(levelname)s - %(message)s"
    info_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = CustomFormatter(debug_format, info_format)

    # ロギングハンドラを設定
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # ロガーを設定
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)


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

    if not (
        logging.getLogger().getEffectiveLevel() == logging.DEBUG
        or logging.getLogger().getEffectiveLevel() == logging.INFO):
        return path_k_tuple_graph

    logging.info("mutual hamming weight matrix computed.")
    logging.debug(
        f"mutual hamming weight matrix of k LCSs:\n{pformat(path_k_tuple_graph.mathcal_H)}"
    )
    parent = path_k_tuple_graph.parent
    logging.debug("parent:")
    for h in parent.keys():
        logging.debug(f"level {h}")
        for q_vec in parent[h].keys():
            logging.debug(f"   vertex {q_vec}")
            for W in parent[h][q_vec].keys():
                logging.debug(f"        matrix {W}")
                for p_vec, W_prime in parent[h][q_vec][W].items():
                    c_vec = [
                        c_vec
                        for (_p_vec, c_vec, _q_vec) in path_k_tuple_graph._in_edges_of(
                            q_vec, h
                        )
                        if _p_vec == p_vec
                    ][0]
                    logging.debug(f"            {c_vec}→{p_vec}→{W_prime}")
    return path_k_tuple_graph

def compute_min_diversity_set(path_k_tuple_graph: PathKTupleGraph) -> set[str]:
    k = path_k_tuple_graph.k
    diversity_min = path_k_tuple_graph.Diversity_min
    diverse_LCS_set = set()
    for W in path_k_tuple_graph.max_min_matrix_set(diversity_min):
        logging.debug(f"diverse LCS set for W = {W}")
        diverse_LCS_set |= path_k_tuple_graph.compute_diverse_LCS_set(W, logging)
    logging.info(f"{k}-Diversity min = {diversity_min}")
    logging.info(f"{k}-Diverse LCS set:\n{pformat(diverse_LCS_set)}")

    # 重複を含まないようにする
    non_duplicate_diverse_LCS_set = set()
    for S in diverse_LCS_set:
        # S をソート
        S = list(S)
        S.sort()
        non_duplicate_diverse_LCS_set.add(tuple(S))

    return non_duplicate_diverse_LCS_set



if __name__ == "__main__":
    args = setup_argparse()
    setup_logging(args.debug_level)

    lcs = compute_lcs(args.X, args.Y)
    print(f"lcs_length = {lcs.length}")
    lcs_graph = compute_lcs_graph(lcs, args.X, args.Y)
    print(f"lcs_count = {len(lcs_graph.LCS_set)}")
    path_k_tuple_graph = compute_path_k_tuple_graph(lcs_graph, args.k)

    print(f"min_diversity = {path_k_tuple_graph.Diversity_min}")
    # print(f"min_diversity_set_count = {len(min_diversity_set)}")
