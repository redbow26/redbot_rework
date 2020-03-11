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

# Owned
__author__ = "Tristan Leroy"
__copyright__ = "None"
__credits__ = ["Tristan Leroy"]
__license__ = "None"
__version__ = "0.0.3"
__maintainer__ = "Tristan Leroy"
__email__ = "contact@redbow.fr"
__status__ = "Devs"


def get_prefix(client, message):
    """
    Get a prefix in the database (server.db file) for each server

    if server don't have prefix return "!"
    """
    conn_prefix = sqlite3.connect("server.db")
    cursor_prefix = conn_prefix.cursor()

    if message.guild:
        cursor_prefix.execute("SELECT prefix FROM SERVER WHERE id_server=?", (str(message.guild.id), ))
        prefix_data = cursor_prefix.fetchone()

        if prefix_data:
            prefix = prefix_data[0]

        else:
            cursor_prefix.execute("INSERT INTO SERVER(id_server, name) VALUES (?, ?)", (message.guild.id, message.guild
                                                                                        .name))
            prefix = "!"
    else:
        prefix = "!"

    conn_prefix.commit()
    conn_prefix.close()

    return prefix


def init_db(db_cursor, db_conn):
    """
    Initialise db if table doesn't exist


    :param db_cursor: Database cursor

    :param db_conn: Database connection
    """

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS SERVER (
                        id_server           VARCHAR(100)    PRIMARY KEY,
                        name                VARCHAR(100)    NOT NULL,
                        prefix              VARCHAR(20)     DEFAULT         '!',
                        log_channel_id      VARCHAR(100),
                        rule_id             VARCHAR(100),
                        base_role_id        VARCHAR(100),
                        hug                 BOOL            NOT NULL        DEFAULT TRUE,
                        kiss                BOOL            NOT NULL        DEFAULT TRUE,
                        boop                BOOL            NOT NULL        DEFAULT TRUE,
                        purge               BOOL            NOT NULL        DEFAULT TRUE,
                        kick                BOOL            NOT NULL        DEFAULT TRUE,
                        ban                 BOOL            NOT NULL        DEFAULT TRUE,
                        yellowchem          BOOL            NOT NULL        DEFAULT TRUE,
                        wrongchanel         BOOL            NOT NULL        DEFAULT TRUE
                        )""")

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS STRAWPOLL (
                            id_strawpoll        INTEGER         PRIMARY KEY         AUTOINCREMENT,
                            id_server           VARCHAR(100)    NOT NULL,
                            id_message          VARCHAR(100)    NOT NULL,
                            text                TEXT            NOT NULL,
                            date                DATE            NOT NULL,
                            choices_dict        TEXT            NOT NULL,
                            finish              BOOLEAN         DEFAULT FALSE       NOT NULL
                            )""")

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS TEMPBAN (
                                id_ban              INTEGER         PRIMARY KEY     AUTOINCREMENT,
                                id_user             VARCHAR(100)    NOT NULL,
                                id_server           VARCHAR(100)    NOT NULL,
                                reason              TEXT            NOT NULL,
                                date_ban            DATE            NOT NULL,
                                date_unban          DATE            NOT NULL
                                )""")

    db_conn.commit()


# Load the config (TOKEN) in the conf.json file
with open("conf.json") as json_file:
    conf = json.load(json_file)
    json_file.close()


class Bot(commands.Bot):
    """
    New Bot class
    Extends discord.ext.commands.Bot

    Use to save the database in the variable bot
    """

    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("descriptions"),
            command_prefix=kwargs.pop("command_prefix")
        )

        self.db_conn = kwargs.pop("db_conn")
        self.db_cursor = kwargs.pop("db_cursor")


# Create main logger and handler for discord.py
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_handler = logging.FileHandler(filename="discord.log", mode='w')
discord_handler.setFormatter(logging.Formatter(fmt='%(levelname)-8s | %(asctime)-15s | %(name)-15s | %(message)s'))
discord_logger.addHandler(discord_handler)

# Create logger for the bot it self (redbot)
logger = logging.getLogger("redbot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="redbot.log", mode='w')
handler.setFormatter(logging.Formatter(fmt='%(levelname)-8s | %(asctime)-15s | %(name)-15s | %(message)s'))
logger.addHandler(handler)

conn = sqlite3.connect("server.db")  # SQLITE3 connection to server.db
cursor = conn.cursor()
init_db(cursor, conn)

DESCRIPTION = ""

bot = Bot(command_prefix=get_prefix, descriptions=DESCRIPTION, db_conn=conn, db_cursor=cursor)
bot.remove_command("help")


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """
    Command for load a cogs
    """

    if extension + ".py" in os.listdir("./cogs"):
        try:
            bot.load_extension(f"cogs.{extension}")
            dm = await ctx.message.author.create_dm()
            await dm.send(f"{extension} has been load")
            logger.info(f"{extension} load")
        except Exception as e:
            logger.error(f"bot can not load {extension}\n{e}")
    else:
        ctx.send("The extension can not be load")
        logger.error(f"{extension} can not be load")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """
    Command for unload a cogs
    """

    try:
        bot.unload_extension(f"cogs.{extension}")
        dm = await ctx.message.author.create_dm()
        await dm.send(f"{extension} has been unload")
        logger.info(f"{extension} unload")
    except Exception as e:
        logger.error(f"bot can not unload {extension}\n{e}")


# TODO: Stream alert [ON/OFF]
# TODO: User stats
# TODO: GET_USERS_STATS commands

# Load all the cogs at the launch of the bot
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            logger.error(f"bot can not load {filename[:-3]} | {e}")


loop = asyncio.get_event_loop()  # Create main loop
try:
    loop.run_until_complete(bot.start(conf["TOKEN"]))  # Launch le bot in the main loop
except KeyboardInterrupt:
    # Keyboard interrupt close the database and stop the main loop
    bot.db_conn.close()  # Close the database
    loop.run_until_complete(bot.logout())
