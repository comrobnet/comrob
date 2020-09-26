"""
The user handler handles the conversion from user to uarm frame, as well as validity and collision checks.
"""
import numpy
import time

from comrob_py.enums.coordinate_frame import CoordinateFrame
from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode
from comrob_py.robot_handler.coordinates import Coordinates
from comrob_py.robot_handler.robot_handler import RobotHandler


class UserHandler:
    """
    The UserHandler object handles the conversion from user to uarm frame, as well as validity and collision checks.
    """
    def __init__(self, edge_length=40, x_offset=0, y_offset=-320, z_offset=0, xy_base_offset=174, z_base_offset=93.5,
                 min_radius_xy=120, max_radius_xy=340, x_start_user=4, y_start_user=8, z_start_user=3):
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
        :type min_radius_xy: float
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

        # track coordinates in user frame
        self.__coordinates = Coordinates(x_start_user, y_start_user, z_start_user, CoordinateFrame.User)
        # track pump status
        self.__pump = False

        # initialize robot handler
        self.__robot_handler = RobotHandler()

        # move to start position
        self.position(self.__coordinates.x, self.__coordinates.y)
        self.height(self.__coordinates.z)

    def __transform(self, coordinates, coordinate_frame):
        """
        Transform coordinates to given frame.
        :param coordinates: coordinates to transform.
        :type coordinates: Coordinates
        :param coordinate_frame: coordinate frame to transform to
        :type coordinate_frame: CoordinateFrame
        """
        if coordinate_frame is coordinates.coordinate_frame:
            message = "The coordinates are already in the desired frame."
            raise ComrobError(ErrorCode.E0012, message)

        # transform from user to uarm
        if coordinate_frame is CoordinateFrame.Uarm and coordinates.coordinate_frame is CoordinateFrame.User:
            x_uarm = (coordinates.x + .5) * self.__edge_length + self.__x_offset
            y_uarm = (coordinates.y + .5) * self.__edge_length + self.__y_offset
            z_uarm = (coordinates.z + .5) * self.__edge_length + self.__z_offset
            coordinates_uarm = Coordinates(x_uarm, y_uarm, z_uarm, coordinate_frame)
            self.__check_workspace(coordinates_uarm)
            return coordinates_uarm

        raise NotImplementedError()

    def height(self, z_user):
        """
        Move to new height in user frame.
        """
        # only change copy before all checks are performed
        new_coordinates_user = self.__coordinates.copy()
        new_coordinates_user.z = z_user
        new_coordinates_uarm = self.__transform(new_coordinates_user, CoordinateFrame.Uarm)
        # TODO (ALR): Add collision tests.
        self.__robot_handler.height(new_coordinates_uarm.z)
        # change coordinates if everything is successful
        self.__coordinates = new_coordinates_user

    def position(self, x_user, y_user):
        """
        Move to position in user frame, keep alignment of end-effector.
        :param x_user: x-position in user frame to move to
        :type x_user: int
        :param y_user: y-position in user frame to move to
        :type y_user: int
        """
        new_coordinates_user = self.__coordinates.copy()
        new_coordinates_user.x = x_user
        new_coordinates_user.y = y_user
        new_coordinates_uarm = self.__transform(new_coordinates_user, CoordinateFrame.Uarm)
        # TODO (ALR): Add collision tests.
        self.__robot_handler.position(new_coordinates_uarm.x, new_coordinates_uarm.y)
        # change wrist rotation to keep orthogonal cube orientation
        new_wrist_angle = self.__calculate_equal_wrist_rotation(self.__coordinates, new_coordinates_user)
        self.__robot_handler.rotate_wrist(new_wrist_angle)
        # change coordinates if everything is successful
        self.__coordinates = new_coordinates_user

    def hold(self):
        """
        Pick-up or drop cube below end-effector.
        The end-effector needs to be above a block to start the pump. The block needs to be directly above the ground
        or another block to turn the pump off.
        """
        # TODO (ALR): Add valid check.
        hold_coordinates_user = self.__coordinates.copy()
        hold_coordinates_uarm = self.__transform(hold_coordinates_user, CoordinateFrame.Uarm)
        z_before_move_uarm = hold_coordinates_uarm.z
        hold_coordinates_uarm.z -= 0.5 * self.__edge_length
        # move down to block surface and wait for command to finish
        self.__robot_handler.height(hold_coordinates_uarm.z)
        time.sleep(0.5)
        # toggle pump
        self.__robot_handler.pump(not self.__pump)
        time.sleep(0.5)
        self.__pump = not self.__pump
        # move back up
        self.__robot_handler.height(z_before_move_uarm)

    def __check_workspace(self, coordinates_uarm):
        """
        Check if coordinates in uarm frame are within the workspace of the robot.
        :param coordinates_uarm: coordinates in uarm frame
        :type coordinates_uarm: Coordinates
        """
        # check if input is in range of robot
        # TODO (ALR): This is not at all accurate, check if this is good enough.
        xy_length = numpy.sqrt(coordinates_uarm.x ** 2 + coordinates_uarm.y ** 2)
        xy_radius = abs(xy_length - self.__xy_base_offset)
        z_radius = abs(coordinates_uarm.z - self.__z_base_offset)
        radius = numpy.sqrt(xy_radius ** 2 + z_radius ** 2)
        if radius > (self.__max_radius_xy - self.__xy_base_offset) or\
                coordinates_uarm.x < 0 or\
                xy_length <= self.__min_radius_xy or\
                coordinates_uarm.z < self.__edge_length + self.__z_offset:
            message = "Position is not in workspace of robot."
            raise ComrobError(ErrorCode.E0009, message)

    def __calculate_equal_wrist_rotation(self, old_coordinates_user, new_coordinates_user):
        """
        Calculates new wrist rotation that keeps the end-effector rotation equal in the world frame.
        :param old_coordinates_user: coordinates of previous position in user frame
        :type old_coordinates_user: Coordinates
        :param new_coordinates_user: coordinates of new position in user frame
        :type new_coordinates_user: Coordinates
        :return: new wrist angle that keeps the object in the same orientation
        :rtype: float
        """
        old_coordinates_uarm = self.__transform(old_coordinates_user, CoordinateFrame.Uarm)
        new_coordinates_uarm = self.__transform(new_coordinates_user, CoordinateFrame.Uarm)
        # angle from world x-axis to arm
        alpha_1_rad = numpy.arctan2(old_coordinates_uarm.y, old_coordinates_uarm.x)
        alpha_2_rad = numpy.arctan2(new_coordinates_uarm.y, new_coordinates_uarm.x)
        alpha_1_deg = numpy.degrees(alpha_1_rad)
        alpha_2_deg = numpy.degrees(alpha_2_rad)
        # angle from world x-axis to end effector orientation (-90 because of the asymmetric servo range 0-180)
        beta_1 = alpha_1_deg + 90.0 - self.__robot_handler.wrist_angle
        # calculate the corresponding new wrist angle for new position, so that the orientation of the grabbed object
        # stays the same
        wrist_new = -beta_1 + alpha_2_deg + 90.0
        # TODO (ALR): We can add a modulo here if there is an issue with this.
        # check that the wrist angle is within the servos range
        if not (0 <= wrist_new <= 180):
            message = "Wrist angle out of range"
            raise ComrobError(ErrorCode.E0003, message)

        return wrist_new
