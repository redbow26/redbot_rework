#!env/bin/python3
# coding: utf-8

# Generic/Built-in
import logging
import json

# Other Libs
import discord
from discord.ext import commands

logger = logging.getLogger("redbot")


class Event(commands.Cog):
    """
    Use to list all of the event
    """
    def __init__(self, bot):
        self.bot = bot
        # Load the settings
        with open("../conf.json") as json_file:
            self.setting = json.load(json_file)
            json_file.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
        print('bot connected...')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            with open("../serveur.json", "r") as f:
                server = json.load(f)
    
            server[str(guild.id)]["prefix"] = "!"
            server[str(guild.id)]["strawpoll"] = {}
            server[str(guild.id)]["log_channel_id"] = None
            server[str(guild.id)]["rule_id"] = None
            server[str(guild.id)]["base_role_id"] = None
    
            with open("../serveur.json", "w") as f:
                json.dump(server, f, indent=4)
            logger.info(f"{guild.name} ({guild.id}) has been added to the serveur.json")

        except Exception as e:
            logger.error(f"{guild.name} ({guild.id}) can not be added to the serveur.json\n{e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            guild = payload.guild
            member = payload.member
            message_id = payload.message_id
            if message_id == self.setting[str(guild.id)]["rule_id"] and self.setting[str(guild.id)]["base_role_id"] \
                    is not None:
                roles = await payload.guild.fetch_roles()
                for r in roles:
                    if r.id == self.setting[str(guild.id)]["base_role_id"]:
                        role = r
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
        try:
            with open("../serveur.json", "r") as f:
                server = json.load(f)

            server.pop(str(guild.id))

            with open("../serveur.json", "w") as f:
                json.dump(server, f, indent=4)
            logger.info(f"{guild.name} ({guild.id}) has been removed from the server.json")

        except Exception as e:
            logger.error(f"{guild.name} ({guild.id}) can not be removed to the serveur.json\n{e}")


def setup(bot):
    bot.add_cog(Event(bot))
