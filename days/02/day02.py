from advent.advent_tools import PuzzleSetup


score = 0
setup = PuzzleSetup(__file__)

with open(setup.input_file, "r") as f:
    for line in f.readlines():
        line = line[:-1]
        if line in ("A X", "B Y", "C Z"):  # draw
            score += 3
            outcome = "draw"
        elif line in ("A Y", "B Z", "C X"):  # win
            score += 6
            outcome = "win"
        else:
            outcome = "loss"
        bonus = {"X": 1, "Y": 2, "Z": 3}[line[-1]]
        score += bonus
        if setup.verbose:
            print(f"{line}: outcome={outcome}, bonus={bonus}")
print(f"Part 1: {score}")

score = 0
with open(setup.input_file, "r") as f:
    for line in f.readlines():
        line = line[:-1]
        o, y = line.split()
        if y == "X":  # loss
            choice = {"A": "C", "B": "A", "C": "B"}[o]
        elif y == "Y":  # draw
            choice = o
            score += 3
        else:  # win
            choice = {"A": "B", "B": "C", "C": "A"}[o]
            score += 6
        bonus = {"A": 1, "B": 2, "C": 3}[choice]
        score += bonus
        if setup.verbose:
            print(f"{line}: choice={choice}, bonus={bonus}")
print(f"Part 2: {score}")
