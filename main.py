from pprint import pprint
from lcs import LCS
from lcs_graph import LCSGraph


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
    lcs_graph = LCSGraph(lcs.previous_position_dict, S, T)
    print("LCS graph")
    print("V_G")
    pprint(lcs_graph.V_G)
    print("E_G")
    pprint(lcs_graph.E_G)
    print("edge label")
    pprint(lcs_graph.edge_label)

    pass
