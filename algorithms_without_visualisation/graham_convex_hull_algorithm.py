from additional_functions.additional_functions import *
from collections import deque
from functools import cmp_to_key


def graham_convex_hull(points, epsilon=10 ** (-12)):
    length = len(points)
    lowest_point = points[0]
    for i in range(length):
        if abs(lowest_point[1] - points[i][1]) < epsilon:
            if lowest_point[0] > points[i][0]:
                lowest_point = points[i]
        elif lowest_point[1] > points[i][1]:
            lowest_point = points[i]

    def graham_cmp(point_a, point_b):
        if point_a[0] == lowest_point[0] and point_a[1] == lowest_point[1]:
            return -1
        elif point_b[0] == lowest_point[0] and point_b[1] == lowest_point[1]:
            return 1
        orient = det(lowest_point, point_a, point_b)
        if orient < -epsilon:
            return 1
        elif epsilon > orient > -epsilon:
            if point_a[1] > point_b[1]:
                return 1
            elif point_a[1] < point_b[1]:
                return -1
            elif abs(point_a[0] - lowest_point[0]) > abs(point_b[0] - lowest_point[0]):
                return 1
            elif abs(point_a[0] - lowest_point[0]) < abs(point_b[0] - lowest_point[0]):
                return -1
            else:
                return 0
        else:
            return -1

    graham_cmp_key = cmp_to_key(graham_cmp)
    sorted_set = sorted(points, key=graham_cmp_key)
    convex_hull = deque()
    convex_hull.append(sorted_set[0])
    convex_hull.append(sorted_set[1])
    i = 2
    while i < length:
        if (convex_hull[0][0] == convex_hull[-1][0] and convex_hull[0][1] == convex_hull[-1][1]) or \
                det(convex_hull[-2], convex_hull[-1], sorted_set[i]) > epsilon:
            convex_hull.append(sorted_set[i])
            i += 1
        else:
            convex_hull.pop()
    return convex_hull
