"""
This file contains the twitch-bot allowing to communicate with the comrob.
"""
from twitchio.ext import commands


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
        self.set_up()

    def set_up(self):
        """
        Set-up function for the bot, declaring event-functions and commands.
        """
        @self.__bot.event
        async def event_ready():
            """
            Function called when the bot goes online.
            """
            print(f"{self.__bot.nick} is online!")
            # this is only needed to send messages within event_ready
            ws = self.__bot._ws
            await ws.send_privmsg(self.__bot.initial_channels, f"/me is online!")

        @self.__bot.event
        async def event_message(context):
            """
            Runs every time a message is sent in chat.
            """
            # make sure the bot ignores itself and the streamer
            if context.author.name.lower() == self.__bot.nick.lower():
                return

            # # if content of message is a command, add it to command buffer
            # if context.content[0] == "!":
            #     command_buffer.append(context.content)
            #
            # print("Command Buffer: ", command_buffer)

            await self.__bot.handle_commands(context)

        @self.__bot.command(name='test')
        async def test(context):
            await context.send('test passed!')

    def run(self):
        """
        Run bot, initialize event loop (blocking).
        """
        self.__bot.run()

