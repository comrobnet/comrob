"""
Main file of comrob project, running the comrob bot and robot controller.
"""
import concurrent.futures
import os
import threading
import time

from collections import deque
from dotenv import load_dotenv

from comrob_py.comrob_bot.comrob_bot import ComrobBot
from comrob_py.enums.command_key import CommandKey, FunctionKey
from comrob_py.robot_handler.command_handler import select_command, send_message
from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode


def main():
    # load env and initialize bot
    load_dotenv()
    comrob_bot = ComrobBot(irc_token=os.environ['TMI_TOKEN'], nick=os.environ['BOT_NICK'],
                           prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
    # start main thread
    comrob_bot_thread_1 = threading.Thread(target=comrob_bot.run)
    comrob_bot_thread_1.start()

    command_buffer = deque()
    loop_time = 5
    while True:
        # define threads for loop
        comrob_bot_thread_2 = threading.Thread(target=comrob_bot.clear_command_buffer)
        send_message(comrob_bot, "You have now " + str(loop_time) + "s to enter commands for the robot.")
        time.sleep(loop_time)

        # get buffer
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(comrob_bot.get_command_buffer)
            command_buffer = future.result()

        try:
            command = select_command(command_buffer)
            send_message(comrob_bot, "Selected command: " + command[CommandKey.Function].value +
                         ", args: " + str(command[CommandKey.Args]) +
                         ", votes: " + str(command[CommandKey.Count]) + ".")
        except ComrobError as error:
            if error.error_code is not ErrorCode.E0011:
                raise ComrobError(error.error_code, error.message)
            send_message(comrob_bot, error.message)

        # clear buffer of bot
        comrob_bot_thread_2.start()
        comrob_bot_thread_2.join()

    comrob_bot_thread_1.join()


if __name__ == '__main__':
    main()
