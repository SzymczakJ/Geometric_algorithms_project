from visualization.visualization_tool import *
from additional_functions.additional_functions import *
from copy import deepcopy


def jarvis_convex_hull(points, epsilon=10 ** (-12), write_to_file=False, filename="jarvis_result"):
    if len(points) < 3:
        return None, None
    lowest_point = points[0]
    for i in range(len(points)):
        if abs(lowest_point[1] - points[i][1]) < epsilon:
            if lowest_point[0] > points[i][0]:
                lowest_point = points[i]
        elif lowest_point[1] > points[i][1]:
            lowest_point = points[i]

    convex_hull = [lowest_point]

    # creating scenes for visualization
    scenes = [Scene(points=[PointsCollection(deepcopy(points), color="black")])]
    convex_hull_lines = []

    first_vector_point = lowest_point
    second_vector_point = lowest_point
    for i in range(len(points)):
        if abs(lowest_point[1] - points[i][1]) < epsilon:
            if second_vector_point[0] < points[i][0]:
                second_vector_point = points[i]
    if second_vector_point[0] == first_vector_point[0] and second_vector_point[1] == first_vector_point[1]:
        second_vector_point = first_vector_point
        first_vector_point = (lowest_point[0] - 1, lowest_point[1])
    else:
        convex_hull.append(second_vector_point)

        # adding scenes for visualization
        convex_hull_lines.append([convex_hull[0], convex_hull[1]])
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                    PointsCollection(deepcopy(convex_hull), color="blue")],
                            lines=[LinesCollection(deepcopy(convex_hull_lines), color="blue")]))

    next_vector_point = None
    while next_vector_point is None or \
            (next_vector_point[0] != lowest_point[0] or next_vector_point[1] != lowest_point[1]):
        next_vector_point = first_vector_point
        for point in points:
            orient = orientation(second_vector_point, next_vector_point, point, epsilon)
            if orient < -epsilon:
                next_vector_point = point
            elif -epsilon < orient < epsilon:
                distance_from_next_point = (next_vector_point[1] - second_vector_point[1]) ** 2 + \
                                           (next_vector_point[0] - second_vector_point[0]) ** 2
                distance_from_point = (point[1] - second_vector_point[1]) ** 2 + \
                                      (point[0] - second_vector_point[0]) ** 2
                if distance_from_point > distance_from_next_point:
                    next_vector_point = point
        convex_hull.append(next_vector_point)

        # adding scenes for visualization
        convex_hull_lines.append([convex_hull[-2], convex_hull[-1]])
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                    PointsCollection(deepcopy(convex_hull), color="blue")],
                            lines=[LinesCollection(deepcopy(convex_hull_lines), color="blue")]))

        first_vector_point = second_vector_point
        second_vector_point = next_vector_point

    # adding scenes for visualization
    convex_hull.append(next_vector_point)
    convex_hull_lines.append([convex_hull[-2], convex_hull[-1]])
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(convex_hull), color="blue")],
                        lines=[LinesCollection(deepcopy(convex_hull_lines), color="blue")]))

    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hull:
                file.write(f"{item}\n")
    return convex_hull[:-1], scenes
