from advent.advent_tools import PuzzleSetup, Timer


setup = PuzzleSetup(__file__)


class Stepper:
    X = 1
    cycle = 0
    s = 0
    sprite = None
    screen = ""

    def take_step(self):
        self.cycle += 1
        if self.cycle % 40 == 20:
            self.s += self.cycle * self.X
        if self.sprite is None or self.cycle % 40 in self.sprite:
            self.screen += "#"
        else:
            self.screen += "."
        if self.cycle % 40 == 0:
            self.screen += "\n"


S = Stepper()
with open(setup.input_file, "r") as f:
    for line in f.readlines():
        if line.startswith("noop"):
            S.take_step()
        elif line.startswith("addx"):
            S.take_step()
            S.take_step()
            S.X += int(line.split()[-1])
            S.sprite = [S.X, S.X+1, S.X+2]
print(f"Part 1: {S.s}")
print(f"Part 2:\n{S.screen}")
