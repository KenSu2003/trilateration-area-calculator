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
        if angle > 2 * math.pi:  # Check for degrees
            raise ValueError("Angle must be in radians. Convert degrees to radians before passing.")
        return 0.5 * r**2 * (angle - math.sin(angle))

    # Validate input points
    if (point1[0] == cx and point1[1] == cy) or (point2[0] == cx and point2[1] == cy):
        raise ValueError("Points cannot be the same as the center of the circle.")

    # Calculate vectors from the circle center to the points
    dx1, dy1 = point1[0] - cx, point1[1] - cy
    dx2, dy2 = point2[0] - cx, point2[1] - cy

    # Ensure the points lie on the circle
    # if not math.isclose(dx1**2 + dy1**2, r**2, rel_tol=1e-5) or \
    #    not math.isclose(dx2**2 + dy2**2, r**2, rel_tol=1e-5):
    #     raise ValueError("Points must lie on the circumference of the circle.")

    # Calculate the angle subtended by the chord
    dot_product = dx1 * dx2 + dy1 * dy2
    magnitude1 = math.sqrt(dx1**2 + dy1**2)
    magnitude2 = math.sqrt(dx2**2 + dy2**2)
    angle = math.acos(dot_product / (magnitude1 * magnitude2))

    # Segment area formula
    return 0.5 * r**2 * (angle - math.sin(angle))

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

# Example Circle and Points
radius = 100
circle = [0, 70, radius]
points = [
    (-26.441028637222537, -26.441028637222537),  # Point 1
    (35.0, 93.67496997597597)  # Point 2
]

# Draw the circle and the points
draw_circle_with_points(circle, points, title="Validating Points on Circle")

# # Circle parameters
radius = 100
circle = [0, 70, radius]
point1 = (35.0, 93.67496997597597)
point2 = (93.67496997597597, 35.0)

# Central angle in degrees
angle_degrees = 0.855654119503876

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

draw_circle_with_points(circle, points, title="Validating Points on Circle")