from advent.advent_tools import PuzzleSetup, Timer
import numpy as np


setup = PuzzleSetup(__file__)

with open(setup.input_file, "r") as f:
    A = np.array([[int(a) for a in line[:-1]] for line in f.readlines()])

m = A.shape[0]
n = A.shape[1]
N = 2 * m + 2 * n - 4
for i in range(1,m-1):
    for j in range(1,n-1):
        if setup.verbose:
            print((i, j), A[i,j])
        if (all(A[:i,j] < A[i,j]) or all(A[i+1:,j] < A[i,j]) or \
                all(A[i,:j] < A[i,j]) or all(A[i,j+1:] < A[i,j])):
            if setup.verbose:
                print(True)
            N += 1
print(f"Part 1: {N}")

S = np.ones(A.shape, dtype=int)
for i in range(m):
    for j in range(n):
        if setup.verbose:
            print((i, j), A[i,j])
        s = 0
        for k in range(i-1,-1,-1):
            if i == 0:
                break
            s += 1
            if A[k,j] >= A[i,j]:
                break
        S[i,j] *= s
        s = 0
        for k in range(i+1,m):
            if i == m-1:
                break
            s += 1
            if A[k,j] >= A[i,j]:
                break
        S[i,j] *= s
        s = 0
        for k in range(j-1,-1,-1):
            if j == 0:
                break
            s += 1
            if A[i,k] >= A[i,j]:
                break
        S[i,j] *= s
        s = 0
        for k in range(j+1,n):
            if j == n-1:
                break
            s += 1
            if A[i,k] >= A[i,j]:
                break
        S[i,j] *= s
if setup.verbose:
    print(S)
print(f"Part 2: {S.max()}")
