from typing import Tuple, TypeVar


Vertex_G = TypeVar("Vertex_G") # LCS グラフの頂点の型
Character = TypeVar("Character") # 文字の型
Edge_G = Tuple[Vertex_G, Character, Vertex_G] # LCS グラフの辺の型

Vertex_H = Tuple[Vertex_G, Vertex_G] # パス対グラフの頂点の型
Edge_H = Tuple[Vertex_H, Tuple[Character, Character], Vertex_H] # パス対グラフの辺の型


