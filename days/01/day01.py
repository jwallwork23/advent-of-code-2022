from advent.advent_tools import PuzzleSetup, Timer
import torch


# Parse user input
setup = PuzzleSetup(__file__)

with Timer(setup, "day01") as t:

    # Read input file
    with open(setup.input_file, "r") as f:
        data = f.read()[:-1].split("\n\n")
    data = [[int(datum) for datum in byelf.split("\n")] for byelf in data]
    data = [sum(byelf) for byelf in data]
    data = torch.tensor(data)

    # Find the maximum
    print(f"Part 1: {data.max()}")

    # Find the top three
    s = 0
    for k in range(3):
        i = data.argmax()
        s += data[i]
        data[i] = -1
    print(f"Part 2: {s}")
