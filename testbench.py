# from calculator import math, calculate_segment_area
import math
import matplotlib.pyplot as plt
import numpy as np
from function_library import *

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


# ———————————————————————————————————— Data Validation ————————————————————————————————————
""" 
Testing calcualted value against the values from ben Frederickson
https://www.benfrederickson.com/calculating-the-intersection-of-3-or-more-circles/ 

"""

# 1. Set Anchors
# anchorA = [0, 0, 1]
# anchorB = [1, 0, 1]
# anchorC = [0, 1, 1]
# anchors = [anchorA,anchorB,anchorC]

# # 2. Calculate the area of the triangle
# valid_points, triangle = find_triangle(anchors)
# triangle_area = calc_triangle_area(triangle)

# # 3. Calculate the area of the segments
# segments_area = calc_segments_area(anchors, valid_points)

# # 4. Calculate the total area
# total_area = triangle_area+segments_area

# print(f"Triangle Area: {triangle_area:.5f}")
# print(f"Segments Area: {segments_area:.5f}")
# print(f"Total Area: {total_area:.5f}")

# # 5. Plot the trilateration
# plot_area(anchors, valid_points)


# 1. Set Anchors
anchorA = [0.36, 0.02, 1.07]
anchorB = [0.01, 0.79, 1.18]
anchorC = [0.78, 0.81, 1.08]
anchors = [anchorA,anchorB,anchorC]

# 2. Calculate the area of the triangle
valid_points, triangle = find_triangle(anchors)
triangle_area = calc_triangle_area(triangle)

# 3. Calculate the area of the segments
segments_area = calc_segments_area(anchors, valid_points)

# 4. Calculate the total area
total_area = triangle_area+segments_area

print(f"Triangle Area: {triangle_area:.5f}")
print(f"Segments Area: {segments_area:.5f}")
print(f"Total Area: {total_area:.5f}")

# 5. Plot the trilateration
plot_area(anchors, valid_points)