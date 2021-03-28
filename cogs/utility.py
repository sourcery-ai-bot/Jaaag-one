import discord
from discord.ext import commands
import platform
import json
from datetime import datetime


class utility(commands.Cog):
    """A cog containing some utility commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    @commands.command(aliases=['inv'])
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Jaaag bot invite',
            description='This is our permenent invite for the bot.',
            color=discord.Color.red(),
            timestamp=datetime.utcnow())

        embed.set_footer(text='Hosted by GhOsT#4615')
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/attachments/696099948072009788/697707125136293938/ezgif.com-gif-maker-19.gif'
        )
        embed.set_author(
            name='Jaaag Help Menu',
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        embed.add_field(
            name="link:",
            value="Invite the bot using [this link](https://cutt.ly/zzh5AGh)",
            inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def serverinfo(self, ctx):
        server = ctx.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(title="**Server Name:**",
                              description=f"{server}",
                              color=discord.Color.red(),
                              timestamp=datetime.utcnow())
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Owner", value=f"{server.owner}", inline=False)
        embed.add_field(name="Server ID", value=server.id, inline=False)
        embed.add_field(name="Member Count",
                        value=server.member_count,
                        inline=False)
        embed.add_field(name="Text/Voice Channels",
                        value=f"{channels}",
                        inline=False)
        embed.add_field(name=f"Roles ({role_length})",
                        value=roles,
                        inline=False)
        embed.set_footer(text=f"Created at: {time}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, ctx):
        pythonv = platform.python_version()
        dpy = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        embed = discord.Embed(title="Jaaag Help Menu",
                              description="**Bot stats**",
                              color=discord.Color.blue(),
                              timestamp=datetime.utcnow())
        embed.add_field(name="**Server count:**",
                        value=f"`{serverCount}` guilds",
                        inline=False)
        embed.add_field(name="**Member count:**",
                        value=f"`{memberCount}` users",
                        inline=False)
        embed.add_field(name="**Python version:**",
                        value=f"`{pythonv}`",
                        inline=False)
        embed.add_field(name="**Discord.py version:**",
                        value=f"`{dpy}`",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):

        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)

        await ctx.send(f"The prefix has been changed to `{prefix}`")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.last_msg = message

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
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

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author
            roles = [role for role in ctx.author.roles]

        else:
            roles = [role for role in member.roles]

        embed = discord.Embed(title=f"{member}",
                              colour=0x33fcff,
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by: {ctx.author}",
                         icon_url=ctx.author.avatar_url)
        embed.set_author(name="User Info: ")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Server Nickname:",
                        value=member.display_name,
                        inline=False)
        embed.add_field(name="Discriminator:",
                        value=member.discriminator,
                        inline=False)
        embed.add_field(name="Current Status:",
                        value=str(member.status).title(),
                        inline=False)
        embed.add_field(
            name="Current Activity:",
            value=
            f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}"
            if member.activity is not None else "None",
            inline=False)
        embed.add_field(
            name="Created At:",
            value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"),
            inline=False)
        embed.add_field(
            name="Joined At:",
            value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"),
            inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]",
                        value=" **|** ".join([role.mention for role in roles]),
                        inline=False)
        embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        await ctx.send(embed=embed)
        return

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member):
        embed = discord.Embed(title=f"{member}'s Avatar!",
                               colour=0x33fcff,
                               timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar_url)      
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        message = await ctx.send("Testing Ping...")

        await message.edit(
            content=
            f"Pong! :ping_pong:\nShard id 0: `{round(self.bot.latency * 1000)}`ms"
        )

    @commands.command(name="test")
    @commands.guild_only()
    async def test(self, ctx: commands.Context):
        await ctx.reply(f"Hey {ctx.author.mention}!")

def setup(bot: commands.Bot):
    bot.add_cog(utility(bot))