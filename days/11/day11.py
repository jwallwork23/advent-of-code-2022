from advent.advent_tools import PuzzleSetup, Timer
import numpy as np


setup = PuzzleSetup(__file__)
intp = np.int64
np.seterr(all="raise")


class Monkey:
    def __init__(self, lines, part):
        self.index = int(lines[0][7:-2])
        self.items = [intp(i) for i in lines[1][17:-1].split(",")]
        self.operation = lines[2][19:-1]
        self.divisor = intp(lines[3].split()[-1])
        self.if_true = intp(lines[4].split()[-1])
        self.if_false = intp(lines[5].split()[-1])
        self.count = 0
        self.part = part
        self.supermod = self.divisor

    def view(self):
        print(f"""
Monkey {self.index}
  Items: {self.items}
  Operation: {self.operation}
  Test: divisible by {self.divisor}
    If true: throw to monkey {self.if_true}
    If false: throw to monkey {self.if_false}""")

    def inspect(self):
        old = intp(self.items.pop(0))
        try:
            new = intp(eval(self.operation))
        except FloatingPointError:
            raise OverflowError(self.operation.replace("old", str(old)))
        if self.part == 1:
            new //= 3
        else:
            new = new % self.supermod
        other = self.if_true if new % self.divisor == 0 else self.if_false
        self.count += 1
        return new, other

    def catch(self, item):
        self.items.append(intp(item))

    @property
    def nitems(self):
        return len(self.items)


def simulate(nround, part):
    with open(setup.input_file, "r") as f:
        data = f.readlines()
    nline = len(data)
    nmonk = (nline + 1) // 7
    monkeys = [Monkey(data[i*7:(i+1)*7], part) for i in range(nmonk)]

    # Determine the "supermodulo" for part 2
    supermod = 1
    for monk in monkeys:
        supermod *= monk.divisor
    for monk in monkeys:
        monk.supermod = supermod

    if setup.verbose:
        print("Round 0\n=======")
        for monk in monkeys:
            monk.view()
    for rnd in range(nround):
        for turn, monk in enumerate(monkeys):
            for _ in range(monk.nitems):
                val, other = monk.inspect()
                monkeys[other].catch(val)
        if setup.verbose:
            if monk.part == 1:
                msg = f"Round {rnd+1}"
                print("\n".join(["", msg, len(msg) * "="]))
                for i, monk in enumerate(monkeys):
                    print(f"Monkey {i}: {monk.items}")
            elif rnd in [0, 19] or (rnd + 1) % 1000 == 0:
                inspections = np.array([monk.count for monk in monkeys])
                print(f"Round {rnd+1} inspections: {inspections}")
    inspections = np.array([monk.count for monk in monkeys], dtype=intp)
    business = inspections.max()
    inspections[inspections.argmax()] = -1
    business *= inspections.max()
    return business


print(f"Part 1: {simulate(20, 1)}")
print(f"Part 2: {simulate(10000, 2)}")
