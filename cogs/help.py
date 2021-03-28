import discord
from discord.ext import commands
from datetime import datetime


class Help(commands.Cog):
    """A cog containing help commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(aliases=["h"])
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:

            em = discord.Embed(color=0x33fcff, timestamp=datetime.utcnow())
            em.set_author(
                name="Jaaag Help Menu",
                icon_url=
                "https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024"
            )
            em.set_footer(text="Use .. before each command")
            em.add_field(
                name="__**Image commands:**__",
                value=
                "`kekw       :` Send a quick kekw gif\n`omgwow     :` Send a quick omg gif\n`oof        :` Send a quick oof gif\n`bonk       :` Send a quick bonk gif\n`wanted     :` try this command to find out more",
                inline=False)
            em.add_field(
                name="__**Fun:**__",
                value=
                "`meme       :` Sends trending memes from reddit\n`8ball      :` Ask the 8ball a question\n`hello      :` Say hello to the bot\n`say        :` Repeats your message\n`rickroll   :` Gives you a rickroll link",
                inline=False)
            em.add_field(
                name="__**Moderation:**__",
                value=
                "`kick       :` Kick a member from the guild\n`ban        :` ban a member from the guild\n`Unban      :` Unban a user from the guild\n`forceban   :` Ban a user that is currently not in the guild\n`mute       :` Mute a member in the guild\n`unmute     :` Unmute a member from the guild\n`purge      :` Delete messages from a channel",
                inline=False)
            em.add_field(
                name="__**Utility:**__",
                value=
                "`test       :` Test if the bot is responding\n`ping       :` Get the bot's gateway latency\n`help       :` Shows this message\n`invite     :` Gives the bot's invite link\n`stats      :` Get some statistics about the bot\n`whois      :` Get some info about a user\n`avatar     :` See a user's avatar\n`uptime     :` See the bot's uptime",
                inline=False)
            em.add_field(
                name="__**Admin Utils:**__",
                value=
                "`setprefix  :` Change the server's prefix for the bot\n`serverinfo :` Get some info about the guild\n`snipe      :` See the last deleted message\n`lockit     :` Lock a channel\n`unlockit   :` Unlock a channel",
                inline=False)
            await ctx.send(embed=em)

    @help.command()
    async def kick(self, ctx):
        codea = """```xml\n<Syntax : ..kick <user> [reason] >```"""

        ema = discord.Embed(description=f"{codea}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        ema.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        ema.set_footer(text="Hosted by GhOsT#4615")
        ema.add_field(
            name="**Kick a user.**",
            value=
            "Kicks a user. Reason is optional, if given, it will show up\nin the audit log",
            inline=False)
        ema.add_field(
            name="**Permissions**",
            value="**Bot: `Kick Members`**\n**User: `Kick Members`**",
            inline=False)
        ema.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=ema)

    @help.command()
    async def ban(self, ctx):
        codeb = """```xml\n<Syntax : ..ban <user> [reason] >```"""

        emb = discord.Embed(description=f"{codeb}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emb.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emb.set_footer(text="Hosted by GhOsT#4615")
        emb.add_field(
            name="**Ban a user.**",
            value=
            "Bans a user. Reason is optional, if given, it will show up\nin the audit log",
            inline=False)
        emb.add_field(name="**Permissions**",
                      value="**Bot: `Ban Members`**\n**User: `Ban Members`**",
                      inline=False)
        emb.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emb)

    @help.command()
    async def forceban(self, ctx):
        codec = """```xml\n<Syntax : ..forceban <user_id> [reason] >```"""

        emc = discord.Embed(description=f"{codec}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emc.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emc.set_footer(text="Hosted by GhOsT#4615")
        emc.add_field(
            name="**Ban a user.**",
            value="Bans a user not in the server. Only accepts user ID's.",
            inline=False)
        emc.add_field(name="**Permissions**",
                      value="**Bot: `Ban Members`**\n**User: `Ban Members`**",
                      inline=False)
        emc.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emc)

    @help.command()
    async def mute(self, ctx):
        coded = """```xml\n<Syntax : ..mute <user> <time> <d> [reason] >```"""

        emd = discord.Embed(description=f"{coded}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emd.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emd.set_footer(text="Hosted by GhOsT#4615")
        emd.add_field(
            name="**Mute a user.**",
            value=
            "Mutes a user. The user will automatically be unmuted\nafter the specified time.",
            inline=False)
        emd.add_field(
            name="**Reference:**",
            value="`s :` seconds\n`m :` minutes\n`h :` hours\n`d :` days",
            inline=False)
        emd.add_field(
            name="**Permissions**",
            value="**Bot: `Kick Members`**\n**User: `Kick Members`**",
            inline=False)
        emd.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emd)

    @help.command()
    async def unban(self, ctx):
        codee = """```xml\n<Syntax : ..unban <user> [reason] >```"""

        eme = discord.Embed(description=f"{codee}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        eme.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        eme.set_footer(text="Hosted by GhOsT#4615")
        eme.add_field(
            name="**Unban a user.**",
            value=
            "Unbans a user from the guild. Reason is optional,\nif given, it will show up in the audit log",
            inline=False)
        eme.add_field(name="**Permissions**",
                      value="**Bot: `Ban Members`**\n**User: `Ban Members`**",
                      inline=False)
        eme.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=eme)

    @help.command()
    async def unmute(self, ctx):
        codef = """```xml\n<Syntax : ..unmute <user> [reason] >```"""

        emf = discord.Embed(description=f"{codef}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emf.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emf.set_footer(text="Hosted by GhOsT#4615")
        emf.add_field(
            name="**Unmute a user.**",
            value=
            "Unmutes a user.  Reason is optional, if given, it will show up\nin the audit log",
            inline=False)
        emf.add_field(
            name="**Permissions**",
            value="**Bot: `Kick Members`**\n**User: `Kick Members`**",
            inline=False)
        emf.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emf)

    @help.command()
    async def purge(self, ctx):
        codeg = """```xml\n<Syntax : ..purge <messages> >```"""

        emg = discord.Embed(description=f"{codeg}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emg.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emg.set_footer(text="Hosted by GhOsT#4615")
        emg.add_field(
            name="**Clear messages.**",
            value="Deletes up a specified amount of messages in\na channel",
            inline=False)
        emg.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Messages`**\n**User: `Manage Messages`**",
            inline=False)
        emg.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emg)

    @help.command(aliases=["lockchan"])
    async def lockit(self, ctx):
        codeh = """```xml\n<Syntax : ..lockit [channel] >\nAliases: lockchan```"""

        emh = discord.Embed(description=f"{codeh}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emh.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emh.set_footer(text="Hosted by GhOsT#4615")
        emh.add_field(
            name="**Lock a channel.**",
            value=
            "Disables the ability of users to send messages\nin a channel",
            inline=False)
        emh.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Channels`**\n**User: `Administrator`**",
            inline=False)
        emh.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emh)

    @help.command(aliases=["ulockchan"])
    async def unlockit(self, ctx):
        codei = """```xml\n<Syntax : ..unlockit [channel] >\nAliases: ulockchan```"""

        emi = discord.Embed(description=f"{codei}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emi.set_author(
            name="Jaaag Help menu",
            icon_url=
            'https://cdn.discordapp.com/avatars/816034868899086386/2333c167cf7af29613894e6e0073ec38.png?size=1024'
        )
        emi.set_footer(text="Hosted by GhOsT#4615")
        emi.add_field(
            name="**Unlock a channel.**",
            value="Enables the ability of users to send messages\nin a channel",
            inline=False)
        emi.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Channels`**\n**User: `Administrator`**",
            inline=False)
        emi.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emi)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
