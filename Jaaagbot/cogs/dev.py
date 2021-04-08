# Imports
import discord
from discord.ext import commands
from datetime import datetime


# Intializing the extension
class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.blacklisted_guilds = [800076084161806346]

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # Sends a message to a private channel informing me that it has joined a guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logchannel = await self.bot.fetch_channel(828972017491116032)
        embed = discord.Embed(color=0x33fcff, timestamp=datetime.utcnow())
        embed.set_author(name="I have joined a server",
                         icon_url=f"{self.bot.user.avatar_url}")
        embed.set_thumbnail(url=f"{guild.icon_url}")
        embed.add_field(name="**Name:**", value=f"{guild}", inline=False)
        embed.add_field(name="**Guild ID:**",
                        value=f"{guild.id}",
                        inline=False)
        embed.add_field(name="**Guild Owner:**",
                        value=f"{guild.owner} ({guild.owner_id})")
        embed.add_field(name="**Guild created at:**",
                        value=f"{guild.created_at}",
                        inline=False)
        embed.add_field(name="**Member Count:**",
                        value=f"{guild.member_count}",
                        inline=False)
        embed.add_field(name="**Tolal server count now:**",
                        value=f"{len(self.bot.guilds)} guilds",
                        inline=False)
        await logchannel.send(embed=embed)

    # Sends a message to a private channel informing me that it has left a guild.
    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        logchannel = await self.bot.fetch_channel(828972017491116032)
        embed = discord.Embed(color=0x33fcff, timestamp=datetime.utcnow())
        embed.set_author(name="I have left a server",
                         icon_url=f"{self.bot.user.avatar_url}")
        embed.set_thumbnail(url=f"{guild.icon_url}")
        embed.add_field(name="**Name:**", value=f"{guild}", inline=False)
        embed.add_field(name="**Guild ID:**",
                        value=f"{guild.id}",
                        inline=False)
        embed.add_field(name="**Guild Owner:**",
                        value=f"{guild.owner} ({guild.owner_id})")
        embed.add_field(name="**Guild created at:**",
                        value=f"{guild.created_at}",
                        inline=False)
        embed.add_field(name="**Member Count:**",
                        value=f"{guild.member_count}",
                        inline=False)
        embed.add_field(name="**Tolal server count now:**",
                        value=f"{len(self.bot.guilds)} guilds",
                        inline=False)
        await logchannel.send(embed=embed)

    # A command that makes the bot leave a server. Only works for the bot owner(me).
    @commands.command(aliases=["leave"])
    @commands.is_owner()
    async def leaveguild(self, ctx, id: str):
        if id == 'this':
            await ctx.send("Ok. I am leaving this guild.")
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(id)
            if guild:
                await guild.leave()
                msg = f"Ok. I am leaving {guild.name}"
            else:
                msg = "I couldn't find a guild matching this ID!"
        await ctx.send(msg)


# Adds the extention
def setup(bot: commands.Bot):
    bot.add_cog(Dev(bot))
