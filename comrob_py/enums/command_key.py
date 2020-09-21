"""
Command enum class storing keys for enum dictionaries.
"""

from enum import Enum


class CommandKey(Enum):
    Function = 0
    Args = 1
    Kwargs = 2
    User = 3
    Count = 4


class FunctionKey(Enum):
    Height = "height"
