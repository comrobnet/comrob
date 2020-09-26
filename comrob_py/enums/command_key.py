"""
Command enum class storing keys for enum dictionaries.
"""

from enum import Enum


class CommandKey(Enum):
    Function = 0
    Args = 1
    User = 2
    Count = 3


class FunctionKey(Enum):
    Height = "height"
    Position = "position"
    Pump = "pump"
