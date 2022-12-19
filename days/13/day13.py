from advent.advent_tools import PuzzleSetup, Timer
import itertools


def check_order(l1, l2):
    m = len(l1)
    n = len(l2)
    if m == 0:
        if n == 0:
            return 0
        elif isinstance(l2[0], list):
            b = check_order([l1], l2)
            if b != 0:
                return b
        else:
            if setup.verbose:
                print(f"right1: len({l1}) < len({l2})")
            return 1
    elif n == 0:
        if isinstance(l1[0], list):
            b = check_order(l1, [l2])
            if b != 0:
                return b
        if setup.verbose:
            print(f"wrong1: len({l1}) > len({l2})")
        return -1
    # print("####l1: ", l1)
    # print("####l2: ", l2)
    for k, (a1, a2) in enumerate(itertools.zip_longest(l1, l2)):
        # print("k: ", k)
        # print("a1: ", a1)
        # print("a2: ", a2)
        # print("l1: ", l1)
        # print("l2: ", l2)
        # print(a1 == [])
        # print(a2 == [])
        # print(k, a1, a2, type(a1), type(a2))
        if a1 == a2:
            continue
        if k == m:
            if k == n:
                return 0
            elif isinstance(a2, list):
                a1 = [a1]
                b = check_order(a1, a2)
                if b != 0:
                    return b
            # if setup.verbose:
            #     print(f"right2: len({l1}) < len({l2})")
            # return 1
        elif k == n:
            if isinstance(a1, list):
                a2 = [a2]
                b = check_order(a1, a2)
                if b != 0:
                    return b
            # if setup.verbose:
            #     print(f"wrong2: len({l1}) > len({l2})")
            # return -1
        if isinstance(a1, list):
            if isinstance(a2, int):
                a2 = [a2]
        else:
            if isinstance(a2, list):
                a1 = [a1]
            elif a1 is None:
                if a2 is None:
                    return 0
                else:
                    return 1
            elif a2 is None:
                return -1
            # elif a1 == a2:
            #     continue
            elif a1 > a2:
                if setup.verbose:
                    print(f"wrong3: {a1} > {a2}")
                return -1
            elif a1 < a2:
                if setup.verbose:
                    print(f"right3: {a1} < {a2}")
                return 1
        if isinstance(a1, list) and isinstance(a2, list):
            b = check_order(a1, a2)
            if b != 0:
                return b
    return 0


setup = PuzzleSetup(__file__)

with open(setup.input_file, "r") as f:
    pairs = [p.split("\n")[:2] for p in f.read().split("\n\n")]

s = 0
for i, pair in enumerate(pairs):
    lhs = []
    rhs = []
    for p, a in zip(pair, [lhs, rhs]):
        level = 0
        arr = a
        n = len(p)
        j = 0
        while j < n:
            c = p[j]
            if c == "[":
                level += 1
                arr.append([])
                arr = arr[-1]
            elif c == "]":
                level -= 1
                arr = a
                for l in range(level):
                    arr = arr[-1]
            elif c == ",":
                pass
            else:
                k = ""
                while p[j] in "0123456789":
                    k += p[j]
                    j += 1
                arr.append(int(k))
                continue
            j += 1
    lhs = lhs[0]
    rhs = rhs[0]

    # Check that the input has been parsed correctly
    p1, p2 = pair
    lstr = str(lhs).replace(" ", "")
    rstr = str(rhs).replace(" ", "")
    assert p1 == lstr, f"{p1} vs {lstr}"
    assert p2 == rstr, f"{p2} vs {rstr}"
    if setup.verbose:
        print(p1, p2)
        print(lstr, rstr)

    # Sum up the pairs that are in the right order
    b = check_order(lhs, rhs)
    if b == 1:
        print(f"Index {i+1} is in the right order")
        s += i+1
    elif b == -1:
        print(f"Index {i+1} is in the wrong order")
    else:
        print(lhs, rhs)
        raise ValueError(f"Index {i+1} gives unexpected value {b}")

print(f"Part 1: {s}")
# TODO: 6368 too low

# print(f"Part 2: {}")
