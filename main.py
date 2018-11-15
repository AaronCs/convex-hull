# Johnny Li and Aaron Chan
# 11-1-2018
# CS 350 Project
# Reference: Introduction to The Design and Analysis of Algorithms by Anany Levitin

from random import randint
import matplotlib.pyplot as plt
import timeit


def brute_hull(data_set):
    """

    :param data_set: [(x, y), . . .]
    :return: convex hull: [(x, y), . . .]

    """

    convex_hull = []
    for p1 in data_set:
        for p2 in data_set[data_set.index(p1) + 1:]:
            if p2 != p1:
                # ax + by = c
                # c = x1y2 - x2y1

                x1 = p1[0]
                y1 = p1[1]

                x2 = p2[0]
                y2 = p2[1]

                a = y2 - y1
                b = x1 - x2
                c = (x1 * y2) - (y1 * x2)
                pos = 0
                neg = 0

                for p3 in data_set:
                    if p3 != p1 and p3 != p2:
                        # Check if ax+by-c has same sign for all points.
                        lin_eq = (a * p3[0]) + (b * p3[1]) - c
                        if lin_eq >= 0:
                            pos += 1
                        if lin_eq <= 0:
                            neg += 1

                # -2 b/c we ignore the points made by the line.
                if pos == (len(data_set) - 2) or neg == (len(data_set) - 2):
                    to_append = (p1, p2)
                    convex_hull.append(to_append)
    return convex_hull


def gift_wrap(data_set):
    convex_hull = []

    # Find leftmost point.
    leftmost = data_set[0]
    for point in data_set:
        if leftmost[0] > point[0]:
            leftmost = point
    print(leftmost)
    return convex_hull


def gen_data(num_points, minimum, maximum):
    """
    :return: randomly generates a point.
    """
    data_set = set()
    x = randint(minimum, maximum)
    y = randint(minimum, maximum)

    while num_points:
        data_set.add((x, y))
        x = randint(minimum, maximum)
        y = randint(minimum, maximum)
        while (x, y) in data_set:
            x = randint(minimum, maximum)
            y = randint(minimum, maximum)
        num_points -= 1
    return data_set


def main():
    data_count = 15
    rand_min, rand_max = 0, 250
    # data_set = list(gen_data(data_count, rand_min, rand_max))
    data_set = [(1, 2), (0, 4), (0, 0), (2, 2), (10, 10), (15, 2)]

    iterate_num = 10000
    setup_code = '''
from __main__ import brute_hull, gen_data
data_count = 15
rand_min, rand_max = 0, 250
data_set = list(gen_data(data_count, rand_min, rand_max))
    '''

    # times = timeit.repeat("brute_hull(data_set)", setup=setup_code, repeat=10, number=iterate_num)
    # print("Brute hull time: {}".format(min(times)))

    convex_hull = gift_wrap(data_set)
    '''
    plt.scatter(*zip(*data_set))
    for line in convex_hull:
        plt.plot(*zip(*line), color="red")
    plt.show()
    '''


if __name__ == "__main__":
    main()
