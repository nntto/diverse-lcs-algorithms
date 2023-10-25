import unittest

from lcs_graph import LCSGraph
from my_enum import Direction
from tests.fixtures import figure_7_2


class TestLCSGraph(unittest.TestCase):
    def test_empty_strings(self):
        S = ""
        T = ""
        previous_position_dict = {}

        lcs_graph = LCSGraph(previous_position_dict, S, T)
        self.assertEqual([(0, 0)], lcs_graph.V_G)
        self.assertEqual({(0, 0): []}, lcs_graph.E_G)
        self.assertEqual({}, lcs_graph.edge_label)

    def test_lcs_figure_7_2(self):
        self.maxDiff = None  # diff出力の文字数制限を解除
        S = figure_7_2.X
        T = figure_7_2.Y
        lcs_graph = LCSGraph(figure_7_2.previous_position_dict, S, T)

        self.assertEqual(
            figure_7_2.V_G,
            lcs_graph.V_G,
        )
        self.assertEqual(
            figure_7_2.E_G,
            lcs_graph.E_G,
        )
        self.assertEqual(
            figure_7_2.edge_label,
            lcs_graph.edge_label,
        )


if __name__ == "__main__":
    unittest.main()
