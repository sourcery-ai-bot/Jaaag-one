# Imports
import asyncio
import discord
from discord import NotFound, Object
from discord.utils import find
from discord.ext import commands
from discord.ext.commands import Converter, Greedy
from discord.ext.commands import BadArgument
from typing import Optional
from datetime import datetime
import logging
from typing import Union
import re
import unicodedata

log = logging.getLogger("Adminutils")


class BannedUser(Converter):
	async def convert(self, ctx, arg):
		if ctx.guild.me.guild_permissions.ban_members:
			if arg.isdigit():
				try:
					return (await ctx.guild.fetch_ban(Object(id=int(arg)))).user
				except NotFound:
					raise BadArgument

		banned = [e.user for e in await ctx.guild.bans()]
		if banned:
			if (user := find(lambda u: str(u) == arg, banned)) is not None:
				return user
			else:
				raise BadArgument


# Intializing the extension
class Mod(commands.Cog):
    """A cog containing some moderation commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

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

    # A command to kick a user from a server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
            await ctx.send(
              f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
            )
        else:
            modlogchannel = data["modlog"]
            modlog = await self.bot.fetch_channel(modlogchannel)
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(f'Done. **{user.name}** was kicked.', delete_after=3)
            embed = discord.Embed(
              title="Kick | :boot:",
              color=0xa84300,
              timestamp=datetime.utcnow()
            )
            embed.add_field(
              name="Offender:",
              value=f"{user.name}#{user.discriminator} {user.mention}",
              inline=False
            )
            embed.add_field(
              name="Reason:",
              value=f"{reason}",
              inline=False
            )
            embed.add_field(
              name="Moderator:",
              value=f"{ctx.author} ({ctx.author.id})",
              inline=False
            )
            await modlog.send(embed=embed)
    
    # A command to ban a user from a server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
            await ctx.send(
              f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
            )
        else:
          modlogchannel = data["modlog"]
          modlog = await self.bot.fetch_channel(modlogchannel)
          await ctx.guild.ban(user, reason=reason)
          await ctx.send(f'Done. **{user.name}** was banned.', delete_after=3)
          embed = discord.Embed(
            title="Ban | :hammer:",
            color=0xe74c3c,
            timestamp=datetime.utcnow()
          )
          embed.add_field(
            name="Offender:",
            value=f"{user.name}#{user.discriminator} {user.mention}",
            inline=False
          )
          embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
          )
          embed.add_field(
            name="Moderator:",
            value=f"{ctx.author} ({ctx.author.id})",
            inline=False
          )
          await modlog.send(embed=embed)

    # A command to ban a user that isn't in the server, can only be used by server moderators and only accepts user id's
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def forceban(self, ctx, user_id: int, *, reason=None):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
            await ctx.send(
              f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
            )
        else:
          modlogchannel = data["modlog"]
          modlog = await self.bot.fetch_channel(modlogchannel)
          await ctx.guild.ban(discord.Object(id=user_id), reason=reason)
          await ctx.send(f'Done. **{self.bot.get_user(user_id)}** was forcebanned.', delete_after=3)
          embed = discord.Embed(
            title="Forceban | :bust_in_silhouette: :hammer:",
            color=0x992d22,
            timestamp=datetime.utcnow()
          )
          embed.add_field(
            name="Offender:",
            value=f"{self.bot.get_user(user_id)} ({user_id})",
            inline=False
          )
          embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
          )
          embed.add_field(
            name="Moderator:",
            value=f"{ctx.author} ({ctx.author.id})",
            inline=False
          )
          await modlog.send(embed=embed)

    # A command to unban a user from a server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, targets: Greedy[BannedUser], *, reason: Optional[str] = "No reason provided."):
      data = await self.bot.modlog.get_by_id(ctx.guild.id)
      if not data or "modlog" not in data:
        await ctx.send(
          f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
          )
      else:
        modlogchannel = data["modlog"]
        modlog = await self.bot.fetch_channel(modlogchannel)
        if not len(targets):
          await ctx.send("One or more required arguments are missing.")

        else:
          for target in targets:
            await ctx.guild.unban(target, reason=reason)

          await ctx.send(f"**{target}** has been unbanned sucessfully", delete_after=3)
          embed = discord.Embed(
            title="Unban | :dove:",
            color=0x33fcff,
            timestamp=datetime.utcnow()
          )
          embed.add_field(
            name="Offender:",
            value=f"{target}",
            inline=False
          )
          embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
          )
          embed.add_field(
            name="Moderator:",
            value=f"{ctx.author} ({ctx.author.id})",
            inline=False
          )
          await modlog.send(embed=embed)

    # A command to mute a user in the server, can only be used by server moderators, the user will be automatically unmuted after the specified mute duration ends
    @commands.command(aliases=["tempmute"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, time: int, d, *, reason=None):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
          await ctx.send(
            f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
          )
        else:
            modlogchannel = data["modlog"]
            modlog = await self.bot.fetch_channel(modlogchannel)
            guild = ctx.guild

            for role in guild.roles:
                if role.name == "Muted":
                    await member.add_roles(role)
                    await ctx.send(f"Muted {member.name} for {time}{d}.", delete_after=3)
                    embed = discord.Embed(
                      title="Server Mute | :mute:",
                      color=0xe67e22,
                      timestamp=datetime.utcnow()
                    )
                    embed.add_field(
                      name="Offender:",
                      value=f"{member.name}#{member.discriminator} {member.mention}",
                      inline=False
                    )
                    embed.add_field(
                      name="Reason:",
                      value=f"{reason}",
                      inline=False
                    )
                    embed.add_field(
                      name="Moderator:",
                      value=f"{ctx.author} ({ctx.author.id})",
                      inline=False
                    )
                    await modlog.send(embed=embed)

                    if d == "s":
                        await asyncio.sleep(time)

                    if d == "m":
                        await asyncio.sleep(time * 60)

                    if d == "h":
                        await asyncio.sleep(time * 60 * 60)

                    if d == "d":
                        await asyncio.sleep(time * 60 * 60 * 24)

                    await member.remove_roles(role)
                    emb = discord.Embed(
                      title="Server Unmute | :speaker:",
                      color=0x2ecc71,
                      timestamp=datetime.utcnow()
                    )
                    emb.add_field(
                      name="Offender:",
                      value=f"{member.name}#{member.discriminator} {member.mention}",
                      inline=False
                    )
                    emb.add_field(
                      name="Reason:",
                      value=f"Automatic unmute from mute made {time}{d} ago\nby {ctx.author} ({ctx.author.id})",
                      inline=False
                    )
                    await modlog.send(embed=emb)
                    return

    # A command to unmute a user in the server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
          await ctx.send(
            f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
          )
        else:
            modlogchannel = data["modlog"]
            modlog = await self.bot.fetch_channel(modlogchannel)
            guild = ctx.guild

            for role in guild.roles:
                if role.name == "Muted":

                    await member.remove_roles(role)
                    await ctx.send(f"Done. Unmuted {member.name}.", delete_after=3)
                    embed = discord.Embed(
                      title="Server Unmute | :speaker:",
                      color=0x2ecc71,
                      timestamp=datetime.utcnow()
                    )
                    embed.add_field(
                      name="Offender:",
                      value=f"{member.name}#{member.discriminator} {member.mention}",
                      inline=False
                    )
                    embed.add_field(
                      name="Reason:",
                      value=f"{reason}",
                      inline=False
                    )
                    embed.add_field(
                      name="Moderator:",
                      value=f"{ctx.author} ({ctx.author.id})",
                      inline=False
                    )
                    await modlog.send(embed=embed)

    
    # A command to delete messages in a text channel, can only be used by server administrators
    @commands.command(aliases=["cleanup"])
    @commands.guild_only()
    @commands.cooldown(1, 8, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
          await ctx.send(
            f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
          )
        else:
            modlogchannel = data["modlog"]
            modlog = await self.bot.fetch_channel(modlogchannel)
            if messages > 99:
                messages = 99
            await ctx.channel.purge(limit=messages + 1)
            await ctx.send(f'Done. {messages} messages were purged.',
                          delete_after=3)
            embed = discord.Embed(
              title="Purge | :speech_balloon:",
              description=f"{messages} messages have been purged in {ctx.channel.mention}",
              color=0xe67e22,
              timestamp=datetime.utcnow()
            )
            embed.add_field(
              name="Moderator:",
              value=f"{ctx.author} ({ctx.author.id})",
              inline=False
            )
            await modlog.send(embed=embed)
    
    @commands.command(aliases=["rename"])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def nick(self, ctx, user: discord.Member = None, *, nickname: str = None):
        data = await self.bot.modlog.get_by_id(ctx.guild.id)
        if not data or "modlog" not in data:
          await ctx.send(
            f"This command requires a modlog to be setup first. Server admins can set one up by typing `{ctx.prefix}modlogset [channel]`."
          )
        else:
            modlogchannel = data["modlog"]
            modlog = await self.bot.fetch_channel(modlogchannel)
            if nickname is None or user is None and len(nickname) >= 2:
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="An error occurred.",
                    description=f"Please follow the format: `{ctx.prefix}setnick {'user'} {'new nickname'}`.\n"
                    f"If you followed the format please make sure that the new nickname is at least two characters long.",
                )
                return await ctx.send(embed=embed)
            await user.edit(nick=nickname, reason=f"Nickname edit by {ctx.message.author.name} ({ctx.message.author.id})")
            await ctx.send(f"Done. Changed {user}'s nickname from {user.display_name} to {nickname}.", delete_after=3)
            embed = discord.Embed(
              title="Nickname change | :lock_with_ink_pen:",
              color=0xe67e22,
              timestamp=datetime.utcnow()
            )
            embed.add_field(
              name="Offender:",
              value=f"{user}\n**Old Nickname:** {user.display_name}\n**New Nickname:** {nickname}",
              inline=False
            )
            embed.add_field(
              name="Moderator:",
              value=f"{ctx.author} ({ctx.author.id})",
              inline=False
            )
            await modlog.send(embed=embed)

    @nick.error
    async def nick_error(self, ctx, error):
        # error handler
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                color=discord.Color.red(),
                title="I am missing a necessary permission.",
                description="Please make sure I have the manage nicknames permission.",
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandError):
            embed = discord.Embed(
                color=discord.Color.red(), title="Something didn't go quite right...", description=" "
            )
            embed.set_author(name=f"{ctx.message.author}", icon_url=f"{ctx.message.author.avatar_url}")
            await ctx.send(embed=embed)
            log.exception(error, exc_info=error)
    
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
def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))
    