import sys
import math


def closest_pair(data_set):
    dist = []
    for p1 in data_set:
        for p2 in data_set:
            if p1 is not p2:
                dist.append(math.sqrt(p1**2 + p2**2))
    return min(dist)


def brute_hull(data_set):
    print("Test")
