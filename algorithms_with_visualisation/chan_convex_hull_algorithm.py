from visualization.visualization_tool import *
from algorithms_without_visualisation.graham_convex_hull_algorithm import graham_convex_hull
from additional_functions.additional_functions import *
from copy import deepcopy
from math import ceil, sqrt
from random import choice


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
    else:
        if det(hull[0], p, hull[mid]) > -epsilon and \
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
    else:
        return find_tangent(p, hull, l, mid - 1, length, epsilon)


def find_next_point(points, C, hull, p, scenes, epsilon):
    idx_x, idx_y = p
    next_p = (idx_x, (idx_y + 1) % len(C[idx_x]))
    for k in range(len(C)):
        if k != idx_x:
            curr_hull = C[k]
            tang = find_tangent(C[idx_x][idx_y], curr_hull, 0, len(curr_hull) - 1, len(curr_hull), epsilon)
            if tang is not None:
                current_convex_lines = create_lines(hull)
                scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                            PointsCollection(deepcopy(hull), color="blue"),
                                            PointsCollection(C[k], color="red"),
                                            PointsCollection([C[k][tang]], color="green"),
                                            PointsCollection([C[next_p[0]][next_p[1]]], color="yellow")],
                                    lines=[LinesCollection(deepcopy(current_convex_lines), color="blue"),
                                           LinesCollection([[hull[len(hull) - 1],
                                                             C[next_p[0]][next_p[1]]]], color="yellow"),
                                           LinesCollection([[hull[len(hull) - 1], C[k][tang]]], color="green"),
                                           LinesCollection(create_lines(C[k]), color="red")]))
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


def partial_hull(points, m, scenes, epsilon):
    groups = divide_on_groups(points, m)
    C = [graham_convex_hull(groups[i]) for i in range(len(groups))]

    colors = ["green", "red", "blue", "black", "purple", "yellow", "orange", "brown", "pink", "cyan", "olive"]
    scenes_colors = [choice(colors) for _ in range(len(groups))]
    scenes.append(Scene(points=[PointsCollection(groups[i], color=scenes_colors[i]) for i in range(len(groups))]))
    all_lines = [create_lines(C[i]) for i in range(len(groups))]
    scenes.append(Scene(points=[PointsCollection(C[i], color=scenes_colors[i]) for i in range(len(groups))],
                        lines=[LinesCollection(all_lines[i], color=scenes_colors[i]) for i in range(len(groups))]))

    point = (0, 0)
    current_convex_hull = []
    for _ in range(m):
        current_convex_hull.append(C[point[0]][point[1]])

        current_convex_lines = create_lines(current_convex_hull)
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                    PointsCollection(deepcopy(current_convex_hull), color="blue")],
                            lines=[LinesCollection(deepcopy(current_convex_lines), color="blue")]))

        next_point = find_next_point(points, C, current_convex_hull, point, scenes, epsilon)
        if next_point == (0, 0):
            return current_convex_hull
        point = next_point
    return None


def chan_convex_hull(points, epsilon=10 ** (-12), write_to_file=False, filename="chan_result"):
    scenes = [Scene(points=[PointsCollection(deepcopy(points), color="black")])]
    convex_hull = None
    m = 4
    while convex_hull is None:
        convex_hull = partial_hull(points, m, scenes, epsilon)
        m = min(m * m, len(points))
    convex_hull_lines = create_lines(convex_hull)
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection(deepcopy(convex_hull_lines), color="blue")]))
    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hull:
                file.write(f"{item}\n")
    return convex_hull, scenes
