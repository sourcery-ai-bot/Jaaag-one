# Imports
import discord
from discord.ext import commands
import random
import platform
import logging
import re
import unicodedata
import aiohttp
from datetime import datetime
import asyncio

# Intializing the extension
class Adminutils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # A command to set the guild prefix for the bot
    @commands.command(aliases=["pre"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix):
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(
            f"The guild prefix has been set to `{prefix}`. Use `{prefix}setprefix [prefix]` to change it again!")
    
    # A command to reset the guild prefix for the bot
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def resetprefix(self, ctx):
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send(
          "The prefix for this guild has been reset to `..`"
        )

    
    # Listener for the command below
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.last_msg = message

    # A command to show the author and the content of the last deleted message in a text channel
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx):
        """A command to snipe delete messages."""
        if not self.last_msg:
            await ctx.send("There is no message to snipe!")
            return  

        author = self.last_msg.author
        content = self.last_msg.content

        embed = discord.Embed(title=f"Message from {author}:",
                              description=content,
                              color=0x33fcff,
                              timestamp=datetime.utcnow())
        await ctx.send(embed=embed)
        		
    
    # A command to set a channel to log moderation events to
    @commands.command(aliases=["mls"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def modlogset(self, ctx, channel: discord.TextChannel=None):
      if channel is None:
        channel=ctx.channel
      await self.bot.modlog.upsert({"_id": ctx.guild.id, "modlog": channel.id})
      await ctx.send(f"Modlog events will now be posted to {channel.mention}.")

    # A command to set the muterole for the guild. this will be used in the updated mute commmand
    @commands.command(aliases=["mrs", "muteset"])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def muteroleset(self, ctx, role: discord.Role=None):
      if role is None:
        await ctx.send("You need do mention a role to be set as the muterole.")
      else:
        await self.bot.muterole.upsert({"_id": ctx.guild.id, "muterole": role.id})
        await ctx.send(f"The muterole has been set to {role.mention}")


# Adds the extention
def setup(bot):
    bot.add_cog(Adminutils(bot))