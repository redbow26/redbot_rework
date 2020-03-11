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


class User(commands.Cog):
    """
    User category commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    @commands.command()
    async def stats(self, ctx, member: discord.Member = None):
        """
        Stats command
        send a embed with the stats of the author or the user

        use:
            !stats [<member>]
        """

        if member is None:
            member = ctx.message.author

        embed = discord.Embed(title=f"{member.display_name}", description=f"{member.name}#{member.discriminator}",
                              colour=discord.Color.blue())
        role_message = ""
        for role in member.roles:
            if role.name != "@everyone":
                role_message += f"{role.name}, "
        if role_message != "":
            role_message = role_message.rstrip(", ")
        else:
            role_message = "Pas de role"

        embed.add_field(name="Role", value=role_message, inline=False)
        embed.add_field(name="Joined at", value=f"{member.joined_at.day}/{member.joined_at.month}/"
                                                f"{member.joined_at.year}", inline=False)
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"{datetime.date.today().day}/{datetime.date.today().month}/"
                              f"{datetime.date.today().year}/")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(User(bot))
