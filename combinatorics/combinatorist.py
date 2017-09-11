#!/usr/bin/env python

"""Combinatorial computations of interest.
"""

import argparse
import math

from algorithms.ds.fenwick import Fenwick
from algorithms.search.binary_search import binary_search


def parse_args():
    """Parse command line arguments.

    Returns:
      args from the argparse module
    """
    usage = """Various combinatorial computations of interest. """
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument(
        '-n', default=10, type=int,
        help='Working on the set [0..n).')
    parser.add_argument(
        '-k', default=3, type=int,
        help='Working with combinatorial objects of size k.')
    return parser.parse_args()


class Combinatorist(object):

    def __init__(self, args):
        """Initialize with commandline arguments.

        Args:
          args: command-line arguments from argparse.
        """
        self.args = args
        self.binom = self._binom()

    def _binom(self):
        """Compute binom(m, i) for 0 <= m <= n and 0 <= i <= k.

        Complexity O(k*n^2).
        Length of binomial coefficients is O(n).

        Returns:
          (n+1)x(k+1) list with binom coefficients.
        """
        binom = [
            [0 for i in range(self.args.k + 1)] for i in range(self.args.n + 1)
        ]
        binom[0][0] = 1
        for i in range(1, self.args.n + 1):
            binom[i][0] = 1
            for j in range(1, min(i, self.args.k) + 1):
                binom[i][j] = binom[i - 1][j - 1] + binom[i - 1][j]
        return binom

    def encode_combination(self, combination):
        """Encode a combination in the combinatorial number system.

        Complexity O(k*n) where k is the length of the combination.
        Length of the binomial coefficients is O(n).

        Args:
          combination: list/tuple, elements are in [0,n), size is k.
        Returns:
          int, 0 <= ret < binom(n, k)
        """
        combination_set = sorted(set(combination))
        ret = 0
        for i, e in enumerate(combination_set):
            ret += self.binom[e][i + 1]
        return ret

    def decode_combination(self, enc):
        """Decode an integer to its combination.

        Complexity O(k*log(n)*n).
        The length of the binomial coefficients is O(n).

        Args:
          enc: int, non-negative, the encoding of a combination.
        Returns:
          list, the decoded combination
        """
        ret = []
        for k in range(self.args.k - 1, -1, -1):
            # Predicate depends on enc and k.
            def pred(mid):
                if enc < self.binom[mid][k + 1]:
                    return True
                else:
                    return enc < self.binom[mid + 1][k + 1]
            lo = k
            hi = self.args.n - self.args.k + k
            e = binary_search(lo, hi, pred)
            enc -= self.binom[e][k + 1]
            ret.append(e)
        return list(reversed(ret))

    @staticmethod
    def factorial(n):
        """Compute n!.

        Complexity O(n^2 log^2(n)). Omega(n^2 log(n)).
        Naive algorithm.

        Args:
          n: int, non-negative.

        Return:
          int, n!
        """
        fact = 1
        for i in range(1, n + 1):
            fact *= i
        return fact

    @staticmethod
    def lehmer_code_from_encoding(enc, k):
        """Convert a number encoding a permutation to the permutation's lehmer
        code.

        Complexity O(k*log^2(k)*loglog^2(k) + k^2 log^2(k)).
        The first term is from a fast factorial algorithm.
        The second term is from the naive factorial algorithm.

        Args:
          enc: int, encoding of a permutation. enc is in [0, k!).
          k: int, permutation is in [0, k). k >= 1.

        Return:
          list, Lehmer code.
        """
        lehmer = []
        fact = math.factorial(k - 1)
        for i in range(k - 1, 0, -1):
            e = enc // fact
            lehmer.append(e)
            enc %= fact
            fact /= i
        # Add the final 0.
        lehmer.append(0)
        return lehmer

    @staticmethod
    def lehmer_code_from_permutation(permutation):
        """Compute the lehmer code of a permutation.

        Complexity O(k*log^2(k)).
        k is the length of the permutation.
        The extra log(k) is from the length of the integers.

        Args:
          permutation: list/tuple, a permutation. Not empty.

        Return:
          list, Lehmer code.
        """
        fenwick = Fenwick([0] * len(permutation), range_updates=False)
        lehmer = []
        for e in permutation:
            lehmer.append(e - fenwick.sum(e))
            fenwick.add(e, 1)
        return lehmer

    @staticmethod
    def _get_prefix_sum_bsearch_predicate(fenwick, prefix_sum):
        """Return a predicate for binary searching prefix sums on a fenwick
        tree.

        A binary search using this predicate will find the leftmost index with
        the given prefix sum.

        Args:
          fenwick: algorithms.ds.fenwick.Fenwick, a fenwick tree.
          prefix_sum: int, the prefix sum we are looking for.

        Return:
          function, can be used as argument to binary search.
        """
        def predicate(idx):
            """Lower bound predicate.
            """
            return prefix_sum <= fenwick.sum(idx)
        return predicate

    @staticmethod
    def decode_permutation(enc, k):
        """Decode an integer to a permutation.

        Complexity O(k^2 log^2(k) + k * log^3(k)).
        First term is lehmer_code_from_encoding().
        Second term is complexity of loop:
          First log factor is from binary search.
          Accessing the underlying array (fenwick tree) takes log(k).
          Last log factor is from the length of the integers.

        Args:
          enc: int, encoding of a permuation. enc is in [0, k!).
          k: int, decoded permutation will be a permutation of [0, k). k >= 1.

        Return:
          list, a permutation of range(k).
        """
        permutation = []
        lehmer = Combinatorist.lehmer_code_from_encoding(enc, k)
        fenwick = Fenwick([0] + [1] * (k - 1), range_updates=False)
        for e in lehmer:
            pred = Combinatorist._get_prefix_sum_bsearch_predicate(fenwick, e)
            idx = binary_search(0, k, pred)
            permutation.append(idx)
            fenwick.add(idx, -1)
        return permutation

    @staticmethod
    def encode_permutation(permutation):
        """Encode a permutation of [0,n) to a unique number in [0, n!).

        Complexity O(n*log^2(n) + n^2*log^2(n) + n^2*log^2(n)).
        First term is lehmer_code_from_permutation().
        Second term is naive factorial algorithm.
        Third term is multiplication inside the loop: log(n) integer times
          i*log(i) integer.

        Args:
          permutation: list/tuple, permutation of [0, len(permuation),
            not empty.

        Return:
          int, permutation encoding.
        """
        lehmer = Combinatorist.lehmer_code_from_permutation(permutation)
        fact = 1
        enc = 0
        # lehmer[-1] is always 0.
        for i in range(1, len(permutation)):
            fact *= i
            enc += lehmer[-i - 1] * fact
        return enc

    def encode_variation(self, variation):
        """Encode a variation.

        Map the variation to the indexes in the sorted order (the combination).
        For example [8, 3, 9, 6] -> [2, 0, 3, 1]. Call this the transformed
        variation. The encoding is:
            enc(combination) * k! + enc_permutation(transformed variation)

        Complexity O(k*log(k)*log(n) + k*n + k^2*log^2(k)).
        First term is sorting k log(n) integers.
        Second term is encode_combination().
        Third term is encode_permutation().

        Args:
          variation: list/tuple, ordered list representing a variation of
            [0, len(variation)).

        Return:
          int, 0 <= ret < (n choose k) * k!

        """
        k = len(variation)
        fact = math.factorial(k)
        combination = sorted(variation)
        d = {combination[i]: i for i in range(k)}
        transformed_variation = [d[e] for e in variation]
        return (self.encode_combination(combination) * fact +
                Combinatorist.encode_permutation(transformed_variation))

    def decode_variation(self, enc):
        """Decode an integer to a variation (order matters!).

        Complexity O(k*log^2(k)*loglog^2(k) + k*log^2(k)*loglog(k) +
                     k*log(n)*n + k^2*log^2(k)).
        First term is efficient factorial.
        Second term is efficient multiplication (enc // fact).
        Third term is decode_combination().
        Fourth term is decode_permutation().

        Args:
          enc: int, encoding of the variation. enc is in [0, n!/(n-k)!).

        Return:
          list, the decoded variation.
        """
        fact = math.factorial(self.args.k)
        combination_enc = enc // fact
        combination = self.decode_combination(combination_enc)
        permutation = self.decode_permutation(enc % fact, self.args.k)
        return [combination[permutation[i]] for i in range(self.args.k)]


def main():
    """Process args and run combinatorial computations.
    """
    args = parse_args()
    combinatorist = Combinatorist(args)


if __name__ == '__main__':
    main()
