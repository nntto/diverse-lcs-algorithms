from collections import deque
from typing import Dict, List
from custom_types import Edge_G, Vertex_G

import numpy as np
from erase_eps import erase_eps
from my_enum import Direction


class LCSGraph:
    V_G: List[Vertex_G]  # (i, j)のリスト
    eps_free_V_G: List[Vertex_G]  # 空遷移除去後の頂点集合
    leveled_eps_free_V_G: Dict[int, List[Vertex_G]]  # 階層化された頂点集合
    E_G: List[Edge_G]  # (i, j) -> [(i', j'), ...]のリスト
    eps_free_E_G: List[Edge_G]  # 空遷移除去後の辺集合
    leveled_eps_free_E_G: Dict[int, List[Edge_G]]  # 階層化された辺集合
    S: str  # 長さmの文字列, 座標(i, j)に対応する文字はS[i-1]

    # 作業用変数
    reached: np.ndarray  # reached[i, j] = True <=> (i, j)に到達済み

    def __init__(self, previous_position_dict, S, T, ell) -> None:
        """文字列SとTに対するLCSグラフを構築する

        入力：
        - previous_position_dict: LCSのDPテーブルの各マスに到達する前のマスの座標を記録したテーブル
        - S: 長さmの文字列
        - T: 長さnの文字列
        - ell: LCSの長さ

        LCSグラフの説明：
        LCSグラフとは3つ組(V_G, E_G, edge_label)である.
        - 頂点集合 V_G: 二つの文字列を比較したときのDPテーブルのマスのうち, LCSの経路に含まれるマスの集合
        - 辺集合 E_G: 有向辺 (u, c, v) の集合
        頂点集合と辺集合は，Sからの距離hを基準に階層化される．
        - V_G = V_G_0, ..., V_G_ell
        - E_G = E_G_1, ..., E_G_ell

        構築方法
        1. DPテーブル構築時に作成した, 各マスに到達する前のマスの座標を記録したテーブルを入力として受け取る．(コード上では辞書で実装)
        2. (m, n)から(0, 0)に到達するまでの全ての経路を辿る．
        3. 辿った経路と頂点をV_G, E_Gに追加する.
           辺ラベルには, LCSを構成する文字または空文字が入る.
            - 文字を設定 <=> (i-1, j-1)->(i,j)に遷移する,かつ,S[i-1] == T[j-1]
            - 空文字を設定 <=> それ以外の場合
        4. 最後に，epsilon除去を行う．
        """
        self.m = len(S)
        self.n = len(T)
        self.V_G = []
        self.E_G = []
        self.edge_label = {}
        self.S = S
        self.T = T

        # reachedの初期化. 全ての要素をFalseにする
        self.reached = np.zeros((self.m + 1, self.n + 1), dtype=bool)

        # (self.m, self.n)から(0, 0)に到達するまでの全ての経路を辿る
        self.rec_reach((self.m, self.n), previous_position_dict)

        # epsilon 除去
        _Sigma, self.eps_free_V_G, self.eps_free_E_G, I, F = erase_eps(
            "", self.V_G, self.E_G, {(0, 0)}, {(self.m, self.n)}
        )

        # epsilon除去後の頂点集合に対して，Sからそれぞれの頂点までの距離を計算する
        distances = self.bfs()

        # epsilon除去後の頂点集合と辺集合を階層化する
        self.compute_leveled_graph(distances)

    def rec_reach(self, u, previous_position_dict: Dict[Vertex_G, List[Direction]]):
        if self.reached[u]:
            return

        self.reached[u] = True
        # uに到達したので，V_Gに追加し，(i,j)から出る辺の集合を初期化
        self.V_G.append(u)

        if u == (0, 0):
            return

        for direct in previous_position_dict.get(u, []):
            # uからdirect方向に遷移した先の頂点
            u_prime = tuple(map(sum, zip(u, direct.value)))

            # 辺ラベルの設定
            # 文字が一致しなかった場合，ラベルは空文字
            c = ""

            # 文字が一致した場合，ラベルはその文字
            if (
                # 左上から遷移する場合のみ，文字が一致する
                direct == Direction.UPPER_LEFT
                and
                # 左上から遷移する場合でも，文字が一致しない場合がある．
                self.S[u_prime[0]] == self.T[u_prime[1]]
            ):
                c = self.S[u_prime[0]]

            # 辺を辺集合に追加する
            self.E_G.append((u_prime, c, u))

            self.rec_reach(u_prime, previous_position_dict)

    def bfs(self):
        """全ての頂点について，始点からの最短経路長を計算する．"""
        queue = deque([(0, 0)])
        # 始点から各頂点までの最短経路長を記録するdictionary
        distances = {(0, 0): 0}

        while queue:
            current_position = queue.popleft()
            current_distance = distances[current_position]

            for edge in [e for e in self.eps_free_E_G if e[0] == current_position]:
                new_position = edge[2]

                # new_positionが訪問されていない場合
                if new_position not in distances:
                    queue.append(new_position)
                    distances[new_position] = current_distance + 1

        return distances

    def compute_leveled_graph(self, distances: Dict[Vertex_G, int]):
        """階層化されたLCSグラフの頂点集合と辺集合を計算する．

        頂点集合と辺集合は，Sからの距離hを基準に階層化される．
        - leveled_eps_free_V_G = V_G_0, ..., V_G_ell
        - leveled_eps_free_E_G = E_G_1, ..., E_G_ell
        """
        self.leveled_eps_free_V_G = {}
        self.leveled_eps_free_E_G = {}

        for v, h in distances.items():
            if h not in self.leveled_eps_free_V_G:
                self.leveled_eps_free_V_G[h] = [v]
            else:
                self.leveled_eps_free_V_G[h].append(v)
            if h + 1 not in self.leveled_eps_free_E_G:
                self.leveled_eps_free_E_G[h + 1] = []

            # 距離hの頂点集合に属する頂点vから距離h+1の頂点uに向かう辺を追加する
            for edge in [e for e in self.eps_free_E_G if e[0] == v]:
                if edge[2] in distances:
                    self.leveled_eps_free_E_G[h + 1].append(edge)
