import bisect, collections, copy, heapq, itertools, math, numpy, string
import sys


def I():
    return int(sys.stdin.readline().rstrip())


def LI():
    return list(map(int, sys.stdin.readline().rstrip().split()))


def S():
    return sys.stdin.readline().rstrip()


def LS():
    return list(sys.stdin.readline().rstrip().split())


N = I()
A = LI()

minone = A.count(-1)
if minone == 0 and len(set(A)) == len(A):
    print("Yes")
    print(" ".join(map(str, A)))
elif len(set(A)) - 1 == len(A) - minone:
    print("Yes")
    amari = set(range(1, N + 1)) - set(A)
    for i in range(N):
        if A[i] == -1:
            A[i] = amari.pop()

    print(" ".join(map(str, A)))
else:
    print("No")
