# Imports
import os
import discord
from discord.ext import commands
from datetime import datetime
import typing
import asyncio
import traceback


# Intializing the extension
class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(
          "{} Cog has been loaded\n-----".format(
            self.__class__.__name__
            )
        )

    # Sends a message to a private channel informing me that it has joined a guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logchannel = await self.bot.fetch_channel(828972017491116032)
        embed = discord.Embed(
          color=0x33fcff, 
          timestamp=datetime.utcnow()
        )
        embed.set_author(
          name="I have joined a server",
          icon_url="{}".format(
            self.bot.user.avatar_url
            )
        )
        embed.set_thumbnail(
          url="{}".format(
            guild.icon_url
            )
        )
        embed.add_field(
          name="**Name:**", 
          value="{}".format(
            guild
            ), 
          inline=False
        )
        embed.add_field(
          name="**Guild ID:**",
          value="{}".format(
            guild.id
            ),
          inline=False
        )
        embed.add_field(
          name="**Guild Owner:**", 
          value="{} ({})".format(
            guild.owner, guild.owner_id
            ), 
          inline=False
        )
        embed.add_field(
          name="**Guild created at:**",
          value="{}".format(
            guild.created_at
            ),
          inline=False
        )
        embed.add_field(
          name="**Member Count:**",
          value="{}".format(
            guild.member_count
            ),
          inline=False
        )
        embed.add_field(
          name="**Tolal server count now:**",
          value="{} guilds".format(
            len(self.bot.guilds)
            ),
          inline=False
        )
        await logchannel.send(embed=embed)

    # Sends a message to a private channel informing me that it has left a guild.
    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        logchannel = await self.bot.fetch_channel(828972017491116032)
        embed = discord.Embed(
          color=0x33fcff, 
          timestamp=datetime.utcnow()
        )
        embed.set_author(
          name="I have left a server",
          icon_url="{}".format(
            self.bot.user.avatar_url
            )
        )
        embed.set_thumbnail(
          url="{}".format(
            guild.icon_url
            )
        )
        embed.add_field(
          name="**Name:**", 
          value="{}".format(
            guild
            ), 
          inline=False
        )
        embed.add_field(
          name="**Guild ID:**",
          value="{}".format(
            guild.id
            ),
          inline=False
        )
        embed.add_field(
          name="**Guild Owner:**",
          value="{} ({})".format(
            guild.owner, guild.owner_id
            ),
          inline=False
        )
        embed.add_field(
          name="**Guild created at:**",
          value="{}".format(
            guild.created_at
            ),
          inline=False
        )
        embed.add_field(
          name="**Member Count:**",
          value="{}".format(
            guild.member_count
            ),
          inline=False
        )
        embed.add_field(
          name="**Tolal server count now:**",
          value="{} guilds".format(
            len(self.bot.guilds)
            ),
          inline=False
        )
        await logchannel.send(embed=embed)

    # A command that makes the bot leave a server. Only works for the bot owner(me).
    @commands.command(aliases=["remove"],
    brief="Leave a guild",
    help="makes the bot leave a server.")
    @commands.is_owner()
    async def leave(self, ctx, id: str):
      if id == 'this':
        await ctx.send(
          "Ok. I am leaving this guild."
          )
        await ctx.guild.leave()
      else:
        guild = self.bot.get_guild(id)
        await guild.leave()
        await ctx.send(
          "Done. I have left {} ({})".format(
            guild.name, guild.id
            )
        )
    
    # Overly complicated cog reload command built watching this video: https://www.youtube.com/watch?v=DFLyOPkHa1w
    @commands.command(aliases=["reload"],
    brief="Reload a Cog",
    help="reloads all or a specific Cog.")
    @commands.is_owner()
    async def update(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Updated all Cogs!",
                    color=0x33fcff,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("Jaaagbot/cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"Jaaagbot.cogs.{ext[:-3]}")
                            self.bot.load_extension(f"Jaaagbot.cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Successfully updated Cog: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to update Cog: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Updated a Cog!",
                    color=0x33fcff,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"Jaaagbot/cogs/{ext}"):
                    embed.add_field(
                        name=f"Failed to update: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"Jaaagbot.cogs.{ext[:-3]}")
                        self.bot.load_extension(f"Jaaagbot.cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Successfully updated Cog: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to update: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    # A command to load my error handler
    @commands.command(aliases=["up-l"],
    brief="Load a listener",
    help="loads a listener from the bot's core.")
    @commands.is_owner()
    async def load_listener(self, ctx, extension):
        self.bot.load_extension(
          f'Jaaagbot.core.{extension}'
          )
        await ctx.send(
          f"`{extension}` Listener has been loaded."
        )

    # A command to unload my error handler
    @commands.command(aliases=["un-l"],
    brief="Unload a Listener",
    help="unloads a listener from the bot's core.")
    @commands.is_owner()
    async def unload_listener(self, ctx, extension):
        self.bot.unload_extension(
          f'Jaaagbot.core.{extension}'
          )
        await ctx.send(
            f"`{extension}` Listener has been unloaded."
        )

    # A command to reload my error handler
    @commands.command(aliases=["re-l"],
    brief="Reload a listener",
    help="reloads a listener from the bot's core.")
    @commands.is_owner()
    async def update_listener(self, ctx, extension):
        self.bot.unload_extension(
          f"Jaaagbot.core.{extension}"
        )
        self.bot.load_extension(
          f'Jaaagbot.core.{extension}'
          )
        await ctx.send(
          f"`{extension}` Listener has been updated."
        )

    # A command to logout the bot
    @commands.command(brief="Shut the bot down",
    help="logs out and stops the bot.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(
          "logging out...  :wave:"
          )
        await ctx.self.bot.close()


# Adds the extention
def setup(bot: commands.Bot):
    bot.add_cog(Dev(bot))