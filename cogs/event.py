#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
        print('bot connected...')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            with open("../serveur.json", "r") as f:
                server = json.load(f)
    
            server[str(guild.id)]["prefix"] = "!"
    
            with open("../serveur.json", "w") as f:
                json.dump(server, f, indent=4)
            logger.info(f"{guild.name} ({guild.id}) has been added to the serveur.json")

        except Exception as e:
            logger.error(f"{guild.name} ({guild.id}) can not be added to the serveur.json | {e}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            with open("../serveur.json", "r") as f:
                server = json.load(f)

            server.pop(str(guild.id))

            with open("../serveur.json", "w") as f:
                json.dump(server, f, indent=4)
            logger.info(f"{guild.name} ({guild.id}) has been removed from the server.json")

        except Exception as e:
            logger.error(f"{guild.name} ({guild.id}) can not be removed to the serveur.json | {e}")


def setup(bot):
    bot.add_cog(Event(bot))
