#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, arg=0):
        try:
            arg = int(arg) + 1
            await ctx.channel.purge(limit=arg)
            logger.info(f"{ctx.channel.name} ({ctx.channel.id}) in {ctx.guild.name} ({ctx.guild.id}) {arg} message "
                        f"has been purge by {ctx.message.author.name} ({ctx.message.author.mention})")
        except Exception as e:
            logger.error(f"{ctx.channel.name} ({ctx.channel.id}) in {ctx.guild.name} ({ctx.guild.id}) can not be "
                         f"purge by {ctx.message.author.name} ({ctx.message.author.mention}) of {arg} message | {e}")


def setup(bot):
    bot.add_cog(Moderation(bot))
