from pprint import pprint
from typing import Any, Dict, Set, Tuple, TypeVar

from tests.fixtures import figure_7_2

T = TypeVar("T") # Generics


def search(position: T, Q:Set[T], E: Set[Tuple[T, Any, T]], reached: Dict[T, bool]):
    """到達可能性を探索する．

    Args:
        position (T): positionから到達可能な頂点を探索する．
        Q (Set[T]): 頂点集合
        E (Set[Tuple[T, any, T]]): 有向辺集合
        reached (Dict[T, bool]): 到達可能な頂点を記録する辞書
    """
    reached[position] = True
    for next_position in [e[2] for e in E if e[0] == position]:
        if next_position not in reached:
            search(next_position, Q, E, reached)

def reachable(Q: Set[T], Delta: Set[Tuple[T, any, T]], X: Set[T]):
    for x in X:
        reached = {}
        search(x, Q, Delta, reached)
    return {p for p in reached.keys() if reached[p]}

def eps_closure(Q:Set[T], Delta: Set[Tuple[T, any, T]], X: Set[T]):
    """NFAから空遷移閉包を求める．

    参考: テキスト「データマイニング」，副手続きEpsClosure
    Args:
        Q (Set[T]): 頂点集合
        Delta (Set[Tuple[T, any, T]]): 有向辺集合
        X (Set[T]): 始点集合

    Returns:
        Set[T]: 空遷移閉包
    """
    Delta_epsilon = {
        (q, a, q_prime) for (q, a, q_prime) in Delta if a == ""
    }

    return reachable(Q, Delta_epsilon, X)

def erase_eps(_Sigma, Q: Set[T], Delta: Set[Tuple[T, any, T]], I: Set[T], F: Set[T]):
    """ 与えられた NFA N = (Σ , Q, ∆, I , F ) から空遷移を除去して，等価な ε-無し NFA M を求める手続き.

    Args:
        _Sigma (_type_): 文字のアルファベット
        Q (Set[T]): 状態集合
        Delta (Set[Tuple[T, any, T]]): 状態遷移関係
        I (Set[T]): 開始状態集合
        F (Set[T]): 受理状態集合

    Returns:
        _type_: _description_
    """
    # 初期化
    Delta_prime = set()
    F_prime = set()

    # 元の NFA N の各状態 p ∈ Q に対して，次のステップをくり返す:
    for p in Q:
        # (1) 状態pから空遷移のみで到達可能な全ての集合EpsClosure_N(p)を求める．
        eps_closure_N_p = eps_closure(Q, Delta, {p})
        # (2) 各状態 r ∈ EpsClosureN ({p}) に対して，N において 
        for r in eps_closure_N_p:
            # r (a)→ q となる全ての状態 q ∈ Q を求めて，それぞれについて次を実行する.
            for (_r, a, q) in [(x_1, a, x_2) for (x_1, a, x_2) in Delta if a != "" and x_1 == r]:
                # (1) 文字遷移 (p, a, q) を状態遷移関係 ∆′ に加える.
                Delta_prime.add((p, a, q))
                # もし状態 q からある受理状態 qf ∈ F へ空遷移閉包で到達可能なら，qをF′ に加える.

                for qf in eps_closure(Q, Delta, {q}):
                    if qf in F:
                        F_prime.add(q)

    return (_Sigma, Q, Delta_prime, I, F_prime)

if __name__=="__main__":
    Q = figure_7_2.V_G
    Delta = {(u[1], figure_7_2.edge_label[u], u[0]) for u in figure_7_2.edge_label}
    pprint(erase_eps("", Q, Delta, {(0, 0)}, {(5, 7)}))



    

# def erapse_eps(sigma: str = "", N: LCSGraph):
#     # 初期化
#     Delta_prime = set()
#     F_prime = set()

#     # NFA Nの各状態pについて繰り返す．
#     for p in N.V_G:
#         if p[1] == 0:
#             F_prime.add(p)
#         else:
#             Delta_prime.add(p)
#     pass
