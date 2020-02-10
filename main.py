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
    with open("serveur.json", "r") as f:
        server = json.load(f)

    return server[str(message.guild.id)]["prefix"]


with open("conf.json") as json_file:
    conf = json.load(json_file)
    json_file.close()

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_handler = logging.FileHandler(filename="discord.log", mode='w')
discord_handler.setFormatter(logging.Formatter(fmt='%(levelname)-8s | %(asctime)-15s | %(name)-15s | %(message)s'))
discord_logger.addHandler(discord_handler)

logger = logging.getLogger("redbot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="redbot.log", mode='w')
handler.setFormatter(logging.Formatter(fmt='%(levelname)-8s | %(asctime)-15s | %(name)-15s | %(message)s'))
logger.addHandler(handler)

@bot.command()
async def load(ctx, extension):
    if extension + ".py" in os.listdir("./cogs"):
        try:
            bot.load_extension(f"cogs.{extension}")
            logger.info(f"{extension} load")
        except Exception as e:
            logger.error(f"bot can not load {extension} | {e}")
    else:
        ctx.send("The extension can not be load")
        logger.error(f"{extension} can not be load")


@bot.command()
async def unload(ctx, extension):
    if extension + ".py" in os.listdir("./cogs"):
        try:
            bot.unload_extension(f"cogs.{extension}")
            logger.info(f"{extension} unload")
        except Exception as e:
            logger.error(f"bot can not unload {extension} | {e}")
    else:
        ctx.send("The extension can not be unload")
        logger.error(f"{extension} can not be unload")


@bot.command()
async def prefix(ctx, arg):
    """
    TODO: Add logging
    """
    with open("serveur.json", "r") as f:
        server = json.load(f)

    server[str(ctx.guild.id)]["prefix"] = arg

    with open("serveur.json", "w") as f:
        json.dump(server, f, indent=4)

# TODO: KICK commands
# TODO: BAN commands
# TODO: UNBAN commands
# TODO: TEMPBAN commands
# TODO: TEMPUNBAN tasks
# TODO: Logging systeme on the serveur
# TODO: HELP commands
# TODO: Manage Serveur settings
# TODO: Ranks on emote
# TODO: Stream alert [ON/OFF]
# TODO: STRAWPOLL commands
# TODO: User stats
# TODO: GET_USERS_STATS commands


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            logger.error(f"bot can not load {filename[:-3]} | {e}")

bot.run(conf["TOKEN"])
