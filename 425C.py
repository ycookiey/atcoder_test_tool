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


from collections import deque

N, Q = LI()
# A = deque(LI())
A = LI()
query = [LI() for _ in range(Q)]


# for q in query:
#     if q[0] == 1:
#         A.rotate(-q[1])
#     else:
#         print(sum(list(itertools.islice(A, q[1] - 1, q[2]))))
#         print()

offset = 0
A.extend(A)
memo = dict()
allsum = int(sum(A) / 2)
for q in query:
    if q[0] == 1:
        offset = (offset + q[1]) % N
    else:
        reversal = False
        l = q[1] - 1 + offset
        r = q[2] - 1 + offset
        if (l, r) in memo:
            print(memo[(l, r)])
            continue
        x, y = l, r
        if r - l > N / 2:
            if r < N:
                l, r = r + 1, l + N - 1
            else:
                l, r = r - N + 1, l - 1
            memo[(x, y)] = allsum - sum(A[l : r + 1])
        else:
            memo[(l, r)] = sum(A[l : r + 1])
        print(memo[(x, y)])
        # print(A[l : r + 1])
