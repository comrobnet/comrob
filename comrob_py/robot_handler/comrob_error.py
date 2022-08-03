"""
This file contains the custom ComrobError class.
"""
from enum import Enum


class ComrobError(Exception):
    """
    Custom ComrobError class.
    """

    def __init__(self, error_code, message):
        """
        Constructor.
        :param error_code: unique error code
        :type error_code: ErrorCode
        :param message: error message
        :type message: str
        """
        self.__error_code = error_code
        self.__message = message

    @property
    def error_code(self):
        return self.__error_code

    @property
    def message(self):
        return self.__message


class ErrorCode(Enum):
    """
    Unique ErrorCode enum for each error.
    """
    E0000 = 0
    E0001 = 1
    E0002 = 2
    E0003 = 3  
    E0004 = 4  
    E0005 = 5  
    E0006 = 6  
    E0007 = 7  
    E0008 = 8  # RobotHandler
    E0009 = 9  # UserHandler
    E0010 = 10  # UserHandler
    E0011 = 11  # CommandHandler
    E0012 = 12  # UserHandler
    E0013 = 13  # UserHandler
