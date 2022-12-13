from advent.advent_tools import PuzzleSetup, Timer
import numpy as np


setup = PuzzleSetup(__file__)

# Read the crates
crates = ""
line = ""
with open(setup.input_file, "r") as f:
    while not line.lstrip().startswith("1"):
        line = f.readline()
        if not line.lstrip().startswith("1"):
            crates += line

crates = crates.replace("    ", "- ").replace(" ", "").replace("[", "").replace("]", "").split("\n")[:-1]
if setup.verbose:
    print(crates)
stacks = [[] for crate in crates[0]]
ncrate = len(crates[0])
nlevel = len(crates)
for j, level in enumerate(reversed(crates)):
    for i in range(ncrate):
        if crates[nlevel-j-1][i] != "-":
            stacks[i].append(crates[nlevel-j-1][i])
if setup.verbose:
    print(stacks)
copy = list([list(s) for s in stacks])

line = ""
with open(setup.input_file, "r") as f:
    while not line.startswith("\n"):
        line = f.readline()

    while line != "":
        line = f.readline()
        if line == "":
            break
        line = line[5:].replace(" from ", ",").replace(" to ", ",")
        amount, src, dest = [int(i) for i in line.split(",")]
        for _ in range(amount):
            stacks[dest-1].append(stacks[src-1].pop())
if setup.verbose:
    print(stacks)
sol = ""
for stack in stacks:
    sol += stack[-1]
print(f"Part 1: {sol}")


stacks = copy
line = ""
tmp = []
with open(setup.input_file, "r") as f:
    while not line.startswith("\n"):
        line = f.readline()

    while line != "":
        line = f.readline()
        if line == "":
            break
        line = line[5:].replace(" from ", ",").replace(" to ", ",")
        amount, src, dest = [int(i) for i in line.split(",")]
        for _ in range(amount):
            tmp.append(stacks[src-1].pop())
        for _ in range(amount):
            stacks[dest-1].append(tmp.pop())
        assert len(tmp) == 0
if setup.verbose:
    print(stacks)
sol = ""
for stack in stacks:
    sol += stack[-1]
print(f"Part 2: {sol}")
