import discord
from discord.ext import commands
import logging
import datetime
import json

bot = commands.Bot(command_prefix=">")
logging.basicConfig(format='%(levelname)s|%(asctime)s|%(message)s', datefmt='%d/%m/%Y %H:%M,%S', filename="redbot.log", filemode="w", level=logging.INFO)

with open("config.json") as json_file:
    conf = json.load(json_file)
    json_file.close()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))
    print('bot connected...')

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