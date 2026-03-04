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


X, Y = LS()

versions = ["Ocelot", "Serval", "Lynx"]

if versions.index(X) >= versions.index(Y):
    print("Yes")
else:
    print("No")
