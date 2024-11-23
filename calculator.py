import math
from sympy import Polygon
import matplotlib.pyplot as plt
import numpy as np

# https://math.stackexchange.com/questions/49787/area-between-three-circles-of-differing-radii
# https://web2.0calc.com/questions/area-of-3-overlapping-circles
# https://www.benfrederickson.com/calculating-the-intersection-of-3-or-more-circles/

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

def find_triangle(anchors):
    anchorA,anchorB,anchorC = anchors
    Iab = circle_intersection_points(anchorA,anchorB)
    Ibc = circle_intersection_points(anchorB,anchorC)
    Iac = circle_intersection_points(anchorA,anchorC)
    intersections = [Iab,Iac,Ibc]

    valid_points = []
    for points in intersections:
        for point in points:
            if is_point_inside_circle(point, anchorA) and \
            is_point_inside_circle(point, anchorB) and \
            is_point_inside_circle(point, anchorC):
                valid_points.append(point)
    vpA, vpB, vpC = valid_points
    triangle = Polygon(vpA, vpB, vpC)
    return valid_points, triangle

def calc_triangle_area(polygon):
    polygon_area = abs(polygon.area)
    return polygon_area
    
def plot_area(valid_points):

    # Plotting the circles, triangle, and valid points
    fig, ax = plt.subplots()
    for circle in anchors:
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

    ax.set_xlim(-150, 250)
    ax.set_ylim(-150, 250)
    ax.set_aspect('equal', adjustable='datalim')
    ax.legend()
    plt.title("Valid Intersection Points and Triangle")
    plt.grid(True)
    plt.show()
     
# https://www.cuemath.com/geometry/segment-of-a-circle/
# https://www.youtube.com/watch?v=vVAl1jyL8X0
def calculate_segment_area(circle, point1, point2, angle=None):
    """Calculate the area of a circular segment."""
    cx, cy, r = circle

    # If the angle (in radians) is given, use it directly
    if angle is not None:
        return 0.5 * r**2 * (angle - math.sin(angle))

    # Adjust points to ensure they lie on the circle
    point1 = adjust_to_circle(point1, circle)
    point2 = adjust_to_circle(point2, circle)

    # Calculate vectors from the circle center to the points
    dx1, dy1 = point1[0] - cx, point1[1] - cy
    dx2, dy2 = point2[0] - cx, point2[1] - cy

    # Calculate the angle subtended by the chord
    dot_product = dx1 * dx2 + dy1 * dy2
    magnitude1 = math.sqrt(dx1**2 + dy1**2)
    magnitude2 = math.sqrt(dx2**2 + dy2**2)
    angle = math.acos(dot_product / (magnitude1 * magnitude2))
    print(circle, point1, point2, angle)
    # Segment area formula
    return 0.5 * r**2 * (angle - math.sin(angle))

def adjust_to_circle(point, circle):
    """Adjust a point to lie exactly on the circle's circumference."""
    cx, cy, r = circle
    dx, dy = point[0] - cx, point[1] - cy
    magnitude = math.sqrt(dx**2 + dy**2)
    if magnitude == 0:
        raise ValueError("Point cannot coincide with the circle center.")
    scale = r / magnitude
    return (cx + dx * scale, cy + dy * scale)

def calc_segments_area(circles, valid_points):
    """Calculate the total area of all circular segments."""
    segment_area = 0

    # Correct mapping of circles to points
    circle_points_map = [
        (circles[0], (valid_points[0], valid_points[1])),  # Points for Circle 1
        (circles[2], (valid_points[1], valid_points[2])),  # Points for Circle 2
        (circles[1], (valid_points[2], valid_points[0]))   # Points for Circle 3
    ]


    # Debug: Print circle-to-point mapping
    print("Circle to Points Mapping:")
    for i, (circle, (p1, p2)) in enumerate(circle_points_map):
        print(f"  Circle {i+1}: {circle}")
        print(f"    Point 1: {p1}")
        print(f"    Point 2: {p2}")
        draw_circle_with_points(circle, (p1, p2), title="Validating Points on Circle")


    for circle, (p1, p2) in circle_points_map:
        print(f"\nProcessing Circle: {circle}")
        print(f"Original Points: {p1}, {p2}")

        # Adjust points if necessary
        p1 = adjust_to_circle(p1, circle)
        p2 = adjust_to_circle(p2, circle)
        print(f"Adjusted Points: {p1}, {p2}")

        # Calculate segment area
        segment_area += calculate_segment_area(circle, p1, p2)

    # print(f"\nTotal Segment Area: {segment_area:.5f}")
    return segment_area

def calculate_total_overlap_area(triangle_area, segment_area):
    """Calculate the total overlap area of the three circles."""
    return triangle_area + segment_area

def draw_circle_with_points(circle, points, title="Circle and Points"):
    """Draw a circle and plot points to verify if they lie on the circle."""
    cx, cy, r = circle
    theta = np.linspace(0, 2 * np.pi, 500)  # Generate points for the circle outline

    # Circle outline
    circle_x = cx + r * np.cos(theta)
    circle_y = cy + r * np.sin(theta)

    # Plot the circle
    plt.figure(figsize=(6, 6))
    plt.plot(circle_x, circle_y, 'b--', label=f"Circle Center: {circle[:2]}, Radius: {r}")
    
    # Plot the points
    for i, point in enumerate(points):
        plt.plot(point[0], point[1], 'ro', label=f"Point {i+1}: {point}")
    
    # Set plot limits and aspect ratio
    plt.xlim(cx - r - 10, cx + r + 10)
    plt.ylim(cy - r - 10, cy + r + 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')

    plt.title(title)
    plt.legend()
    plt.show()

# 1. Set Anchors
anchorA = [0, 0, 100]
anchorB = [75, 0, 100]
anchorC = [50, 50, 100]
anchors = [anchorA,anchorB,anchorC]

# 2. Calculate the area of the triangle
valid_points, triangle = find_triangle(anchors)
triangle_area = calc_triangle_area(triangle)

# 3. Calculate the area of the segments
segments_area = calc_segments_area(anchors, valid_points)

# 4. Calculate the total area
total_area = triangle_area+segments_area

print(f"Triangle Area: {triangle_area:.2f}")
print(f"Segments Area: {segments_area:.2f}")
print(f"Total Area: {total_area:.2f}")

# 5. Plot the trilateration
plot_area(valid_points)