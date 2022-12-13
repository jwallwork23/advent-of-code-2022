from advent.advent_tools import PuzzleSetup


setup = PuzzleSetup(__file__)

s1 = 0
s2 = 0
with open(setup.input_file, "r") as f:
    for line in f.readlines():
        elf1, elf2 = line.split(",")
        elf1 = set(range(*[int(m)+i for i, m in enumerate(elf1.split("-"))]))
        elf2 = set(range(*[int(m)+i for i, m in enumerate(elf2.split("-"))]))
        if elf1.issubset(elf2) or elf2.issubset(elf1):
            s1 += 1
        if len(elf1.intersection(elf2)) > 0:
            s2 += 1
print(f"Part 1: {s1}")
print(f"Part 2: {s2}")
