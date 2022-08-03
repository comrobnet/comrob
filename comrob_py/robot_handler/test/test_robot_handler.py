"""
Test robot handler.
"""
import unittest

from comrob_py.robot_handler.robot_handler import RobotHandler


class TestRobotHandler(unittest.TestCase):
    def setUp(self):
        self.__robot_handler = RobotHandler()
        super().setUp()

    def tearDown(self):
        self.__robot_handler.disconnect()
        super().tearDown()

    def test_init(self):
        """
        Test init.
        """
        pass

