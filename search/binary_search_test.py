#!/usr/bin/env python

import unittest

from binary_search import binary_search

class BinarySearchTest(unittest.TestCase):

    def get_go_left_lower_bound(self, arr, searchee):
        def go_left(mid):
            return searchee <= arr[mid]
        return go_left


    def get_go_left_upper_bound(self, arr, searchee):
        def go_left(mid):
            return searchee < arr[mid]
        return go_left


    def test_smaller_than_all(self):
        arr = [-7, -3, 0, 2, 8, 13]
        go_left_lb = self.get_go_left_lower_bound(arr, -9)
        go_left_ub = self.get_go_left_upper_bound(arr, -9)
        self.assertEqual(0, binary_search(0, len(arr), go_left_lb))
        self.assertEqual(0, binary_search(0, len(arr), go_left_ub))


    def test_equal_to_first(self):
        arr = [-7, -3, 0, 2, 8, 13]
        go_left_lb= self.get_go_left_lower_bound(arr, -7)
        go_left_ub = self.get_go_left_upper_bound(arr, -7)
        self.assertEqual(0, binary_search(0, len(arr), go_left_lb))
        self.assertEqual(1, binary_search(1, len(arr), go_left_ub))


    def test_insert_in_middle(self):
        arr = [-7, -3, 0, 2, 8, 13]

        go_left_lb= self.get_go_left_lower_bound(arr, -5)
        self.assertEqual(1, binary_search(0, len(arr), go_left_lb))
        go_left_lb= self.get_go_left_lower_bound(arr, -4)
        self.assertEqual(1, binary_search(0, len(arr), go_left_lb))
        go_left_lb= self.get_go_left_lower_bound(arr, -3)
        self.assertEqual(1, binary_search(0, len(arr), go_left_lb))
        go_left_lb= self.get_go_left_lower_bound(arr, -1)
        self.assertEqual(2, binary_search(0, len(arr), go_left_lb))
        go_left_lb= self.get_go_left_lower_bound(arr, 0)
        self.assertEqual(2, binary_search(0, len(arr), go_left_lb))

        go_left_ub = self.get_go_left_upper_bound(arr, -5)
        self.assertEqual(1, binary_search(0, len(arr), go_left_ub))
        go_left_ub = self.get_go_left_upper_bound(arr, -4)
        self.assertEqual(1, binary_search(0, len(arr), go_left_ub))
        go_left_ub = self.get_go_left_upper_bound(arr, -3)
        self.assertEqual(2, binary_search(0, len(arr), go_left_ub))
        go_left_ub = self.get_go_left_upper_bound(arr, -1)
        self.assertEqual(2, binary_search(0, len(arr), go_left_ub))
        go_left_ub = self.get_go_left_upper_bound(arr, 0)
        self.assertEqual(3, binary_search(0, len(arr), go_left_ub))


    def test_equal_to_last(self):
        arr = [-7, -3, 0, 2, 8, 13]
        go_left_lb= self.get_go_left_lower_bound(arr, 13)
        go_left_ub = self.get_go_left_upper_bound(arr, 13)
        self.assertEqual(len(arr)-1, binary_search(0, len(arr), go_left_lb))
        self.assertEqual(len(arr), binary_search(0, len(arr), go_left_ub))


    def test_bigger_than_all(self):
        arr = [-7, -3, 0, 2, 8, 13]
        go_left_lb= self.get_go_left_lower_bound(arr, 14)
        go_left_ub = self.get_go_left_upper_bound(arr, 14)
        self.assertEqual(len(arr), binary_search(0, len(arr), go_left_lb))
        self.assertEqual(len(arr), binary_search(0, len(arr), go_left_ub))


    def test_left_end_of_landing(self):
        arr = [3, 3, 3, 7, 8]
        go_left_lb= self.get_go_left_lower_bound(arr, 3)
        go_left_ub = self.get_go_left_upper_bound(arr, 3)
        self.assertEqual(0, binary_search(0, len(arr), go_left_lb))
        self.assertEqual(3, binary_search(0, len(arr), go_left_ub))
        arr = [1, 1, 2, 2, 3, 3, 3, 7, 8]
        go_left_lb= self.get_go_left_lower_bound(arr, 3)
        go_left_ub = self.get_go_left_upper_bound(arr, 3)
        self.assertEqual(4, binary_search(0, len(arr), go_left_lb))
        self.assertEqual(7, binary_search(0, len(arr), go_left_ub))
        arr = [1, 1, 2, 2, 2.5, 2.8, 3, 3, 3]
        go_left_lb= self.get_go_left_lower_bound(arr, 3)
        go_left_ub = self.get_go_left_upper_bound(arr, 3)
        self.assertEqual(6, binary_search(0, len(arr), go_left_lb))
        self.assertEqual(len(arr), binary_search(0, len(arr), go_left_ub))


    def test_subrange(self):
        arr = [-7, -3, 0, 2, 2, 2, 8, 8, 13]
        go_left_lb= self.get_go_left_lower_bound(arr, 2)
        go_left_ub = self.get_go_left_upper_bound(arr, 2)
        self.assertEqual(3, binary_search(2, 7, go_left_lb))
        self.assertEqual(6, binary_search(2, 7, go_left_ub))
        go_left_ub = self.get_go_left_upper_bound(arr, 13)
        self.assertEqual(7, binary_search(2, 7, go_left_ub))


    def test_i_know_a_number(self):
        def smaller(guess):
            return 42 < guess
        def smaller_or_equal(guess):
            return 42 <= guess
        self.assertEqual(42, binary_search(10, 100, smaller_or_equal))
        # Using the wrong predicate gives a wrong result.
        self.assertEqual(43, binary_search(41, 43, smaller))
        self.assertEqual(42, binary_search(41, 43, smaller_or_equal))
        # Using the wrong predicate gives a wrong result.
        self.assertEqual(43, binary_search(42, 43, smaller))
        self.assertEqual(42, binary_search(42, 43, smaller_or_equal))


    def get_greatest_smaller_or_equal_pred(self, arr, searchee):
        def pred(mid):
            if mid >= 0 and searchee < arr[mid]:
                return True
            else:
                # Bounds check is unnecessary if we are searching in [-1,n-1).
                return mid == len(arr)-1 or searchee < arr[mid+1]
        return pred


    def test_greatest_smaller_or_equal(self):
        arr = [-7, -3, 0, 2, 2, 2, 8, 10, 13]
        pred = self.get_greatest_smaller_or_equal_pred(arr, -9)
        self.assertEqual(-1, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, -7)
        self.assertEqual(0, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, -5)
        self.assertEqual(0, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, 1)
        self.assertEqual(2, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, 2)
        self.assertEqual(5, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, 3)
        self.assertEqual(5, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, 13)
        self.assertEqual(len(arr)-1, binary_search(-1, len(arr)-1, pred))
        pred = self.get_greatest_smaller_or_equal_pred(arr, 14)
        self.assertEqual(len(arr)-1, binary_search(-1, len(arr)-1, pred))


    def get_smallest_greater_or_equal_pred(self, arr, searchee):
        def pred(mid):
            return arr[mid] >= searchee
        return pred


    def test_smallest_greater_or_equal(self):
        arr = [-7, -3, 0, 2, 2, 2, 8, 10, 13]
        pred = self.get_smallest_greater_or_equal_pred(arr, -9)
        self.assertEqual(0, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, -7)
        self.assertEqual(0, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, -5)
        self.assertEqual(1, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, 1)
        self.assertEqual(3, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, 2)
        self.assertEqual(3, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, 3)
        self.assertEqual(6, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, 13)
        self.assertEqual(len(arr)-1, binary_search(0, len(arr), pred))
        pred = self.get_smallest_greater_or_equal_pred(arr, 14)
        self.assertEqual(len(arr), binary_search(0, len(arr), pred))


if __name__ == '__main__':
    unittest.main()
