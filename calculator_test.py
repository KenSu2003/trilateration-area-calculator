import math
import matplotlib.pyplot as plt
from sympy import Polygon

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

def is_point_inside_circle(point, circle):
    """Check if a point is inside a circle."""
    x, y = point
    cx, cy, r = circle
    return (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2

def calculate_segment_area(circle, point1, point2):
    """Calculate the area of the circular segment between two points on a circle."""
    cx, cy, r = circle
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the angle subtended by the chord
    dx1, dy1 = x1 - cx, y1 - cy
    dx2, dy2 = x2 - cx, y2 - cy
    angle = math.acos((dx1 * dx2 + dy1 * dy2) / (math.sqrt(dx1**2 + dy1**2) * math.sqrt(dx2**2 + dy2**2)))

    # Segment area formula
    return 0.5 * r**2 * (angle - math.sin(angle))

# Define circles
circleA = [0, 0, 100]
circleB = [70, 0, 100]
circleC = [0, 70, 100]

# Find intersection points
intersect_AB = circle_intersection_points(circleA, circleB)
intersect_BC = circle_intersection_points(circleB, circleC)
intersect_AC = circle_intersection_points(circleA, circleC)

# Filter points inside all three circles
valid_points = []
for points in [intersect_AB, intersect_BC, intersect_AC]:
    for point in points:
        if all((point[0] - cx)**2 + (point[1] - cy)**2 <= r**2 for cx, cy, r in [circleA, circleB, circleC]):
            valid_points.append(point)

# Ensure we have exactly three valid points
if len(valid_points) == 3:
    # Create a triangle using valid points
    triangle = Polygon(*valid_points)
    triangle_area = abs(triangle.area)

    # Calculate segment areas
    segment_area = 0
    for circle, (p1, p2) in zip([circleA, circleB, circleC], [(valid_points[0], valid_points[1]),
                                                             (valid_points[1], valid_points[2]),
                                                             (valid_points[2], valid_points[0])]):
        segment_area += calculate_segment_area(circle, p1, p2)

    # Total overlap area
    total_overlap_area = triangle_area + segment_area

    # Print results
    print("Triangle Vertices:", triangle.vertices)
    print(f"Triangle Area = {triangle_area:.2f}")
    print(f"Segment Area = {segment_area:.2f}")
    print(f"Total Overlap Area = {total_overlap_area:.2f}")

    # Plotting the circles, triangle, and segments
    fig, ax = plt.subplots()

    # Plot circles
    circles = [circleA, circleB, circleC]
    for circle in circles:
        cx, cy, r = circle
        circle_plot = plt.Circle((cx, cy), r, color='b', fill=False, linestyle='--')
        ax.add_artist(circle_plot)
        ax.plot(cx, cy, 'o', label=f"Circle Center ({cx}, {cy})")

    # Plot valid intersection points
    for point in valid_points:
        ax.plot(point[0], point[1], 'ro', label=f"Valid Point {point}")

    # Plot triangle edges
    triangle_x = [p[0] for p in valid_points] + [valid_points[0][0]]
    triangle_y = [p[1] for p in valid_points] + [valid_points[0][1]]
    ax.plot(triangle_x, triangle_y, 'g-', label="Triangle Edges")

    # Shade the triangle
    ax.fill(triangle_x, triangle_y, color='green', alpha=0.4, label="Shaded Triangle")

    # Plot settings
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)
    ax.set_aspect('equal', adjustable='datalim')
    ax.legend()
    plt.title("Valid Intersection Points, Triangle, and Segments")
    plt.grid(True)
    plt.show()
else:
    print("Unable to form a valid triangle with the given circles.")