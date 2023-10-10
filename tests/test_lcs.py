import unittest
import numpy as np
from numpy.testing import assert_array_equal

from lcs import LCS
from utils import print_array_diff

# 配列の一致を確認するための関数
# 配列が一致しない場合，どの要素が異なるかを表示する
def assert_array_equal_with_diff(expected, actual):
    try:
        assert_array_equal(expected, actual)
    except AssertionError:
        print_array_diff(expected, actual)
        raise


class TestLCS(unittest.TestCase):
    def test_empty_strings(self):
        lcs = LCS("", "")
        self.assertEqual(lcs.length, 0)
        assert_array_equal_with_diff(lcs.dp_table, np.zeros((1, 1)))

    def test_lcs_figure_7_2(self):
        self.maxDiff = None  # diff出力の文字数制限を解除
        lcs = LCS("ABACB", "BABBCAB")
        self.assertEqual(lcs.length, 4)
        assert_array_equal_with_diff(
            lcs.dp_table,
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1],
                    [0, 1, 1, 2, 2, 2, 2, 2],
                    [0, 1, 2, 2, 2, 2, 3, 3],
                    [0, 1, 2, 2, 2, 3, 3, 3],
                    [0, 1, 2, 3, 3, 3, 3, 4],
                ]
            ),
        )

    def test_lcs_between_same_string(self):
        lcs = LCS("ABACB", "ABACB")
        self.assertEqual(lcs.length, 5)
        assert_array_equal_with_diff(
            lcs.dp_table,
            np.array(
                [
                    [0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1],
                    [0, 1, 2, 2, 2, 2],
                    [0, 1, 2, 3, 3, 3],
                    [0, 1, 2, 3, 4, 4],
                    [0, 1, 2, 3, 4, 5],
                ]
            ),
        )

    def test_lcs_between_subsequence1(self):
        lcs = LCS("ABACB", "ABA")
        self.assertEqual(lcs.length, 3)
        assert_array_equal_with_diff(
            lcs.dp_table,
            np.array(
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 1],
                    [0, 1, 2, 2],
                    [0, 1, 2, 3],
                    [0, 1, 2, 3],
                    [0, 1, 2, 3],
                ]
            ),
        )

    def test_lcs_between_subsequence2(self):
        lcs = LCS("ABA", "ABACB")
        self.assertEqual(lcs.length, 3)
        assert_array_equal_with_diff(
            lcs.dp_table,
            np.array(
                [
                    [0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1],
                    [0, 1, 2, 2, 2, 2],
                    [0, 1, 2, 3, 3, 3],
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
