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


N, M, C = LI()
As = LI()

# 各地点にいる人数のリストを生成

# リストを前から処理していく。
# [a,b,c,d]の次はaをポップした状態を考えるのでは

# 具体的な位置の情報は不要。どういう順序かが大事

c = collections.Counter(As)
sc = sorted(c.items(), key=lambda x: x[0])
# sc.append(sc.pop(0))
# print(sc)

init = 0
last_pos = sc[-1][0]
r = -1
# for r, (_, i) in enumerate(sc):
#     init += i
#     if C < init:
#         break

# result = init
# print(r)
# todo 多分違うこれ
# X = init

dsc: list = sc + sc
X = c[last_pos]


def nextX(X, last_pos):
    global r
    temp = X - c[last_pos]
    # print(temp)
    # print(dsc)
    for r_t, (_, i) in enumerate(dsc[r + 1 :], 1):
        temp += i
        if C <= temp:
            r += r_t
            # print(X, last_pos, "→", temp)

            return temp


result = 0
for pos, num in sc:
    X = nextX(X, pos)
    distance = pos - last_pos
    if distance <= 0:
        distance += M
    # if distance == 0:
    #     distance = 1
    result += X * distance
    # print(result)
    # print("add", X, "x", distance)
    last_pos = pos
print(result)
