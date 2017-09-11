#!/usr/bin/env python

"""General binary search.
"""

def binary_search(lo, hi, go_left):
    """Binry search a range by predicate.

    lo <= hi
    Args:
      lo: int, lower bound of range, inclusive.
      hi: int, higher bound of range, exclusive.
      go_left: function, a predicate that says which way to search.
    Returns:
      int, index where binary search ends, [lo, hi].
    """
    if lo >= hi:
        return lo
    mid = lo + (hi-lo)//2
    if go_left(mid):
        return binary_search(lo, mid, go_left)
    else:
        return binary_search(mid+1, hi, go_left)
