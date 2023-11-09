from typing import Dict, List, Tuple
from my_enum import Direction
import numpy as np

UP = Direction.UP
LEFT = Direction.LEFT
UPPER_LEFT = Direction.UPPER_LEFT


# テストケース用の例を格納する抽象クラス
class LCSExample:
    X: str
    Y: str
    length: int
    LCS_set: set[str]
    hamming_distance: int
    diverse_LCS_set: set[Tuple[str, str]]


class figure_7_2(LCSExample):
    X = "ABACB"
    Y = "BABBCABX"
    length = 4
    LCS_set = {"ABCB", "BACB", "ABAB"}
    hamming_distance = 3
    diverse_LCS_set = {("BACB", "ABAB"), ("ABAB", "BACB")}


class lastCharIsDifferent(LCSExample):
    X = "ABACB"
    Y = "BABBCAB"
    length = 4
    LCS_set = {"ABCB", "BACB", "ABAB"}
    hamming_distance = 3
    diverse_LCS_set = {("BACB", "ABAB"), ("ABAB", "BACB")}


class SameString(LCSExample):
    X = "ABACB"
    Y = "ABACB"
    length = 5
    LCS_set = {"ABACB"}
    hamming_distance = 0
    diverse_LCS_set = {("ABACB", "ABACB")}


class Subsequence1(LCSExample):
    X = "ABACB"
    Y = "ABA"
    length = 3
    LCS_set = {"ABA"}
    hamming_distance = 0
    diverse_LCS_set = {("ABA", "ABA")}


class Subsequence2(LCSExample):
    X = "ABA"
    Y = "ABACB"
    length = 3
    LCS_set = {"ABA"}
    hamming_distance = 0
    diverse_LCS_set = {("ABA", "ABA")}


class epsilon(LCSExample):
    X = ""
    Y = ""
    length = 0
    LCS_set = {""}
    hamming_distance = 0
    diverse_LCS_set = {("", "")}
