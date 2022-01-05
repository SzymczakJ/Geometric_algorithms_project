from visualization.visualization_tool import *
from additional_functions.additional_functions import *
from copy import deepcopy


def is_in_polygon(polygon, point, epsilon):
    n = len(polygon)
    for i in range(n):
        if orientation(polygon[i], polygon[(i + 1) % n], point, epsilon) > 0:
            return False
    return True


def compute_tangent(polygon, point, epsilon):
    n = len(polygon)

    # index 0 - left tangent,
    # index 1 - right tangent,
    tangents = [0, 0]

    prev_orientation = orientation(polygon[0], polygon[1], point, epsilon)
    i = 1
    while i < n:
        current_orientation = orientation(polygon[i], polygon[(i + 1) % n], point, epsilon)
        if current_orientation != prev_orientation and prev_orientation != 0:
            tangents[0] = i
            prev_orientation = current_orientation
            i += 1
            break
        prev_orientation = current_orientation
        i += 1

    while i < n:
        current_orientation = orientation(polygon[i], polygon[(i + 1) % n], point, epsilon)
        if current_orientation != prev_orientation and prev_orientation != 0:
            tangents[1] = i
            i += 1
            break
        prev_orientation = current_orientation
        i += 1

    if orientation(polygon[tangents[0]], polygon[tangents[1]], point, epsilon) == -1:
        tangents[0], tangents[1] = tangents[1], tangents[0]

    return tangents


def incremental_convex_hull(points, epsilon=10 ** (-12), write_to_file=False, filename="incremental_convex_hull"):
    if len(points) < 3:
        return None, None
    n = len(points)
    convex_hull = [points[0], points[1], points[2]]

    # creating scenes for visualization
    scenes = [Scene(points=[PointsCollection(deepcopy(points), color="black")])]

    # adding scenes for visualization
    lines_to_draw = create_lines(convex_hull)
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black")],
                        lines=[LinesCollection(deepcopy(lines_to_draw), color="blue")]))

    if orientation(convex_hull[0], convex_hull[1], convex_hull[2], epsilon) == 1:
        convex_hull[1], convex_hull[2] = convex_hull[2], convex_hull[1]
    if n == 3:
        if write_to_file:
            with open(f'{filename}.txt', 'w') as file:
                for item in convex_hull:
                    file.write(f"{item}\n")
        return convex_hull, scenes

    for i in range(3, n):
        # adding scenes for visualization
        lines_to_draw = create_lines(convex_hull)
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                    PointsCollection([points[i]], color="red")],
                            lines=[LinesCollection(deepcopy(lines_to_draw), color="blue")]))

        if not is_in_polygon(convex_hull, points[i], epsilon):
            left_tangent_index, right_tangent_index = compute_tangent(convex_hull, points[i], epsilon)

            # adding scenes for visualization
            lines_to_draw = create_lines(convex_hull)
            scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                        PointsCollection([points[i]], color="red")],
                                lines=[LinesCollection(deepcopy(lines_to_draw), color="blue"),
                                       LinesCollection([(convex_hull[left_tangent_index], points[i]),
                                                        (convex_hull[right_tangent_index], points[i])], color="red")]))

            if (left_tangent_index + 1) % len(convex_hull) != right_tangent_index:
                right_tangent = convex_hull[right_tangent_index]
                j = (left_tangent_index + 1) % len(convex_hull)
                while convex_hull[j] != right_tangent:
                    convex_hull.pop(j)
                    if j == len(convex_hull):
                        j = 0
                convex_hull.insert(j, points[i])
            else:
                convex_hull.insert(right_tangent_index, points[i])

        # adding scenes for visualization
        lines_to_draw = create_lines(convex_hull)
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black")],
                            lines=[LinesCollection(deepcopy(lines_to_draw), color="blue")]))

    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hull:
                file.write(f"{item}\n")
    return convex_hull, scenes
