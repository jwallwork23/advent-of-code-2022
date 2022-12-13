from advent.advent_tools import PuzzleSetup
import numpy as np


def str2int(c):
    """
    Convert the character to unicode and adjust.
    """
    o = ord(c)
    offset = 38 if c == c.upper() else 96
    return o - offset


setup = PuzzleSetup(__file__)

s = 0
with open(setup.input_file, "r") as f:
    for nline, line in enumerate(f.readlines()):  # Count lines
        n = len(line[:-1]) // 2
        first, second = line[:n], line[n:]  # Split each line in two
        for c in first:
            if c in second:
                s += str2int(c)
print(f"Part 1: {s}")
nline += 1

with open(setup.input_file, "r") as f:
    lines = np.array([set(line[:-1]) for line in f.readlines()])
s = sum([str2int(list(l0.intersection(l1.intersection(l2)))[0])
        for l0, l1, l2 in lines.reshape((nline//3, 3))])
print(f"Part 2: {s}")
