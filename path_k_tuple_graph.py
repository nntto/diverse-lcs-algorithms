from itertools import combinations, combinations_with_replacement
from pprint import pprint
from typing import Dict, List, Tuple

from custom_types import Edge_G, Edge_H, Vertex_G, Vertex_H


class PathKTupleGraph:
    s_vec: Vertex_H  # パス対グラフの入口
    t_vec: Vertex_H  # パス対グラフの出口
    k: int  # diverse LCS を構成するLCSの本数
    ell: int  # LCS グラフの階層数
    mathcal_H: Dict[int, Dict[Vertex_H, int]]  # mutual hamming weight matrix
    Diversity_min: int  # diverse LCS の最小ハミング距離
    # パスラベルを取ると，diverse LCS となるk本のLCSが得られる．

    # diverse LCS 集合
    diverse_LCS_set: set[Tuple[str, str]]

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

        for h in range(1, self.ell + 1):
            mathcal_H[h] = {}
            for q_vec in self._vertices(h):
                mathcal_H[h][q_vec] = []
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
                        mathcal_H[h][q_vec].append(W)
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

    def _compute_diversity_min(self):
        diversity_min = -float("inf")
        for W in self.mathcal_H[self.ell][self.t_vec]:
            d_min = min(
                [W[i1][i2] for i1 in range(self.k) for i2 in range(self.k) if i1 > i2]
            )
            diversity_min = max(diversity_min, d_min)
        return diversity_min
