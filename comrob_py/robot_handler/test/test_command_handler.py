"""
Test file for command handler.
"""
import unittest

from collections import deque

from comrob_py.enums.command_key import CommandKey, FunctionKey
from comrob_py.robot_handler.command_handler import select_command


class TestCommandHandler(unittest.TestCase):
    def test_select_command(self):
        command_buffer_1 = deque()
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [1]})
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [1]})
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [2]})
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [2]})
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [2]})
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [3]})
        command_buffer_1.append({CommandKey.Function: FunctionKey.Height, CommandKey.Args: [2]})
        command_1 = select_command(command_buffer_1)
        # test if correct command is selected and count is correct
        self.assertEqual(command_1, {CommandKey.Function: FunctionKey.Height, CommandKey.Args: [2], CommandKey.Count: 4})
