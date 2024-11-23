import math
from calculator import calculate_segment_area

# Test case for half the area of a circle
def test_calculate_segment_area():
    radius = 10
    circle = (0, 0, radius)

    # Points forming the diameter of the circle
    point1 = (-radius, 0)  # Leftmost point on the circle
    point2 = (radius, 0)   # Rightmost point on the circle

    # Expected area (half of the circle's area)
    expected_area = 0.5 * math.pi * radius**2

    # Calculate the segment area
    calculated_area = calculate_segment_area(circle, point1, point2)

    # Assert the calculated area is approximately equal to the expected area
    assert math.isclose(calculated_area, expected_area, rel_tol=1e-5), \
        f"Test failed: expected {expected_area}, got {calculated_area}"

    print(f"Test passed: Segment area = {calculated_area:.5f}, Expected = {expected_area:.5f}")

# Run the test
test_calculate_segment_area()