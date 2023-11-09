from typing import Dict, List, Tuple

from custom_types import Edge_G, Edge_H, Vertex_G, Vertex_H


class PathTupleGraph:
    hamming_distance: int
    leveled_V_G: Dict[int, List[Vertex_G]]
    leveled_E_G: Dict[int, List[Edge_G]]
    V_H: List[Vertex_H]  # diverse LCS の頂点集合
    E_H: List[Edge_H]  # diverse LCS の辺集合
    L: Dict[Vertex_H, int]  # Sから各頂点までの最大距離積パスのハミング距離を格納するDPテーブル
    # パスラベルを取ると，diverse LCS となる2本のLCSが得られる．

    def __init__(
        self,
        leveled_V_G: Dict[int, List[Vertex_G]],
        leveled_E_G: Dict[int, List[Edge_G]],
    ) -> None:
        self.leveled_V_G = leveled_V_G
        self.leveled_E_G = leveled_E_G
        self._initialize_graph()

    def _initialize_graph(self) -> None:
        s = self.leveled_V_G[0][0]  # LCS グラフの入口
        t = self.leveled_V_G[max(self.leveled_V_G)][0]  # LCS グラフの出口
        S, T = (s, s), (t, t)  # diverse LCS のパス対グラフの始点と終点

        self.V_H, self.E_H, self.L = self._compute_dp(S)
        self.hamming_distance = self.L[T]

    def _compute_dp(
        self, S: Vertex_H
    ) -> Tuple[List[Vertex_H], List[Edge_H], Dict[Vertex_G, int],]:
        L = {S: 0}  # Base case
        V_H = [S]
        E_H = []

        for h in range(1, len(self.leveled_V_G)):
            for U in self._vertices(h):
                # S から U までの最大距離積パスのハミング距離を計算する
                max_dist = self._max_product_path_dist(U, L, h)
                L[U] = max_dist

                V_H.append(U)
                self._update_E_H(U, L, E_H, h)

        return V_H, E_H, L

    def _vertices(self, h: int) -> List[Vertex_H]:
        """パス対グラフ上のh階層目の頂点集合を返す

        Args:
            h (int): 階層

        Returns:
            List[Vertex_H]: h階層目の頂点集合
        """
        return [(u1, u2) for u1 in self.leveled_V_G[h] for u2 in self.leveled_V_G[h]]

    def _max_product_path_dist(
        self,
        U: Vertex_H,
        L: Dict[Vertex_H, int],
        h: int,
    ) -> int:
        """パス対グラフ上の頂点 S から頂点 U までの最大距離積パスのハミング距離を返す

        Args:
            U (Vertex_H): 頂点
            L (Dict[Vertex_H, int]): DPテーブル
            h (int): 頂点 U の属する

        Returns:
            int: S から U までの最大距離積パスのハミング距離
        """
        max_length = 0
        for Edge in self._in_edges_of(U, h):
            V = Edge[0]
            c1, c2 = Edge[1]
            delta = 0 if c1 == c2 else 1
            max_length = max(max_length, L[V] + delta)
        return max_length

    def _in_edges_of(self, U: Vertex_H, h: int) -> List[Edge_H]:
        """U の入辺集合を返す

        Args:
            U (Vertex_H): _description_
            h (int): 頂点 U の属する階層

        Returns:
            List[Edge_H]: Uの入辺集合
        """
        return [
            ((v1, v2), (c1, c2), U)
            for v1, c1, u1 in self.leveled_E_G[h]
            if u1 == U[0]
            for v2, c2, u2 in self.leveled_E_G[h]
            if u2 == U[1]
        ]

    def _update_E_H(
        self, U: Vertex_H, L: Dict[Vertex_H, int], E_H: List[Edge_H], h: int
    ) -> None:
        for Edge in self._in_edges_of(U, h):
            V = Edge[0]
            c1, c2 = Edge[1]

            delta = 0 if c1 == c2 else 1
            if L[V] + delta == L[U]:
                E_H.append((V, (c1, c2), U))
