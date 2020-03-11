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


class Strawpoll(commands.Cog):
    """
    Strawpoll category commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.conn = bot.db_conn
        self.cursor = bot.db_cursor

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def strawpoll(self, ctx):
        """
        Strawpoll group
        send the id and the name of each strawpoll for the server

        use:
            !strawpoll
        """

        message = "id: message\n"
        try:
            self.cursor.execute("SELECT id_strawpoll, text FROM STRAWPOLL WHERE id_server=?",
                                (str(ctx.guild.id),))
            data = self.cursor.fetchall()

            for i in range(0, len(data)):
                message += f"{data[i][0]}: {data[i][1]}\n"
                if i % 10 == 0:
                    await ctx.send(message)
                    message = "id: message\n"

        except Exception as e:
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not get all of the strawpoll\n{e}")

    @strawpoll.command()
    @commands.has_permissions(manage_messages=True)
    async def create(self, ctx, text: str, *choices: str):
        """
        Create strawpoll
        create a strawpoll for the server with a text and every choice (ten choices max)
        and send it with the embed format

        use:
            !strawpoll create "<the text>" "<choice 1>" ["<choice 2>" ...]
        """

        emote = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        choices_dict = {}

        try:
            embed = discord.Embed(title="Strawpoll", description=text, colour=discord.Color.red())
            for i in range(0, len(choices)):
                embed.add_field(name=f"{emote[i]}   :", value=f"{choices[i]}", inline=False)
                choices_dict[emote[i]] = choices[i]

            self.cursor.execute('SELECT max(id_strawpoll) FROM STRAWPOLL')
            data = self.cursor.fetchone()
            if data[0] is None:
                max_id = 0
            else:
                max_id = int(data[0])

            embed.set_footer(text=f"id: {max_id + 1}, created by: {ctx.author.name}")
            await ctx.channel.purge(limit=1)

            message = await ctx.send(embed=embed)

            for i in range(0, len(choices)):
                await message.add_reaction(emote[i])

            self.cursor.execute(
                """INSERT INTO STRAWPOLL(id_server, id_message, text, date, choices_dict) VALUES (?, ?, ?, ?, ?)""",
                (str(ctx.guild.id), str(message.id), text, str(datetime.datetime.now()), json.dumps(choices_dict),))

            logger.info(f"{ctx.guild.name} ({ctx.guild.id}) strawpoll created")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not create the strawpoll\n{e}")

        finally:
            self.conn.commit()

    @strawpoll.command()
    @commands.has_permissions(manage_messages=True)
    async def stop(self, ctx, id_strawpoll):
        """
        Stop strawpoll
        Stop and send the result of the strawpoll in dm with the id pass in the command

        use:
            !strawpoll stop <strawpoll_id>
        """

        result = {"1️⃣": 0, "2️⃣": 0, "3️⃣": 0, "4️⃣": 0, "5️⃣": 0, "6️⃣": 0, "7️⃣": 0, "8️⃣": 0, "9️⃣": 0, "🔟": 0}
        result_user = {"1️⃣": [], "2️⃣": [], "3️⃣": [], "4️⃣": [], "5️⃣": [], "6️⃣": [],
                       "7️⃣": [], "8️⃣": [], "9️⃣": [], "🔟": []}

        try:
            id_strawpoll = int(id_strawpoll)

        except ValueError as e:
            await ctx.send(f"{id_strawpoll} is not a identifier of a message, it must me a integer")

        try:
            self.cursor.execute("SELECT id_message, choices_dict FROM STRAWPOLL WHERE id_strawpoll=?",
                                (str(id_strawpoll),))
            data = self.cursor.fetchone()

            if data:
                id_message = data[0]
                choice_dict = json.loads(data[1])

                message = await ctx.channel.fetch_message(id_message)

                reactions = message.reactions

                for reaction in reactions:
                    if reaction.emoji in result:
                        async for user in reaction.users():
                            if not user.bot:
                                result[reaction.emoji] += 1
                                result_user[reaction.emoji].append(user.name)

                dm = await ctx.message.author.create_dm()
                message = ""

                for u, v in choice_dict.items():
                    message += f"{v}: {result[u]}, {result_user[u]} \n"

                await dm.send(message)

            else:
                await ctx.send("cette identifiant ne designe pas de strawpoll")

        except Exception as e:
            logger.error(f"{ctx.guild.name} ({ctx.guild.id}) can not get the strawpoll"
                         f":{id_strawpoll}\n{e}")


def setup(bot):
    bot.add_cog(Strawpoll(bot))
