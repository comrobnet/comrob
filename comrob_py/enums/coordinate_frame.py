"""
This file stores the enums used by the coordinate class.
"""
from enum import Enum


class CoordinateFrame(Enum):
    """
    The CoordinateFrame enum denotes the kind of frame of coordinates, e.g user frame or uarm frame.
    """
    User = "user"
    Uarm = "uarm"
