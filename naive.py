import argparse
import logging
from itertools import combinations
from pprint import pformat, pprint

from lcs import LCS
from main import setup_argparse, setup_logging

def compute_lcs_set(lcs: LCS) -> set[str]:
    logging.info(f"LCS computed for strings '{lcs.X}' and '{lcs.Y}'")
    logging.info(f"LCS length = {lcs.length}")
    logging.debug(f"DP table:\n{pformat(lcs.dp_table)}")
    logging.debug(
        f"Previous position dict:\n{pformat({k: [e.name for e in v] for k, v in lcs.previous_position_dict.items()})}"
    )
    lcs_set = lcs.lcs_set()
    logging.info(f"LCS set:\n{pformat(lcs_set)}")
    return lcs_set

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def minimum_hamming_distance(S):
    return min(hamming_distance(s1, s2) for s1, s2 in combinations(S, 2))

def min_diversity_k_string(k, str_set):
    min_diversity = -float("inf")

    for S in combinations(str_set, k):
        if min_diversity <= (diversity := minimum_hamming_distance(S)):
            min_diversity = diversity

    return min_diversity


def main():
    args = setup_argparse()
    setup_logging(args.debug_level)
    
    logging.info(f"Received the following string X: {args.X}")
    logging.info(f"Received the following string Y: {args.Y}")
    logging.info(f"Received the following value of k: {args.k}")

    lcs = LCS(args.X, args.Y)
    print(f"lcs_length = {lcs.length}")
    lcs_set = compute_lcs_set(lcs)
    print(f"lcs_count = {len(lcs_set)}")
    
    min_diversity = min_diversity_k_string(args.k, lcs_set)
    logging.info(f"Minimum diversity: {min_diversity}")
    print(f"min_diversity = {min_diversity}")

if __name__ == "__main__":
    main()
