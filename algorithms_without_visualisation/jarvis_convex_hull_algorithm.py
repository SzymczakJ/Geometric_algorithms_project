from additional_functions.additional_functions import *


def jarvis_convex_hull(points, epsilon=10 ** (-12)):
    length = len(points)
    lowest_point = points[0]
    for i in range(length):
        if abs(lowest_point[1] - points[i][1]) < epsilon:
            if lowest_point[0] > points[i][0]:
                lowest_point = points[i]
        elif lowest_point[1] > points[i][1]:
            lowest_point = points[i]

    convex_hull = [lowest_point]
    first_vector_point = lowest_point
    second_vector_point = lowest_point
    for i in range(length):
        if abs(lowest_point[1] - points[i][1]) < epsilon:
            if second_vector_point[0] < points[i][0]:
                second_vector_point = points[i]
    if second_vector_point[0] == first_vector_point[0] and second_vector_point[1] == first_vector_point[1]:
        second_vector_point = first_vector_point
        first_vector_point = (lowest_point[0] - 1, lowest_point[1])
    else:
        convex_hull.append(second_vector_point)
    next_vector_point = None

    while next_vector_point is None or (
            next_vector_point[0] != lowest_point[0] or next_vector_point[1] != lowest_point[1]):
        next_vector_point = first_vector_point
        for point in points:
            orient = det(second_vector_point, next_vector_point, point)
            if orient < -epsilon:
                next_vector_point = point
            elif -epsilon < orient < epsilon:
                distance_from_next_point = (next_vector_point[1] - second_vector_point[1]) ** 2 + (
                        next_vector_point[0] - second_vector_point[0]) ** 2
                distance_from_point = (point[1] - second_vector_point[1]) ** 2 + \
                                      (point[0] - second_vector_point[0]) ** 2
                if distance_from_point > distance_from_next_point:
                    next_vector_point = point
        convex_hull.append(next_vector_point)
        first_vector_point = second_vector_point
        second_vector_point = next_vector_point
    return convex_hull[:-1]
