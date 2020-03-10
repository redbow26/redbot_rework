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


class Other(commands.Cog):
    """
    Other category commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def yellowchem(self, ctx):
        """
        yellow chem command
        reply a message

        use:
            !yellowchem
        """

        try:
            self.cursor.execute("SELECT yellowchem FROM SERVER WHERE id_server=?", (str(ctx.guild.id), ))
            data = self.cursor.fetchone()

            if data:
                if data[0]:
                    await ctx.send("yellow chem is fucking trash !")

        except Exception as e:
            logger.error(f'{ctx.message.author} ({ctx.message.author.mention}) in {ctx.guild.name} ({ctx.guild.id}) '
                         f'can not send yellowchem\n{e}')

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def wrongchannel(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Other(bot))
