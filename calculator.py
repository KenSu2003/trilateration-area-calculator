import math
from sympy import Polygon
import matplotlib.pyplot as plt



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

def find_area(polygon):
    polygon_area = abs(polygon.area)
    print(f"Polygon Area = {polygon_area:.2f}")
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
     

anchorA = [0, 0, 100]
anchorB = [70, 0, 100]
anchorC = [0, 70, 100]
anchors = [anchorA,anchorB,anchorC]
vps, triangle = find_triangle(anchors)
triangle_area = find_area(triangle)
plot_area(vps)
