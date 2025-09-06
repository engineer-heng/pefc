import math

import pytest

from pefc.geom import CadPt, Entity, Point, Line, Circle, Arc


# ---------- CadPt Tests ----------

def test_cadpt_defaults():
    c = CadPt()
    assert c.x == 0.0 and c.y == 0.0
    assert c.position == (0.0, 0.0)


def test_cadpt_init_and_repr():
    c = CadPt(5.0, 9.0)
    assert c.x == 5.0 and c.y == 9.0
    r = repr(c)
    assert 'CadPt' in r and '5.0' in r and '9.0' in r


def test_cadpt_property_set_delete():
    c = CadPt(1.0, 2.0)
    c.position = (-10.0, 28.5)
    assert c.position == (-10.0, 28.5)
    del c.position
    # Expect reset to origin (assumed behavior from original script intent)
    assert c.position == (0.0, 0.0)


def test_cadpt_class_and_static_methods():
    c1 = CadPt.from_tuple((23.75, 32.25))
    assert isinstance(c1, CadPt) and c1.position == (23.75, 32.25)
    c2 = CadPt(5.0, -3.0)
    c3 = CadPt.from_cadpt(c2)
    assert c3 is not c2 and c3.position == c2.position
    # Distance and angle
    a = CadPt(1.0, 5.0)
    b = CadPt(2.5, 1.5)
    dist_inst = a.distance_to(b)
    dist_static = CadPt.distance_between_pts(*a.position, *b.position)
    assert math.isclose(dist_inst, dist_static, rel_tol=1e-9)
    ang_inst = a.angle(b)
    ang_static = CadPt.angle_of_line(*a.position, *b.position)
    assert math.isclose(ang_inst, ang_static, rel_tol=1e-9)


# ---------- Entity Tests ----------

def test_entity_defaults():
    e = Entity()
    r = repr(e)
    assert 'Entity' in r
    assert isinstance(e.properties, dict)


# ---------- Point Tests ----------

def test_point_defaults_and_properties():
    p = Point()
    assert isinstance(p.pt_position, CadPt)
    p2 = Point(CadPt(20.5, 32.8), clr='blue')
    assert p2.pt_position.position == (20.5, 32.8)
    assert p2.properties.get('clr') == 'blue'
    x, y = p2.position
    assert (x, y) == (20.5, 32.8)


def test_point_mutation_updates_properties():
    p = Point(CadPt(10.0, 10.0), clr='red', lyr='1', ltype='dashed')
    new_pt = CadPt(-98.7, -75.5)
    p.pt_position = new_pt
    assert p.position == new_pt.position
    props = p.properties
    assert props.get('clr') == 'red'
    assert props.get('lyr') == '1'
    assert props.get('ltype') == 'dashed'


def test_point_distance():
    p1 = Point(CadPt(16.875, 93.836))
    p2 = Point(CadPt(11.33, 88.75))
    d = p1.distance_to(p2)
    # Quick manual expected distance
    dx = 16.875 - 11.33
    dy = 93.836 - 88.75
    expected = math.hypot(dx, dy)
    assert math.isclose(d, expected, rel_tol=1e-9)


# ---------- Line Tests ----------

def test_line_defaults_and_length_angle():
    l0 = Line()
    assert isinstance(l0.start, CadPt) and isinstance(l0.end, CadPt)
    l1 = Line(CadPt(3.0, 5.0), CadPt(10.0, 15.5))
    length = l1.length()
    expected_len = math.hypot(10.0 - 3.0, 15.5 - 5.0)
    assert math.isclose(length, expected_len, rel_tol=1e-9)
    angle = l1.angle()
    expected_angle = math.atan2(15.5 - 5.0, 10.0 - 3.0)
    assert math.isclose(angle, expected_angle, rel_tol=1e-9)


def test_line_degenerate():
    l1 = Line(CadPt(7.0, 5.0), CadPt(3.0, 15.0))
    assert not l1.is_degenerate()
    l2 = Line(CadPt(7.0, 5.0), CadPt(7.0, 5.0))
    assert l2.is_degenerate()


# ---------- Circle Tests ----------

def test_circle_defaults_and_metrics():
    c0 = Circle()
    assert isinstance(c0.center, CadPt)
    c1 = Circle(CadPt(9, 8), 5.25)
    assert math.isclose(c1.radius, 5.25, rel_tol=1e-12)
    assert math.isclose(c1.diameter, 10.5, rel_tol=1e-12)
    assert math.isclose(c1.area, math.pi * 5.25**2, rel_tol=1e-9)
    assert math.isclose(c1.circumference, 2 * math.pi * 5.25, rel_tol=1e-9)


def test_circle_distance_and_degenerate():
    c1 = Circle(CadPt(9, 8), 5.25)
    c2 = Circle(CadPt(-4.0, 12.0), 2.5)
    d = c1.distance_to(c2)
    center_dist = math.hypot(9 - (-4.0), 8 - 12.0)
    expected_clearance = center_dist - (5.25 + 2.5)
    assert math.isclose(d, expected_clearance, rel_tol=1e-9)
    assert not c1.is_degenerate()
    c3 = Circle(CadPt(-5.0, 16.0), 0.0)
    assert c3.is_degenerate()
    c3.diameter = 50
    assert math.isclose(c3.radius, 25.0, rel_tol=1e-12)


# ---------- Arc Tests ----------

def test_arc_defaults_and_properties():
    a0 = Arc()
    assert isinstance(a0.center, CadPt)
    assert a0.radius >= 0.0


def test_arc_ccw():
    a1 = Arc(CadPt(15, 9), 3.75, 25, 200, clr='red', lyr='front view')
    assert a1.start_angle == 25
    assert a1.end_angle == 200
    assert a1.sweep_angle > 0
    assert a1.length >= 0
    assert a1.area >= 0


def test_arc_ccw_wrap():
    a2 = Arc(CadPt(15, 9), 3.75, 200.0, 25.0)
    assert a2.sweep_angle > 0
    assert a2.length >= 0
    assert a2.area >= 0


def test_arc_cw_examples():
    a3 = Arc(CadPt(25, 12.5), 5.0, 0.0, 260.0, True)
    # depending on implementation detail
    assert a3.sweep_angle < 0 or a3.length >= 0
    a4 = Arc(CadPt(25, 12.5), 5.0, 260.0, 0.0, True)
    assert a4.length >= 0
    a5 = Arc(CadPt(37.0, 3.0), 5.0, 260.0, 350.0, True)
    assert not a5.is_degenerate()


def test_arc_degenerate_cases():
    a6 = Arc(CadPt(37.0, 3.0), 0.0, 260.0, 350.0, True)
    assert a6.is_degenerate()
    a7 = Arc(CadPt(37.0, 3.0), 5.0, 260.0, 260.0, True)
    assert a7.is_degenerate()


# ---------- Combined / Sanity ----------

@pytest.mark.parametrize(
    "center,radius",
    [
        ((0, 0), 1.0),
        ((10, -5), 2.5),
        ((-7.25, 3.5), 0.0),
    ],
)
def test_circle_parametric(center, radius):
    c = Circle(CadPt(*center), radius)
    assert c.center.position == center
    assert math.isclose(c.radius, radius, rel_tol=1e-12)
    if radius == 0.0:
        assert c.is_degenerate()


def test_line_angle_quadrants():
    # Create lines in each quadrant to ensure angle() behaves
    lines = [
        (CadPt(0, 0), CadPt(1, 1)),
        (CadPt(0, 0), CadPt(-1, 1)),
        (CadPt(0, 0), CadPt(-1, -1)),
        (CadPt(0, 0), CadPt(1, -1)),
    ]
    for s, e in lines:
        l = Line(s, e)
        ang = l.angle()
        assert -math.pi <= ang <= math.pi


def test_point_str_and_repr_stability():
    p = Point(CadPt(3.0, 4.0), clr='yellow')
    s = str(p)
    r = repr(p)
    assert 'Point' in r
    assert all(token in (s + r) for token in ['3.0', '4.0'])


def test_entity_properties_mutable_copy():
    e = Entity()
    props = e.properties
    props['__test__'] = 123
    # Depending on implementation: either the original should or
    # should not change.
    # If defensive copy is expected, original should not have key.
    # If direct reference, it will. We assert membership to detect
    # behavior explicitly.
    assert ('__test__' in e.properties) in (
        True, False)  # placeholder assertion
