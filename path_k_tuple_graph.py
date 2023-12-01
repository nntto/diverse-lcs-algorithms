from itertools import combinations, combinations_with_replacement
import logging
from pprint import pformat, pprint
from typing import Dict, List, Tuple

from custom_types import Edge_G, Edge_H, Vertex_G, Vertex_H
from utils import hash


class PathKTupleGraph:
    s_vec: Vertex_H  # パス対グラフの入口
    t_vec: Vertex_H  # パス対グラフの出口
    k: int  # diverse LCS を構成するLCSの本数
    ell: int  # LCS グラフの階層数
    mathcal_H: Dict[int, Dict[Vertex_H, int]]  # mutual hamming weight matrix
    Diversity_min: int  # diverse LCS の最小ハミング距離
    parent: Dict[
        int, Dict[Vertex_H, Dict[list[list[int]], Tuple[Vertex_H, list[list[int]]]]]
    ]  # 多様なLCSを構成するための親子関係, 一次キーは，階層h, (頂点，ハミング距離行列)のタプル
    # パスラベルを取ると，diverse LCS となるk本のLCSが得られる．

    # diverse LCS 集合
    diverse_LCS_set: set[set[str]]

    def __init__(
        self,
        leveled_V_G: Dict[int, List[Vertex_G]],
        leveled_E_G: Dict[int, List[Edge_G]],
        k: int,
    ) -> None:
        self.leveled_V_G = leveled_V_G
        self.leveled_E_G = leveled_E_G
        self.k = k
        self._initialize_graph()

    def _initialize_graph(self) -> None:
        s = self.leveled_V_G[0][0]  # LCS グラフの入口
        t = self.leveled_V_G[max(self.leveled_V_G)][0]  # LCS グラフの出口

        self.s_vec, self.t_vec = (s,) * self.k, (t,) * self.k
        self.ell = max(self.leveled_V_G)
        self.mathcal_H = self._compute_mutual_hamming_weight_matrix()
        self.Diversity_min = self._compute_diversity_min()

    def gen_W_0(self):
        return [[0] * self.k for _ in range(self.k)]

    def _compute_mutual_hamming_weight_matrix(
        self,
    ) -> Tuple[List[Vertex_H], List[Edge_H], Dict[Vertex_G, int],]:
        # k * k のハミング距離行列を計算する．
        # 初期値は全て0
        mathcal_H = {0: {self.s_vec: [self.gen_W_0()]}}
        self.parent = {0: {self.s_vec: {hash(self.gen_W_0()): {}}}}

        for h in range(1, self.ell + 1):
            mathcal_H[h] = {}
            self.parent[h] = {}
            for q_vec in self._vertices(h):
                mathcal_H[h][q_vec] = set()
                self.parent[h][q_vec] = {}
                for e_vec in self._in_edges_of(q_vec, h):
                    p_vec = e_vec[0]
                    c_vec = e_vec[1]
                    for W_prime in mathcal_H[h - 1][p_vec]:
                        W = self.gen_W_0()
                        for k1, k2 in [
                            (i, j) for i in range(self.k) for j in range(self.k)
                        ]:
                            W[k1][k2] = W_prime[k1][k2] + (
                                0 if c_vec[k1] == c_vec[k2] else 1
                            )
                        mathcal_H[h][q_vec].add(hash(W))
                        if hash(W) not in self.parent[h][q_vec]:
                            self.parent[h][q_vec][hash(W)] = {}
                        self.parent[h][q_vec][hash(W)][p_vec] = W_prime
        return mathcal_H

    def _vertices(self, h: int) -> List[Vertex_H]:
        """パス対グラフ上のh階層目の頂点集合を返す.
        LCSグラフのh階層目の頂点集合の直積集合である．

        Args:
            h (int): 階層

        Returns:
            List[Vertex_H]: h階層目の頂点集合
        """
        prev_v_vec_list = [()]
        for _ in range(self.k):
            v_vec_list = []
            for prev_v_vec in prev_v_vec_list:
                for v in self.leveled_V_G[h]:
                    v_vec_list.append(prev_v_vec + (v,))
            prev_v_vec_list = v_vec_list
        return v_vec_list

    def _in_edges_of(self, U: Vertex_H, h: int) -> List[Edge_H]:
        """U の入辺集合を返す

        Args:
            U (Vertex_H):
            h (int): 頂点 U の属する階層

        Returns:
            List[Edge_H]: Uの入辺集合
        """
        prev_e_vec_list = [((), (), ())]
        for i in range(self.k):
            e_vec_list = []

            in_edges_of_ui = [edge for edge in self.leveled_E_G[h] if edge[2] == U[i]]
            for prev_e_vec in prev_e_vec_list:
                for e in in_edges_of_ui:
                    e_vec_list.append(
                        (
                            prev_e_vec[0] + (e[0],),
                            prev_e_vec[1] + (e[1],),
                            prev_e_vec[2] + (e[2],),
                        )
                    )
            prev_e_vec_list = e_vec_list
        return e_vec_list

    def _compute_diversity_min(self) -> int:
        diversity_min = -float("inf")
        for W in self.mathcal_H[self.ell][self.t_vec]:
            d_min = min(
                [W[i1][i2] for i1 in range(self.k) for i2 in range(self.k) if i1 > i2]
            )
            diversity_min = max(diversity_min, d_min)
        return diversity_min

    def compute_diverse_LCS_set(
        self, min_diversity: int, logging: logging
    ) -> set[set[str]]:
        # 最小ハミング距離が min_diversity のハミング行列のリストを作成
        matrix_set = set()
        for W in self.mathcal_H[self.ell][self.t_vec]:
            d_min = min(
                [W[i1][i2] for i1 in range(self.k) for i2 in range(self.k) if i1 > i2]
            )
            if d_min == min_diversity:
                matrix_set.add(tuple([tuple(W[i]) for i in range(self.k)]))

        logging.debug(f"find all diverse LCSs from matrix list: {pformat(matrix_set)}")
        # ハミング行列のリストから，diverse LCS の集合を構築
        diverse_LCS_set = set()
        for W in matrix_set:
            logging.debug(f"find all diverse LCSs from matrix: {W}")
            self.dfs(self.ell, self.t_vec, W, [], diverse_LCS_set, logging)

        return diverse_LCS_set

    def dfs(
        self, h, q_vec, W, path_label_vec: list[list[str]], output_set, logging=None
    ):
        if logging:
            label_vec = path_label_vec[-1] if path_label_vec else "()"
            logging.debug(f"dfs(h={h}, q_vec={q_vec}, W={W}), label_vec={label_vec}")

        # 頂点 q_vec から親頂点 p_vec への辺のラベルを取得する
        parents = self.parent[h][q_vec][hash(W)]

        # 親が存在しない場合，パスラベル配列を出力集合に追加する
        if not parents:
            labels = [""] * self.k
            for i in range(self.k):
                for c_vec in path_label_vec:
                    labels[i] = c_vec[i] + labels[i]
            if logging:
                logging.debug(f"output: {labels}")
            output_set.add(tuple(labels))
            return

        for p_vec, W_prime in parents.items():
            # 頂点 q_vec から親頂点 p_vec への辺のラベルベクトル c_vec を取得する
            c_vec = ["" for _ in range(self.k)]
            for i in range(self.k):
                p = p_vec[i]
                q = q_vec[i]
                edges = [
                    edge
                    for edge in self.leveled_E_G[h]
                    if edge[0] == p and edge[2] == q
                ]
                if len(edges) != 1:
                    raise Exception("辺の数が1ではありません")
                (_p, c, _p) = edges[0]
                c_vec[i] = c

            # 再帰呼び出し
            self.dfs(
                h - 1, p_vec, W_prime, path_label_vec + [c_vec], output_set, logging
            )
