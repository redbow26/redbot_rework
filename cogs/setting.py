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

    # TODO: Manage Server settings

    @commands.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def prefix(self, ctx, arg):
        try:
            self.cursor.execute("UPDATE SERVER SET prefix = ? WHERE id_server = ?", (arg, str(ctx.guild.id),))
            logger.info(f"Prefix changed for {ctx.guild.name}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Prefix not change for {ctx.guild.name}\n{e}")
        finally:
            self.conn.commit()

    @commands.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def settings(self, ctx):
        # TODO: Make embed to list all of the setting for the server
        pass

    @commands.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def log(self, ctx, arg=""):
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

    @commands.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def regle(self, ctx, arg=""):
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

    @commands.command()
    @commands.check(is_guild_owner_or_is_owner())
    async def base_role(self, ctx, role: discord.Role):
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


def setup(bot):
    bot.add_cog(Setting(bot))
