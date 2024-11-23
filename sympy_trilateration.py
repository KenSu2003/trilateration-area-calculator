from sympy import symbols, Eq, solve, sqrt, atan2, pi, sin
from sympy.geometry import Point, Polygon, Circle
import matplotlib.pyplot as plt


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


def calculate_circular_segments(circles, polygon):
    """Calculate the areas of the circular segments (curved parts) for each circle."""
    circular_segment_areas = 0
    for cx, cy, r in circles:
        circle = Circle(Point(cx, cy), r)
        for i in range(len(polygon.vertices)):
            # Get two consecutive vertices of the polygon
            p1 = polygon.vertices[i]
            p2 = polygon.vertices[(i + 1) % len(polygon.vertices)]

            # Check if both vertices are on the circle
            if circle.encloses_point(p1) and circle.encloses_point(p2):
                # Calculate the angle of the arc
                theta = abs(atan2(p2.y - cy, p2.x - cx) - atan2(p1.y - cy, p1.x - cx))
                theta = theta if theta <= pi else 2 * pi - theta  # Ensure smallest angle

                # Area of the circular segment
                segment_area = 0.5 * r**2 * (theta - sin(theta))
                circular_segment_areas += segment_area.evalf()
    return circular_segment_areas


def calculate_area_of_intersection(circles):
    """Calculate the total area of intersection of three circles, including curved portions."""
    # Step 1: Find the polygon formed by intersection points
    polygon = find_polygon_intersection(circles)

    if polygon is None:
        print("No intersection polygon could be formed.")
        return 0

    # Step 2: Calculate the area of the polygon
    polygon_area = polygon.area.evalf()
    print(f"Polygon area (triangle or more): {polygon_area:.2f}")

    # Step 3: Calculate the areas of the circular segments
    circular_segment_area = calculate_circular_segments(circles, polygon)
    print(f"Total area of the circular segments: {circular_segment_area:.2f}")

    # Step 4: Total area is the sum of the polygon area and the circular segment areas
    total_area = polygon_area + circular_segment_area
    print(f"Total area of intersection (polygon + curved parts): {total_area:.2f}")
    return total_area


def plot_circles_and_intersection(circles, polygon):
    """Plot the circles, intersection polygon, and shade the area of intersection."""
    fig, ax = plt.subplots()

    # Plot each circle
    for cx, cy, r in circles:
        circle = plt.Circle((cx, cy), r, fill=False, linestyle="--", color="black")
        ax.add_artist(circle)
        ax.plot(cx, cy, 'o', label=f"Circle Center ({cx}, {cy})")

    # Plot the intersection polygon and shade the area
    if polygon:
        x_coords = [p.x for p in polygon.vertices] + [polygon.vertices[0].x]
        y_coords = [p.y for p in polygon.vertices] + [polygon.vertices[0].y]

        # Shade the area
        ax.fill(x_coords, y_coords, color="green", alpha=0.3, label="Intersection Area")

        # Plot the polygon boundary
        ax.plot(x_coords, y_coords, 'g-', label="Intersection Polygon")

    # Set plot limits and labels
    ax.set_xlim(-300, 300)
    ax.set_ylim(-300, 300)
    ax.set_aspect('equal', adjustable='datalim')
    ax.legend()
    plt.title("Circles and Intersection Polygon with Shaded Area")
    plt.show()


# Example usage
circles = [(0, 0, 100), (70, 0, 100), (0, 70, 100)]  # (x, y, radius) for each circle
area = calculate_area_of_intersection(circles)
print(f"The total area of intersection is: {area:.2f}")

# Plot the circles and the shaded intersection area
polygon = find_polygon_intersection(circles)
plot_circles_and_intersection(circles, polygon)