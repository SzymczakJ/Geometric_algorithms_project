from Geometric_algorithms_project.additional_functions.det import det

def is_in_polygon(polygon, point):
    n = len(polygon)
    for i in range(n):
        if det(polygon[i], polygon[(i + 1) % n], point) > 0:
            return False

    return True


def compute_tangent(polygon, point):
    n = len(polygon)
    # indeks 0 - lewa styczna, indeks 1 - prawa styczna
    tangents = [0, 0]

    prev_orientation = det(polygon[0], polygon[1], point)
    i = 1
    while i < n:
        current_orientation = det(polygon[i], polygon[(i + 1) % n], point)
        if current_orientation != prev_orientation and prev_orientation != 0:
            tangents[0] = i
            prev_orientation = current_orientation
            i += 1
            break
        prev_orientation = current_orientation
        i += 1

    while i < n:
        current_orientation = det(polygon[i], polygon[(i + 1) % n], point)
        if current_orientation != prev_orientation and prev_orientation != 0:
            tangents[1] = i
            prev_orientation = current_orientation
            i += 1
            break
        prev_orientation = current_orientation
        i += 1

    if det(polygon[tangents[0]], polygon[tangents[1]], point) == -1:
        tangents[0], tangents[1] = tangents[1], tangents[0]

    return tangents


def polygon_to_lines(polygon):
    lines = []
    n = len(polygon)
    lines.append((polygon[n - 1], polygon[0]))
    for i in range(n - 1):
        lines.append((polygon[i], polygon[i + 1]))
    return lines


def incremental_convex_hull(points, epsilon=10 ** (-12), write_to_file=False, filename="incremental_convex_hull"):
    n = len(points)
    convex_hull = [points[0], points[1], points[2]]

    if det(convex_hull[0], convex_hull[1], convex_hull[2]) == 1:
        convex_hull[1], convex_hull[2] = convex_hull[2], convex_hull[1]
    if n == 3:
        if write_to_file:
            with open(f'{filename}.txt', 'w') as file:
                for item in convex_hull:
                    file.write(f"{item}\n")
        return convex_hull

    for i in range(3, n):
        if not is_in_polygon(convex_hull, points[i]):
            left_tangent_index, right_tangent_index = compute_tangent(convex_hull, points[i])
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

    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hull:
                file.write(f"{item}\n")
    return convex_hull