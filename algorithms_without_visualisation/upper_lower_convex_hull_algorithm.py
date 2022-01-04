from additional_functions.additional_functions import *


def upper_lower_convex_hull(points, epsilon=10 ** (-12)):
    if len(points) < 3:
        return None
    sorted_points = sorted(points, key=lambda x: (x[0], x[1]))

    # upper convex hull
    upper_hull = [sorted_points[0], sorted_points[1]]

    for idx, value in enumerate(sorted_points[2:]):
        while len(upper_hull) > 1 and orientation(upper_hull[-2], upper_hull[-1], value, epsilon) != 1:
            upper_hull.pop()
        upper_hull.append(value)

    # lower convex hull
    lower_hull = [sorted_points[0], sorted_points[1]]

    for idx, value in enumerate(sorted_points[2:]):
        while len(lower_hull) > 1 and orientation(lower_hull[-2], lower_hull[-1], value, epsilon) != -1:
            lower_hull.pop()
        lower_hull.append(value)
    lower_hull.reverse()
    upper_hull.pop()
    lower_hull.pop()
    upper_hull.extend(lower_hull)
    return upper_hull
