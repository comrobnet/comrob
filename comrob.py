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


def main():
    # load env and initialize bot
    load_dotenv()
    comrob_bot = ComrobBot(irc_token=os.environ['TMI_TOKEN'], nick=os.environ['BOT_NICK'],
                           prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
    # define comrob bot threads
    comrob_bot_thread_1 = threading.Thread(target=comrob_bot.run)

    # start main thread
    comrob_bot_thread_1.start()
    command_buffer = deque()
    while True:
        time.sleep(10)
        comrob_bot_thread_2 = threading.Thread(target=comrob_bot.clear_command_buffer)
        # get buffer
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(comrob_bot.get_command_buffer)
            command_buffer = future.result()

        # clear buffer of bot
        comrob_bot_thread_2.start()
        comrob_bot_thread_2.join()

    comrob_bot_thread_1.join()


if __name__ == '__main__':
    main()
