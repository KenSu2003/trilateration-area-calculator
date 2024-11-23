import math
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import matplotlib.pyplot as plt

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
    if points:
        centroid = (
            sum(p[0] for p in points) / len(points),
            sum(p[1] for p in points) / len(points),
        )
        points = sorted(points, key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0]))

    return Polygon(points) if points else Polygon()

def calculate_segment_area(circle, point1, point2):
    """Calculate the area of the circular segment between two points on a circle."""
    cx, cy, r = circle
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the chord length
    chord_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Calculate the angle subtended by the chord at the center of the circle
    angle = 2 * math.asin(chord_length / (2 * r))

    # Area of the circular segment
    segment_area = 0.5 * r ** 2 * (angle - math.sin(angle))
    return segment_area

def calculate_area_of_intersection_with_segments(circles):
    """Calculate the total area of intersection, including segments."""
    polygon = find_polygon_intersection(circles)

    # Polygon area
    polygon_area = polygon.area if not polygon.is_empty else 0
    print(polygon_area)

    # Segment areas
    segment_area = 0
    if not polygon.is_empty:
        coords = list(polygon.exterior.coords)

        for i in range(len(coords) - 1):
            point1 = coords[i]
            point2 = coords[i + 1]

            for circle in circles:
                cx, cy, r = circle
                if ((point1[0] - cx) ** 2 + (point1[1] - cy) ** 2 <= r ** 2 and
                    (point2[0] - cx) ** 2 + (point2[1] - cy) ** 2 <= r ** 2):
                    segment_area += calculate_segment_area(circle, point1, point2)
                    break

    return polygon_area + segment_area

def plot_circles_and_intersection_with_segments(circles, polygon):
    """Plot the circles and shade the full intersection area."""
    fig, ax = plt.subplots()

    # Plot each circle
    for cx, cy, r in circles:
        circle = plt.Circle((cx, cy), r, fill=False, linestyle="--")
        ax.add_artist(circle)
        ax.plot(cx, cy, 'o', label=f"Circle Center ({cx}, {cy})")

    # Plot and shade the intersection polygon
    if not polygon.is_empty and polygon.is_valid:
        x, y = polygon.exterior.xy
        ax.fill(x, y, 'g', alpha=0.4, label="Intersection Area (Shaded)")
        ax.plot(x, y, 'g-', label="Intersection Polygon")

    # Set plot limits and labels
    ax.set_xlim(-300, 300)
    ax.set_ylim(-300, 300)
    ax.set_aspect('equal', adjustable='datalim')
    ax.legend()
    plt.title("Circles and Intersection Area (Including Segments)")
    plt.show()

# Example usage:
circles = [(0, 0, 100), (70, 0, 100), (0, 70, 100)]  # (x, y, radius) for each circle
area = calculate_area_of_intersection_with_segments(circles)
print(f"The area of intersection is: {area:.2f}")

# Plot the circles and the intersection polygon
polygon = find_polygon_intersection(circles)
plot_circles_and_intersection_with_segments(circles, polygon)