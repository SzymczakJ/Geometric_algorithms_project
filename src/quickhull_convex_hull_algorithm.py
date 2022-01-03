from visualization.visualization_tool import *
from additional_functions.additional_functions import *
from copy import deepcopy


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


def create_hull_lines(hull):
    lines = []
    for i in range(len(hull) - 1):
        lines.append([hull[i], hull[i + 1]])
    lines.append([hull[len(hull) - 1], hull[0]])
    return lines


def recursive_quickhull(points, convex_hull, p_1, p_2, scenes, epsilon):
    if len(points) == 0:
        return []

    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection(deepcopy([[p_1, p_2]]), color="red")]))

    p_3 = calculate_distance(points, p_1, p_2)
    if p_3 is None:
        return []
    points.remove(p_3)
    convex_hull.append(p_3)

    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue"),
                                PointsCollection([p_3], color="red")],
                        lines=[LinesCollection(deepcopy([[p_1, p_2]]), color="red")]))

    remove_points_inside(points, p_1, p_2, p_3, epsilon)

    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection([[p_1, p_2], [p_1, p_3], [p_2, p_3]], color="red")]))

    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection([[p_2, p_3]], color="red")]))

    return recursive_quickhull(points, convex_hull, p_1, p_3, scenes, epsilon) + [p_3] + \
           recursive_quickhull(points, convex_hull, p_3, p_2, scenes, epsilon)


def quickhull_convex_hull(points, epsilon=10 ** (-12), write_to_file=False, filename="quickhull_result"):
    if len(points) < 3:
        return None, None
    sorted_points = sorted(points, key=lambda x: x[0])
    p_1 = sorted_points[0]
    p_2 = sorted_points[-1]

    scenes = [Scene(points=[PointsCollection(deepcopy(sorted_points), color="black")])]

    sorted_points.remove(p_1)
    sorted_points.remove(p_2)
    convex_hull = [p_1, p_2]
    hull = [p_1] + recursive_quickhull(sorted_points, convex_hull, p_1, p_2, scenes, epsilon) + \
           [p_2] + recursive_quickhull(sorted_points, convex_hull, p_2, p_1, scenes, epsilon)

    hull_lines = create_hull_lines(hull)
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection(deepcopy(hull_lines), color="blue")]))
    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hull:
                file.write(f"{item}\n")
    return hull, scenes
