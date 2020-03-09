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
        try:
            self.cursor.execute("SELECT hug FROM SERVER WHERE id_server=?", (str(ctx.guild.id), ))
            data = self.cursor.fetchone()

            if data:
                if data[0]:
                    author = ctx.message.author
                    if member is not None and member != self.bot:
                        dm = await member.create_dm()
                        await dm.send(f"{author.name} send you a hug")
                    else:
                        dm = await author.create_dm()
                        await dm.send("*hug*")

        except Exception as e:
            logger.error(f'{ctx.message.author} ({ctx.message.author.mention}) in {ctx.guild.name} ({ctx.guild.id}) '
                         f'can not hug\n{e}')

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def kiss(self, ctx, member: discord.Member = None):
        try:
            self.cursor.execute("SELECT kiss FROM SERVER WHERE id_server=?", (str(ctx.guild.id), ))
            data = self.cursor.fetchone()

            if data:
                if data[0]:
                    author = ctx.message.author
                    if member is not None:
                        dm = await member.create_dm()
                        await dm.send(f"{author.name} kiss you")
                    else:
                        dm = await author.create_dm()
                        await dm.send("*kiss*")

        except Exception as e:
            logger.error(f'{ctx.message.author} ({ctx.message.author.mention}) in {ctx.guild.name} ({ctx.guild.id}) '
                         f'can not kiss\n{e}')

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def boop(self, ctx, member: discord.Member = None):
        try:
            self.cursor.execute("SELECT boop FROM SERVER WHERE id_server=?", (str(ctx.guild.id), ))
            data = self.cursor.fetchone()

            if data:
                if data[0]:
                    author = ctx.message.author
                    if member is not None:
                        dm = await member.create_dm()
                        await dm.send(f"{author.name} boop you")
                    else:
                        dm = await author.create_dm()
                        await dm.send("*boop*")

        except Exception as e:
            logger.error(f'{ctx.message.author} ({ctx.message.author.mention}) in {ctx.guild.name} ({ctx.guild.id}) '
                         f'can not boop\n{e}')


def setup(bot):
    bot.add_cog(Love(bot))
