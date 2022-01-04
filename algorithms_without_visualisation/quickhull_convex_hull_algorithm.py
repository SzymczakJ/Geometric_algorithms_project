from additional_functions.additional_functions import *


def det(a, b, c):
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = c
    first = (a_x - c_x) * (b_y - c_y)
    second = (a_y - c_y) * (b_x - c_x)
    return first - second


def calculate_distance(points, p_1, p_2):
    result = None
    for i in range(len(points)):
        if orientation(p_1, p_2, points[i]) == 1:
            if result is None or det(p_1, p_2, points[i]) < det(p_1, p_2, result):
                result = points[i]
    return result


def is_inside(p_1, p_2, p_3, p, epsilon):
    if det(p_1, p_2, p) > -epsilon and det(p_2, p_3, p) > -epsilon and det(p_3, p_1, p) > -epsilon:
        return True
    return False


def remove_points_inside(points, p_1, p_2, p_3, epsilon):
    new_points = []
    for p in points:
        if not is_inside(p_1, p_2, p_3, p, epsilon):
            new_points.append(p)
    points.clear()
    points += new_points


def recursive_quickhull(points, convex_hull, p_1, p_2, epsilon):
    if len(points) == 0:
        return []

    p_3 = calculate_distance(points, p_1, p_2)
    if p_3 is None:
        return []
    points.remove(p_3)
    convex_hull.append(p_3)

    remove_points_inside(points, p_1, p_2, p_3, epsilon)

    return recursive_quickhull(points, convex_hull, p_1, p_3, epsilon) + [p_3] + \
           recursive_quickhull(points, convex_hull, p_3, p_2, epsilon)


def quickhull_convex_hull(points, epsilon=10 ** (-12)):
    if len(points) < 3:
        return None
    sorted_points = sorted(points, key=lambda x: x[0])
    p_1 = sorted_points[0]
    p_2 = sorted_points[-1]

    sorted_points.remove(p_1)
    sorted_points.remove(p_2)
    convex_hull = [p_1, p_2]
    hull = [p_1] + recursive_quickhull(sorted_points, convex_hull, p_1, p_2, epsilon) + \
           [p_2] + recursive_quickhull(sorted_points, convex_hull, p_2, p_1, epsilon)
    return hull
