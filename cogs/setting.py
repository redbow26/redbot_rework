#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


class Setting(commands.Cog):
    """
    Setting commands
    """
    def __init__(self, bot):
        self.bot = bot
        # Load the setting
        with open("../conf.json") as json_file:
            self.setting = json.load(json_file)
            json_file.close()

    # TODO: Manage Server settings

    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def prefix(self, ctx, arg):
        try:
            with open("../serveur.json", "r") as f:
                server = json.load(f)

            server[str(ctx.guild.id)]["prefix"] = arg

            with open("../serveur.json", "w") as f:
                json.dump(server, f, indent=4)
                
            logger.info(f"Prefix changed for {ctx.guild.name}")
        except Exception as e:
            logger.error(f"Prefix not change for {ctx.guild.name}\n{e}")

    @commands.group()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def settings(self, ctx):
        # TODO: Make embed to list all of the setting for the server
        pass

    @settings.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def log(self, ctx, arg=""):
        try:
            if arg.lower() in ["none", "no", ""]:
                self.setting[str(ctx.guild.id)]["log_channel"] = None

                with open("../serveur.json", "w") as f:
                    json.dump(self.setting, f, indent=4)
                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set None to log channel")

            else:
                if isinstance(arg, int):
                    self.setting[str(ctx.guild.id)]["log_channel"] = int(arg)

                    with open("../serveur.json", "w") as f:
                        json.dump(self.setting, f, indent=4)
                    logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set {arg} to log channel")
                else:
                    ctx.send(f"{arg} is not a identifier of a channel, it must me a integer")

        except Exception as e:
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not change the log setting to {arg}\n{e}")


def setup(bot):
    bot.add_cog(Setting(bot))
