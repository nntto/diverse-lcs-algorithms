import unittest
from main import compute_lcs, compute_lcs_graph, compute_path_tuple_graph
from tests.fixtures import (
    LCSExample,
    SameString,
    Subsequence1,
    Subsequence2,
    epsilon,
    figure_7_2,
    lastCharIsDifferent,
)


class LCSTestCases(unittest.TestCase):
    def check_lcs_scenario(self, case_class: LCSExample):
        lcs = compute_lcs(case_class.X, case_class.Y)
        lcs_graph = compute_lcs_graph(lcs, case_class.X, case_class.Y)
        lcs_path_tuple_graph = compute_path_tuple_graph(lcs_graph)

        self.assertEqual(lcs.length, case_class.length)
        self.assertEqual(lcs_graph.LCS_set, case_class.LCS_set)
        self.assertEqual(
            lcs_path_tuple_graph.hamming_distance, case_class.hamming_distance
        )
        self.assertEqual(
            lcs_path_tuple_graph.diverse_LCS_set, case_class.diverse_LCS_set
        )

    def test_figure_7_2(self):
        self.check_lcs_scenario(figure_7_2)

    def test_last_char_is_different(self):
        self.check_lcs_scenario(lastCharIsDifferent)

    def test_same_string(self):
        self.check_lcs_scenario(SameString)

    def test_subsequence_1(self):
        self.check_lcs_scenario(Subsequence1)

    def test_subsequence_2(self):
        self.check_lcs_scenario(Subsequence2)

    def test_epsilon(self):
        self.check_lcs_scenario(epsilon)


if __name__ == "__main__":
    unittest.main()
