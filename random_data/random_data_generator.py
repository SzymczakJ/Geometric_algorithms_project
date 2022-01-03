from random import uniform
from math import pi, cos, sin, inf


def random_points_on_the_range(num_of_points, ranges):
    random_points = [None for _ in range(num_of_points)]
    for i in range(num_of_points):
        random_x = uniform(ranges[0], ranges[1])
        random_y = uniform(ranges[0], ranges[1])
        random_points[i] = (random_x, random_y)
    return random_points


def random_points_on_the_circle(num_of_points, center, R):
    random_points = [None for _ in range(num_of_points)]
    for i in range(num_of_points):
        alpha = 2 * pi * uniform(0, 1)
        random_points[i] = (R * cos(alpha) + center[0], R * sin(alpha) + center[1])
    return random_points


def random_points_on_the_rectangle(num_of_points, vertices):
    min_y = min_x = inf
    max_y = max_x = inf
    for v in vertices:
        min_x = min(min_x, v[0])
        min_y = min(min_y, v[1])
        max_x = max(max_x, v[0])
        max_y = max(max_y, v[1])

    x_side = abs(max_x - min_x)
    y_side = abs(max_y - min_y)
    total_range = 2 * x_side + 2 * y_side
    ranges = [(0, y_side), (y_side, 2 * y_side),
              (2 * y_side, 2 * y_side + x_side), (2 * y_side + x_side, total_range)]

    # Każdy bok ma swój przedział, dzięki temu otrzymujemy jeden duży przedział w którym
    # losowany jest 1 punkt i jest przydzielany do odpowiedniego boku. Taki podział
    # generowania punktów na bokach prostokąta zapewnia najlepszy rozkład
    # prawdopodobieństwa dla różnych długości boków.

    random_points = []
    for v in vertices:
        random_points.append(v)

    for _ in range(num_of_points - 4):
        point = uniform(0, total_range)

        # left side
        if ranges[0][0] <= point <= ranges[0][1]:
            result = (min_x, min_y + point)

        # right side
        elif ranges[1][0] < point <= ranges[1][1]:
            result = (max_x, min_y + (point - ranges[1][0]))

        # bottom side
        elif ranges[2][0] < point <= ranges[2][1]:
            result = (min_x + (point - ranges[2][0]), min_y)

        # upper side
        else:
            result = (min_x + (point - ranges[3][0]), max_y)
        random_points.append(result)
    return random_points


def random_points_on_square(side_num_of_points, diag_num_of_points, vertices):
    min_y = min_x = inf
    max_y = max_x = inf
    for v in vertices:
        min_x = min(min_x, v[0])
        min_y = min(min_y, v[1])
        max_x = max(max_x, v[0])
        max_y = max(max_y, v[1])

    side = abs(max_x - min_x)
    total_range = 2 * side

    # Każdy bok ma swój przedział, dzięki temu otrzymujemy jeden duży przedział w którym
    # losowany jest 1 punkt i jest przydzielany do odpowiedniego boku. Taki podział
    # generowania punktów na bokach prostokąta zapewnia najlepszy rozkład
    # prawdopodobieństwa dla różnych długości boków.

    random_points = []
    for v in vertices:
        random_points.append(v)

    # Points on sides of square
    for _ in range(side_num_of_points):
        point = uniform(0, total_range)
        if 0 <= point <= total_range / 2:
            side_result = (min_x, min_y + point)
        else:
            side_result = (min_x + (point - total_range / 2), min_y)
        random_points.append(side_result)

    # Points on diagonals of square
    for _ in range(diag_num_of_points):
        point = uniform(0, total_range)
        if 0 <= point <= total_range / 2:
            diag_result = (min_x + point, min_y + point)
        else:
            diag_result = (min_x + (point - total_range / 2), max_y - (point - total_range / 2))
        random_points.append(diag_result)
    return random_points
