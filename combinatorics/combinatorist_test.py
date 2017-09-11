#!/usr/bin/env python

import unittest

from combinatorist import Combinatorist
from namedlist import namedlist


class CombinatoristTest(unittest.TestCase):

    def test_binom(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=10, k=3)
        combinatorist = Combinatorist(args)

        expected = [
            [1, 0, 0, 0], [1, 1, 0, 0], [1, 2, 1, 0], [1, 3, 3, 1],
            [1, 4, 6, 4], [1, 5, 10, 10], [1, 6, 15, 20], [1, 7, 21, 35],
            [1, 8, 28, 56], [1, 9, 36, 84], [1, 10, 45, 120]
        ]
        self.assertEqual(expected, combinatorist.binom)

    def test_encode_combination(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=10, k=4)
        combinatorist = Combinatorist(args)

        self.assertEqual(0, combinatorist.encode_combination([0, 1, 2, 3]))
        self.assertEqual(3, combinatorist.encode_combination([0, 4, 2, 3]))
        self.assertEqual(7, combinatorist.encode_combination([5, 3, 2, 0]))
        self.assertEqual(11, combinatorist.encode_combination([1, 5, 4, 2]))

        # Setting a different n should give the same results.
        args = Args(n=6, k=4)
        combinatorist = Combinatorist(args)

        self.assertEqual(0, combinatorist.encode_combination([0, 1, 2, 3]))
        self.assertEqual(3, combinatorist.encode_combination([0, 4, 2, 3]))
        self.assertEqual(7, combinatorist.encode_combination([5, 3, 2, 0]))
        self.assertEqual(11, combinatorist.encode_combination([1, 5, 4, 2]))

    def test_decode_combination(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=10, k=4)
        combinatorist = Combinatorist(args)

        self.assertEqual([0, 1, 2, 3], combinatorist.decode_combination(0))
        self.assertEqual([0, 2, 3, 4], combinatorist.decode_combination(3))
        self.assertEqual([0, 2, 3, 5], combinatorist.decode_combination(7))
        self.assertEqual([1, 2, 4, 5], combinatorist.decode_combination(11))

        # Setting a different n should give the same results.
        args = Args(n=6, k=4)
        combinatorist = Combinatorist(args)

        self.assertEqual([0, 1, 2, 3], combinatorist.decode_combination(0))
        self.assertEqual([0, 2, 3, 4], combinatorist.decode_combination(3))
        self.assertEqual([0, 2, 3, 5], combinatorist.decode_combination(7))
        self.assertEqual([1, 2, 4, 5], combinatorist.decode_combination(11))

    def test_encode_combination_order(self):
        """Test ordering of combinations encodings.
        """
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=10, k=4)
        combinatorist = Combinatorist(args)

        self.assertEqual([0, 1, 2, 3], combinatorist.decode_combination(0))
        self.assertEqual([0, 1, 2, 4], combinatorist.decode_combination(1))
        self.assertEqual([0, 1, 3, 4], combinatorist.decode_combination(2))
        self.assertEqual([0, 2, 3, 4], combinatorist.decode_combination(3))
        self.assertEqual([1, 2, 3, 4], combinatorist.decode_combination(4))
        self.assertEqual([0, 1, 2, 5], combinatorist.decode_combination(5))
        self.assertEqual([0, 1, 3, 5], combinatorist.decode_combination(6))
        self.assertEqual([0, 2, 3, 5], combinatorist.decode_combination(7))
        self.assertEqual([1, 2, 3, 5], combinatorist.decode_combination(8))
        self.assertEqual([0, 1, 4, 5], combinatorist.decode_combination(9))
        self.assertEqual([0, 2, 4, 5], combinatorist.decode_combination(10))
        self.assertEqual([1, 2, 4, 5], combinatorist.decode_combination(11))
        self.assertEqual([0, 3, 4, 5], combinatorist.decode_combination(12))
        self.assertEqual([1, 3, 4, 5], combinatorist.decode_combination(13))
        self.assertEqual([2, 3, 4, 5], combinatorist.decode_combination(14))
        self.assertEqual([0, 1, 2, 6], combinatorist.decode_combination(15))

    def test_k_0(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=10, k=0)
        combinatorist = Combinatorist(args)

        self.assertEqual(0, combinatorist.encode_combination([]))
        self.assertEqual([], combinatorist.decode_combination(0))

        # Setting a different n should give the same results.
        args = Args(n=6, k=0)
        combinatorist = Combinatorist(args)

        self.assertEqual(0, combinatorist.encode_combination([]))
        self.assertEqual([], combinatorist.decode_combination(0))

    def test_k_equals_n(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=10, k=10)
        combinatorist = Combinatorist(args)

        self.assertEqual(0, combinatorist.encode_combination(list(range(10))))
        self.assertEqual(list(range(10)), combinatorist.decode_combination(0))

        # Setting a different n should give the same results.
        args = Args(n=6, k=6)
        combinatorist = Combinatorist(args)

        self.assertEqual(0, combinatorist.encode_combination(list(range(6))))
        self.assertEqual(list(range(6)), combinatorist.decode_combination(0))

    def test_lehmer_code_from_encoding(self):
        # Length 1.
        self.assertEqual([0], Combinatorist.lehmer_code_from_encoding(0, 1))

        # Length 2.
        self.assertEqual([0, 0], Combinatorist.lehmer_code_from_encoding(0, 2))
        self.assertEqual([1, 0], Combinatorist.lehmer_code_from_encoding(1, 2))

        # Length 3.
        self.assertEqual([0, 0, 0],
                         Combinatorist.lehmer_code_from_encoding(0, 3))
        self.assertEqual([0, 1, 0],
                         Combinatorist.lehmer_code_from_encoding(1, 3))
        self.assertEqual([1, 0, 0],
                         Combinatorist.lehmer_code_from_encoding(2, 3))
        self.assertEqual([1, 1, 0],
                         Combinatorist.lehmer_code_from_encoding(3, 3))
        self.assertEqual([2, 0, 0],
                         Combinatorist.lehmer_code_from_encoding(4, 3))
        self.assertEqual([2, 1, 0],
                         Combinatorist.lehmer_code_from_encoding(5, 3))

    def test_lehmer_code_from_permutation(self):
        self.assertEqual([0, 0, 0, 0],
                         Combinatorist.lehmer_code_from_permutation(
                             [0, 1, 2, 3]))
        self.assertEqual([3, 2, 1, 0],
                         Combinatorist.lehmer_code_from_permutation(
                             [3, 2, 1, 0]))
        self.assertEqual([0, 1, 0, 0],
                         Combinatorist.lehmer_code_from_permutation(
                             [0, 2, 1, 3]))
        self.assertEqual([1, 2, 0, 0],
                         Combinatorist.lehmer_code_from_permutation(
                             [1, 3, 0, 2]))
        self.assertEqual([3, 1, 0, 0],
                         Combinatorist.lehmer_code_from_permutation(
                             [3, 1, 0, 2]))

        self.assertEqual([4, 2, 3, 2, 1, 0],
                         Combinatorist.lehmer_code_from_permutation(
                             [4, 2, 5, 3, 1, 0]))

    def test_encode_permutation(self):
        # Length 1.
        self.assertEqual([0], Combinatorist.decode_permutation(0, 1))

        # Length 2.
        self.assertEqual([0, 1], Combinatorist.decode_permutation(0, 2))
        self.assertEqual([1, 0], Combinatorist.decode_permutation(1, 2))

        # Length 3.
        self.assertEqual([0, 1, 2], Combinatorist.decode_permutation(0, 3))
        self.assertEqual([0, 2, 1], Combinatorist.decode_permutation(1, 3))
        self.assertEqual([1, 0, 2], Combinatorist.decode_permutation(2, 3))
        self.assertEqual([1, 2, 0], Combinatorist.decode_permutation(3, 3))
        self.assertEqual([2, 0, 1], Combinatorist.decode_permutation(4, 3))
        self.assertEqual([2, 1, 0], Combinatorist.decode_permutation(5, 3))

    def test_decode_permutation(self):
        # Length 1.
        self.assertEqual(0, Combinatorist.encode_permutation([0]))

        # Length 2.
        self.assertEqual(0, Combinatorist.encode_permutation([0, 1]))
        self.assertEqual(1, Combinatorist.encode_permutation([1, 0]))

        # Length 3.
        self.assertEqual(0, Combinatorist.encode_permutation([0, 1, 2]))
        self.assertEqual(1, Combinatorist.encode_permutation([0, 2, 1]))
        self.assertEqual(2, Combinatorist.encode_permutation([1, 0, 2]))
        self.assertEqual(3, Combinatorist.encode_permutation([1, 2, 0]))
        self.assertEqual(4, Combinatorist.encode_permutation([2, 0, 1]))
        self.assertEqual(5, Combinatorist.encode_permutation([2, 1, 0]))

    def test_encode_variation(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=3, k=2)
        combinatorist = Combinatorist(args)

        # 2 out of 3.
        self.assertEqual(0, combinatorist.encode_variation([0, 1]))
        self.assertEqual(1, combinatorist.encode_variation([1, 0]))
        self.assertEqual(2, combinatorist.encode_variation([0, 2]))
        self.assertEqual(3, combinatorist.encode_variation([2, 0]))
        self.assertEqual(4, combinatorist.encode_variation([1, 2]))
        self.assertEqual(5, combinatorist.encode_variation([2, 1]))

    def test_decode_variation(self):
        Args = namedlist('Args', ['n', 'k'])
        args = Args(n=3, k=2)
        combinatorist = Combinatorist(args)

        # 2 out of 3.
        self.assertEqual([0, 1], combinatorist.decode_variation(0))
        self.assertEqual([1, 0], combinatorist.decode_variation(1))
        self.assertEqual([0, 2], combinatorist.decode_variation(2))
        self.assertEqual([2, 0], combinatorist.decode_variation(3))
        self.assertEqual([1, 2], combinatorist.decode_variation(4))
        self.assertEqual([2, 1], combinatorist.decode_variation(5))


if __name__ == '__main__':
    unittest.main()
