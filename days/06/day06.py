from advent.advent_tools import PuzzleSetup, Timer


setup = PuzzleSetup(__file__)

for i, l in enumerate((4, 14)):
    with open(setup.input_file, "r") as f:
        for line in f.readlines():
            line = line[:-1]
            for j in range(len(line)-l+1):
                if len(set(line[j:j+l])) == l:
                    print(f"Part {i+1}: {j+l}")
                    break
