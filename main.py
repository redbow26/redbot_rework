#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import datetime
import json
import os

# Other Libs
import discord
from discord.ext import commands

# Owned
__author__ = "Tristan Leroy"
__copyright__ = "None"
__credits__ = ["Tristan Leroy"]
__license__ = "None"
__version__ = "0.0.1"
__maintainer__ = "Tristan Leroy"
__email__ = "contact@redbow.fr"
__status__ = "Devs"


def get_prefix(client, message):
    """
    Get a prefix in the serveur.json file for a specific server
    """
    with open("serveur.json", "r") as f:
        server = json.load(f)
    if message.guild:
        return server[str(message.guild.id)]["prefix"]
    else:
        return "!"


# Load the config (TOKEN) in the conf.json file
with open("conf.json") as json_file:
    conf = json.load(json_file)
    json_file.close()

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")

# Create logger and handler for discord
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_handler = logging.FileHandler(filename="discord.log", mode='w')
discord_handler.setFormatter(logging.Formatter(fmt='%(levelname)-8s | %(asctime)-15s | %(name)-15s | %(message)s'))
discord_logger.addHandler(discord_handler)

# Create logger for all of the bot
logger = logging.getLogger("redbot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="redbot.log", mode='w')
handler.setFormatter(logging.Formatter(fmt='%(levelname)-8s | %(asctime)-15s | %(name)-15s | %(message)s'))
logger.addHandler(handler)


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """
    Use for load a cogs
    """
    if extension + ".py" in os.listdir("./cogs"):
        try:
            bot.load_extension(f"cogs.{extension}")
            dm = await ctx.message.author.create_dm()
            await dm.send(f"{extension} has been load")
            logger.info(f"{extension} load")
        except Exception as e:
            logger.error(f"bot can not load {extension}\n{e}")
    else:
        ctx.send("The extension can not be load")
        logger.error(f"{extension} can not be load")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """
        Use for unload a cogs
    """
    try:
        bot.unload_extension(f"cogs.{extension}")
        dm = await ctx.message.author.create_dm()
        await dm.send(f"{extension} has been unload")
        logger.info(f"{extension} unload")
    except Exception as e:
        logger.error(f"bot can not unload {extension}\n{e}")

# TODO: Ranks on emote
# TODO: Stream alert [ON/OFF]
# TODO: STRAWPOLL commands
# TODO: User stats
# TODO: GET_USERS_STATS commands

# Load all the cogs at the launch of the bot
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            logger.error(f"bot can not load {filename[:-3]} | {e}")

# Launch le bot
bot.run(conf["TOKEN"])
