from advent.advent_tools import PuzzleSetup, Timer
import glob
import os
import pathlib
import shutil


setup = PuzzleSetup(__file__)
sizes = []
valid = []

# Create the file tree
mode = setup.input_file[:-4]
shutil.rmtree(mode)
os.mkdir(mode)
with open(setup.input_file, "r") as f:
    f.readline()
    path = ""
    line = None
    while line != "":
        line = f.readline()[:-1]
        if line == "":
            break
        elif line == "$ cd ..":
            path = "/".join(path.split("/")[:-1])
        elif line.startswith("$ cd"):
            path = f"{path}/{line[5:]}"
            os.mkdir(f"{mode}/{path}")
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            continue
        else:
            size, name = line.split()
            with open(f"{mode}/{path}/{name}", "w") as fout:
                fout.write(size)


def du(name):
    """
    Calculate the size of a subdirectory recursively.
    """
    size = 0
    for file in glob.glob(f"{name}/*"):
        if pathlib.Path(file).is_file():
            with open(file, "r") as f:
                size += int(f.readline())
        else:
            size += du(file)
    if setup.verbose:
        print(name, size)
    sizes.append(size)
    if size < 100000:
        valid.append(size)
    return size


# Check the size of each subdir recursively
du(mode)
print(f"Part 1: {sum(valid)}")


# Find the smallest file suitable for deletion
full = 70000000
reqd = 30000000
sizes.sort()
taken = sizes[-1]
for size in sizes:
    if taken - size <= full - reqd:
        print(f"Part 2: {size}")
        break
