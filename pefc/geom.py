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


@dataclass
class CadPt():
    """ CadPt provide the x, y coordinates data for the Entity's sub-classes.
        CadPt()
    """
    x: float = 0.0
    y: float = 0.0

    @classmethod
    def from_tuple(cls, coords: tuple):  # cls is CadPt
        """ Constructor for tuple

            coords: tuple of (x, y)
        """
        return cls(*coords)

    @classmethod
    def from_cadpt(cls, cad_point):
        """ Constructor for CadPt

            cad_point: CadPt
        """
        return cls(cad_point.x, cad_point.y)

    def __str__(self):
        return (f'{self.__class__.__name__}: Position = ({self.x}, {self.y})')

    @property
    def position(self):
        """ Return a tuple of(x, y) of the point"""
        return (self.x, self.y)

    @position.setter
    def position(self, coords: tuple):
        """ Sets the new x, y coordinates of the CadPt.

                coords: tuple, set CadPt's(x, y) coordinate

            Usage
            -----
                >>> cpt = CadPt(5.0, 9.0)
                >>> print(cpt)
                >>> CadPt(x=5.0, y=9.0)
                >>> cpt.position = (-10.0, 28.5)
                >>> print('cpt =', cpt.position)
                >>> CadPt(x=-10.0, y=28.5)
        """
        self.x = coords[0]
        self.y = coords[1]

    @position.deleter
    def position(self):
        """ Delete the point will reset it back to default values (0.0, 0.0)
            instead of some unknown coordinates.

            Usage
            -----
                >>> cpt = CadPt(-10.0, 28.5)
                >>> print(cpt)
                >>> CadPt(-10.0, 28.5)
                >>> del cpt.position
                >>> print(cpt)
                >>> CadPt(x=0.0, y=0.0)
        """
        self.x = 0.0
        self.y = 0.0

    def distance_to(self, other):
        """ Returns the distance from this point to the other point

            other: CadPt
        """
        return sqrt((other.x-self.x)**2 + (other.y-self.y)**2)

    @staticmethod
    def distance_between_pts(x1, y1, x2, y2):
        """ Returns the distance between two points

            x1: float, x coordinate of first point
            y1: float, y coordinate of first point

            x2: float, x coordinate of second point
            y2: float, y coordinate of second point
        """
        return sqrt((x2-x1)**2 + (y2-y1)**2)

    @staticmethod
    def angle_of_line(x1, y1, x2, y2):
        """ Angle of imaginary line made by two points

            x1: float, x coordinate of line's first point
            y1: float, y coordinate of line's first point

            x2: float, x coordinate of line's second point
            y2: float, y coordinate of line's second point
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
    def angle(self, other):
        """ Returns the angle in degrees of a line from this CadPt point to
            the other CadPt point to the X-axis

            other: CadPt
        """
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        return self.angle_of_line(x1, y1, x2, y2)

    def is_coincident(self, other):
        """ Returns whether both points are coincident, that is, they
            lie exactly on top of each other.  True if they are.

            other: CadPt
        """
        if isclose(self.x, other.x, abs_tol=1.0E-10) and  \
           isclose(self.y, other.y, abs_tol=1.0E-10):
            return True
        return False


class Entity:
    """ Base Entity for CAD Objects
    """

    def __init__(self, clr='bylayer', lyr='bylayer', ltype='bylayer'):
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

    def __init__(self, pos=None, *args, **kwargs):
        """ Constructor for the Point Entity

            pos: CadPt, point position, default = CadPt()
        """
        super().__init__(*args, **kwargs)
        self.pt_position = pos if pos is not None else CadPt()

    def __str__(self):
        return (f'{self.__class__.__name__}: '
                f'Position=({self.pt_position.x}, {self.pt_position.y})')

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.pt_position!r})')

    @property
    def position(self):  # same name as QCAD
        """ Return a tuple of (x, y) of the Point"""
        return self.pt_position.position

    @position.setter
    def position(self, coords: tuple):
        """ Sets the Point to a tuple of (x, y) """
        self.pt_position = coords

    def distance_to(self, other):
        """ Returns the distance from this Entity's point
            to the other point """
        return self.pt_position.distance_to(other.pt_position)


class Line(Entity):
    """ Line Entity for CAD geometry derived from Entity class.
    """

    def __init__(self, spt=None, ept=None, *args, **kwargs):
        """ Constructor for the Line Entity

            spt: CadPt, start point, default = CadPt()

            ept: CadPt, end point, default = CadPt()
        """
        super().__init__(*args, **kwargs)
        self.start_point = spt if spt is not None else CadPt()
        self.end_point = ept if ept is not None else CadPt()

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
    def lstart(self):
        """ Return a tuple of (x, y) of the Line's start point"""
        return self.start_point.position

    @lstart.setter
    def lstart(self, coords: tuple):
        """ Sets the Line's start point to a tuple of (x, y) """
        self.start_point = coords

    @property
    def lend(self):
        """ Return a tuple of (x, y) of the Line's end point"""
        return self.end_point.position

    @lend.setter
    def lend(self, coords: tuple):
        """ Sets the Line's end point to a tuple of (x, y) """
        self.end_point = coords

    def length(self):
        """ Returns the length of Line """
        return self.start_point.distance_to(self.end_point)

    def angle(self):
        """ Returns the angle in degrees of Line from X-axis """
        return self.start_point.angle(self.end_point)


class Circle(Entity):
    """ Circle Entity for CAD geometry derived from Entity class.
    """

    def __init__(self, cen_pt=None, rad=1.0, *args, **kwargs):
        """ Constructor for the Circle Entity

            cen_pt: CadPt, center point, default CadPt()

            rad: float, radius, default is 1.0
        """
        super().__init__(*args, **kwargs)
        self.center_point = cen_pt if cen_pt is not None else CadPt()
        self.radius = rad

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
        """ Return a tuple of (x, y) of the Center Point"""
        return self.center_point.position

    @center.setter
    def center(self, coords: tuple):
        """ Sets the Center Point to a tuple of (x, y) """
        self.center_point = coords

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

    def __init__(self, cen_pt=None, rad=1.0, start_ang=0.0, end_ang=90.0,
                 cw=False, *args, **kwargs):
        """ Constructor for the Arc Entity

            cen_pt: CadPt, center point, default = CadPt()

            rad: float, radius, default is 1.0

            start_ang: float, start ang, default is 0.0 degrees

            end_ang: float, end angle, default is 90 degrees

            cw: bool, clockwise, default is False
        """
        super().__init__(*args, **kwargs)
        self.center_point = cen_pt if cen_pt is not None else CadPt()
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
        """ Return a tuple of (x, y) of the Arc center point"""
        return self.center_point.position

    @center.setter
    def center(self, coords: tuple):
        """ Sets the Arc center point to a tuple of (x, y) """
        self.center_point = coords

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
