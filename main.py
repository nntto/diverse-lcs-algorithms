from lcs import LCS


if __name__ == "__main__":
    # LCSのDPテーブルを計算
    lcs = LCS("ACBDA", "BDCABA")
    print(lcs.length)
    print(lcs.dp_table)
    print(lcs.previous_position_table)

    # 2次元LCSグラフ G = (V_G, E_G, lab)を計算する．
    # Gは，LCSの到達可能性グラフのこと
    # ./figure/Reachability_graph.png を参照
    pass
