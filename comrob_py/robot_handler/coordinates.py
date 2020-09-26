"""
This file contains the coordinates object, which is used to store coordinates in different frames.
"""
import numpy

from comrob_py.enums.coordinate_frame import CoordinateFrame
from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode


class Coordinates:
    """
    The coordinates class stores coordinates in different frames and offers different functionalities.
    """
    def __init__(self, x, y, z, coordinate_frame):
        """
        Initialization method
        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param z: z-coordinate
        :type z: float
        :param coordinate_frame: frame of given coordinates
        :type coordinate_frame: CoordinateFrame        
        """
        self.__coordinates = numpy.array([x, y, z])
        self.__coordinate_frame = coordinate_frame

    def __copy__(self):
        """
        Copy override.
        """
        return Coordinates(self.x, self.y, self.z, self.__coordinate_frame)

    def copy(self):
        """
        Copy override.
        """
        return self.__copy__()

    @property
    def x(self):
        """
        x getter.
        """
        return self.__coordinates[0]
    
    @property
    def y(self):
        """
        y getter.
        """
        return self.__coordinates[1]
    
    @property
    def z(self):
        """
        z getter.
        """
        return self.__coordinates[2]

    @property
    def coordinate_frame(self):
        """
        coordinate_frame getter.
        """
        return self.__coordinate_frame

    @x.setter
    def x(self, x):
        """
        x setter.
        """
        self.__coordinates[0] = x

    @y.setter
    def y(self, y):
        """
        y setter.
        """
        self.__coordinates[1] = y
    
    @z.setter
    def z(self, z):
        """
        z setter.
        """
        self.__coordinates[2] = z
