"""
Test file for coordinates.py
"""
import unittest

from comrob_py.enums.coordinate_frame import CoordinateFrame
from comrob_py.robot_handler.coordinates import Coordinates


class TestCoordinates(unittest.TestCase):
    """
    Unittest for Coordinates class.
    """
    def test_init(self):
        """
        Test initialization and setters/getters.
        """
        x_1 = 1
        y_1 = 2
        z_1 = 3
        c_1 = Coordinates(x_1, y_1, z_1, CoordinateFrame.User)
        # test getters
        self.assertEqual(x_1, c_1.x)
        self.assertEqual(y_1, c_1.y)
        self.assertEqual(z_1, c_1.z)
        self.assertEqual(CoordinateFrame.User, c_1.coordinate_frame)
        # test setters
        x_2 = 4
        y_2 = 5
        z_2 = 6
        c_1.x = x_2
        c_1.y = y_2
        c_1.z = z_2
        self.assertEqual(x_2, c_1.x)
        self.assertEqual(y_2, c_1.y)
        self.assertEqual(z_2, c_1.z)


