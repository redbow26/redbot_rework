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


def is_guild_owner_or_is_owner():
    def predicate(ctx):
        return (ctx.guild is not None and ctx.guild.owner_id == ctx.author.id) or (ctx.author.id == 175990133240233984)

    return commands.check(predicate)


class Setting(commands.Cog):
    """
    Setting commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    @commands.group(invoke_without_command=True)
    @commands.check(is_guild_owner_or_is_owner())
    async def settings(self, ctx):
        """
        Settings group
        Print a list of all the settings

        use:
            !setting
        """
        # TODO: Make embed to list all of the setting for the server
        pass

    @settings.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def prefix(self, ctx, arg):
        """
        Prefix settings
        Show the prefix or change it

        use:
            !setting <prefix>
        """

        try:
            self.cursor.execute("UPDATE SERVER SET prefix = ? WHERE id_server = ?", (arg, str(ctx.guild.id),))
            logger.info(f"Prefix changed for {ctx.guild.name}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Prefix not change for {ctx.guild.name}\n{e}")
        finally:
            self.conn.commit()

    @settings.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def log(self, ctx, arg=""):
        """
        Log settings
        setup the log id
        to remove the log don't put arg

        use:
            !setting [<log channel id>]
        """

        try:
            if arg.lower() in ["none", "no", ""]:
                self.cursor.execute("UPDATE SERVER SET log_channel_id = ? WHERE id_server = ?",
                                    (None, str(ctx.guild.id),))

                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set None for the log channel id")
            else:
                try:
                    int(arg)
                    self.cursor.execute("UPDATE SERVER SET log_channel_id = ? WHERE id_server = ?",
                                        (str(arg), str(ctx.guild.id),))

                    logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set {arg} for the log channel id")
                except ValueError as e:
                    await ctx.send(f"{arg} is not a identifier of a channel, it must me a integer")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not change the log setting to {arg}\n{e}")

        finally:
            self.conn.commit()

    @settings.command(aliases=["regle"])
    @commands.check(is_guild_owner_or_is_owner())
    async def rule(self, ctx, arg=""):
        """
        Rule settings
        setup the rule message id
        to remove the rule don't put arg

        use:
            !setting [<regle>]
        """

        try:
            if arg.lower() in ["none", "no", ""]:
                self.cursor.execute("UPDATE SERVER SET rule_id = ? WHERE id_server = ?",
                                    (None, str(ctx.guild.id),))

                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set None for the rule id")
            else:
                try:
                    int(arg)
                    self.cursor.execute("UPDATE SERVER SET rule_id = ? WHERE id_server = ?",
                                        (str(arg), str(ctx.guild.id),))

                    logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set {arg} for the rule id")
                except ValueError as e:
                    await ctx.send(f"{arg} is not a identifier of a message, it must me a integer")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not change the rule id setting to {arg}\n{e}")

        finally:
            self.conn.commit()

    @settings.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def base_role(self, ctx, role: discord.Role):
        """
        Base role settings
        setup the base role id
        to remove the base role tag @everyone

        use:
            !setting [<base_role>]
        """

        try:
            role_id = role.id
            if role.is_default():
                self.cursor.execute("UPDATE SERVER SET rule_id = ? WHERE id_server = ?",
                                    (None, str(ctx.guild.id),))

                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set None for the base role id")

            else:
                self.cursor.execute("UPDATE SERVER SET rule_id = ? WHERE id_server = ?",
                                    (role_id, str(ctx.guild.id),))

                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) has set {role_id} for the base role id")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not change the rule id setting to {role_id}\n{e}")

        finally:
            self.conn.commit()

    @commands.command(aliases=["activer"])
    @commands.check(is_guild_owner_or_is_owner())
    async def activate(self, ctx, command: str):
        """
        activate command
        activate one command for the server

        use:
            !activate <command>
        """

        command = command.lower().split()
        command_list = ["hug", "kiss", "boop", "purge", "kick", "ban", "yellowchem", "wrongchanel"]

        try:
            if command in command_list:
                self.cursor.execute("UPDATE SERVER SET ? = TRUE WHERE id_server = ?",
                                    (command, str(ctx.guild.id),))

                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) activate {command} in the database")
            else:
                await ctx.send("La commande n'existe pas.")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not activate {command} in the database\n{e}")

        finally:
            self.conn.commit()

    @commands.command(aliases=["desactiver"])
    @commands.check(is_guild_owner_or_is_owner())
    async def deactivate(self, ctx, command: str):
        """
        Deactivate command
        Deactivate one command for the server

        use:
            !deactivate <command>
        """

        command = command.lower().split()
        command_list = ["hug", "kiss", "boop", "purge", "kick", "ban", "yellowchem", "wrongchanel"]

        try:
            if command in command_list:
                self.cursor.execute("UPDATE SERVER SET ? = FALSE WHERE id_server = ?",
                                    (command, str(ctx.guild.id),))

                logger.info(f"{ctx.guild.name} ({ctx.guild.id}) deactivate {command} in the database")
            else:
                await ctx.send("La commande n'existe pas.")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not deactivate {command} in the database\n{e}")

        finally:
            self.conn.commit()


def setup(bot):
    bot.add_cog(Setting(bot))
