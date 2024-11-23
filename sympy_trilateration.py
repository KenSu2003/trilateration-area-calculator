from sympy import symbols, Eq, solve, sqrt, Polygon, integrate, atan2
from sympy.geometry import Circle, Point, Segment

def circle_intersection_points(circle1, circle2):
    """Find intersection points of two circles."""
    x, y = symbols('x y')
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    
    # Define the equations of the two circles
    eq1 = Eq((x - x1)**2 + (y - y1)**2, r1**2)
    eq2 = Eq((x - x2)**2 + (y - y2)**2, r2**2)
    
    # Solve the system of equations to find intersection points
    solutions = solve([eq1, eq2], (x, y))
    return [Point(p[0], p[1]) for p in solutions]

def find_polygon_intersection(circles):
    """Find the polygon formed by intersection points of multiple circles."""
    points = []
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            points += circle_intersection_points(circles[i], circles[j])

    # Keep only points inside all circles
    def is_point_inside_all_circles(point):
        px, py = point.x, point.y
        return all((px - cx)**2 + (py - cy)**2 <= r**2 for cx, cy, r in circles)

    points = [p for p in points if is_point_inside_all_circles(p)]

    # If fewer than three points, no valid polygon
    if len(points) < 3:
        return None

    # Sort points counterclockwise around the centroid
    centroid_x = sum(p.x for p in points) / len(points)
    centroid_y = sum(p.y for p in points) / len(points)
    centroid = Point(centroid_x, centroid_y)
    points.sort(key=lambda p: atan2(p.y - centroid.y, p.x - centroid.x))

    # Create a polygon
    return Polygon(*points)

def calculate_area_of_intersection(circles):
    """Calculate the area of intersection of multiple circles."""
    polygon = find_polygon_intersection(circles)

    # If no valid polygon exists, the area is zero
    if polygon is None:
        return 0

    # Calculate polygon area symbolically
    return polygon.area

def plot_circles_and_intersection(circles, polygon):
    """Plot the circles and the intersection polygon."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # Plot each circle
    for cx, cy, r in circles:
        circle = plt.Circle((cx, cy), r, fill=False, linestyle="--")
        ax.add_artist(circle)
        ax.plot(cx, cy, 'o', label=f"Circle Center ({cx}, {cy})")

    # Plot the intersection polygon
    if polygon:
        x_coords = [p.x for p in polygon.vertices] + [polygon.vertices[0].x]
        y_coords = [p.y for p in polygon.vertices] + [polygon.vertices[0].y]
        ax.plot(x_coords, y_coords, 'g-', label="Intersection Polygon")

    # Set plot limits and labels
    ax.set_xlim(-300, 300)
    ax.set_ylim(-300, 300)
    ax.set_aspect('equal', adjustable='datalim')
    ax.legend()
    plt.title("Circles and Intersection Polygon")
    plt.show()

# Example usage:
circles = [(0, 0, 100), (70, 0, 100), (0, 70, 100)]  # (x, y, radius) for each circle
area = calculate_area_of_intersection(circles).evalf(6)
print(f"The area of intersection is: {area}")

# Plot the circles and the intersection polygon
polygon = find_polygon_intersection(circles)
plot_circles_and_intersection(circles, polygon)