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
ABs = [LI() for _ in range(N)]

zyoken = [[] for _ in range(N)]

learned = set()  # indexで表現（0~N-1

# [[2,3],...] の場合スキル1を取得したならスキル2,3を取得できる
for i, (a, b) in enumerate(ABs):
    if a == 0:
        learned.add(i)
    else:
        zyoken[a - 1].append(i)
        zyoken[b - 1].append(i)
# print(zyoken)

# last_count=0
# count=len(learned)
newSkills = set(learned)
while newSkills:
    # print(f"newSkills: {newSkills}, learned: {learned}")
    recentSkills = newSkills
    newSkills = set()
    for i in recentSkills:
        newSkills.update(set(zyoken[i]))
    newSkills -= learned
    learned.update(newSkills)
print(len(learned))
