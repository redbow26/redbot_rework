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


class Moderation(commands.Cog):
    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    # TODO: UNBAN commands
    # TODO: TEMPBAN commands
    # TODO: TEMPUNBAN tasks

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, arg=0):
        """
        purge command
        purge a chanel with a specified amount of messages

        use:
            !purge <number of message>
        """

        try:
            self.cursor.execute("SELECT purge FROM SERVER WHERE id_server=?", (str(ctx.guild.id),))
            data = self.cursor.fetchone()

            if data:
                if data[0]:
                    arg = int(arg) + 1
                    await ctx.channel.purge(limit=arg)
                    logger.info(
                        f"{ctx.channel.name} ({ctx.channel.id}) in {ctx.guild.name} ({ctx.guild.id}) {arg} message "
                        f"has been purge by {ctx.message.author.name} ({ctx.message.author.mention})")
        except Exception as e:
            logger.error(f"{ctx.channel.name} ({ctx.channel.id}) in {ctx.guild.name} ({ctx.guild.id}) can not be "
                         f"purge by {ctx.message.author.name} ({ctx.message.author.mention}) of {arg} message\n{e}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=""):
        """
        Kick command
        kick a user, send him a message and log the kick on the log channel

        use:
            !kick <member> <reason>
        """

        author = ctx.message.author
        guild = ctx.guild
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if member:
            if reason != "":
                try:
                    self.cursor.execute("SELECT kick, log_channel_id FROM SERVER WHERE id_server=?",
                                        (str(ctx.guild.id),))
                    data = self.cursor.fetchone()

                    if data:
                        if data[0]:
                            dm = await member.create_dm()
                            embed_dm = discord.Embed(title="Kick",
                                                     description="---------------------------------------------"
                                                                 "---------", color=discord.Color.red())
                            embed_dm.add_field(name="Kicked by: ", value=f"{author.mention}", inline=False)
                            embed_dm.add_field(name="Server: ", value=f"{guild.name}", inline=False)
                            embed_dm.add_field(name="Reason: ",
                                               value=f"{reason}\n---------------------------------------------------"
                                                     f"---",inline=False)
                            embed_dm.set_footer(text=f"Requested by {author}  {date}", icon_url=author.avatar_url)

                            await dm.send(embed=embed_dm)

                            await guild.kick(user=member, reason=reason)

                            if self.setting[str(guild.id)]["log_channel"] is not None:
                                channel = await self.bot.fetch_channel(int(data[1]))
                                embed = discord.Embed(title="Member kick",
                                                      description="---------------------------------------------"
                                                                  "---------", color=0x00ff00)
                                embed.add_field(name="Kicked by: ", value=f"{author.mention}", inline=False)
                                embed.add_field(name="Kicked: ", value=f"<@{member.id}>", inline=False)
                                embed.add_field(name="Reason: ",
                                                value=f"{reason}\n-------------------------------------------------"
                                                      f"-----", inline=False)
                                embed.set_footer(text=f"Requested by {author}  {date}", icon_url=author.avatar_url)

                                await channel.send(embed=embed)

                            logger.info(f'{member.name} ({member.mention}) in {guild.name} ({guild.id})'
                                        f' kicked by {author.name} ({author.mention}) for "{reason}"')
                except Exception as e:
                    logger.error(f'{member.name} ({member.mention}) in {guild.name} ({guild.id}) can not be '
                                 f' kick by {author.name} ({author.mention}) for "{reason}"\n{e}')
            else:
                await ctx.send("You need to precise a reason")
        else:
            await ctx.send("To kick someone you need to tag this person")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=""):
        """
        Ban command
        ban a user, send him a message and log the ban on the log chanel

        use:
            !ban <member> <reason>
        """

        author = ctx.message.author
        guild = ctx.guild
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if member:
            if reason != "":
                try:
                    self.cursor.execute("SELECT ban, log_channel_id FROM SERVER WHERE id_server=?",
                                        (str(ctx.guild.id),))
                    data = self.cursor.fetchone()

                    if data:
                        if data[0]:
                            dm = await member.create_dm()
                            embed_dm = discord.Embed(title="Ban", description="---------------"
                                                                              "---------------------------------------",
                                                     color=discord.Color.red())
                            embed_dm.add_field(name="Banned by: ", value=f"{author.mention}", inline=False)
                            embed_dm.add_field(name="Server: ", value=f"{guild.name}", inline=False)
                            embed_dm.add_field(name="Reason: ",
                                               inline=False,
                                               value=f"{reason}\n-----------------------------------------------------"
                                                     f"-")
                            embed_dm.set_footer(text=f"Requested by {author}  {date}", icon_url=author.avatar_url)

                            await dm.send(embed=embed_dm)

                            if self.setting[str(guild.id)]["log_channel"] is not None:
                                channel = await self.bot.fetch_channel(int(data[1]))

                                await guild.ban(user=member, reason=reason)
                                embed = discord.Embed(title="Member ban", description="-----------------------"
                                                                                      "-------------------------------",
                                                      color=0x00ff00)
                                embed.add_field(name="Ban by: ", value=f"{author.mention}", inline=False)
                                embed.add_field(name="Ban: ", value=f"<@{member.id}>", inline=False)
                                embed.add_field(name="Reason: ",
                                                value=f"{reason}\n----------------------------------------------"
                                                      f"--------", inline=False)
                                embed.set_footer(text=f"Requested by {author}  {date}", icon_url=author.avatar_url)

                                await channel.send(embed=embed)

                            logger.info(f'{member.name} ({member.mention}) in {guild.name} ({guild.id})'
                                        f' banned by {author.name} ({author.mention}) for "{reason}"')
                except Exception as e:
                    logger.error(f'{member.name} ({member.mention}) in {guild.name} ({guild.id}) can not be '
                                 f' ban by {author.name} ({author.mention}) for "{reason}"\n{e}')
            else:
                await ctx.send("You need to precise a reason")
        else:
            await ctx.send("To ban someone you need to tag this person")


def setup(bot):
    bot.add_cog(Moderation(bot))
