import unittest
import numpy as np
from numpy.testing import assert_array_equal

from lcs import LCS
from my_enum import Direction
from tests.fixtures import SameString, Subsequence1, Subsequence2, figure_7_2
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
        lcs = LCS(figure_7_2.X, figure_7_2.Y)
        self.assertEqual(
            figure_7_2.length, lcs.length,
        )
        assert_array_equal_with_diff(
            figure_7_2.dp_table,
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            figure_7_2.previous_position_dict,
            lcs.previous_position_dict,
        )

    def test_lcs_between_same_string(self):
        self.maxDiff = None  # diff出力の文字数制限を解除
        lcs = LCS(SameString.X, SameString.Y)
        self.assertEqual(SameString.length, lcs.length)
        assert_array_equal_with_diff(
            SameString.dp_table,
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            SameString.previous_position_dict,
            lcs.previous_position_dict,
        )

    def test_lcs_between_subsequence1(self):
        lcs = LCS(Subsequence1.X, Subsequence1.Y)
        self.assertEqual(Subsequence1.length, lcs.length)
        assert_array_equal_with_diff(
            Subsequence1.dp_table,
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            Subsequence1.previous_position_dict,
            lcs.previous_position_dict,
        )

    def test_lcs_between_subsequence2(self):
        lcs = LCS(Subsequence2.X, Subsequence2.Y)
        self.assertEqual(Subsequence2.length, lcs.length)
        assert_array_equal_with_diff(
            Subsequence2.dp_table,
            lcs.dp_table,
        )
        self.assert_previous_position_dict_equal_with_diff(
            Subsequence2.previous_position_dict,
            lcs.previous_position_dict,
        )

    def assert_previous_position_dict_equal_with_diff(self, expected, actual):
        # 移動前の位置を比較する辞書の同一性を確認する
        actual_names = {k: [e.name for e in v] for k, v in actual.items()}
        expected_names = {k: [e.name for e in v] for k, v in expected.items()}
        self.assertEqual(expected_names, actual_names)


if __name__ == "__main__":
    unittest.main()
