# Johnny Li and Aaron Chan
# 11-1-2018
# CS 350 Project
# Reference: Introduction to The Design and Analysis of Algorithms by Anany Levitin

from random import randint
import matplotlib.pyplot as plt
from collections import Counter
from scipy.spatial import ConvexHull as scipy_hull
import math
import timeit
import csv
import os
import multiprocessing


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


def brutehull(data_set):
    """

    :param data_set: [(x, y), . . .]
    :return: convex hull: [(x, y), . . .]

    """

    convex_hull = []
    for p1 in data_set:
        for p2 in data_set[data_set.index(p1) + 1:]:
            if p2 != p1:
                count = 0
                one_side = True
                for p3 in data_set:
                    if p3 != p1 and p3 != p2:
                        if count == 0:
                            first_side = find_side(p3, p1, p2)
                            count += 1
                        else:
                            # Check if ax+by-c has same sign for all points.
                            if find_side(p3, p1, p2) != first_side:
                                one_side = False

                if one_side:
                    to_append = (p1, p2)
                    convex_hull.append(to_append)
    return convex_hull


def gift_wrap(data_set):
    convex_hull = []

    # Find leftmost point.
    current = find_leftmost(data_set)
    # Pseudo do-while loop
    i = 0
    while True:
        if len(convex_hull) > len(data_set):
            break
        convex_hull.append(current)
        endpoint = data_set[i]
        if current == endpoint:
            i += 1
            endpoint = data_set[i % len(data_set)]
        for point in data_set:
            left = find_side(point, current, endpoint)
            if left == 2:
                endpoint = point
        current = endpoint
        if current == convex_hull[0]:
            break

    return convex_hull


def find_side(to_compare, line_start, line_end):
    x1, y1 = line_start[0], line_start[1]
    x2, y2 = line_end[0], line_end[1]

    # value = (x2 - x1)(to_compare[1] - y1) - (to_compare[0] - x1)(y2 - y1)

    position = ((y2 - y1) * (to_compare[0] - x1)) - ((x2 - x1) * (to_compare[1] - y1))
    if position == 0:
        return 0
    return 1 if (position > 0) else 2


def find_leftmost(data_set):
    leftmost = data_set[0]
    for point in data_set:
        # If x coord in leftmost is > x coord of point.
        if leftmost[0] > point[0]:
            leftmost = point
    return leftmost


def find_rightmost(data_set):
    rightmost = data_set[0]
    for point in data_set:
        # If x coord in rightmost is < x coord of point.
        if rightmost[0] < point[0]:
            rightmost = point
    return rightmost


def quickhull(data_set):
    convex_hull = []
    leftmost = find_leftmost(data_set)
    rightmost = find_rightmost(data_set)
    convex_hull.append(leftmost)
    convex_hull.append(rightmost)
    # Split points into upper and lower.
    upper_hull = []
    lower_hull = []
    for point in data_set:
        if point != leftmost and point != rightmost:
            side = find_side(point, leftmost, rightmost)
            if side == 1:
                lower_hull.append(point)
            if side == 2:
                upper_hull.append(point)

    convex_hull = convex_hull + mini_hull(leftmost, rightmost, upper_hull) + mini_hull(leftmost, rightmost, lower_hull)

    return convex_hull


def mini_hull(line_start, line_end, data_set):
    # recursive helper for quickhull
    if not data_set:
        return data_set
    if len(data_set) == 1:
        return data_set
    convex_hull = []
    furthest = data_set[0]
    # Ensure that furthest does not clash with leftmost or rightmost.

    max_dist = rel_distance(line_start, line_end, furthest)
    for point in data_set:
        temp_furthest = rel_distance(line_start, line_end, point)
        if temp_furthest > max_dist:
            furthest = point
            max_dist = temp_furthest
    convex_hull.append(furthest)
    left_data = []
    right_data = []

    if find_side(line_start, line_end, furthest) == 1:
        # If it's the right-side hull, make sure that it's checking the line made from starting with furthest.
        for point in data_set:
            # If point is on the left side from line_start to furthest, add to left hull.
            if find_side(point, furthest, line_start) == 2:
                left_data.append(point)
            elif find_side(point, line_end, furthest) == 2:
                right_data.append(point)
    else:
        for point in data_set:
            # If point is on the left side from line_start to furthest, add to left hull.
            if find_side(point, line_start, furthest) == 2:
                left_data.append(point)
            elif find_side(point, furthest, line_end) == 2:
                right_data.append(point)
    convex_hull = convex_hull + mini_hull(line_start, furthest, left_data) + mini_hull(furthest, line_end, right_data)

    return convex_hull


def rel_distance(line_start, line_end, to_compare):
    # Returns relative distance from the line made by line_start and line_end
    x1, y1 = line_start[0], line_start[1]
    x2, y2 = line_end[0], line_end[1]

    # value = (x2 - x1)(to_compare[1] - y1) - (to_compare[0] - x1)(y2 - y1)
    return abs((y2 - y1) * (to_compare[0] - x1) - ((x2 - x1) * (to_compare[1] - y1)))


def sort_clockwise(data):
    # Find center of shape.
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    # Contains array of tuples of (point, angle)
    angles = []
    centroid = (sum(x) / len(data), sum(y) / len(data))
    for point in data:
        angle = (math.atan2(point[1] - centroid[1], point[0] - centroid[0]))
        angles.append((point, angle))
    angles.sort(key=lambda p: p[1])
    return [p[0] for p in angles]


def gen_gift_wrap_lines(data):
    '''

    :param data: array of tuples [(x, y), . . .]
    :return: array of tuples of tuples [[(x1, y1), (x2, y2)], . . .]
    '''
    fixed = []
    data_len = len(data)
    for i in range(0, data_len):
        if i < data_len - 1:
            line = (data[i], data[i + 1])
        else:
            # makes it connect back to the first point.
            line = (data[i], data[0])
        fixed.append(line)
    return fixed


def gen_quick_lines(data):
    fixed = []
    data_len = len(data)
    for i in range(0, data_len - 1, 2):
        line = (data[i], data[i + 1])
        fixed.append(line)
    return fixed


def compare_hulls(hull1, hull2, hull3):
    hull1_counter = Counter(hull1)
    if hull1_counter == Counter(hull2) :
        return hull1_counter == Counter(hull3)


def time_hull(data_set, timeit_string, result, i):
    iterate_num = 4

    # Do 10 -> 100 -> 1000 -> 10000
    setup_code = f'''
from __main__ import gift_wrap, quickhull, brutehull
from scipy.spatial import ConvexHull as scipy_hull
data_set = {data_set}
    '''

    result[i] = timeit.timeit(timeit_string, setup=setup_code, number=iterate_num) / iterate_num


def draw_convex_hull(hull, type):
    hull_types = {"gift_wrap": 0, "quick_hull": 1, "brute_hull": 2}
    type_hull = hull_types[type]
    if type_hull == 0:
        hull = gen_gift_wrap_lines(hull)
    if type_hull == 1:
        hull = gen_gift_wrap_lines(sort_clockwise(hull))

    for line in hull:
        plt.plot(*zip(*line), color="red")


def write_to_csv(data, data_count, filename, i):
    hull_names = ["scipy", "gift_wrap", "quickhull", "brutehull"]
    with open(filename, mode="a") as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',')
        # Super janky but whatever.
        if i == 0:
            data_writer.writerow(["Data Count:"] + hull_names)
        data_writer.writerow([data_count] + data[:])


def main():
    csv_filename = "./output/results.csv"
    timeit_strings = ["scipy_hull(data_set)", "gift_wrap(data_set)", "quickhull(data_set)", "brutehull(data_set)"]
    if os.path.isfile(csv_filename):
        os.remove(csv_filename)
    else:
        print("CSV DELETION ERROR")
    data_count = [10, 100, 1000]
    rand_min, rand_max = 0, [50, 500, 5000]

    # data_count = [10, 100, 1000, 10000, 100000]
    # rand_min, rand_max = 0, [50, 500, 5000, 50000, 500000]

    for count in range(len(data_count)):
        results = multiprocessing.Array("d", [-1] * len(timeit_strings))
        data_set = list(gen_data(data_count[count], rand_min, rand_max[count]))
        for string in timeit_strings:
            p = multiprocessing.Process(target=time_hull, name="time_hull", args=(data_set, string,
                                                                                  results, timeit_strings.index(string)))
            p.start()
            # If it takes longer than 60 seconds for the function to run, terminate it.
            p.join(60)
            if p.is_alive():
                print("Killing process. {0} for {1} is taking too long.".format(string, data_count[count]))
                p.terminate()
                p.join()
        write_to_csv(results, data_count[count], csv_filename, count)
    # Data sets to test: Random, Circle, Star?, Parallel lines?
    # plt.scatter(*zip(*data_set))


    # print("Brute hull time: {}".format(times))
    # hull_names = ["scipy", "gift_wrap", "quickhull", "brutehull"]
    '''
    hull = brutehull(data_set)
    draw_convex_hull(hull, "brute_hull")
    plt.show()
    '''


if __name__ == "__main__":
    main()
