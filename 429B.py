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


N, M = LI()
As = LI()

temp = sum(As)

for A in As:
    if temp - A == M:
        print("Yes")
        exit()
print("No")

# TODO: 問題解決のロジックを実装
