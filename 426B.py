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


St = S()

t = St[0]

for i, s in enumerate(St):
    if s == t:
        continue
    else:
        if i == 1 and St[0] != St[2]:
            print(St[0])
            exit()
        else:
            print(St[i])
            exit()
