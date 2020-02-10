#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="!commande [arg] [...]", colour=discord.Color.red())
        embed.add_field(name="Classique", value="`!help`", inline=True)
        embed.add_field(name="Modération", value="`!kick`\n`!ban`\n`!tempban`", inline=True)
        embed.add_field(name="Setting", value="`!prefix`\n`!config`", inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
