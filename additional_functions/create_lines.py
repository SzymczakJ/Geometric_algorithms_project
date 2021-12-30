def create_lines(points):
    lines = []
    for p in range(len(points) - 1):
        lines.append((points[p], points[p + 1]))
    lines.append((points[-1], points[0]))
    return lines
