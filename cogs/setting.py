#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


class Setting(commands.Cog):
    """
    Setting commands
    """
    def __init__(self, bot):
        self.bot = bot

    # TODO: Manage Server settings

    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
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
