# Imports
import discord
from discord.ext import commands
from datetime import datetime


# Intializing the extension
class utility(commands.Cog):
    """A cog containing some utility commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # A command to get the invite link for the bot
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(
            description="[Invite link](https://discord.com/api/oauth2/authorize?client_id=816034868899086386&permissions=8&scope=bot)",
            color=0x33fcff,
            timestamp=datetime.utcnow())
        embed.set_footer(text='Developed by GhOsT#4615')
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/696099948072009788/697707125136293938/ezgif.com-gif-maker-19.gif"
        )
        embed.set_author(
            name="Invite Jaaag Bot!",
            icon_url=
            f"{self.bot.user.avatar_url}"
        )
        await ctx.send(embed=embed)

    # A command to view dome information about the server
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
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

    # A simple command for getting information about a user
    @commands.command()
    @commands.guild_only()
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
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=ctx.author.avatar_url)
        embed.set_author(name="User Info: ")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Server Nickname:",
                        value=member.display_name,
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
            value=member.created_at.strftime("%a, %d %B %Y, %I:%M, %p UTC"),
            inline=False)
        embed.add_field(
            name="Joined At:",
            value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"),
            inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]",
                        value=" **,** ".join([role.mention for role in roles]),
                        inline=False)
        embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        await ctx.send(embed=embed)
        return

    # A simple command to get the profile picture of a user
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member):
        embed = discord.Embed(title=f"{member}'s Avatar!",
                              colour=0x33fcff,
                              timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    # A command to get the bot's websocket latency
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        message = await ctx.send("Testing Ping...")

        await message.edit(
            content=f"Pong! :ping_pong:\n`{round(self.bot.latency * 1000)}`ms")

    # A command to 'test' if the bot is responding
    @commands.command(name="test")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def test(self, ctx: commands.Context):
        await ctx.send("I am alive!")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def source(self, ctx):
        embed = discord.Embed(colour=0x33fcff,
                              timestamp=ctx.message.created_at)
        embed.set_author(name=f"{self.bot.user.name} Help Menu",
                         icon_url=f"{self.bot.user.avatar_url}")
        embed.set_thumbnail(
            url=
            'https://user-images.githubusercontent.com/41782385/59523230-55488280-8f03-11e9-9abe-e8e0f3d9a245.gif'
        )
        embed.add_field(
            name="Source Code",
            value=
            "[Click here](https://github.com/Arman0334/Jaaag-one) to view my source code!\n\nDeveloped and hosted by GhosT#4615",
            inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vote(self, ctx):
        embed = discord.Embed(color=0x33fcff, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="Doitdoitdoitdoit!")
        embed.add_field(
            name="Vote for us!",
            value=
            "Bot list links:\n[Top.gg](https://top.gg/bot/816034868899086386/vote)",
            inline=False)
        await ctx.send(embed=embed)
    

# Adds the extention
def setup(bot: commands.Bot):
    bot.add_cog(utility(bot))
