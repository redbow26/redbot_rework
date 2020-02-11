#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Setting(commands.Cog):
    """
    Setting commands
    """
    def __init__(self, bot):
        self.bot = bot

    # TODO: Manage Server settings

    @commands.command()
    async def prefix(self, ctx, arg):
        try:
            with open("../serveur.json", "r") as f:
                server = json.load(f)

            server[str(ctx.guild.id)]["prefix"] = arg

            with open("../serveur.json", "w") as f:
                json.dump(server, f, indent=4)
                
            logger.info(f"Prefix changed for {ctx.guild.name}")
        except Exception as e:
            logger.error(f"Prefix not change for {ctx.guild.name}\n{e}")


def setup(bot):
    bot.add_cog(Setting(bot))
