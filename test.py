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
from comrob_py.robot_handler.user_handler import UserHandler


def main():
    # load env and initialize bot
    load_dotenv()
    # start robot / user handler
    user_handler = UserHandler(edge_length_xy=float(os.environ["EDGE_LENGTH_XY"]),
                               edge_length_z=float(os.environ["EDGE_LENGTH_Z"]),
                               x_offset=float(os.environ["X_OFFSET"]),
                               y_offset=float(os.environ["Y_OFFSET"]),
                               z_offset=float(os.environ["Z_OFFSET"]),
                               xy_base_offset=float(os.environ["XY_BASE_OFFSET"]),
                               z_base_offset=float(os.environ["Z_BASE_OFFSET"]),
                               min_radius_xy=float(os.environ["MIN_RADIUS_XY"]),
                               max_radius_xy=float(os.environ["MAX_RADIUS_XY"]),
                               x_start_user=int(os.environ["X_START_USER"]),
                               y_start_user=int(os.environ["Y_START_USER"]),
                               z_start_user=int(os.environ["Z_START_USER"]))

    time.sleep(5)
    user_handler.position(4, 4)
    time.sleep(5)
    user_handler.height(1)
    user_handler.hold()
    #user_handler.height(3)
    time.sleep(5)
    user_handler.position(4, 5)
    time.sleep(5)
    user_handler.position(4, 6)
    time.sleep(5)
    user_handler.position(3, 4)
    time.sleep(5)
    user_handler.position(3, 5)
    time.sleep(5)
    user_handler.position(3, 6)
    time.sleep(5)
    user_handler.position(2, 4)
    time.sleep(5)
    user_handler.position(2, 5)
    time.sleep(5)
    user_handler.position(2, 6)
    time.sleep(5)
    user_handler.position(3, 7)
    time.sleep(5)
    user_handler.position(2, 7)
    time.sleep(5)
    user_handler.hold()


if __name__ == '__main__':
    main()
