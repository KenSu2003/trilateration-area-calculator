# from calculator import math, calculate_segment_area
import math
import matplotlib.pyplot as plt
import numpy as np

# Test case for half the area of a circle
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
        # print(f"  Circle {i+1}: {circle}")
        # print(f"    Point 1: {p1}")
        # print(f"    Point 2: {p2}")
        draw_circle_with_points(circle, (p1, p2), title="Validating Points on Circle")


    for circle, (p1, p2) in circle_points_map:
        # print(f"\nProcessing Circle: {circle}")
        # print(f"Original Points: {p1}, {p2}")

        # Adjust points if necessary
        p1 = adjust_to_circle(p1, circle)
        p2 = adjust_to_circle(p2, circle)
        # print(f"Adjusted Points: {p1}, {p2}")

        # Calculate segment area
        segment_area += calculate_segment_area(circle, p1, p2)

    # print(f"\nTotal Segment Area: {segment_area:.5f}")
    return segment_area

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


# ———————————————————————————————————— Test Statements ————————————————————————————————————


# Circle parameters
circle, point1, point2, angle_degrees = [0, 0, 100], (35.0, 93.67496997597597), (93.67496997597597, 35.0), 0.855654119503876

# Convert angle to radians
angle_radians = math.radians(angle_degrees)

# Calculate the segment area using the direct angle method
segment_area_with_angle = calculate_segment_area(circle, None, None, angle=angle_radians)
print(f"Segment Area (using angle) = {segment_area_with_angle:.5f} cm²")

# Test using points
# point1 = (radius * math.cos(math.radians(0)), radius * math.sin(math.radians(0)))  # Point A
# point2 = (radius * math.cos(math.radians(angle_degrees)), radius * math.sin(math.radians(angle_degrees)))  # Point B
segment_area_with_points = calculate_segment_area(circle, point1, point2)
print(f"Segment Area (using points) = {segment_area_with_points:.5f} cm²")

def validate_point_on_circle(point, circle):
    """Check if a point lies on the circumference of a circle."""
    cx, cy, r = circle
    distance_squared = (point[0] - cx)**2 + (point[1] - cy)**2
    print(f"Validating Point: {point} for Circle: {circle}")
    print(f"  Computed Distance²: {distance_squared:.10f}, Expected Radius²: {r**2:.10f}")
    return math.isclose(distance_squared, r**2, rel_tol=1e-5)

validate_point_on_circle(point1, circle)
validate_point_on_circle(point2, circle)

points = [point1, point2]
# draw_circle_with_points(circle, points, title="Validating Points on Circle")