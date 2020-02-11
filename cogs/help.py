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

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="!commande [arg] [...]", colour=discord.Color.red())
        embed.add_field(name="Classique", value="`!help`", inline=True)
        embed.add_field(name="Modération", value="`!kick`\n`!ban`\n`!tempban`", inline=True)
        embed.add_field(name="Setting", value="`!prefix`\n`!config`", inline=True)
        embed.add_field(name="Fun", value="`!hug`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def classique(self, ctx):
        embed = discord.Embed(title="Classique", description="Commande classique", colour=discord.Color.red())
        embed.add_field(name="!help", value="`Affiche ce message`", inline=True)

        await ctx.send(embed=embed)

    @help.command()
    async def moderation(self, ctx):
        embed = discord.Embed(title="Modération", description="Commande de modération", colour=discord.Color.red())

        await ctx.send(embed=embed)

    @help.command()
    async def setting(self, ctx):
        embed = discord.Embed(title="Setting", description="Commande de configuration", colour=discord.Color.red())

        await ctx.send(embed=embed)

    @help.command()
    async def fun(self, ctx):
        embed = discord.Embed(title="Fun", description="Commande fun", colour=discord.Color.red())
        embed.add_field(name="!hug", value="`envoie un hug`", inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
