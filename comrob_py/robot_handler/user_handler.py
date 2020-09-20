"""
The user handler handles the conversion from user to uarm frame, as well as validity and collision checks.
"""
import numpy

from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode
from comrob_py.robot_handler.robot_handler import RobotHandler


class UserHandler:
    """
    The UserHandler object handles the conversion from user to uarm frame, as well as validity and collision checks.
    """
    def __init__(self, edge_length=40, x_offset=0, y_offset=-320, z_offset=0, xy_base_offset=174, z_base_offset=93.5,
                 min_radius_xy=120, max_radius_xy=340):
        """
        Constructor, defines basic values of user frame.
        :param edge_length: side length of unit cube in mm
        :type edge_length: float
        :param x_offset: offset of user frame in x direction in mm
        :type x_offset: float
        :param y_offset: offset of user frame in y direction in mm
        :type y_offset: float
        :param z_offset: offset of user frame in z direction in mm
        :type z_offset: float
        :param xy_base_offset: offset of workspace in xy-plane
        :type xy_base_offset: float
        :param z_base_offset: offset of uarm base in z-direction in mm
        :type z_base_offset: float
        :param min_radius_xy: minimum workspace radius
        :type min_radius_xy:float
        :param max_radius_xy: maximum workspace radius
        :type max_radius_xy: float
        """
        self.__edge_length = edge_length
        self.__x_offset = x_offset
        self.__y_offset = y_offset
        self.__z_offset = z_offset
        self.__xy_base_offset = xy_base_offset
        self.__z_base_offset = z_base_offset
        self.__min_radius_xy = min_radius_xy
        self.__max_radius_xy = max_radius_xy

        # initialize robot handler
        self.__robot_handler = RobotHandler()

    def position_user_to_uarm(self, x_user, y_user, z_uarm):
        """
        Transform x, y -position in user frame to x, y position in uarm frame. For user frame specification refer
        to the board design. Checks if position is in workspace.
        :param x_user: x-position in user frame
        :type x_user: int
        :param y_user: y-position in user frame
        :type y_user: int
        :paramDie gewünschte Höhe ist für den Roboter nicht erreichbar, bitte geben Sie einen anderen Wert an z_uarm: z-position in uarm frame
        :type z_uarm: float
        :return: position in uarm frame {'x': x, 'y', y}
        :rtype: dict
        """
        # transform coordinates
        # adding .5 to be in center of square
        x_uarm = (x_user + .5) * self.__edge_length + self.__x_offset
        y_uarm = (y_user + .5) * self.__edge_length + self.__y_offset

        # check if input is in range of robot
        # TODO (ALR): This is not at all accurate, check if this is good enough.
        xy_length = numpy.sqrt(x_uarm ** 2 + y_uarm ** 2)
        xy_radius = abs(xy_length - self.__xy_base_offset)
        z_radius = abs(z_uarm - self.__z_base_offset)
        radius = numpy.sqrt(xy_radius ** 2 + z_radius ** 2)
        if radius > (self.__max_radius_xy - self.__xy_base_offset) or x_uarm < 0 or xy_length <= self.__min_radius_xy:
            message = "Position is not in working range of robot."
            raise ComrobError(ErrorCode.E0009, message)

        return {'x': x_uarm, 'y': y_uarm}

    def height_user_to_uarm(self, z_user, x_uarm, y_uarm):
        """
        Transform z-position in user frame to uarm frame, check if height is in workspace.
        :param z_user: z-position in user frame
        :type z_user: int
        :param x_uarm: x-position in uarm frame
        :type x_uarm: float
        :param y_uarm: y-position in uarm frame
        :type y_uarm: float
        :return: z position in uarm frame in mm
        :rtype: float
        """
        # calculate height in uarm frame
        z_uarm = self.__z_offset + z_user * self.__edge_length

        # check if height is valid
        xy_length = numpy.sqrt(x_uarm ** 2 + y_uarm ** 2)
        xy_radius = abs(xy_length - self.__xy_base_offset)
        z_radius = abs(z_uarm - self.__z_base_offset)
        radius = numpy.sqrt(xy_radius ** 2 + z_radius ** 2)
        # check if z_uarm value in workspace
        if radius > (
                self.__max_radius_xy - self.__xy_base_offset) or z_uarm < self.__z_offset or z_uarm < self.__edge_length + self.__z_offset:
            message = "Height is not in working range of robot."
            raise ComrobError(ErrorCode.E0004, message)

        return z_uarm

    def height(self, z_user):
        """
        Move to new height in user frame.
        """
        z_uarm = self.height_user_to_uarm(z_user, self.__robot_handler.x_uarm, self.__robot_handler.y_uarm)
        # TODO (ALR): Add collision tests.
        self.__robot_handler.height(z_uarm)

