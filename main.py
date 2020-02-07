#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import datetime
import json

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


bot = commands.Bot(command_prefix=get_prefix)

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_handler = logging.FileHandler(filename="discord.log", encoding='uft-8', filemode="w",)
discord_handler.setFormatter(logging.Formatter(format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%d/%m/%Y '
                                                                                                       '%H:%M,%S'))

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%d/%m/%Y %H:%M,%S', encoding='utf-8',
                    filemode="w", filename="redbot.log", level=logging.INFO)

with open("conf.json") as json_file:
    conf = json.load(json_file)
    json_file.close()


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
    print('bot connected...')


@bot.event
async def on_guild_join(guild):
    """
    TODO: Add logging
    """
    with open("serveur.json", "r") as f:
        server = json.load(f)

    server[str(guild.id)]["prefix"] = "!"

    with open("serveur.json", "w") as f:
        json.dump(server, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    """
    TODO: Add logging
    """
    with open("serveur.json", "r") as f:
        server = json.load(f)

    server.pop(str(guild.id))

    with open("serveur.json", "w") as f:
        json.dump(server, f, indent=4)


@bot.command()
async def prefix(ctx, prefix):
    """
    TODO: Add logging
    """
    with open("serveur.json", "r") as f:
        server = json.load(f)

    server[str(ctx.guild.id)]["prefix"] = prefix

    with open("serveur.json", "w") as f:
        json.dump(server, f, indent=4)

"""
TODO: KICK commands
TODO: BAN commands
TODO: UNBAN commands
TODO: TEMPBAN commands
TODO: TEMPUNBAN tasks
TODO: Logging systeme on the serveur
TODO: HELP commands
TODO: Manage Serveur settings
TODO: Multiple prefix
TODO: CHANGE_PREFIX commands
TODO: Ranks on emote
TODO: Stream alert [ON/OFF]
TODO: STRAWPOLL commands
TODO: User stats
TODO: GET_USERS_STATS commands
"""

bot.run(conf["TOKEN"])
