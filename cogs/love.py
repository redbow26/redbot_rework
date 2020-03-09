#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import datetime
import json
import os
import asyncio
import sqlite3

# Other Libs
import discord
from discord.ext import commands

discord_logger = logging.getLogger('discord')
logger = logging.getLogger("redbot")


class Love(commands.Cog):
    """
    Love category commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        if member is not None and member != self.bot:
            dm = await member.create_dm()
            await dm.send(f"{author.name} send you a hug")
        else:
            dm = await author.create_dm()
            await dm.send("*hug*")

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def kiss(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        if member is not None:
            dm = await member.create_dm()
            await dm.send(f"{author.name} kiss you")
        else:
            dm = await author.create_dm()
            await dm.send("*kiss*")

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def boop(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        if member is not None:
            dm = await member.create_dm()
            await dm.send(f"{author.name} boop you")
        else:
            dm = await author.create_dm()
            await dm.send("*boop*")


def setup(bot):
    bot.add_cog(Love(bot))
