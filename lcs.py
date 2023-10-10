from typing import Dict, List, Tuple
import numpy as np

from my_enum import Direction


class LCS:
    # LCSのDPテーブル
    dp_table: np.ndarray
    # (m, n) からトレースを辿る際に，(0, 0)に到達するまでの経路を記録する
    previous_position_dict: Dict[Tuple[int, int], List[Tuple[int, int]]]
    # LCSの長さ
    length: int

    def __init__(self, S: str, T: str) -> None:
        m = len(S) + 1
        n = len(T) + 1

        dp_table = np.zeros((m, n), dtype=int)
        previous_position_dict = {}

        # dpテーブルの上端の行の初期化
        for i in range(0, m):
            dp_table[i, 0] = 0
        # dpテーブルの左端の列の初期化
        for j in range(0, n):
            dp_table[0, j] = 0

        for i in range(1, m):
            for j in range(1, n):
                # 文字が一致した場合，delta = 1
                delta = 1 if S[i - 1] == T[j - 1] else 0

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
        self.length = dp_table[m - 1, n - 1]

