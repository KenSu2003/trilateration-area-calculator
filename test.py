import math
from sympy import Point, Polygon, pi, sin, acos
from testbench import draw_circle_with_points
from calculator import find_triangle

def calculate_segment_area(circle, point1, point2, angle=None):
    """Calculate the area of a circular segment."""
    cx, cy, r = circle

    # If the angle (in radians) is given, use it directly
    if angle is not None:
        return 0.5 * r**2 * (angle - sin(angle))

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

    print(f"\nTotal Segment Area: {segment_area:.5f}")
    return segment_area


def calculate_total_overlap_area(triangle_area, segment_area):
    """Calculate the total overlap area of the three circles."""
    return triangle_area + segment_area


# Example Data
radius = 100
circle1 = [0, 0, radius]
circle2 = [100, 0, radius]
circle3 = [0, 100, radius]
circles = [circle1, circle2, circle3]

valid_points, triangle = find_triangle(circles)


# valid_points = [
#     (35.0, 93.67496997597597),  # Intersection Point 1
#     (93.67496997597597, 35.0),  # Intersection Point 2
#     (-26.441028637222537, -26.441028637222537)  # Intersection Point 3
# ]

# Calculate the area of the triangle formed by valid points using Sympy
triangle = Polygon(Point(valid_points[0]), Point(valid_points[1]), Point(valid_points[2]))
triangle_area = float(triangle.area)
print(f"Triangle Area: {triangle_area:.5f}")

# Calculate the total segment area
segments_area = calc_segments_area(circles, valid_points)

# Calculate the total overlap area
total_overlap_area = calculate_total_overlap_area(triangle_area, segments_area)
print(f"\nTotal Overlap Area: {total_overlap_area:.5f}")