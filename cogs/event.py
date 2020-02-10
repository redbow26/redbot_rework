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
        """
        TODO: Add logging
        """
        with open("../serveur.json", "r") as f:
            server = json.load(f)

        server[str(guild.id)]["prefix"] = "!"

        with open("../serveur.json", "w") as f:
            json.dump(server, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        TODO: Add logging
        """
        with open("../serveur.json", "r") as f:
            server = json.load(f)

        server.pop(str(guild.id))

        with open("../serveur.json", "w") as f:
            json.dump(server, f, indent=4)


def setup(bot):
    bot.add_cog(Event(bot))
