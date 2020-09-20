"""
Main file for the comrob bot.
"""
import os

from dotenv import load_dotenv

from comrob_py.comrob_bot.comrob_bot import ComrobBot


if __name__ == '__main__':
    load_dotenv()
    comrob_bot = ComrobBot(irc_token=os.environ['TMI_TOKEN'], nick=os.environ['BOT_NICK'],
                           prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
    comrob_bot.run()

