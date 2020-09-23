"""
This file offers functions that handle the command queue.
"""
import time
import threading

from comrob_py.enums.command_key import CommandKey, FunctionKey
from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode


def select_command(command_queue):
    """
    This functions gets a command queue and selects the function which gets the most votes from users.
    :param command_queue: dictionary containing commands and arguments from different users.
    :type command_queue: dequeue
    :return: command with highest number of votes, first command otherwise
    :rtype: dict
    """
    if len(command_queue) == 0:
        message = "No command in command queue."
        raise ComrobError(ErrorCode.E0011, message)

    # count number of commands
    command_ranking = dict()
    for command in command_queue:
        # turn function and args into tuples to be hashable
        command_tuple = (command[CommandKey.Function], tuple(command[CommandKey.Args]))
        if command_ranking.get(command_tuple, False):
            command_ranking[command_tuple] += 1
        else:
            command_ranking[command_tuple] = 1

    max_count = 0
    max_command = None
    for command in command_ranking:
        if command_ranking[command] > max_count:
            max_command = command
            max_count = command_ranking[command]

    return {CommandKey.Function: max_command[0], CommandKey.Args: list(max_command[1]), CommandKey.Count: max_count}


def send_message(bot, message):
    """
    Utility function which sends a message on the bot.
    :param bot: bot on which to send the message
    :type bot: ComrobBot
    :param message: message to send on the bot
    :type message: str
    """
    thread = threading.Thread(target=bot.send_message, args=(message,))
    thread.start()
    thread.join()
