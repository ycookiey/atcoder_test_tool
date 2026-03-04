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


c = collections.Counter(A)
# print(c)
result = 0
for k, v in c.items():
    if 2 <= v:
        result += int(v * (v - 1) / 2 * (N - v))
print(result)
