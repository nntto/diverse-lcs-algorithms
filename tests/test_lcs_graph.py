import json
import unittest
import numpy as np
from numpy.testing import assert_array_equal

from lcs import LCS
from lcs_graph import LCSGraph


class TestLCSGraph(unittest.TestCase):
    def test_empty_strings(self):
        S = ""
        T = ""
        lcs = LCS(S, T)

        lcs_graph = LCSGraph(lcs.previous_position_dict, S, T)
        self.assertEqual([(0, 0)], lcs_graph.V_G)
        self.assertEqual({(0, 0): []}, lcs_graph.E_G)
        self.assertEqual({}, lcs_graph.edge_label)

    def test_lcs_figure_7_2(self):
        self.maxDiff = None  # diff出力の文字数制限を解除
        S = "ABACB"
        T = "BABBCAB"
        lcs = LCS(S, T)

        lcs_graph = LCSGraph(lcs.previous_position_dict, S, T)

        self.assertEqual(
            [
                (5, 7),
                (4, 6),
                (3, 6),
                (2, 5),
                (2, 4),
                (2, 3),
                (1, 2),
                (0, 1),
                (0, 0),
                (1, 3),
                (4, 5),
                (3, 4),
                (3, 3),
                (3, 2),
                (2, 1),
                (1, 0),
            ],
            lcs_graph.V_G,
        )
        self.assertEqual(16, len(lcs_graph.V_G))
        self.assertEqual(
            {
                (0, 0): [],
                (0, 1): [(0, 0)],
                (1, 0): [(0, 0)],
                (1, 2): [(0, 1)],
                (1, 3): [(1, 2)],
                (2, 1): [(1, 0)],
                (2, 3): [(1, 2)],
                (2, 4): [(2, 3), (1, 3)],
                (2, 5): [(2, 4)],
                (3, 2): [(2, 1)],
                (3, 3): [(2, 3), (3, 2)],
                (3, 4): [(2, 4), (3, 3), (2, 3)],
                (3, 6): [(2, 5)],
                (4, 5): [(3, 4)],
                (4, 6): [(3, 6), (4, 5)],
                (5, 7): [(4, 6)],
            },
            lcs_graph.E_G,
        )
        self.assertEqual(
            {
                ((0, 1), (0, 0)): "",
                ((1, 0), (0, 0)): "",
                ((1, 2), (0, 1)): "A",
                ((1, 3), (1, 2)): "",
                ((2, 1), (1, 0)): "B",
                ((2, 3), (1, 2)): "B",
                ((2, 4), (1, 3)): "B",
                ((2, 4), (2, 3)): "",
                ((2, 5), (2, 4)): "",
                ((3, 2), (2, 1)): "A",
                ((3, 3), (2, 3)): "",
                ((3, 3), (3, 2)): "",
                ((3, 4), (2, 3)): "",
                ((3, 4), (2, 4)): "",
                ((3, 4), (3, 3)): "",
                ((3, 6), (2, 5)): "A",
                ((4, 5), (3, 4)): "C",
                ((4, 6), (3, 6)): "",
                ((4, 6), (4, 5)): "",
                ((5, 7), (4, 6)): "B",
            },
            lcs_graph.edge_label,
        )


if __name__ == "__main__":
    unittest.main()
