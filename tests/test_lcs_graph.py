import unittest

from lcs_graph import LCSGraph
from my_enum import Direction


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
        S = "ABACB"
        T = "BABBCAB"
        previous_position_dict = {
            (1, 0): [Direction.UP],
            (2, 0): [Direction.UP],
            (3, 0): [Direction.UP],
            (4, 0): [Direction.UP],
            (5, 0): [Direction.UP],
            (0, 1): [Direction.LEFT],
            (0, 2): [Direction.LEFT],
            (0, 3): [Direction.LEFT],
            (0, 4): [Direction.LEFT],
            (0, 5): [Direction.LEFT],
            (0, 6): [Direction.LEFT],
            (0, 7): [Direction.LEFT],
            (1, 1): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (1, 2): [Direction.UPPER_LEFT],
            (1, 3): [Direction.LEFT],
            (1, 4): [Direction.LEFT],
            (1, 5): [Direction.LEFT],
            (1, 6): [Direction.LEFT, Direction.UPPER_LEFT],
            (1, 7): [Direction.LEFT],
            (2, 1): [Direction.UPPER_LEFT],
            (2, 2): [Direction.UP, Direction.LEFT],
            (2, 3): [Direction.UPPER_LEFT],
            (2, 4): [Direction.LEFT, Direction.UPPER_LEFT],
            (2, 5): [Direction.LEFT],
            (2, 6): [Direction.LEFT],
            (2, 7): [Direction.LEFT, Direction.UPPER_LEFT],
            (3, 1): [Direction.UP],
            (3, 2): [Direction.UPPER_LEFT],
            (3, 3): [Direction.UP, Direction.LEFT],
            (3, 4): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (3, 5): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (3, 6): [Direction.UPPER_LEFT],
            (3, 7): [Direction.LEFT],
            (4, 1): [Direction.UP],
            (4, 2): [Direction.UP],
            (4, 3): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (4, 4): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (4, 5): [Direction.UPPER_LEFT],
            (4, 6): [Direction.UP, Direction.LEFT],
            (4, 7): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (5, 1): [Direction.UP, Direction.UPPER_LEFT],
            (5, 2): [Direction.UP],
            (5, 3): [Direction.UPPER_LEFT],
            (5, 4): [Direction.LEFT, Direction.UPPER_LEFT],
            (5, 5): [Direction.UP, Direction.LEFT],
            (5, 6): [Direction.UP, Direction.LEFT, Direction.UPPER_LEFT],
            (5, 7): [Direction.UPPER_LEFT],
        }
        lcs_graph = LCSGraph(previous_position_dict, S, T)

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
