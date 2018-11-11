# Johnny Li and Aaron Chan
# 11-1-2018
# CS 350 Project
# Reference: Introduction to The Design and Analysis of Algorithms by Anany Levitin


def brute_hull(data_set):
    """

    :param data_set: [(x, y), . . .]
    :return: convex hull: [(x, y), . . .]

    """

    convex_hull = []
    for p1 in data_set:
        for p2 in data_set:
            if p2 != p1:
                # ax + by = c
                # c = x1y2 - x2y1
                in_set = True
                a = p1[1] - p2[1]
                b = p1[0] - p2[0]
                c = (p1[0] * p2[1]) - (p1[1] * p1[0])
                signs = []

                for p3 in data_set:
                    if (p3 != p1) and (p3 != p2):
                        # Check if ax+by-c has same sign for all points.
                        signs.append((a * p3[0]) + (b * p3[1]) - c)

                pos = False
                neg = False
                for sign in signs:
                    if sign > 0:
                        pos = True
                    if sign < 0:
                        neg = True

                if not (pos and neg):
                    convex_hull.append(p2)
    return convex_hull


def gift_wrap(data_set):
    pass


def main():
    data_set = []
    brute_hull(data_set)


if __name__ == "__main__":
    main()
