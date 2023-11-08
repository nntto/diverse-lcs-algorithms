from pprint import pprint
from typing import Dict, List, Tuple


class DiverseLCSGraph:
    hamming_distance: int
    leveled_V_G: Dict[int, List[Tuple[int, int]]]
    leveled_E_G: Dict[int, List[Tuple[Tuple[int, int], str, List[Tuple[int, int]]]]]
    V_H: List[Tuple[Tuple[int, int], Tuple[int, int]]]  # diverse LCSのパス対グラフの頂点集合
    E_H: List[  # diverse LCSのパス対グラフの辺集合
        Tuple[
            Tuple[Tuple[int, int], Tuple[int, int]],  # LCSグラフの頂点対
            Tuple[str, str],  # 辺ラベルの対
            Tuple[Tuple[int, int], Tuple[int, int]],  # LCSグラフの頂点対
        ]
    ]
    L: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]  # diverse LCSのハミング距離
    # パスラベルを取ると，diverse LCS となる2本のLCSが得られる．

    def __init__(
        self,
        leveled_V_G: Dict[int, List[Tuple[int, int]]],
        leveled_E_G: Dict[
            int, List[Tuple[Tuple[int, int], str, List[Tuple[int, int]]]]
        ],
    ) -> None:
        s = leveled_V_G[0][0]  # 始点．V_G_0は始点のみからなる頂点集合
        t = leveled_V_G[len(leveled_V_G) - 1][0]  # 終点．V_G_ellは終点のみからなる頂点集合

        self.leveled_E_G = leveled_E_G
        self.leveled_V_G = leveled_V_G

        self.L = self.DP((s, s))
        self.hamming_distance = self.L[(t, t)]

    def DP(self, S: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        """動的計画法でdiverse LCSのハミング距離を計算する．
        同時に，diverse LCSのパス対グラフを構築する．
        """
        L = {}
        L[S] = 0  # 基底ケース

        self.V_H = []
        self.E_H = []

        for h in range(1, len(self.leveled_V_G)):
            for u1 in self.leveled_V_G[h]:
                for u2 in self.leveled_V_G[h]:
                    L[(u1, u2)] = 0
                    # 先端が u1, u2 である辺を列挙
                    for edge1 in [e for e in self.leveled_E_G[h] if e[2] == u1]:
                        for edge2 in [e for e in self.leveled_E_G[h] if e[2] == u2]:
                            v1 = edge1[0]
                            v2 = edge2[0]
                            delta = 0 if edge1[1] == edge2[1] else 1
                            L[(u1, u2)] = max(L[(u1, u2)], L[(v1, v2)] + delta)

                    # パス対グラフを構築
                    for edge1 in [e for e in self.leveled_E_G[h] if e[2] == u1]:
                        for edge2 in [e for e in self.leveled_E_G[h] if e[2] == u2]:
                            v1 = edge1[0]
                            v2 = edge2[0]
                            delta = 0 if edge1[1] == edge2[1] else 1

                            if L[(v1, v2)] + delta == L[(u1, u2)]:
                                if (u1, u2) not in self.V_H:
                                    self.V_H.append((u1, u2))
                                self.E_H.append(
                                    ((v1, v2), (edge1[1], edge2[1]), (u1, u2))
                                )

        return L
