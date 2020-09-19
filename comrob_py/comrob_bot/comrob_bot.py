"""
This file contains the twitch-bot allowing to communicate with the comrob.
"""
import os

from collections import deque
from dotenv import load_dotenv
from twitchio.ext import commands


load_dotenv()

command_buffer = deque()

# set up the bot
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)


@bot.event
async def event_ready():
    """
    Called once when the bot goes online.
    """
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


@bot.event
async def event_message(context):
    """
    Runs every time a message is sent in chat.
    """
    # make sure the bot ignores itself and the streamer
    if context.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    # if content of message is a command, add it to command buffer
    if context.content[0] == "!":
        command_buffer.append(context.content)

    print("Command Buffer: ", command_buffer)
    # await bot.handle_commands(context)


@bot.command(name='test')
async def test(context):
    await context.send('test passed!')


if __name__ == "__main__":
    bot.run()
