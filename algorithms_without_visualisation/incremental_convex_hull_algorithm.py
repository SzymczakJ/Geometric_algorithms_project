from additional_functions.additional_functions import *


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


def incremental_convex_hull(points, epsilon=10 ** (-12)):
    n = len(points)
    if n < 3:
        return None
    convex_hull = [points[0], points[1], points[2]]

    if orientation(convex_hull[0], convex_hull[1], convex_hull[2], epsilon) == 1:
        convex_hull[1], convex_hull[2] = convex_hull[2], convex_hull[1]
    if n == 3:
        return convex_hull

    for i in range(3, n):
        if not is_in_polygon(convex_hull, points[i], epsilon):
            left_tangent_index, right_tangent_index = compute_tangent(convex_hull, points[i], epsilon)
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
    return convex_hull
