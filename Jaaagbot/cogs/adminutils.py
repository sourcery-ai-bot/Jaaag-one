# Imports
import discord
from discord.ext import commands
from datetime import datetime


# Intializing the extension
class Adminutils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(
          "{} Cog has been loaded\n-----".format(
            self.__class__.__name__
            )
        )

    # A command to set the guild prefix for the bot
    @commands.command(aliases=["pre"],
    brief="Set the prefix",
    help="Set the guild's prefix for the bot.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix):
        await self.bot.config.upsert(
          {"_id": ctx.guild.id, "prefix": prefix}
        )
        await ctx.send(
          "The guild prefix has been set to `{}`. Use `{}setprefix [prefix]` to change it again!".format(
            prefix, prefix
            )
        )
    
    # A command to reset the guild prefix for the bot
    @commands.command(aliases=["reprefix"],
    brief="Reset the prefix",
    help="Reset the guild prefix for the bot to `..`")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def resetprefix(self, ctx):
        await self.bot.config.unset(
          {"_id": ctx.guild.id, "prefix": 1}
        )
        await ctx.send(
          "The prefix for this guild has been reset to `..`"
        )

    
    # Listener for the command below
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.last_msg = message

    # A command to show the author and the content of the last deleted message in a text channel
    @commands.command(
    brief="See the last deleted message",
    help="See the last deleted message in\na text channel and it's author.")
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx):
        if not self.last_msg:
            await ctx.send(
              "There is no message to snipe!"
            )
            return  

        author = self.last_msg.author
        content = self.last_msg.content

        embed = discord.Embed(
          title="Message from {}:".format(
            author
            ),
          description=content,
          color=0x33fcff,
          timestamp=datetime.utcnow()
        )
        await ctx.send(embed=embed)
        		
    
    # A command to set a channel to log moderation events to
    @commands.command(aliases=["mls"],
    brief="Set a modlog channel",
    help="Sets a channel for mod events to be posted to.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def modlogset(self, ctx, channel: discord.TextChannel=None):
      if channel is None:
        channel=ctx.channel
      await self.bot.modlog.upsert(
        {"_id": ctx.guild.id, "modlog": channel.id}
      )
      await ctx.send(
        "Modlog events will now be posted to {}.".format(
          channel.mention
          )
      )

    # A command to set the muterole for the guild. this will be used in the updated mute commmand
    @commands.command(aliases=["mrs", "muteset"],
    brief="Set the muterole",
    help="Sets the role to be assigned when the mute command is used.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def muteroleset(self, ctx, role: discord.Role=None):
      if role is None:
        await ctx.send(
          "You need do mention a role to be set as the muterole."
        )
      else:
        await self.bot.muterole.upsert(
          {"_id": ctx.guild.id, "muterole": role.id}
        )
        await ctx.send(
          "The muterole has been set to {}".format(
            role.mention
            )
        )


# Adds the extention
def setup(bot):
    bot.add_cog(Adminutils(bot))