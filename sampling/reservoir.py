#!/usr/bin/env python

"""Reservoir sampling.
"""

import argparse
import random
import sys

def parse_args():
    """Parse command line arguments.

    Returns:
      args from the argparse module
    """
    usage = """Reservoir sampling. """
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument(
        '--sample-size', '-s', default=5, type=int,
        help='Size of the reservoir.')
    return parser.parse_args()


class Reservoir(object):

    def __init__(self, stream, size):
        """Initialize reservoir sampling algorithm.

        Args:
          stream: iterator, stream to sample from
          size: int, size of reservoir
        """
        self.stream = stream
        self.size = size


    def sample(self):
        """Run reservoir sampling algorithm.

        Return:
          list, the sample from the stream
        """
        n = 0
        reservoir = []
        while True:
            try:
                item = next(self.stream)
                n += 1
                if len(reservoir) < self.size:
                    reservoir.append(item)
                else:
                    r = random.randint(0, n - 1)
                    if r < self.size:
                        reservoir[r] = item
            except StopIteration:
                break

        return reservoir


def stdin_gen():
    """Generator function for stdin lines.
    """
    for line in sys.stdin:
        yield line.strip()


def main():
    """Sample lines from stdin.
    """
    args = parse_args()
    reservoir = Reservoir(stdin_gen(), args.sample_size)
    sample = reservoir.sample()
    print('Sample:')
    for line in sample:
        print(line)


if __name__ == '__main__':
    main()
