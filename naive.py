import argparse
import logging
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

def setup_argparse():
    parser = argparse.ArgumentParser(description="Calculate k-diverse string sets and their minimum Hamming distance.")
    parser.add_argument('str_set', nargs='+', type=str, help="Set of strings to consider for k-diverse calculations")
    parser.add_argument('k', type=int, help="Value of k for k-diverse calculation")
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    args = setup_argparse()
    setup_logging()
    
    logging.info(f"Received the following string set: {args.str_set}")
    logging.info(f"Received the following value of k: {args.k}")
    
    min_diversity, min_diversity_set = min_diversity_k_string(args.k, args.str_set)
    logging.info(f"Minimum diversity: {min_diversity}")
    logging.info(f"Minimum diversity set: {min_diversity_set}")

if __name__ == "__main__":
    main()
