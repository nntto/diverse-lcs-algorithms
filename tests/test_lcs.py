import unittest
import numpy as np
from numpy.testing import assert_array_equal

from lcs import LCS
from my_enum import Direction
from utils import print_array_diff

UP = Direction.UP
LEFT = Direction.LEFT
UPPER_LEFT = Direction.UPPER_LEFT

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
        self.assertEqual(0, lcs.length)
        assert_array_equal_with_diff(np.zeros((1, 1)), lcs.dp_table)
        self.assertEqual({}, lcs.previous_position_dict)

    def test_lcs_figure_7_2(self):
        self.maxDiff = None  # diff出力の文字数制限を解除
        lcs = LCS("ABACB", "BABBCAB")
        self.assertEqual(
            4, lcs.length,
        )
        assert_array_equal_with_diff(
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
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            {
                (0, 1): [LEFT],
                (0, 2): [LEFT],
                (0, 3): [LEFT],
                (0, 4): [LEFT],
                (0, 5): [LEFT],
                (0, 6): [LEFT],
                (0, 7): [LEFT],
                (1, 0): [UP],
                (1, 1): [UP, LEFT, UPPER_LEFT],
                (1, 2): [UPPER_LEFT],
                (1, 3): [LEFT],
                (1, 4): [LEFT],
                (1, 5): [LEFT],
                (1, 6): [LEFT, UPPER_LEFT],
                (1, 7): [LEFT],
                (2, 0): [UP],
                (2, 1): [UPPER_LEFT],
                (2, 2): [UP, LEFT],
                (2, 3): [UPPER_LEFT],
                (2, 4): [LEFT, UPPER_LEFT],
                (2, 5): [LEFT],
                (2, 6): [LEFT],
                (2, 7): [LEFT, UPPER_LEFT],
                (3, 0): [UP],
                (3, 1): [UP],
                (3, 2): [UPPER_LEFT],
                (3, 3): [UP, LEFT],
                (3, 4): [UP, LEFT, UPPER_LEFT],
                (3, 5): [UP, LEFT, UPPER_LEFT],
                (3, 6): [UPPER_LEFT],
                (3, 7): [LEFT],
                (4, 0): [UP],
                (4, 1): [UP],
                (4, 2): [UP],
                (4, 3): [UP, LEFT, UPPER_LEFT],
                (4, 4): [UP, LEFT, UPPER_LEFT],
                (4, 5): [UPPER_LEFT],
                (4, 6): [UP, LEFT],
                (4, 7): [UP, LEFT, UPPER_LEFT],
                (5, 0): [UP],
                (5, 1): [UP, UPPER_LEFT],
                (5, 2): [UP],
                (5, 3): [UPPER_LEFT],
                (5, 4): [LEFT, UPPER_LEFT],
                (5, 5): [UP, LEFT],
                (5, 6): [UP, LEFT, UPPER_LEFT],
                (5, 7): [UPPER_LEFT],
            },
            lcs.previous_position_dict,
        )

    def test_lcs_between_same_string(self):
        self.maxDiff = None  # diff出力の文字数制限を解除
        lcs = LCS("ABACB", "ABACB")
        self.assertEqual(5, lcs.length)
        assert_array_equal_with_diff(
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
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            {
                (0, 1): [LEFT],
                (0, 2): [LEFT],
                (0, 3): [LEFT],
                (0, 4): [LEFT],
                (0, 5): [LEFT],
                (1, 0): [UP],
                (1, 1): [UPPER_LEFT],
                (1, 2): [LEFT],
                (1, 3): [LEFT, UPPER_LEFT],
                (1, 4): [LEFT],
                (1, 5): [LEFT],
                (2, 0): [UP],
                (2, 1): [UP],
                (2, 2): [UPPER_LEFT],
                (2, 3): [LEFT],
                (2, 4): [LEFT],
                (2, 5): [LEFT, UPPER_LEFT],
                (3, 0): [UP],
                (3, 1): [UP, UPPER_LEFT],
                (3, 2): [UP],
                (3, 3): [UPPER_LEFT],
                (3, 4): [LEFT],
                (3, 5): [LEFT],
                (4, 0): [UP],
                (4, 1): [UP],
                (4, 2): [UP],
                (4, 3): [UP],
                (4, 4): [UPPER_LEFT],
                (4, 5): [LEFT],
                (5, 0): [UP],
                (5, 1): [UP],
                (5, 2): [UP, UPPER_LEFT],
                (5, 3): [UP],
                (5, 4): [UP],
                (5, 5): [UPPER_LEFT],
            },
            lcs.previous_position_dict,
        )

    def test_lcs_between_subsequence1(self):
        lcs = LCS("ABACB", "ABA")
        self.assertEqual(3, lcs.length)
        assert_array_equal_with_diff(
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
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            {
                (0, 1): [LEFT],
                (0, 2): [LEFT],
                (0, 3): [LEFT],
                (1, 0): [UP],
                (1, 1): [UPPER_LEFT],
                (1, 2): [LEFT],
                (1, 3): [LEFT, UPPER_LEFT],
                (2, 0): [UP],
                (2, 1): [UP],
                (2, 2): [UPPER_LEFT],
                (2, 3): [LEFT],
                (3, 0): [UP],
                (3, 1): [UP, UPPER_LEFT],
                (3, 2): [UP],
                (3, 3): [UPPER_LEFT],
                (4, 0): [UP],
                (4, 1): [UP],
                (4, 2): [UP],
                (4, 3): [UP],
                (5, 0): [UP],
                (5, 1): [UP],
                (5, 2): [UP, UPPER_LEFT],
                (5, 3): [UP],
            },
            lcs.previous_position_dict,
        )

    def test_lcs_between_subsequence2(self):
        lcs = LCS("ABA", "ABACB")
        self.assertEqual(3, lcs.length)
        assert_array_equal_with_diff(
            np.array(
                [
                    [0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1],
                    [0, 1, 2, 2, 2, 2],
                    [0, 1, 2, 3, 3, 3],
                ]
            ),
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            {
                (0, 1): [LEFT],
                (0, 2): [LEFT],
                (0, 3): [LEFT],
                (0, 4): [LEFT],
                (0, 5): [LEFT],
                (1, 0): [UP],
                (1, 1): [UPPER_LEFT],
                (1, 2): [LEFT],
                (1, 3): [LEFT, UPPER_LEFT],
                (1, 4): [LEFT],
                (1, 5): [LEFT],
                (2, 0): [UP],
                (2, 1): [UP],
                (2, 2): [UPPER_LEFT],
                (2, 3): [LEFT],
                (2, 4): [LEFT],
                (2, 5): [LEFT, UPPER_LEFT],
                (3, 0): [UP],
                (3, 1): [UP, UPPER_LEFT],
                (3, 2): [UP],
                (3, 3): [UPPER_LEFT],
                (3, 4): [LEFT],
                (3, 5): [LEFT],
            },
            lcs.previous_position_dict,
        )

    def assert_previous_position_dict_equal_with_diff(self, expected, actual):
        # 移動前の位置を比較する辞書の同一性を確認する
        actual_names = {k: [e.name for e in v] for k, v in actual.items()}
        expected_names = {k: [e.name for e in v] for k, v in expected.items()}
        self.assertEqual(expected_names, actual_names)


if __name__ == "__main__":
    unittest.main()
