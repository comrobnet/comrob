"""
This class handles the direct communication with the uArm Swift pro.
"""
import time

from uarm_python_sdk.uarm.wrapper.swift_api import SwiftAPI

from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode
from comrob_py.robot_handler.mock_swift_api import MockSwiftApi


class RobotHandler:
    """
    This class handles the direct communication with the uArm swift pro and offers the basic functions.
    """
    def __init__(self):
        """
        Init function.
        """
        # connect to uArm
        try:
            self.__swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
            self.__swift.waiting_ready(timeout=5)
        except Exception:  # can only except like this due to error kind used in swift api
            self.__swift = MockSwiftApi()

        # set general mode: 0
        self.__swift.set_mode(0)

        # initialize empty position values
        self.__x_uarm = 0
        self.__y_uarm = 0
        self.__z_uarm = 0
        self.__wrist_angle = 0
        # set values
        self.reset()

    @property
    def x_uarm(self):
        return self.__x_uarm

    @property
    def y_uarm(self):
        return self.__y_uarm

    @property
    def z_uarm(self):
        return self.__z_uarm

    def disconnect(self):
        """
        Disconnect robot.
        """
        self.__swift.flush_cmd()
        time.sleep(1)
        self.__swift.disconnect()

    def reset(self):
        """
        Reset robot, go back to start position.
        """
        # reset arm to home
        self.__swift.reset(wait=True, speed=10000)
        # get pose values in uarm frame
        pose = self.__swift.get_position()
        # check if successful
        if isinstance(pose, list):
            self.__x_uarm = pose[0]
            self.__y_uarm = pose[1]
            self.__z_uarm = pose[2]
        else:
            message = "Robot position not readable."
            raise ComrobError(ErrorCode.E0008, message)

        # set servo value in degrees
        wrist_angle = 90.0
        self.__swift.set_servo_angle(servo_id=3, angle=wrist_angle)
        self.__wrist_angle = wrist_angle

        self.__swift.flush_cmd()

    def height(self, z):
        """
        Move robot to height in uarm frame.
        :param z: new height of robot to move to, in uarm coordinate frame.
        :type z: float
        """
        self.__swift.set_position(z=z)
        self.__swift.flush_cmd()
        self.__z_uarm = z