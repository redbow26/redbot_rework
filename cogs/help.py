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


class Help(commands.Cog):
    """
    Help category commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    # General help
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="!command [<arg> <arg> ...]"
                                                        "\nargument = <argument>"
                                                        "\noptionnal argument = [<argument>]"
                                                        "\nchoice argument = (<arg1> | <arg2>)", colour=discord.Color.red())
        embed.add_field(name="Classique", value="`!help`", inline=True)
        embed.add_field(name="Modération", value="`!kick`\n`!ban`\n`!tempban`", inline=True)
        embed.add_field(name="Setting", value="`!prefix`\n`!config`", inline=True)
        embed.add_field(name="Love", value="`!hug`\n`!kiss`\n`!boop`", inline=True)
        embed.add_field(name="Other", value="`!yellowchem`", inline=True)
        embed.add_field(name="Strawpoll", value="`!strawpoll [(create|stop)]`", inline=True)

        await ctx.send(embed=embed)

    # Category help
    @help.command()
    async def classique(self, ctx):
        embed = discord.Embed(title="Classique", description="Commande classique", colour=discord.Color.red())
        embed.add_field(name="!help", value="`send this message`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def moderation(self, ctx):
        embed = discord.Embed(title="Modération", description="Commande de modération", colour=discord.Color.red())
        embed.add_field(name="!kick", value="`kick the user`", inline=True)
        embed.add_field(name="!ban", value="`ban the user`", inline=True)
        embed.add_field(name="!tempban", value="`ban temporary the user`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def setting(self, ctx):
        embed = discord.Embed(title="Setting", description="Commande de configuration", colour=discord.Color.red())
        embed.add_field(name="!prefix", value="`change the prefix for the server`", inline=True)
        embed.add_field(name="!config", value="`change the config for the server`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def love(self, ctx):
        embed = discord.Embed(title="Love", description="Love commands", colour=discord.Color.red())
        embed.add_field(name="!hug", value="`send a hug`", inline=True)
        embed.add_field(name="!kiss", value="`send a kiss`", inline=True)
        embed.add_field(name="!boop", value="`send a boop`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def strawpoll(self, ctx):
        embed = discord.Embed(title="Strawpoll", description="Strawpoll commands", colour=discord.Color.red())
        embed.add_field(name="create", value="`create a strawpoll`\n`!strawpoll create \"<the text>\" \"<choice 1>\" "
                                             "[\"<choice 2>\" ...]`", inline=True)
        embed.add_field(name="stop", value="`stop a strawpoll`\n`!strawpoll stop <strawpoll_id>`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def other(self, ctx):
        embed = discord.Embed(title="Other", description="Other commands", colour=discord.Color.red())
        embed.add_field(name="!yellowchem", value="`send \"yellow chem is fucking trash !\"`", inline=True)

        await ctx.send(embed=embed)

    # Individual help commands


def setup(bot):
    bot.add_cog(Help(bot))
