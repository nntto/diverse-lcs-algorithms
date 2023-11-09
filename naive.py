from itertools import combinations


def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def minimum_hamming_distance(S):
    return min(hamming_distance(s1, s2) for s1, s2 in combinations(S, 2))


def min_diversity_k_string(k, str_set):
    min_diversity = -float("inf")
    min_diversity_set = set()

    for S in combinations(str_set, k):
        if min_diversity < (diversity := minimum_hamming_distance(S)):
            min_diversity = diversity
            min_diversity_set = S

    return min_diversity, min_diversity_set


if __name__ == "__main__":
    LCS_set = {
        "BACBAACXY",
        "ABABAACYY",
        "ABCBAACYY",
        "ABABAACXY",
        "BACBAACYY",
        "ABCBAACXY",
    }

    k = 3

    print(min_diversity_k_string(k, LCS_set))

    LCS_set = {"ABCB", "BACB", "ABAB"}
    k = 3
    print(min_diversity_k_string(k, LCS_set))
    k = 2
    print(min_diversity_k_string(k, LCS_set))
