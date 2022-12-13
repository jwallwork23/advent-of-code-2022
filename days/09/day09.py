from advent.advent_tools import PuzzleSetup, Timer
import numpy as np


setup = PuzzleSetup(__file__)

sign = lambda x: x if x == 0 else x // abs(x)
signs = lambda v: np.array([sign(x) for x in v])
steps = {
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
}

def simulate(l):
    rope = np.zeros((l+1, 2))
    visited = {tuple(rope[-1, :])}
    with open(setup.input_file, "r") as f:
        for line in f.readlines():
            direction, dist = line.split()
            for _ in range(int(dist)):
                rope[0, :] += steps[direction]
                diff = rope[:-1, :] - rope[1:, :]
                for i in range(l):
                    if any(abs(diff[i]) > 1):
                        rope[i+1, :] += signs(diff[i])
                visited.add(tuple(rope[-1, :].copy()))
    return len(visited)


print(f"Part 1: {simulate(1)}")
print(f"Part 2: {simulate(9)}")
