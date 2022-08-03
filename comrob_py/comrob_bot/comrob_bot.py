"""
This file contains the twitch-bot allowing to communicate with the comrob.
"""
import asyncio

from collections import deque
from twitchio.ext import commands

from comrob_py.enums.command_key import CommandKey, FunctionKey


class ComrobBot:
    """
    The ComrobBot class handles the communication with the twitch chat and the robot controller
    """
    def __init__(self, irc_token, nick, prefix, initial_channels):
        """
        Init function for the bot.
        :param irc_token: oath token to use for irc for twitch chat
        :type irc_token: str
        :param nick: nickname of bot
        :type nick: str
        :param prefix: prefix for bot command
        :type prefix: str
        :param initial_channels: channels for bot to join on startup
        :type initial_channels: list
        """
        # set up the bot
        self.__bot = commands.Bot(irc_token=irc_token, nick=nick, prefix=prefix, initial_channels=initial_channels)
        self.__command_buffer = deque()

        self.__set_up()

    def __set_up(self):
        """
        Set-up function for the bot, declaring event-functions and commands.
        """
        @self.__bot.event
        async def event_ready():
            """
            Function called when the bot goes online.
            """
            print(self.__bot.nick, "is online!")
            # this is only needed to send messages within event_ready
            ws = self.__bot._ws
            await ws.send_privmsg(*self.__bot.initial_channels, f"/me is online!")

        @self.__bot.event
        async def event_message(context):
            """
            Runs every time a message is sent in chat.
            :param context: message context
            :type context: twitchio.dataclasses.Message
            """
            # make sure the bot ignores itself and the streamer
            if context.author.name.lower() == self.__bot.nick.lower():
                return

            await self.__bot.handle_commands(context)

        @self.__bot.command()
        async def height(context, z: int):
            """
            Height command !height z. Adds command "height" with argument z to the command queue.
            :param context: message context
            :type context: twitchio.dataclasses.Message
            :param z: argument of height function, indicates target height of robot in user frame
            :type z: int
            """
            user_name = context.author.name.lower()
            if self.__check_user(user_name):
                await context.send("Only one command per user per session @" + user_name + ".")
                return
            self.__command_buffer.append({CommandKey.Function: FunctionKey.Height,
                                          CommandKey.Args: [z],
                                          CommandKey.User: user_name})
            await context.send("Command: \"height " + str(z) + "\" added to the command queue.")

        @self.__bot.command()
        async def position(context, x: int, y: int):
            """
            Position command !position x y. Adds command position with arguments x and y to the command queue.
            :param context: message context
            :type context: twitchio.dataclasses.Message
            :param x: argument of position function, indicates target x-position of robot in user frame
            :type x: int
            :param y: argument of position function, indicates target y-position of robot in user frame
            :type y: int
            """
            user_name = context.author.name.lower()
            if self.__check_user(user_name):
                await context.send("Only one command per user per session @" + user_name + ".")
                return
            self.__command_buffer.append({CommandKey.Function: FunctionKey.Position,
                                          CommandKey.Args: [x, y],
                                          CommandKey.User: user_name})
            await context.send("Command: \"position " + str(x) + " " + str(y) + "\" added to the command queue.")

        @self.__bot.command()
        async def hold(context):
            """
            Hold command !position x y. Adds command hold to the command queue. Toggles holding of a block.
            :param context: message context
            :type context: twitchio.dataclasses.Message
            """
            user_name = context.author.name.lower()
            if self.__check_user(user_name):
                await context.send("Only one command per user per session @" + user_name + ".")
                return
            self.__command_buffer.append({CommandKey.Function: FunctionKey.Hold,
                                          CommandKey.Args: [],
                                          CommandKey.User: user_name})
            await context.send("Command: \"hold\" added to the command queue.")

    def run(self):
        """
        Run bot, initialize event loop (blocking).
        """
        self.__bot.run()

    def get_command_buffer(self):
        """
        Get command buffer.
        :return: buffer storing all command added
        :rtype: deque
        """
        return self.__command_buffer.copy()

    def clear_command_buffer(self):
        """
        Clears command buffer.
        """
        self.__command_buffer = deque()

    def send_message(self, message):
        """
        Send message to stream at any time.
        :param message: message to be sent in channel chat
        :type message: str
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.__bot._ws.send_privmsg(*self.__bot.initial_channels, message))
        loop.close()

    def __check_user(self, user_name):
        """
        Check if user already submitted command in command queue.
        :param user_name: name of user to be checked
        :type user_name: str
        :return: true if user name in command buffer
        :rtype: bool
        """
        return user_name in [info[CommandKey.User] for info in self.__command_buffer]
