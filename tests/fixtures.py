from typing import Dict, List, Tuple
from my_enum import Direction
import numpy as np

UP = Direction.UP
LEFT = Direction.LEFT
UPPER_LEFT = Direction.UPPER_LEFT

class figure_7_2():
    X = "ABACB"
    Y = "BABBCAB"
    length = 4
    dp_table = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 2, 2, 2, 2, 2],
            [0, 1, 2, 2, 2, 2, 3, 3],
            [0, 1, 2, 2, 2, 3, 3, 3],
            [0, 1, 2, 3, 3, 3, 3, 4],
        ]
    )
    previous_position_dict = {
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
    }
    V_G = [
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
    ]
    E_G = {
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
    }
    edge_label = {
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
    }

class SameString():
    X = "ABACB"
    Y = "ABACB"
    length = 5
    dp_table = np.array(
        [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 2, 2, 2, 2],
            [0, 1, 2, 3, 3, 3],
            [0, 1, 2, 3, 4, 4],
            [0, 1, 2, 3, 4, 5],
        ]
    )
    previous_position_dict = {
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
    }

class Subsequence1:
    X = "ABACB"
    Y = "ABA"
    length = 3
    dp_table = np.array(
        [
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 2, 2],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
        ]
    )
    previous_position_dict = {
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
    }

class Subsequence2:
    X = "ABA"
    Y = "ABACB"
    length = 3
    dp_table = np.array(
        [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 2, 2, 2, 2],
            [0, 1, 2, 3, 3, 3],
        ]
    )
    previous_position_dict = {
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
    }