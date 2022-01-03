from Geometric_algorithms_project.additional_functions.det import det as orientation
from incremental_convex_hull_algorithm import incremental_convex_hull

def polygon_to_lines(polygon):
    lines = []
    n = len(polygon)
    lines.append((polygon[n - 1], polygon[0]))
    for i in range(n - 1):
        lines.append((polygon[i], polygon[i + 1]))
    return lines

def merge_hulls(left_convex_hull, right_convex_hull):
    right_n = len(right_convex_hull)
    left_n = len(left_convex_hull)
    rightmost_point = 0
    for i in range(left_n):
        if left_convex_hull[i][0] > left_convex_hull[rightmost_point][0]:
            rightmost_point = i
    leftmost_point = 0
    for i in range(right_n):
        if left_convex_hull[i][0] > right_convex_hull[leftmost_point][0]:
            leftmost_point = i
    left_convex_point = rightmost_point
    right_convex_point = leftmost_point

    while orientation(left_convex_hull[left_convex_point], right_convex_hull[right_convex_point],
                      right_convex_hull[(right_convex_point + 1) % right_n]) != -1 or orientation(
            right_convex_hull[right_convex_point], left_convex_hull[left_convex_point],
            left_convex_hull[(left_convex_point - 1) % left_n]) != 1:
        while orientation(left_convex_hull[left_convex_point], right_convex_hull[right_convex_point],
                          right_convex_hull[(right_convex_point + 1) % right_n]) != -1:
            right_convex_point = (right_convex_point + 1) % right_n
        while orientation(right_convex_hull[right_convex_point], left_convex_hull[left_convex_point],
                          left_convex_hull[(left_convex_point - 1) % left_n]) != 1:
            left_convex_point = (left_convex_point - 1) % left_n
    points_of_tangent = [left_convex_point, right_convex_point]

    left_convex_point = rightmost_point
    right_convex_point = leftmost_point
    while orientation(left_convex_hull[left_convex_point], right_convex_hull[right_convex_point],
                      right_convex_hull[(right_convex_point - 1) % right_n]) != 1 or orientation(
            right_convex_hull[right_convex_point], left_convex_hull[left_convex_point],
            left_convex_hull[(left_convex_point + 1) % left_n]) != -1:
        while orientation(left_convex_hull[left_convex_point], right_convex_hull[right_convex_point],
                          right_convex_hull[(right_convex_point - 1) % right_n]) != 1:
            right_convex_point = (right_convex_point - 1) % right_n
        while orientation(right_convex_hull[right_convex_point], left_convex_hull[left_convex_point],
                          left_convex_hull[(left_convex_point + 1) % left_n]) != -1:
            left_convex_point = (left_convex_point + 1) % left_n
    points_of_tangent.append(left_convex_point)
    points_of_tangent.append(right_convex_point)

    res = [left_convex_hull[points_of_tangent[0]]]
    i = points_of_tangent[1]
    while i != points_of_tangent[3]:
        res.append(right_convex_hull[i])
        i = (i + 1) % right_n
    res.append(right_convex_hull[points_of_tangent[3]])
    i = points_of_tangent[2]
    while i != points_of_tangent[0]:
        res.append(left_convex_hull[i])
        i = (i + 1) % left_n
    return res


def divide_and_conquer(points, epsilon=10 ** (-12), write_to_file=False, filename="divide_and_conquer"):
    prev_points_division = [sorted(points, key=lambda x: x[0])]
    new_points_division = []

    while len(prev_points_division[0]) > 5:
        for points_group in prev_points_division:
            new_points_division.append(points_group[:int((len(points_group) + 1) / 2)])
            new_points_division.append(points_group[int((len(points_group) + 1) / 2):])
        prev_points_division = new_points_division
        new_points_division = []

    convex_hulls = [0] * len(prev_points_division)
    for i in range(len(prev_points_division)):
        convex_hulls[i] = incremental_convex_hull(prev_points_division[i])

    lines_to_draw = []
    for i in range(len(convex_hulls)):
        lines = polygon_to_lines(convex_hulls[i])
        for line in lines:
            lines_to_draw.append(line)

    new_convex_hulls = []
    while len(convex_hulls) > 1:
        i = 0
        while i + 1 < len(convex_hulls):
            new_convex_hulls.append(merge_hulls(convex_hulls[i], convex_hulls[i + 1]))
            i += 2
        convex_hulls = new_convex_hulls
        new_convex_hulls = []

        lines_to_draw = []
        for i in range(len(convex_hulls)):
            lines = polygon_to_lines(convex_hulls[i])
            for line in lines:
                lines_to_draw.append(line)

    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hulls:
                file.write(f"{item}\n")

    return convex_hulls[0]