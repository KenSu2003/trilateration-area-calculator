import math
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

def circle_intersection_points(circle1, circle2):
    """Find intersection points of two circles."""
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    dx, dy = x2 - x1, y2 - y1
    d = math.sqrt(dx ** 2 + dy ** 2)

    if d > r1 + r2 or d < abs(r1 - r2):
        return []  # No intersection or one circle is inside the other

    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - a ** 2)

    xm = x1 + a * dx / d
    ym = y1 + a * dy / d

    xs1 = xm + h * dy / d
    ys1 = ym - h * dx / d

    xs2 = xm - h * dy / d
    ys2 = ym + h * dx / d

    return [(xs1, ys1), (xs2, ys2)]

def find_polygon_intersection(circles):
    """Find the polygon intersection of multiple circles."""
    points = []
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            points += circle_intersection_points(circles[i], circles[j])

    # Keep only points inside all circles
    def is_point_inside_all_circles(point):
        x, y = point
        return all((x - cx) ** 2 + (y - cy) ** 2 <= r ** 2 for cx, cy, r in circles)

    points = [p for p in points if is_point_inside_all_circles(p)]

    # Sort points counterclockwise around the centroid
    centroid = (
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
    )
    points = sorted(points, key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0]))

    return Polygon(points)

def calculate_area_of_intersection(circles):
    """Calculate the area of trilateration for three circles."""
    # Find the polygon intersection
    polygon = find_polygon_intersection(circles)

    # If no valid polygon exists
    if not polygon or not polygon.is_valid or polygon.is_empty:
        return 0

    # Calculate polygon area
    polygon_area = polygon.area

    # Calculate the circle arc areas
    arc_area = 0
    for i in range(len(polygon.exterior.coords) - 1):
        x1, y1 = polygon.exterior.coords[i]
        x2, y2 = polygon.exterior.coords[i + 1]

        for cx, cy, r in circles:
            if ((x1 - cx) ** 2 + (y1 - cy) ** 2 <= r ** 2) and ((x2 - cx) ** 2 + (y2 - cy) ** 2 <= r ** 2):
                angle = math.atan2(y2 - cy, x2 - cx) - math.atan2(y1 - cy, x1 - cx)
                angle = angle if angle >= 0 else 2 * math.pi + angle
                arc_area += 0.5 * r ** 2 * angle
                break

    return polygon_area + arc_area

# Example usage:
circles = [(0, 0, 100), (70, 0, 100), (0, 70, 100)]  # (x, y, radius) for each circle
area = calculate_area_of_intersection(circles)
print(f"The area of trilateration is: {area:.2f}")
