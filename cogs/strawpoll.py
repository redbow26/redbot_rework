#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Strawpoll(commands.Cog):
    """
    Strawpoll category commands
    """
    def __init__(self, bot):
        self.bot = bot
        # Load the setting
        with open("../conf.json") as json_file:
            self.setting = json.load(json_file)
            json_file.close()


def setup(bot):
    bot.add_cog(Strawpoll(bot))
