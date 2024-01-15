from typing import Dict, List
from custom_types import Vertex_G
import numpy as np

from my_enum import Direction


class LCS:
    # LCSのDPテーブル
    dp_table: np.ndarray
    # (m, n) からトレースを辿る際に，(0, 0)に到達するまでの経路を記録する
    previous_position_dict: Dict[Vertex_G, List[Direction]]
    # LCSの長さ
    length: int

    m: int
    n: int
    X: str
    Y: str

    def __init__(self, X: str, Y: str) -> None:
        m = len(X)
        n = len(Y)
        self.m = m
        self.n = n
        self.X = X
        self.Y = Y

        dp_table = np.zeros((m + 1, n + 1), dtype=int)
        previous_position_dict = {}

        # dpテーブルの上端の行の初期化
        for i in range(0, m + 1):
            dp_table[i, 0] = 0
            if i != 0:
                previous_position_dict[(i, 0)] = [Direction.UP]
        # dpテーブルの左端の列の初期化
        for j in range(0, n + 1):
            dp_table[0, j] = 0
            if j != 0:
                previous_position_dict[(0, j)] = [Direction.LEFT]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # 文字が一致した場合，delta = 1
                delta = 1 if X[i - 1] == Y[j - 1] else 0

                # dpテーブルの更新
                dp_table[i, j] = max(
                    dp_table[i - 1, j],  # 上からの更新
                    dp_table[i, j - 1],  # 左からの更新
                    dp_table[i - 1, j - 1] + delta,  # 左上からの更新
                )

                # dpテーブルの更新に伴い，次の位置を記録する
                previous_position_dict[(i, j)] = []
                if dp_table[i, j] == dp_table[i - 1, j]:
                    previous_position_dict[(i, j)].append(Direction.UP)
                if dp_table[i, j] == dp_table[i, j - 1]:
                    previous_position_dict[(i, j)].append(Direction.LEFT)
                if dp_table[i, j] == dp_table[i - 1, j - 1] + delta:
                    previous_position_dict[(i, j)].append(Direction.UPPER_LEFT)

        self.dp_table = dp_table
        self.previous_position_dict = previous_position_dict
        self.length = dp_table[m, n]
    
    def lcs_set(self) -> set[str]:
        """LCS集合を返す"""
        lcs_set = set()
        self._trace_lcs(self.m, self.n, "", lcs_set)
        return lcs_set
    
    def _trace_lcs(self, i: int, j: int, lcs: str, lcs_set: set[str]) -> None:
        """(i, j)からトレースを辿り，LCS集合を求める"""
        if i == 0 or j == 0:
            lcs_set.add(lcs[::-1])
            return
        
        for direction in self.previous_position_dict[(i, j)]:
            if direction == Direction.UP:
                self._trace_lcs(i - 1, j, lcs, lcs_set)
            elif direction == Direction.LEFT:
                self._trace_lcs(i, j - 1, lcs, lcs_set)
            elif direction == Direction.UPPER_LEFT:
                if self.X[i - 1] != self.Y[j - 1]:
                    # 文字が一致しない場合はスキップ
                    continue
                else:
                    self._trace_lcs(i - 1, j - 1, lcs + self.X[i - 1], lcs_set)
            else:
                raise ValueError(f"Invalid direction: {direction}")
        

