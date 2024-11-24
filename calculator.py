from function_library import *

# 1. Set Anchors
anchorA = [0, 0, 100]
anchorB = [100, 0, 100]
anchorC = [50, 100, 100]
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