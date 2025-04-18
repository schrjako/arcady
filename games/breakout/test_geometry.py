import math
from geometry import Point, Line, Circle

# Tests for Point operations

def test_point_addition_subtraction():
    p1 = Point(2, 3)
    p2 = Point(-1, 5)
    sum_pt = p1 + p2
    diff_pt = p1 - p2
    assert sum_pt.x == 1 and sum_pt.y == 8
    assert diff_pt.x == 3 and diff_pt.y == -2


def test_point_multiplication_division():
    p1 = Point(4, 6)
    p2 = Point(2, 3)
    prod = p1 * p2
    quot = p1 / p2
    assert prod.x == 8 and prod.y == 18
    assert math.isclose(quot.x, 2.0) and math.isclose(quot.y, 2.0)

# Tests for distance and phi

def test_distance_to_and_phi():
    p = Point(3, 4)
    origin = Point(0, 0)
    assert math.isclose(p.distance_to(origin), 5.0, rel_tol=1e-9)
    # phi = atan2(4, 3)
    assert math.isclose(p.phi, math.atan2(4, 3), rel_tol=1e-9)

# Tests for Line.eval

def test_line_eval_sides():
    # Line from (0,0) to (1,0) is horizontal x-axis: a=0, b=1, c=0
    line = Line(Point(0, 0), Point(1, 0))
    above = Point(0, 1)
    below = Point(0, -1)
    on_line = Point(0.5, 0)
    assert line.eval(above) < 0
    assert line.eval(below) > 0
    assert math.isclose(line.eval(on_line), 0.0, rel_tol=1e-9)

# Tests for Line.intersection

def test_line_intersection_point():
    l1 = Line(Point(0, 0), Point(1, 1))
    l2 = Line(Point(0, 1), Point(1, 0))
    inter = l1.intersection(l2)
    assert inter is not None
    assert math.isclose(inter.x, 0.5, rel_tol=1e-9)
    assert math.isclose(inter.y, 0.5, rel_tol=1e-9)


def test_parallel_lines_no_intersection():
    l1 = Line(Point(0, 0), Point(1, 1))
    l2 = Line(Point(0, 1), Point(1, 2))  # same slope, parallel
    assert l1.intersection(l2) is None

# Tests for Circle.intersection

def test_tangent_line_returns_one_point():
    # Circle centered at origin with radius 5
    circle = Circle(Point(0, 0), 5)
    # Tangent line at (5, 0): vertical line x=5
    line = Line(Point(5, 0), Point(5, 1))

    intersections = circle.intersections(line)
    # Should return exactly one intersection at (5,0)
    assert len(intersections) == 1, "Expected exactly one intersection for the tangent line"
    pt = intersections[0]
    assert math.isclose(pt.x, 5, rel_tol=1e-9)
    assert math.isclose(pt.y, 0, rel_tol=1e-9)


def test_secant_line_returns_two_points():
    circle = Circle(Point(0, 0), 5)
    # Horizontal line through y=3 cuts circle in two points
    line = Line(Point(-10, 3), Point(10, 3))

    intersections = circle.intersections(line)
    assert len(intersections) == 2, "Expected two intersections for a secant line"
    xs = sorted(pt.x for pt in intersections)
    # Solutions x = ±4
    assert math.isclose(xs[0], -4, rel_tol=1e-9)
    assert math.isclose(xs[1], 4, rel_tol=1e-9)


def test_no_intersection_returns_empty_list():
    circle = Circle(Point(0, 0), 5)
    # Line outside circle at y=6
    line = Line(Point(-10, 6), Point(10, 6))

    intersections = circle.intersections(line)
    assert intersections == [], "Expected no intersections for a line outside the circle"


def test_degenerate_line_point_on_circle():
    circle = Circle(Point(0, 0), 5)
    pt_on = Point(5, 0)
    line = Line(pt_on, pt_on)

    intersections = circle.intersections(line)
    assert len(intersections) == 1
    assert intersections[0] == pt_on


def test_degenerate_line_point_off_circle():
    circle = Circle(Point(0, 0), 5)
    pt_off = Point(6, 0)
    line = Line(pt_off, pt_off)

    intersections = circle.intersections(line)
    assert intersections == []
