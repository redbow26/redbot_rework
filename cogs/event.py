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


class Event(commands.Cog):
    """
    Use to list all of the event
    """
    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    @commands.Cog.listener()
    async def on_ready(self):
        """
        When the bot is ready
        """

        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
        print('bot connected...')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        listener on every guild join

        - add the guild on the database
        """

        try:
            self.cursor.execute("INSERT INTO SERVER(id_server, name) VALUES (?, ?)", (guild.id, guild.name))

            logger.info(f"{guild.name} ({guild.id}) has been added to the database")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{guild.name} ({guild.id}) can not be added to the database\n{e}")

        finally:
            self.conn.commit()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        listener on every reaction add

        - check for the rule message to put base role
        """

        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        message_id = payload.message_id

        try:
            if guild:
                self.cursor.execute("SELECT rule_id, base_role_id FROM SERVER WHERE id_server=?", (str(guild.id), ))
                data = self.cursor.fetchone()

                if data:
                    if message_id == int(data[0]) and data[1] is not None:
                        role = guild.get_role(int(data[1]))
                        await member.add_roles(role, reason="Accept the rule")
                        logger.info(f'{member} ({member.mention}) in {guild.name} ({guild.id}) has get the base role')

        except Exception as e:
            logger.error(f'{member} ({member.mention}) in {guild.name} ({guild.id}) can not get the base role\n{e}')

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        pass

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        listener on every guild join

        - add the guild on the database
        """

        try:
            self.cursor.execute("DELETE FROM SERVER WHERE id_server=?", (str(guild.id), ))
            logger.error(f"{guild.name} ({guild.id}) has been added to the database")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{guild.name} ({guild.id}) can not be removed to the database\n{e}")

        finally:
            self.conn.commit()


def setup(bot):
    bot.add_cog(Event(bot))
