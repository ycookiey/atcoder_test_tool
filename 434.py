# %%

import sys


def I():
    return int(sys.stdin.readline().rstrip())


def LI():
    return list(map(int, sys.stdin.readline().rstrip().split()))


def S():
    return sys.stdin.readline().rstrip()


def LS():
    return list(sys.stdin.readline().rstrip().split())


W, B = LI()
# %%
# W, B = 100, 100


# %%
W = W * 1000
result = W // B

# %%
print(result + 1)

# %%
