import sys


def I():
    return int(sys.stdin.readline().rstrip())


def LI():
    return list(map(int, sys.stdin.readline().rstrip().split()))


def S():
    return sys.stdin.readline().rstrip()


def LS():
    return list(sys.stdin.readline().rstrip().split())


T = I()

for _ in range(T):
    N, H = LI()
    tlu = [LI() for _ in range(N)]
    lastT = 0
    lastMin = lastMax = H
    result = "Yes"
    for t, l, u in tlu:
        dt = t - lastT
        lastT = t
        realMin = max(lastMin - dt, 0)
        realMax = lastMax + dt
        if realMax < l or u < realMin:
            result = "No"
            break
        else:
            lastMin = max(l, realMin, 0)
            lastMax = min(u, realMax)
    print(result)
