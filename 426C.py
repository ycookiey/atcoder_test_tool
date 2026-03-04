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


N, Q = LI()
XY = [LI() for _ in range(Q)]

x_final_max = max(map(lambda x: x[0], XY))
# y_final_max = max(map(lambda x: x[1], XY))

# 既出Xの最小<既出Yの最小
# 既出Xの最大<既出Yの最大
# 既出Xの最大と既出Yの最小は不等号不可
# 既出X maxより小さいXは0出力
# 既出Y maxより大きいXが出たらX出力 (初回同様)

# 二回目の操作について
# x2が x1とy1の間かどうかを知りたい
# y1<x2ならx2出力
# 間なら残ってるやつをアップデート= x2-x1

# 下からまとめてどんどんなくなっていく

x_max = 0
y_max = 0

# x_min+1が最低バージョン
#
ys = {}
for x, y in XY:
    if x <= x_max:
        print(0)
    elif y_max <= x:
        print(x)
        t = ys.get(y, 0)
        if y <= x_final_max:
            ys[y] = t + x
    else:
        sumt = 0
        # print(ys)
        for i in sorted(ys.keys()):
            if i <= x:
                sumt += ys.pop(i)
            else:
                break
        print(x - x_max + sumt)
        t = ys.get(y, 0)
        if y <= x_final_max:
            ys[y] = t + x - x_max + sumt

    x_max = max(x, x_max)
    y_max = max(y, y_max)
