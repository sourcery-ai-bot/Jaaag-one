# Imports
import discord
from discord.ext import commands
import asyncio


# Intializing the extension
class Mod(commands.Cog):
    """A cog containing some moderation commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        
    # A command to kick a user from a server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'Done. {user.name} was kicked.', delete_after=3)
    
    # A command to ban a user from a server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'Done. {user.name} was banned.', delete_after=3)

    # A command to ban a user that isn't in the server, can only be used by server moderators and only accepts user id's
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def forceban(self, ctx, user_id: int, *, reason=None):
        await ctx.guild.ban(discord.Object(id=user_id), reason=reason)
        await ctx.send(f'Done. {self.bot.get_user(user_id)} was forcebanned.',
                       delete_after=3)

    # A command to unban a user from a server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """ Unban a user from the guild"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned sucessfully",
                           delete_after=3)
            return

    # A command to mute a user in the server, can only be used by server moderators, the user will be automatically unmuted after the specified mute duration ends
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def mute(self,
                   ctx,
                   member: discord.Member,
                   time: int,
                   d,
                   *,
                   reason=None):
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)

                embed = discord.Embed(
                    title="Mute! :mute:",
                    description=f"{member.mention} has been muted.",
                    colour=discord.Colour.red())
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="Responsible moderator:",
                                value=f"{ctx.author.mention}",
                                inline=False)
                embed.add_field(name="time left till unmute:",
                                value=f"{time}{d}",
                                inline=False)
                await ctx.send(embed=embed, delete_after=3)

                if d == "s":
                    await asyncio.sleep(time)

                if d == "m":
                    await asyncio.sleep(time * 60)

                if d == "h":
                    await asyncio.sleep(time * 60 * 60)

                if d == "d":
                    await asyncio.sleep(time * 60 * 60 * 24)

                await member.remove_roles(role)

                embed = discord.Embed(
                    title="Unmute! :loud_sound:",
                    description=f"{member.mention} has been unmuted.",
                    colour=discord.Colour.red())
                embed.add_field(
                    name=f"Automatic unmute after {time}{d}",
                    value=
                    f"Member in question: {member.mention}\nResponsible moderator: {ctx.author.mention}",
                    inline=False)
                await ctx.send(embed=embed, delete_after=3)

                return

    # A command to unmute a user in the server, can only be used by server moderators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.remove_roles(role)

                embed = discord.Embed(
                    title="Unmute! :loud_sound:",
                    description=f"{member.mention} has been unmuted.",
                    colour=discord.Colour.red())
                embed.add_field(name="Reason:",
                                value=f"{reason}",
                                inline=False)
                embed.add_field(name="Responsible moderator:",
                                value=f"{ctx.author.mention}",
                                inline=False)
                await ctx.send(embed=embed, delete_after=3)
    
    # A command to delete messages in a text channel, can only be used by server administrators
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        if messages > 99:
            messages = 99
        await ctx.channel.purge(limit=messages + 1)
        await ctx.send(f'Done. {messages} messages were purged.',
                       delete_after=3)
    
    # A command to disable the ability of users to send messsages in a text channel, can only be used by server administrators
    @commands.command(aliases=['lockchan'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockit(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"Done. Locked {ctx.channel.mention}")
    
    # The opposite of the above command
    @commands.command(aliases=['ulockchan'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlockit(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"Done. Unlocked {ctx.channel.mention}")

# Adds the extention
def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))