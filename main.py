from pprint import pprint
from diverse_lcs_graph import DiverseLCSGraph
from lcs import LCS
from lcs_graph import LCSGraph
from erase_eps import erase_eps


if __name__ == "__main__":
    # example from figure/Reachability_graph.png
    S = "ABACB"
    T = "BABBCAB"

    # LCSのDPテーブルを計算
    lcs = LCS(S, T)
    print(f"LCS length = {lcs.length}")
    print("DP table")
    print(lcs.dp_table)
    print("previous position dict")
    pprint({k: [e.name for e in v] for k, v in lcs.previous_position_dict.items()})

    # LCSの計算結果をもとに，LCSグラフを計算
    lcs_graph = LCSGraph(lcs.previous_position_dict, S, T, lcs.length)
    print("LCS graph")
    print("epsilon-free V_G")
    pprint(lcs_graph.eps_free_V_G)
    print("epsilon-free E_G")
    pprint(lcs_graph.eps_free_E_G)
    print("leveled_eps_free V_G")
    pprint(lcs_graph.leveled_eps_free_V_G)
    print("leveled_eps_free E_G")
    pprint(lcs_graph.leveled_eps_free_E_G)

    # diverse LCSの計算
    diverse_lcs_graph = DiverseLCSGraph(
        lcs_graph.leveled_eps_free_V_G, lcs_graph.leveled_eps_free_E_G
    )
    print("diverse LCS graph")
    print("DP table")
    pprint(diverse_lcs_graph.L)
    print("V_H")
    pprint(diverse_lcs_graph.V_H)
    print("E_H")
    pprint(diverse_lcs_graph.E_H)
    print("hamming distance")
    print(diverse_lcs_graph.hamming_distance)

    pass
