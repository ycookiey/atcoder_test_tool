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
result = 0
for i in range(1, N + 1):
    result += i**3 * (-1) ** i
print(result)
