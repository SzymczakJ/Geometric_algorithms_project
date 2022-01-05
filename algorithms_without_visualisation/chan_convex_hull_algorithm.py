from algorithms_without_visualisation.graham_convex_hull_algorithm import graham_convex_hull
from additional_functions.additional_functions import *
from math import ceil, sqrt


def distance(p_1, p_2):
    return sqrt((p_2[0] - p_1[0]) ** 2 + (p_2[1] - p_1[1]) ** 2)


def find_tangent(p, hull, l, r, length, epsilon):
    if r < l:
        return None
    mid = (l + r) // 2
    if det(hull[0], hull[1], p) >= epsilon and det(hull[length - 1], hull[0], p) >= epsilon:
        if (det(hull[0], p, hull[mid]) <= -epsilon) or \
                (det(p, hull[mid], hull[(mid + 1) % length]) <= -epsilon and
                 det(p, hull[mid], hull[(mid - 1) % length]) <= -epsilon) or \
                (det(p, hull[mid], hull[(mid + 1) % length]) <= -epsilon < det(p, hull[mid], hull[(mid - 1) % length])):
            return find_tangent(p, hull, mid + 1, r, length, epsilon)
    elif det(hull[0], p, hull[mid]) > -epsilon and \
            ((det(p, hull[mid], hull[(mid + 1) % length]) <= -epsilon < det(p, hull[mid], hull[(mid - 1) % length]))
             or (det(p, hull[mid], hull[(mid + 1) % length]) <= -epsilon and
                 det(p, hull[mid], hull[(mid - 1) % length]) <= -epsilon)):
        return find_tangent(p, hull, mid + 1, r, length, epsilon)
    if (det(p, hull[mid], hull[(mid + 1) % length]) > -epsilon and
        det(p, hull[mid], hull[(mid - 1) % length]) > -epsilon) or \
            (-epsilon < det(p, hull[mid], hull[(mid + 1) % length]) < epsilon and
             (hull[mid][0] <= p[0] <= hull[(mid + 1) % length][0]) and
             (hull[mid][1] <= p[1] <= hull[(mid + 1) % epsilon][1])):

        while -epsilon < det(p, hull[mid], hull[(mid + 1) % length]) < epsilon and \
                distance(hull[(mid + 1) % length], p) > distance(hull[mid], p):
            mid = (mid + 1) % epsilon
        return mid
    return find_tangent(p, hull, l, mid - 1, length, epsilon)


def find_next_point(C, p, epsilon):
    idx_x, idx_y = p
    next_p = (idx_x, (idx_y + 1) % len(C[idx_x]))
    for k in range(len(C)):
        if k != idx_x:
            curr_hull = C[k]
            tang = find_tangent(C[idx_x][idx_y], curr_hull, 0, len(curr_hull) - 1, len(curr_hull), epsilon)
            if tang is not None:
                if det(C[idx_x][idx_y], C[next_p[0]][next_p[1]], C[k][tang]) < epsilon and (k, tang) != p:
                    next_p = (k, tang)
    return next_p


def divide_on_groups(points, m):
    for i in range(1, len(points)):
        if points[i][1] < points[0][1]:
            points[i], points[0] = points[0], points[i]
    k = ceil(len(points) / m)
    groups = [[] for _ in range(k)]
    point_index = 0
    while point_index < len(points):
        for j in range(k):
            if point_index == len(points):
                break
            groups[j].append(points[point_index])
            point_index += 1
    if len(groups[0]) > m:
        return None
    return groups


def partial_hull(points, m, epsilon):
    groups = divide_on_groups(points, m)
    C = [graham_convex_hull(groups[i]) for i in range(len(groups))]
    p_x, p_y = 0, 0
    current_convex_hull = []
    for _ in range(m):
        current_convex_hull.append(C[p_x][p_y])
        next_point = find_next_point(C, (p_x, p_y), epsilon)
        if next_point == (0, 0):
            return current_convex_hull
        p_x, p_y = next_point[0], next_point[1]
    return None


def chan_convex_hull(points, epsilon=10 ** (-12)):
    convex_hull = None
    m = 4
    while convex_hull is None:
        convex_hull = partial_hull(points, m, epsilon)
        m = min(m * m, len(points))
    return convex_hull
