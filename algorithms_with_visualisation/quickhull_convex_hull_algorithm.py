from visualization.visualization_tool import *
from additional_functions.additional_functions import *
from copy import deepcopy


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


def recursive_quickhull(points, convex_hull, p_1, p_2, scenes, epsilon):
    if len(points) == 0:
        return []

    # adding scenes for visualization
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection(deepcopy([[p_1, p_2]]), color="red")]))

    p_3 = calculate_distance(points, p_1, p_2)
    if p_3 is None:
        return []
    points.remove(p_3)
    convex_hull.append(p_3)

    # adding scenes for visualization
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue"),
                                PointsCollection([p_3], color="red")],
                        lines=[LinesCollection(deepcopy([[p_1, p_2]]), color="red")]))

    remove_points_inside(points, p_1, p_2, p_3, epsilon)

    # adding scenes for visualization
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection([[p_1, p_2], [p_1, p_3], [p_2, p_3]], color="red")]))

    # adding scenes for visualization
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

    # creating scenes for visualization
    scenes = [Scene(points=[PointsCollection(deepcopy(sorted_points), color="black")])]

    sorted_points.remove(p_1)
    sorted_points.remove(p_2)
    curr_hull = [p_1, p_2]
    convex_hull = [p_1] + recursive_quickhull(sorted_points, curr_hull, p_1, p_2, scenes, epsilon) + \
                  [p_2] + recursive_quickhull(sorted_points, curr_hull, p_2, p_1, scenes, epsilon)

    # adding scenes for visualization
    hull_lines = create_lines(convex_hull)
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(curr_hull), color="blue")],
                        lines=[LinesCollection(deepcopy(hull_lines), color="blue")]))

    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in curr_hull:
                file.write(f"{item}\n")
    return convex_hull, scenes
