#!/usr/bin/env python

import unittest

from fenwick import Fenwick


class FenwickTest(unittest.TestCase):

    def test_fenwick(self):
        l = [3, 1, 2, -1]
        tree = Fenwick(l, range_updates=False)
        range_tree = Fenwick(l, range_updates=True)

        # Sum before update.
        self.assertEqual(3, tree.sum(0))
        self.assertEqual(3, range_tree.sum(0))
        self.assertEqual(4, tree.sum(1))
        self.assertEqual(4, range_tree.sum(1))
        self.assertEqual(6, tree.sum(2))
        self.assertEqual(6, range_tree.sum(2))
        self.assertEqual(5, tree.sum(3))
        self.assertEqual(5, range_tree.sum(3))

        # Update.
        tree.add(1, 1)
        range_tree.add(1, 1)
        self.assertEqual(3, tree.sum(0))
        self.assertEqual(3, range_tree.sum(0))
        self.assertEqual(5, tree.sum(1))
        self.assertEqual(5, range_tree.sum(1))
        self.assertEqual(7, tree.sum(2))
        self.assertEqual(7, range_tree.sum(2))
        self.assertEqual(6, tree.sum(3))
        self.assertEqual(6, range_tree.sum(3))

        # Range update.
        range_tree.add_to_range(1, 2, 3)
        self.assertEqual(3, range_tree.sum(0))
        self.assertEqual(8, range_tree.sum(1))
        self.assertEqual(13, range_tree.sum(2))
        self.assertEqual(12, range_tree.sum(3))

    def count_inversions(self, arr):
        """Count the number of inversions in arr.

        Args:
          arr: list of numbers

        Return:
          int, number of inversions
        """
        tree = Fenwick([0] * len(arr), range_updates=False)
        inv = 0
        for i, e in enumerate(arr):
            inv += i - tree.sum(e)
            tree.add(e, 1)
        return inv

    def test_count_inversions(self):
        """Count inversions in a permutation.
        """
        self.assertEqual(0, self.count_inversions([0, 1, 2, 3]))
        self.assertEqual(1, self.count_inversions([0, 2, 1, 3]))
        self.assertEqual(2, self.count_inversions([1, 0, 3, 2]))
        self.assertEqual(3, self.count_inversions([1, 3, 0, 2]))
        self.assertEqual(4, self.count_inversions([1, 3, 2, 0]))
        self.assertEqual(5, self.count_inversions([3, 1, 2, 0]))
        self.assertEqual(6, self.count_inversions([3, 2, 1, 0]))


if __name__ == '__main__':
    unittest.main()
