# Imports
import discord
from discord.ext import commands
import random
from typing import Union
import platform
import logging
import re
import unicodedata
import aiohttp
from datetime import datetime
import asyncio

# Intializing the extension
class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(aliases=["lockchan"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def lockit(self, ctx: commands.Context, channel: Union[discord.TextChannel, discord.VoiceChannel] = None,):
        author = ctx.author
        role = ctx.guild.default_role
        if channel is None:
            channel = ctx.channel

        overwrite = channel.overwrites_for(role)
        bot_overwrite = channel.overwrites_for(ctx.bot.user)

        if channel.type == discord.ChannelType.text:
            if overwrite.send_messages is False:
                return await ctx.send(
                    "{} is already locked. To unlock it, please use `{}ulockit {}`".format(
                        channel.mention, ctx.prefix, channel.id
                    )
                )
            if not bot_overwrite.send_messages:
                bot_overwrite.update(send_messages=True)
            overwrite.update(send_messages=False)
        elif channel.type == discord.ChannelType.voice:
            if overwrite.connect is False:
                return await ctx.send(
                    "{} is already locked. To unlock it, please use `{}ulockit {}`".format(
                        channel.mention, ctx.prefix, channel.id
                    )
                )
            overwrite.update(connect=False)
        try:
            await channel.set_permissions(
                ctx.bot.user,
                overwrite=bot_overwrite,
                reason=f"Securing overrides for {ctx.bot.user.name}",
            )
            await channel.set_permissions(
                role,
                overwrite=overwrite,
                reason="Lockdown in effect. Action requested by {} ({})".format(
                  author.name, author.id
                ),
            )
        except discord.Forbidden:
            return await ctx.send("Error: Bot doesn't have perms to adjust that channel.")
        await ctx.send(
          "Done. Locked {}".format(
            channel.mention
            )
        )

    @commands.command(aliases=["ulockchan"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def unlockit(self, ctx: commands.Context, channel: Union[discord.TextChannel, discord.VoiceChannel] = None,):
        author = ctx.author
        role = ctx.guild.default_role
        if channel is None:
            channel = ctx.channel

        overwrite = channel.overwrites_for(role)

        if channel.type == discord.ChannelType.text:
            if overwrite.send_messages is None:
                return await ctx.send(
                    "{} is already unlocked. To lock it, please use `{}lockit {}`".format(
                        channel.mention, ctx.prefix, channel.id
                    )
                )
            overwrite.update(send_messages=None)
        elif channel.type == discord.ChannelType.voice:
            if overwrite.connect is None:
                return await ctx.send(
                    "{} is already unlocked. To lock it, please use `{}lockit {}`".format(
                        channel.mention, ctx.prefix, channel.id
                    )
                )
            overwrite.update(connect=None)

        try:
            await channel.set_permissions(
                role,
                overwrite=overwrite,
                reason="Lockdown over. Action requested by {} ({})".format(
                  author.name, author.id
                ),
            )
        except discord.Forbidden:
            return await ctx.send("Error: Bot doesn't have perms to adjust that channel.")
        await ctx.send(
          "Unlocked {}".format(
            channel.mention
            )
        )  
    
		
# Adds the extention
def setup(bot):
    bot.add_cog(Channels(bot))
