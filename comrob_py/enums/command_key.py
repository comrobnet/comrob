"""
Command enum class storing keys for enum dictionaries.
"""

from enum import Enum


class CommandKey(Enum):
    function = 0
    args = 1
    kwargs = 2
    user = 3
