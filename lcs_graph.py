from typing import Dict, List, Tuple

import numpy as np
from my_enum import Direction


class LCSGraph:
    V_G: List[Tuple[int, int]]  # (i, j)のリスト
    E_G: Dict[Tuple[int, int], List[Tuple[int, int]]]  # (i, j) -> [(i', j'), ...]の辞書
    edge_label: Dict[Tuple[Tuple[int, int], Tuple[int, int]], str]  # 辺のラベル
    S: str  # 長さmの文字列, 座標(i, j)に対応する文字はS[i-1]

    # 作業用変数
    reached: np.ndarray  # reached[i, j] = True <=> (i, j)に到達済み

    def __init__(self, previous_position_dict, S, T) -> None:
        """文字列SとTに対するLCSグラフを構築する

        LCSグラフとは3つ組(V_G, E_G, edge_label)である.
        - 頂点集合 V_G: 二つの文字列を比較したときのDPテーブルのマスのうち, LCSの経路に含まれるマスの集合
        - 辺集合 E_G: V_Gの各頂点に対して, その頂点から遷移可能な頂点の集合
        - 辺のラベル: 辺(u, v)に対して, uからvに遷移するときに追加される文字

        構築方法
        1. DPテーブル構築時に作成した, 各マスに到達する前のマスの座標を記録したテーブルを入力として受け取る．(コード上では辞書で実装)
        2. (m, n)から(0, 0)に到達するまでの全ての経路を辿る．
        3. 辿った経路と頂点をV_G, E_Gに追加する.
           同時に, 辺のラベルを設定する. ラベルには, LCSを構成する文字または空文字が入る.
            - 文字を設定 <=> (i-1, j-1)->(i,j)に遷移する,かつ,S[i-1] == T[j-1]
            - 空文字を設定 <=> それ以外の場合
        """
        self.m = len(S)
        self.n = len(T)
        self.V_G = []
        self.E_G = {}
        self.edge_label = {}
        self.S = S
        self.T = T

        # reachedの初期化. 全ての要素をFalseにする
        self.reached = np.zeros((self.m + 1, self.n + 1), dtype=bool)

        # (self.m, self.n)から(0, 0)に到達するまでの全ての経路を辿る
        self.rec_reach((self.m, self.n), previous_position_dict)

    def rec_reach(
        self, u, previous_position_dict: Dict[Tuple[int, int], List[Direction]]
    ):
        if self.reached[u]:
            return

        self.reached[u] = True
        # uに到達したので，V_Gに追加し，(i,j)から出る辺の集合を初期化
        self.V_G.append(u)
        self.E_G[u] = []

        if u == (0, 0):
            return

        for direct in previous_position_dict.get(u, []):
            # uからdirect方向に遷移した先の頂点
            u_prime = tuple(map(sum, zip(u, direct.value)))

            # uからu_primeに辺を張る
            self.E_G[u].append(u_prime)

            # ラベルの設定
            if (
                # 左上から遷移する場合のみ，文字が一致する
                direct == Direction.UPPER_LEFT
                and
                # 左上から遷移する場合でも，文字が一致しない場合がある．
                self.S[u_prime[0]] == self.T[u_prime[1]]
            ):
                # 文字が一致した場合，ラベルはその文字
                self.edge_label[(u, u_prime)] = self.S[u_prime[0]]
            else:
                # 文字が一致しなかった場合，ラベルは空文字
                self.edge_label[(u, u_prime)] = ""

            self.rec_reach(u_prime, previous_position_dict)

