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


N, M, K = LI()

ABs = [LI() for _ in range(K)]

count = [0] * N

for human, prob in ABs:
    count[human - 1] += 1
    if count[human - 1] == M:
        print(human, end=" ")
