#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if member is not None:
            dm = await member.create_dm()
            await dm.send(f"{ctx.message.author.mention} send you a hug")
        else:
            dm = await ctx.message.author.create_dm()
            await dm.send("*hug*")


def setup(bot):
    bot.add_cog(Fun(bot))
