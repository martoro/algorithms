"""Implementation of a fenwick tree with range updates.

For a reference see here:
  https://goo.gl/T83PC1
"""


class Fenwick(object):

    def __init__(self, arr, range_updates=True):
        """Initialize the Fenwick tree.

        Args:
          arr: list/tuple of numbers.

        Return:
          void
        """
        self._range_updates = range_updates
        self._add = [0] * len(arr)
        if range_updates:
            self._mul = [0] * len(arr)
        else:
            # Alias self._mul to save on memory.
            self._mul = self._add
        for i, e in enumerate(arr):
            self.add(i, e)

    def add(self, idx, val):
        """Add val to element and index idx.

        Args:
          idx: int, index where val should be added.
          val: number, value to add at location idx.

        Return:
          void
        """
        self.add_to_range(idx, idx, val)

    def add_to_range(self, left, right, val):
        """Add val to each of the elements in the range.

        Args:
          left: int, index of left element of range, inclusive.
          right: int, index of right element of range, inclusive.
          val: number, value to add.

        Return:
          void
        """
        self._update(left, val, -(left - 1) * val)
        self._update(right, -val, right * val)

    def _update(self, idx, mul, add):
        """Update of the internal structures of the fenwick tree.

        Args:
          idx: int, index of the update.
          mul: multiplicative value to add.
          add: additive value to add.

        Return:
          void
        """
        n = len(self._mul)
        while idx < n:
            self._mul[idx] += mul
            self._add[idx] += add
            # The following will make index 0 useless:
            #   idx += (idx & -idx)
            idx |= (idx + 1)

    def sum(self, idx):
        """Compute the prefix sum up to an index.

        Args:
          idx: int, index of last element of the prefix sum.

        Return:
          number, the prefix sum.
        """
        x = idx
        mul = 0
        add = 0
        while idx >= 0:
            mul += self._mul[idx]
            add += self._add[idx]
            # The following will make index 0 useless:
            #   idx -= (idx & -idx)
            idx = (idx & (idx + 1)) - 1

        ret = add
        if self._range_updates:
            ret += mul * x
        return ret
