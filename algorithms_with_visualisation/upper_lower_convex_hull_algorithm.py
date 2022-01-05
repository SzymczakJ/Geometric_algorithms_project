from visualization.visualization_tool import *
from additional_functions.additional_functions import *
from copy import deepcopy


def upper_lower_convex_hull(points, epsilon=10 ** (-12), write_to_file=False, filename="upper_lower_result"):
    if len(points) < 3:
        return None, None
    sorted_points = sorted(points, key=lambda x: (x[0], x[1]))

    # creating scenes for visualization
    scenes = [Scene(points=[PointsCollection(deepcopy(points), color="black")])]

    # upper convex hull
    upper_hull = [sorted_points[0], sorted_points[1]]
    upper_hull_lines = [(sorted_points[0], sorted_points[1])]

    for idx, value in enumerate(sorted_points[2:]):
        # adding scenes for visualization
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                    PointsCollection([upper_hull[-1]], color="blue"),
                                    PointsCollection([upper_hull[-2]], color="blue"),
                                    PointsCollection(deepcopy(upper_hull), color="green")],
                            lines=[LinesCollection([[upper_hull[-2], value]], color="red"),
                                   LinesCollection([[upper_hull[-1], value]], color="red"),
                                   LinesCollection(deepcopy(upper_hull_lines), color="green")]))

        while len(upper_hull) > 1 and orientation(upper_hull[-2], upper_hull[-1], value, epsilon) != 1:
            upper_hull.pop()
            upper_hull_lines.pop()

            # adding scenes for visualization
            scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                        PointsCollection(deepcopy(upper_hull), color="green"),
                                        PointsCollection([value], color="red")],
                                lines=[LinesCollection(deepcopy(upper_hull_lines), color="red"),
                                       LinesCollection([[upper_hull[-1], value]], color="yellow")]))

        upper_hull.append(value)
        upper_hull_lines.append((upper_hull[-2], upper_hull[-1]))

    # lower convex hull
    lower_hull = [sorted_points[0], sorted_points[1]]
    lower_hull_lines = [(sorted_points[0], sorted_points[1])]

    for idx, value in enumerate(sorted_points[2:]):
        # adding scenes for visualization
        scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                    PointsCollection([lower_hull[-1]], color="blue"),
                                    PointsCollection([lower_hull[-2]], color="blue"),
                                    PointsCollection(deepcopy(lower_hull), color="green")],
                            lines=[LinesCollection(deepcopy(upper_hull_lines), color="blue"),
                                   LinesCollection(deepcopy(lower_hull_lines), color="red"),
                                   LinesCollection([[lower_hull[-2], value]], color="red"),
                                   LinesCollection([[lower_hull[-1], value]], color="red")]))

        while len(lower_hull) > 1 and orientation(lower_hull[-2], lower_hull[-1], value, epsilon) != -1:
            lower_hull.pop()
            lower_hull_lines.pop()

            # adding scenes for visualization
            scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                        PointsCollection(deepcopy(lower_hull), color="green"),
                                        PointsCollection([value], color="red")],
                                lines=[LinesCollection(deepcopy(upper_hull_lines), color="blue"),
                                       LinesCollection(deepcopy(lower_hull_lines), color="red"),
                                       LinesCollection([[lower_hull[-1], value]], color="yellow")]))

        lower_hull.append(value)
        lower_hull_lines.append((lower_hull[-2], lower_hull[-1]))

    # adding scenes for visualization
    scenes.append(Scene(points=[PointsCollection(deepcopy(points), color="black"),
                                PointsCollection(deepcopy(upper_hull), color="blue"),
                                PointsCollection(deepcopy(lower_hull), color="green")],
                        lines=[LinesCollection(deepcopy(upper_hull_lines), color="blue"),
                               LinesCollection(deepcopy(lower_hull_lines), color="green")]))

    lower_hull.reverse()
    upper_hull.pop()
    lower_hull.pop()
    convex_hull = upper_hull + lower_hull
    if write_to_file:
        with open(f'{filename}.txt', 'w') as file:
            for item in convex_hull:
                file.write(f"{item}\n")
    return convex_hull, scenes
