from collections import deque
from typing import Dict, List
from custom_types import Edge_G, Vertex_G

import numpy as np
from erase_eps import erase_eps
from my_enum import Direction


class LCSGraph:
    # 3 種類の頂点集合
    V_G: List[Vertex_G]  # (i, j)のリスト
    eps_free_V_G: List[Vertex_G]  # 空遷移除去後の頂点集合
    leveled_eps_free_V_G: Dict[int, List[Vertex_G]]  # 階層化された頂点集合

    # 3 種類の辺集合
    E_G: List[Edge_G]  # (i, j) -> [(i', j'), ...]のリスト
    eps_free_E_G: List[Edge_G]  # 空遷移除去後の辺集合
    leveled_eps_free_E_G: Dict[int, List[Edge_G]]  # 階層化された辺集合

    X: str  # 長さmの文字列, 座標(i, j)に対応する文字はS[i-1]
    s: Vertex_G  # LCSグラフの入口に対応する座標
    t: Vertex_G  # LCSグラフの出口に対応する座標

    # 作業用変数
    reached: np.ndarray  # reached[i, j] = True <=> (i, j)に到達済み

    def __init__(self, previous_position_dict, X, Y, s, t) -> None:
        """文字列SとTに対するLCSグラフを構築する

        入力：
        - previous_position_dict: LCSのDPテーブルの各マスに到達する前のマスの座標を記録したテーブル
        - X: 長さmの文字列
        - Y: 長さnの文字列
        - s: LCSグラフの入口に対応する座標
        - t: LCSグラフの出口に対応する座標

        LCSグラフの説明：
        LCSグラフとは3つ組(V_G, E_G, edge_label)である.
        - 頂点集合 V_G: 二つの文字列を比較したときのDPテーブルのマスのうち, LCSの経路に含まれるマスの集合
        - 辺集合 E_G: 有向辺 (u, c, v) の集合
        頂点集合と辺集合は，Sからの距離hを基準に階層化される．
        - V_G = V_G_0, ..., V_G_ell
        - E_G = E_G_1, ..., E_G_ell

        構築方法
        1. DPテーブル構築時に作成した, 各マスに到達する前のマスの座標を記録したテーブルを入力として受け取る．
        2. tからsに到達する全ての経路を辿る．
        3. 辿った経路と頂点をV_G, E_Gに追加する.
           辺ラベルには, LCSを構成する文字または空文字が入る.
            - 文字を設定 <=> (i-1, j-1)->(i,j)に遷移する,かつ,X[i-1] == Y[j-1]
            - 空文字を設定 <=> それ以外の場合
        4. epsilon除去を行う．
        5. 階層化を行う
        """
        self.m = len(X)
        self.n = len(Y)
        self.V_G = []
        self.E_G = []
        self.X = X
        self.Y = Y
        self.s = s
        self.t = t

        # 到達可能性マップの初期化
        self.reached = np.zeros((self.m + 1, self.n + 1), dtype=bool)

        # t から s へのパスをたどりグラフを構築
        self._rec_reach(t, previous_position_dict)

        # epsilon遷移を削除したグラフを構築
        _Sigma, self.eps_free_V_G, self.eps_free_E_G, I, F = erase_eps(
            "", self.V_G, self.E_G, {s}, {t}
        )

        # epsilon遷移を削除したグラフの頂点集合に対して，Sからそれぞれの頂点までの距離を計算する
        distances = self._bfs()

        # 階層化されたグラフを計算
        self._compute_leveled_graph(distances)

    def _rec_reach(self, u, previous_position_dict: Dict[Vertex_G, List[Direction]]):
        """与えられた頂点 u から入口へのパスを再帰的に探索し、グラフを構築する。"""
        if self.reached[u]:
            return
        self.reached[u] = True

        self.V_G.append(u)

        if u == self.s:
            return

        # u の入り辺の始点 u' を探索する
        # 同時に，辺集合を構築する
        for direct in previous_position_dict.get(u, []):
            u_prime = tuple(map(sum, zip(u, direct.value)))

            # 辺ラベルの構築
            c = ""
            if (
                direct == Direction.UPPER_LEFT
                and self.X[u_prime[0]] == self.Y[u_prime[1]]
            ):
                # 左上から遷移かつ，文字が一致する場合のみ辺ラベルに文字を設定する
                c = self.X[u_prime[0]]

            # 構築した辺 e を辺集合に追加する
            e = (u_prime, c, u)
            self.E_G.append(e)

            # u' から再帰的に探索する
            self._rec_reach(u_prime, previous_position_dict)

    def _bfs(self):
        """全ての頂点について，始点からの最短経路長を計算する．"""
        queue = deque([self.s])
        # 始点から各頂点までの最短経路長を記録するdictionary
        distances = {self.s: 0}

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

    def _compute_leveled_graph(self, distances: Dict[Vertex_G, int]):
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
