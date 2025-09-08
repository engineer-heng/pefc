# Python Engineering Foundation Class Library (pefc)
# geom Library, originated date: 2020-05-05
# Copyright(C) 2020-2025 Heng Swee Ngee
#
# Released under the MIT License - https://opensource.org/licenses/MIT
#

""" A module to implement CAD 2D Entity classes.
    Can be used to create 2D CAD entities objects in python from
    CAD applications such as AutoCAD, QCAD etc.
    No DXF converter so need to create objects manually.
"""

from dataclasses import dataclass
from math import sqrt, atan2, isclose, pi, degrees, radians, fabs

# NOTE: A geometric point is an abstract concept representing a precise
# location in space or a mathematical space, possessing only position
# and no size, length, width, or depth. It’s a fundamental building
# block of geometry, used to define shapes like lines and planes.
# It’s usually represented by a dot. This is different from CAD points,
# which may have additional properties like layer, color, etc.


@dataclass
class GeoPt():
    """ GeoPt provide the x, y coordinates data for the Entity's sub-classes.
        GeoPt() defaults to origin (0.0, 0.0) if no parameters are given.
        Not to be confused with CAD Point entity.
    """
    x: float = 0.0
    y: float = 0.0

    @classmethod
    def from_tuple(cls, coords: tuple[float, float]):
        """ Constructor for tuple

            coords: tuple of (x, y)
        """
        return cls(*coords)

    @classmethod
    def from_geopt(cls, cad_point: 'GeoPt'):  # 'GeoPt' for forward reference
        """ Constructor for GeoPt

            cad_point: GeoPt
        """
        return cls(cad_point.x, cad_point.y)

    def __str__(self):
        return (f'{self.__class__.__name__}: Position = ({self.x}, {self.y})')

    @property
    def position(self):
        """ Return a tuple of(x, y) of the point"""
        return (self.x, self.y)

    @position.setter
    def position(self, coords: tuple[float, float]):
        """ Sets the new x, y coordinates of the GeoPt.

                coords: tuple, set GeoPt's(x, y) coordinate

            Usage
            -----
                >>> gpt = GeoPt(5.0, 9.0)
                >>> print(gpt)
                >>> GeoPt(x=5.0, y=9.0)
                >>> gpt.position = (-10.0, 28.5)
                >>> print('Position of gpt =', gpt.position)
                >>> Position of gpt = (-10.0, 28.5)
        """
        self.x = coords[0]
        self.y = coords[1]

    @position.deleter
    def position(self):
        """ Delete the point will reset it back to default values (0.0, 0.0)
            instead of some unknown coordinates.

            Usage
            -----
                >>> gpt = GeoPt(-10.0, 28.5)
                >>> print(gpt)
                >>> GeoPt(-10.0, 28.5)
                >>> del gpt.position
                >>> print(gpt)
                >>> GeoPt(x=0.0, y=0.0)
        """
        self.x = 0.0
        self.y = 0.0

    def distance_to(
            self, other: 'GeoPt') -> float:  # 'GeoPt' for forward reference
        """ Returns the distance from this point to the other point

            other: GeoPt
        """
        return sqrt((other.x-self.x)**2 + (other.y-self.y)**2)

    @staticmethod
    def distance_between_pts(x1: float, y1: float,
                             x2: float, y2: float) -> float:
        """ Returns the distance between two points

            x1: float, x coordinate of first point
            y1: float, y coordinate of first point

            x2: float, x coordinate of second point
            y2: float, y coordinate of second point
        """
        return sqrt((x2-x1)**2 + (y2-y1)**2)

    @staticmethod
    def angle_of_line(x1: float, y1: float, x2: float, y2: float) -> float:
        """ Angle of imaginary line made by two points

            x1: float, x coordinate of line's first point
            y1: float, y coordinate of line's first point

            x2: float, x coordinate of line's second point
            y2: float, y coordinate of line's second point

            Returns an angle in degrees of a line defined by two endpoints
         """
        if isclose(x1, x2, abs_tol=1.0E-10):
            # rt_atan2 not used because of the need to set precision
            tmp = -pi/2 if ((y2-y1) < 0.0) else pi/2
        else:
            # safe to use atan2 since x2-x1=0.0 is taken care of
            tmp = atan2((y2-y1), (x2-x1))

        return degrees(tmp if (tmp >= 0.0) else 2.0 * pi + tmp)  # tmp -ve

    # Returns an angle in degrees of a line defined by two endpoints,
    # (x1,y1) to (x2,y2).
    # The angle is measured from the X axis of the current construction plane,
    # in radians, with angles increasing in the counterclockwise direction.
    # Same as ADS's ads_angle. Calculations are in radians.
    # return a value in degrees that is between 0 and 360
    def angle(self, other: 'GeoPt') -> float:
        """ Returns the angle in degrees of a line from this GeoPt point to
            the other GeoPt point to the X-axis

            other: GeoPt
        """
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        return self.angle_of_line(x1, y1, x2, y2)

    def is_coincident(self, other: 'GeoPt') -> bool:
        """ Returns whether both points are coincident, that is, they
            lie exactly on top of each other.  True if they are.

            other: GeoPt
        """
        if isclose(self.x, other.x, abs_tol=1.0E-10) and  \
           isclose(self.y, other.y, abs_tol=1.0E-10):
            return True
        return False


class Entity:
    """ Base Entity for CAD Objects
    """

    def __init__(self, clr: str = 'bylayer', lyr: str = 'bylayer',
                 ltype: str = 'bylayer'):
        """ Entity's Constructor

            clr: str, Entity color, default = 'white'

            lyr: str, Entity layer, default = 'bylayer'

            ltype: str, Entity linetype, default = 'continuous'
        """
        self._entity_type = self.__class__.__name__
        self.color = clr
        self.layer = lyr
        self.linetype = ltype

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'entity_type={self.entity_type}, color={self.color}, '
                f'layer={self.layer}, linetype={self.linetype}')

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.color!r}, {self.layer!r}, {self.linetype!r})')

    @property
    def entity_type(self):
        """ Returns the Entity type """
        return self._entity_type

    @property
    def properties(self):
        """ Returns dict of entity's properties
        """
        return {'entity_type': self._entity_type, 'color': self.color,
                'layer': self.layer, 'linetype': self.linetype
                }


class Point(Entity):
    """ Point Entity for CAD geometry derived from Entity class.
    """

    def __init__(self, pos: GeoPt | tuple[float, float] = GeoPt(),
                 *args, **kwargs):
        """ Constructor for the Point Entity

            pos: GeoPt, point position, default = GeoPt()
        """
        super().__init__(*args, **kwargs)
        if isinstance(pos, tuple):
            self.pt_position: GeoPt = GeoPt.from_tuple(pos)
        elif isinstance(pos, GeoPt):
            self.pt_position: GeoPt = GeoPt.from_geopt(pos)
        else:
            raise TypeError("pos must be GeoPt or (x, y) tuple")

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'Position=({self.pt_position.x}, {self.pt_position.y})')

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.pt_position!r})')

    @property
    def position(self):  # same name as QCAD
        """ Return a GeoPt of the Point"""
        return self.pt_position

    @position.setter
    def position(self, pos: GeoPt | tuple[float, float]):
        """ Sets the Point to a GeoPt or tuple of (x, y) """
        if isinstance(pos, tuple):
            self.pt_position: GeoPt = GeoPt.from_tuple(pos)
        elif isinstance(pos, GeoPt):
            self.pt_position: GeoPt = GeoPt.from_geopt(pos)
        else:
            raise TypeError("pos must be GeoPt or (x, y) tuple")

    def distance_to(self, other):
        """ Returns the distance from this Entity's point
            to the other point """
        return self.pt_position.distance_to(other.pt_position)


class Line(Entity):
    """ Line Entity for CAD geometry derived from Entity class.
    """

    def __init__(self, spt: GeoPt | tuple[float, float] = GeoPt(),
                 ept: GeoPt | tuple[float, float] = GeoPt(), *args, **kwargs):
        """ Constructor for the Line Entity

            spt: GeoPt, start point, default = GeoPt()

            ept: GeoPt, end point, default = GeoPt()
        """
        super().__init__(*args, **kwargs)
        if isinstance(spt, tuple):
            self.start_point: GeoPt = GeoPt.from_tuple(spt)
        elif isinstance(spt, GeoPt):
            self.start_point: GeoPt = GeoPt.from_geopt(spt)
        else:
            raise TypeError("Start point, spt must be GeoPt or (x, y) tuple")
        if isinstance(ept, tuple):
            self.end_point: GeoPt = GeoPt.from_tuple(ept)
        elif isinstance(ept, GeoPt):
            self.end_point: GeoPt = GeoPt.from_geopt(ept)
        else:
            raise TypeError("End point, ept must be GeoPt or (x, y) tuple")

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'Start point=({self.start_point.x}, {self.start_point.y}), '
                f'End point=({self.end_point.x}, {self.end_point.y})'
                )

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.start_point!r}, {self.end_point!r})')

    def is_degenerate(self):
        """ Returns true if Line degenerates into a point.
            It is degenerate if start_point = end_point
        """
        if (self.start_point.is_coincident(self.end_point)):
            return True
        return False

    @property
    def ln_start(self):
        """ Return a GeoPt of the Line's start point"""
        return self.start_point

    @ln_start.setter
    def ln_start(self, coords: GeoPt | tuple[float, float]):
        """ Sets the Line's start point to a tuple of (x, y) """
        if isinstance(coords, tuple):
            self.start_point: GeoPt = GeoPt.from_tuple(coords)
        elif isinstance(coords, GeoPt):
            self.start_point: GeoPt = GeoPt.from_geopt(coords)
        else:
            raise TypeError("Start point must be GeoPt or (x, y) tuple")

    @property
    def ln_end(self):
        """ Return a GeoPt of the Line's end point"""
        return self.end_point

    @ln_end.setter
    def ln_end(self, coords: GeoPt | tuple[float, float]):
        """ Sets the Line's end point to a tuple of (x, y) """
        if isinstance(coords, tuple):
            self.end_point: GeoPt = GeoPt.from_tuple(coords)
        elif isinstance(coords, GeoPt):
            self.end_point: GeoPt = GeoPt.from_geopt(coords)
        else:
            raise TypeError("End point must be GeoPt or (x, y) tuple")

    def length(self):
        """ Returns the length of Line """
        return self.start_point.distance_to(self.end_point)

    def angle(self):
        """ Returns the angle in degrees of Line from X-axis """
        return self.start_point.angle(self.end_point)


class Circle(Entity):
    """ Circle Entity for CAD geometry derived from Entity class.
    """

    def __init__(self, cen_pt: GeoPt | tuple[float, float] = GeoPt(),
                 rad: float = 1.0, *args, **kwargs):
        """ Constructor for the Circle Entity

            cen_pt: GeoPt, center point, default GeoPt()

            rad: float, radius, default is 1.0
        """
        super().__init__(*args, **kwargs)
        if isinstance(cen_pt, tuple):
            self.center_point: GeoPt = GeoPt.from_tuple(cen_pt)
        elif isinstance(cen_pt, GeoPt):
            self.center_point: GeoPt = GeoPt.from_geopt(cen_pt)
        else:
            raise TypeError("Start point, spt must be GeoPt or (x, y) tuple")
        self.radius: float = rad

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'center={(self.center_point.x, self.center_point.y)}, '
                f'radius={self.radius}')

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.center_point!r}, {self.radius!r})')

    def is_degenerate(self):
        """ Returns True if circle degenerates into a point.
            It is degenerate if radius=0.0
        """
        if isclose(self.radius, 0.0, abs_tol=1.0E-10):
            return True  # Acad rejects arcs that have rad=0.0
        return False

    @property
    def center(self):
        """ Return a GeoPt of the Center Point"""
        return self.center_point

    @center.setter
    def center(self, cen_pt: GeoPt | tuple[float, float]):
        """ Sets the Center Point to a tuple of (x, y) """
        if isinstance(cen_pt, tuple):
            self.center_point: GeoPt = GeoPt.from_tuple(cen_pt)
        elif isinstance(cen_pt, GeoPt):
            self.center_point: GeoPt = GeoPt.from_geopt(cen_pt)
        else:
            raise TypeError("Center point must be GeoPt or (x, y) tuple")

    @property
    def diameter(self):  # no radius because it can access by .radius
        return (2.0*self.radius)

    @diameter.setter
    def diameter(self, new_dia):
        self.radius = new_dia / 2.0

    @property
    def area(self):
        return (pi*self.radius*self.radius)

    @property
    def circumference(self):
        return (2.0*pi*self.radius)

    def distance_to(self, other):
        """ Returns the distance from this Entity's center point
            to the other center point """
        return self.center_point.distance_to(other.center_point)


class Arc(Entity):
    """ Arc Entity for CAD geometry derived from Entity class.
    """

    def __init__(self, cen_pt: GeoPt | tuple[float, float] = GeoPt(),
                 rad: float = 1.0, start_ang: float = 0.0,
                 end_ang: float = 90.0, cw: bool = False, *args, **kwargs):
        """ Constructor for the Arc Entity

            cen_pt: GeoPt, center point, default = GeoPt()

            rad: float, radius, default is 1.0

            start_ang: float, start ang, default is 0.0 degrees

            end_ang: float, end angle, default is 90 degrees

            cw: bool, clockwise, default is False
        """
        super().__init__(*args, **kwargs)
        if isinstance(cen_pt, tuple):
            self.center_point: GeoPt = GeoPt.from_tuple(cen_pt)
        elif isinstance(cen_pt, GeoPt):
            self.center_point: GeoPt = GeoPt.from_geopt(cen_pt)
        else:
            raise TypeError("Center point must be GeoPt or (x, y) tuple")
        self.radius = rad
        self.start_angle = start_ang
        self.end_angle = end_ang
        self.clockwise = cw  # default is anti-clockwise

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'center={(self.center_point.x, self.center_point.y)}, '
                f'radius={self.radius}, start_angle={self.start_angle}, '
                f'end_angle={self.end_angle}, clockwise={self.clockwise}')

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.center_point!r}, {self.radius!r}, '
                f'{self.start_angle!r}, {self.end_angle})')

    def is_degenerate(self):
        """ Returns True if arc degenerates into a point or Circle
            It is degenerate if start_angle = end_angle or radius=0.0
        """
        if isclose(self.radius, 0.0, abs_tol=1.0E-10):
            return True  # Acad rejects arcs that have rad=0.0
        if isclose(self.start_angle, self.end_angle, abs_tol=1.0E-10):
            # Acad accepts arcs that have radius and start angle = end angle
            # which is displayed as a point with radius or a circle
            return True
        return False

    @property
    def center(self):
        """ Return a GeoPt of the Arc center point"""
        return self.center_point

    @center.setter
    def center(self, cen_pt: GeoPt | tuple):
        """ Sets the Arc center point to a GeoPt or (x, y) tuple"""
        if isinstance(cen_pt, tuple):
            self.center_point: GeoPt = GeoPt.from_tuple(cen_pt)
        elif isinstance(cen_pt, GeoPt):
            self.center_point: GeoPt = GeoPt.from_geopt(cen_pt)
        else:
            raise TypeError("Center point must be GeoPt or (x, y) tuple")

    @property
    def sweep_angle(self):
        """ Get the sweep angle in degrees between the start and end points
            of the Arc. Returns a positive or negative value
            depending on direction of arc.
        """
        if not self.clockwise:  # anti-clockwise CCW
            if self.end_angle <= self.start_angle:
                ret_val = 360-(self.start_angle-self.end_angle)
            else:
                ret_val = self.end_angle-self.start_angle
        else:  # clockwise CW, values here are negative
            if self.end_angle >= self.start_angle:
                ret_val = (self.end_angle-self.start_angle)-360
            else:
                ret_val = self.end_angle-self.start_angle
        return ret_val

    @property
    def diameter(self):  # no radius because it can access by .radius
        return (2.0*self.radius)

    @diameter.setter
    def diameter(self, new_dia):
        self.radius = new_dia / 2.0

    @property
    def area(self):
        return (0.5*radians(fabs(self.sweep_angle))*self.radius*self.radius)

    @property
    def length(self):
        return (self.radius*radians(fabs(self.sweep_angle)))


class Polyline(Entity):
    """ Polyline (2D) Entity.
        Stores an ordered list of vertices (GeoPt) and optional arc
        information via AutoCAD-style bulge factors.

        Bulge:
            bulge = tan(theta / 4) where theta is the included central angle
            of the arc segment (positive CCW, negative CW) joining this
            vertex to the next. bulge = 0 => straight segment.

        Features:
        - Add / insert / remove vertices (with optional bulge)
        - Length (accounts for arc segments)
        - Area (closed only; includes arc segment circular sector correction)
        - Bounding box (vertex based; does not yet expand for arc extremes)
        - Conversion to/from tuples: (x, y) or (x, y, bulge)
    """

    def __init__(self, vertices=None, closed: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vertices: list[GeoPt] = []
        # bulge[i] applies to segment from vertex i to i+1 (wraps if closed)
        self._bulges: list[float] = []
        if vertices:
            for v in vertices:
                if isinstance(v, (tuple, list)) and len(v) == 3:
                    self.add_vertex((v[0], v[1]), bulge=float(v[2]))
                else:
                    self.add_vertex(v)
        self.closed = closed

    # ---------- Internal helpers ----------

    def _as_geopt(self, v):
        if isinstance(v, GeoPt):
            return GeoPt.from_geopt(v)
        if (isinstance(v, (tuple, list))
                and len(v) == 2
                and all(isinstance(n, (int, float)) for n in v)):
            return GeoPt(float(v[0]), float(v[1]))
        raise TypeError("Vertex must be GeoPt or (x, y) numeric tuple/list")

    # ---------- Core API ----------

    @property
    def vertices(self):
        return list(self._vertices)

    @property
    def bulges(self):
        return list(self._bulges)

    @property
    def n_vertices(self):
        return len(self._vertices)

    def add_vertex(self, v, bulge: float = 0.0):
        self._vertices.append(self._as_geopt(v))
        self._bulges.append(float(bulge))

    def insert_vertex(self, idx: int, v, bulge: float = 0.0):
        self._vertices.insert(idx, self._as_geopt(v))
        self._bulges.insert(idx, float(bulge))

    def remove_vertex(self, idx: int):
        del self._vertices[idx]
        del self._bulges[idx]

    def set_bulge(self, idx: int, bulge: float):
        self._bulges[idx] = float(bulge)

    def clear(self):
        self._vertices.clear()
        self._bulges.clear()

    def close(self):
        self.closed = True

    def open(self):
        self.closed = False

    def is_closed(self) -> bool:
        return self.closed

    def is_degenerate(self):
        return self.n_vertices < 2

    # ---------- Geometry utilities ----------

    @staticmethod
    def _segment_lengths_and_angles(p1: GeoPt, p2: GeoPt, bulge: float):
        """Return (length, arc_flag, arc_length, theta, radius)
           If bulge≈0 => straight segment: length = chord, arc_flag=False.
           Else arc_flag=True with extra arc metrics.
        """
        from math import atan, sin, fabs
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        chord = sqrt(dx*dx + dy*dy)
        if isclose(bulge, 0.0, abs_tol=1e-12):
            return chord, False, chord, 0.0, 0.0
        theta = 4.0 * atan(bulge)            # signed central angle (radians)
        # Radius: chord = 2 R sin(theta/2)
        # Guard against extremely small sin
        half = theta / 2.0
        s = sin(half)
        if isclose(s, 0.0, abs_tol=1e-16):
            return chord, False, chord, 0.0, 0.0
        radius = chord / (2.0 * s)
        arc_len = fabs(radius * theta)
        return chord, True, arc_len, theta, radius

    # ---------- Geometry ----------

    def length(self) -> float:
        if self.n_vertices < 2:
            return 0.0
        total = 0.0
        last_index = self.n_vertices - 1
        seg_count = last_index if not self.closed else self.n_vertices
        for i in range(seg_count):
            j = (i + 1) % self.n_vertices
            _, is_arc, seg_len, _, _ = self._segment_lengths_and_angles(
                self._vertices[i], self._vertices[j], self._bulges[i]
            )
            total += seg_len
        return total

    def area(self) -> float:
        """Signed area including arc segments (closed only).
           Straight part via shoelace on chord endpoints.
           Arc correction: sum( (R^2)*(theta - sin(theta))/2 ) (signed).
        """
        if not self.closed or self.n_vertices < 3:
            return 0.0
        # Shoelace over chord endpoints
        s = 0.0
        verts = self._vertices
        n = self.n_vertices
        for i in range(n):
            x1, y1 = verts[i].position
            x2, y2 = verts[(i+1) % n].position
            s += (x1 * y2) - (x2 * y1)
        poly_area = 0.5 * s

        # Arc corrections
        from math import sin
        arc_corr = 0.0
        for i in range(n):
            j = (i + 1) % n
            chord, is_arc, _, theta, radius = self._segment_lengths_and_angles(
                verts[i], verts[j], self._bulges[i]
            )
            if is_arc and radius != 0.0:
                # Sector - triangle = R^2*(theta - sin(theta))/2 (theta signed)
                arc_corr += (radius * radius) * (theta - sin(theta)) / 2.0

        return poly_area + arc_corr

    def bounding_box(self):
        if self.n_vertices == 0:
            return None
        xs = [v.x for v in self._vertices]
        ys = [v.y for v in self._vertices]
        # NOTE: Does not expand for arc extrema (future enhancement)
        return (min(xs), min(ys), max(xs), max(ys))

    # ---------- Conversions ----------

    def to_tuples(self):
        # Include bulge only if any non-zero
        if any(not isclose(b, 0.0, abs_tol=1e-12) for b in self._bulges):
            return [(v.x, v.y, b) for v, b in
                    zip(self._vertices, self._bulges)]
        return [v.position for v in self._vertices]

    @classmethod
    def from_tuples(cls, coords_iterable, closed=False, *args, **kwargs):
        return cls(vertices=coords_iterable, closed=closed, *args, **kwargs)

    # ---------- Representations ----------

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'closed={self.closed}, '
                f'n_vertices={self.n_vertices}, '
                f'length={self.length():.6f}')

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.to_tuples()!r}, closed={self.closed!r})')


# ---------- Simple Tests ----------
if __name__ == '__main__':
    gpt1 = GeoPt(5.0, 9.0)
    print('GeoPt gpt1 =', gpt1)
    print('gpt1.x type is', type(gpt1.x))
    gpt1.position = (-10.0, 28.5)
    print('Position of gpt1 =', gpt1.position)
    pt1 = Point(gpt1, clr='red', lyr='1', ltype='dashed')
    print('Point pt1 =', pt1)
    print('Properties of pt1 =', pt1.properties)
    print('Position of pt1 =', pt1.position.position)
    pt2 = Point(GeoPt(15.0, 30.0),
                **{'clr': 'blue', 'lyr': '2', 'ltype': 'solid'})
    print('Point pt2 =', pt2)
    print('Properties of pt2 =', pt2.properties)
    pt3 = Point()
    print('Point pt3 =', pt3)
    pt4 = Point((100.5, 50.0), clr='green', lyr='3', ltype='dotted')
    print('Point pt4 =', pt4)
    gpt2 = GeoPt.from_tuple((20.5, 32.8))
    print('GeoPt gpt2 =', gpt2)
    gpt3 = GeoPt.from_geopt(gpt1)
    print('GeoPt gpt3 =', gpt3)
    print('Distance between gpt1 and gpt2 =', gpt1.distance_to(gpt2))
    print('Angle of line from gpt1 to gpt2 =', gpt1.angle(gpt2))
    gpt4 = GeoPt(3, 10)
    print('GeoPt gpt4 =', gpt4)
    print('gpt4.x type is', type(gpt4.x))
    gpt5 = GeoPt('5', '8')  # type: ignore  # test str to float conversion
    print('GeoPt gpt5 =', gpt5)
    gpt6 = GeoPt.from_geopt(gpt3)
    print('GeoPt gpt6 =', gpt6)
    gpt7 = GeoPt.from_tuple((100.5, 50.0))
    print('GeoPt gpt7 =', gpt7)
    ln1 = Line(gpt1, gpt2, clr='yellow', lyr='4', ltype='dashdot')
    print('Line ln1 =', ln1)
    print('Properties of ln1 =', ln1.properties)
    print('Length of ln1 =', ln1.length())
    print('Angle of ln1 =', ln1.angle())
    print('Is ln1 degenerate? =', ln1.is_degenerate())
    ln2 = Line((5.0, 9.0), (5.0, 9.0))
    print('Line ln2 =', ln2)
    print('Is ln2 degenerate? =', ln2.is_degenerate())
    cir1 = Circle(gpt1, 10.0, clr='cyan', lyr='5', ltype='center')
    print('Circle cir1 =', cir1)
    print('Properties of cir1 =', cir1.properties)
    print('Area of cir1 =', cir1.area)
    print('Circumference of cir1 =', cir1.circumference)
    print('Diameter of cir1 =', cir1.diameter)
    print('Is cir1 degenerate? =', cir1.is_degenerate())
    cir2 = Circle((5.0, 9.0), 0.0)
    print('Circle cir2 =', cir2)
    print('Is cir2 degenerate? =', cir2.is_degenerate())
    arc1 = Arc(gpt1, 10.0, 0.0, 90.0, False,
               clr='magenta', lyr='6', ltype='phatom')
    print('Arc arc1 =', arc1)
    print('Properties of arc1 =', arc1.properties)
    print('Area of arc1 =', arc1.area)
    print('Length of arc1 =', arc1.length)
    print('Diameter of arc1 =', arc1.diameter)
    print('Sweep angle of arc1 =', arc1.sweep_angle)
    print('Is arc1 degenerate? =', arc1.is_degenerate())
    arc2 = Arc((5.0, 9.0), 10.0, 0.0, 0.0)
    print('Arc arc2 =', arc2)
    print('Is arc2 degenerate? =', arc2.is_degenerate())
    arc3 = Arc((5.0, 9.0), 0.0, 0.0, 90.0)
    print('Arc arc3 =', arc3)
    print('Is arc3 degenerate? =', arc3.is_degenerate())
