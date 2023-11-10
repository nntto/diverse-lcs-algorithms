from pprint import pprint
import unittest
from unittest.mock import patch

from path_k_tuple_graph import PathKTupleGraph


class TestPathKTupleGraph(unittest.TestCase):
    def setUp(self):
        self.MockPathKTupleGraph = patch("path_k_tuple_graph.PathKTupleGraph").start()
        self.MockPathKTupleGraph.leveled_V_G = {
            0: [(0, 0)],
            1: [(1, 2), (2, 1)],
            2: [(2, 3), (2, 4), (3, 2)],
            3: [(4, 5), (3, 6)],
            4: [(5, 7)],
        }
        self.MockPathKTupleGraph.leveled_E_G = {
            1: [((0, 0), "A", (1, 2)), ((0, 0), "B", (2, 1))],
            2: [((1, 2), "B", (2, 3)), ((1, 2), "B", (2, 4)), ((2, 1), "A", (3, 2))],
            3: [
                ((2, 3), "C", (4, 5)),
                ((2, 3), "A", (3, 6)),
                ((2, 4), "C", (4, 5)),
                ((2, 4), "A", (3, 6)),
                ((3, 2), "C", (4, 5)),
            ],
            4: [((4, 5), "B", (5, 7)), ((3, 6), "B", (5, 7))],
            5: [],
        }
        self.MockPathKTupleGraph.k = 3

    def test_vertices(self):
        self.MockPathKTupleGraph._vertices = PathKTupleGraph._vertices
        assert (
            len(self.MockPathKTupleGraph._vertices(self.MockPathKTupleGraph, 0))
            == 1**3
        )
        assert (
            len(self.MockPathKTupleGraph._vertices(self.MockPathKTupleGraph, 1))
            == 2**3
        )
        assert (
            len(self.MockPathKTupleGraph._vertices(self.MockPathKTupleGraph, 2))
            == 3**3
        )
        assert (
            len(self.MockPathKTupleGraph._vertices(self.MockPathKTupleGraph, 3))
            == 2**3
        )
        assert (
            len(self.MockPathKTupleGraph._vertices(self.MockPathKTupleGraph, 4))
            == 1**3
        )

    def test_in_edges_of(self):
        self.MockPathKTupleGraph._in_edges_of = PathKTupleGraph._in_edges_of
        assert (
            len(
                self.MockPathKTupleGraph._in_edges_of(
                    self.MockPathKTupleGraph, ((5, 7), (5, 7), (5, 7)), 4
                )
            )
            == 2**3
        )
        assert (
            len(
                self.MockPathKTupleGraph._in_edges_of(
                    self.MockPathKTupleGraph, ((4, 5), (4, 5), (4, 5)), 3
                )
            )
            == 3**3
        )
        assert (
            len(
                self.MockPathKTupleGraph._in_edges_of(
                    self.MockPathKTupleGraph, ((3, 6), (4, 5), (4, 5)), 3
                )
            )
            == 2 * 3 * 3
        )
