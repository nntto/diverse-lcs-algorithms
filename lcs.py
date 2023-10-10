from typing import Dict, List, Tuple
import numpy as np


class LCS:
    # LCSのDPテーブル
    dp_table: np.ndarray
    # LCSの長さ
    length: int

    def __init__(self, S: str, T: str) -> None:
        m = len(S) + 1
        n = len(T) + 1

        dp_table = np.zeros((m, n), dtype=int)

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


        self.dp_table = dp_table
        self.length = dp_table[m - 1, n - 1]

