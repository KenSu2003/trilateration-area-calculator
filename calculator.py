import math
from sympy import Polygon

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

anchorA = [0, 0, 100]
anchorB = [100, 0, 100]
anchorC = [50, 100, 100]

Iab = circle_intersection_points(anchorA,anchorB)
Iab = Iab[1] # Pick the point far top point

Ibc = circle_intersection_points(anchorB,anchorC)
Ibc = Ibc[0] # Pick the point far left point

Iac = circle_intersection_points(anchorA,anchorC)
Iac = Iac[1] # Pick the point far right point

triangle = Polygon(Iab,Iac,Ibc)

print(triangle.vertices)

traingle_area = abs(triangle.area)
print(f"{traingle_area:.2f}")
