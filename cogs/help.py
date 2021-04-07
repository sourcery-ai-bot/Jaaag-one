# Imports
import discord
from discord.ext import commands
from datetime import datetime


# Intializing the extension
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # base help command containing a list of all available commands. This is also a command group so the subcommands are like: ..help <command_name>
    @commands.group(aliases=["h"])
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:

            em = discord.Embed(color=0x33fcff, timestamp=datetime.utcnow())
            em.set_author(name=f"{self.bot.user.name} Help Menu",
                          icon_url=f"{self.bot.user.avatar_url}")
            em.set_footer(text="Use .. before each command")
            em.add_field(
                name="__**Images/gifs:**__",
                value="`wanted     :` try this command to find out more",
                inline=False)
            em.add_field(
                name="__**Fun:**__",
                value=
                "`meme       :` Sends trending memes from reddit\n`8ball      :` Ask the 8ball a question\n`insult     :` Insult someone\n`hello      :` Say hello to the bot\n`say        :` Repeats your message",
                inline=False)
            em.add_field(
                name="__**Moderation:**__",
                value=
                "`kick       :` Kick a member from the guild\n`ban        :` ban a member from the guild\n`Unban      :` Unban a user from the guild\n`forceban   :` Ban a user that is currently not in the guild\n`mute       :` Mute a member in the guild\n`unmute     :` Unmute a member from the guild\n`purge      :` Delete messages from a channel\n`nick       :` Change a user's nickname",
                inline=False)
            em.add_field(
                name="__**Utility:**__",
                value=
                "`test       :` Test if the bot is responding\n`ping       :` Get the bot's gateway latency\n`help       :` Shows this message\n`invite     :` Gives the bot's invite link\n`stats      :` Get some statistics about the bot\n`whois      :` Get some info about a user\n`avatar     :` See a user's avatar\n`serverinfo :` Get some info about the guild\n`vote       :` Vote for the bot",
                inline=False)
            em.add_field(
                name="__**Admin Utils:**__",
                value=
                "`setprefix  :` Change the server's prefix for the bot\n`resetprefix:` Reset the server prefix for the bot\n`snipe      :` See the last deleted message\n`lockit     :` Lock a channel\n`unlockit   :` Unlock a channel\n`modlogset  :` Set the modlo channel",
                inline=False)
            em.add_field(
                name="__**Useful links:**__",
                value=
                "[Bot invite](https://discord.com/api/oauth2/authorize?client_id=816034868899086386&permissions=8&scope=bot) • [Support server invite](https://discord.gg/DCJwTY8kVP)",
                inline=False)
            await ctx.send(embed=em)
    
    # Help command for the kick command
    @help.command()
    async def kick(self, ctx):
        codea = f"""```xml\n<Syntax : {ctx.prefix}kick <user> [reason] >```"""

        ema = discord.Embed(description=f"{codea}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        ema.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        ema.set_footer(text="Developed by GhOsT#4615")
        ema.add_field(
            name="**Kick a user.**",
            value=
            "Kicks a user. Reason is optional, if given, it will show up\nin the audit log\n\nThis command requires a modlog channel to be setup",
            inline=False)
        ema.add_field(
            name="**Permissions**",
            value="**Bot: `Kick Members`**\n**User: `Kick Members`**",
            inline=False)
        ema.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=ema)

    # Help command for the ban command
    @help.command()
    async def ban(self, ctx):
        codeb = f"""```xml\n<Syntax : {ctx.prefix}ban <user> [reason] >```"""

        emb = discord.Embed(description=f"{codeb}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emb.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emb.set_footer(text="Developed by GhOsT#4615")
        emb.add_field(
            name="**Ban a user.**",
            value=
            "Bans a user. Reason is optional, if given, it will show up\nin the audit log\n\nThis command requires a modlog channel to be setup",
            inline=False)
        emb.add_field(name="**Permissions**",
                      value="**Bot: `Ban Members`**\n**User: `Ban Members`**",
                      inline=False)
        emb.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emb)

    # Help command for the forceban command
    @help.command()
    async def forceban(self, ctx):
        codec = f"""```xml\n<Syntax : {ctx.prefix}forceban <user_id> [reason] >```"""

        emc = discord.Embed(description=f"{codec}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emc.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emc.set_footer(text="Developed by GhOsT#4615")
        emc.add_field(
            name="**Ban a user.**",
            value="Bans a user not in the server. Only accepts user ID's.\n\nThis command requires a modlog channel to be setup",
            inline=False)
        emc.add_field(name="**Permissions**",
                      value="**Bot: `Ban Members`**\n**User: `Ban Members`**",
                      inline=False)
        emc.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emc)

    # Help command for the mute command
    @help.command()
    async def mute(self, ctx):
        coded = f"""```xml\n<Syntax : {ctx.prefix}mute <user> <time> [reason] >```"""

        emd = discord.Embed(description=f"{coded}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emd.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emd.set_footer(text="Developed by GhOsT#4615")
        emd.add_field(
            name="**Mute a user.**",
            value=
            "Mutes a user. The user will automatically be unmuted\nafter the specified time.\n\nThis command requires a modlog channel to be setup",
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

    # Help command for the unban command
    @help.command()
    async def unban(self, ctx):
        codee = f"""```xml\n<Syntax : {ctx.prefix}unban <user> [reason] >```"""

        eme = discord.Embed(description=f"{codee}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        eme.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        eme.set_footer(text="Developed by GhOsT#4615")
        eme.add_field(
            name="**Unban a user.**",
            value=
            "Unbans a user from the guild. Reason is optional,\nif given, it will show up in the audit log\n\nThis command requires a modlog channel to be setup",
            inline=False)
        eme.add_field(name="**Permissions**",
                      value="**Bot: `Ban Members`**\n**User: `Ban Members`**",
                      inline=False)
        eme.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=eme)

    # Help command for the unmute command
    @help.command()
    async def unmute(self, ctx):
        codef = f"""```xml\n<Syntax : {ctx.prefix}unmute <user> [reason] >```"""

        emf = discord.Embed(description=f"{codef}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emf.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emf.set_footer(text="Developed by GhOsT#4615")
        emf.add_field(
            name="**Unmute a user.**",
            value=
            "Unmutes a user.  Reason is optional, if given, it will show up\nin the audit log\n\nThis command requires a modlog channel to be setup",
            inline=False)
        emf.add_field(
            name="**Permissions**",
            value="**Bot: `Kick Members`**\n**User: `Kick Members`**",
            inline=False)
        emf.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emf)

    # Help command for the purge command
    @help.command()
    async def purge(self, ctx):
        codeg = f"""```xml\n<Syntax : {ctx.prefix}purge <messages> >\nAlias: {ctx.prefix}cleanup```"""

        emg = discord.Embed(description=f"{codeg}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emg.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emg.set_footer(text="Developed by GhOsT#4615")
        emg.add_field(
            name="**Clear messages.**",
            value="Deletes up a specified amount of messages in\na channel\n\nThis command requires a modlog\nchannel to be setup",
            inline=False)
        emg.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Messages`**\n**User: `Manage Messages`**",
            inline=False)
        emg.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 8 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emg)

    # Help command for the channel-lock command
    @help.command(aliases=["lockchan"])
    async def lockit(self, ctx):
        codeh = f"""```xml\n<Syntax : {ctx.prefix}lockit [channel] >\nAlias: {ctx.prefix}lockchan```"""

        emh = discord.Embed(description=f"{codeh}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emh.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emh.set_footer(text="Developed by GhOsT#4615")
        emh.add_field(
            name="**Lock selected text/voice channel.**",
            value=
            "Disables the ability of users to send messages\nin a text channel or join a voice channel.",
            inline=False)
        emh.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Channels`**\n**User: `Manage Messages`**",
            inline=False)
        emh.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emh)

    # Help command for the channel-unlock command
    @help.command(aliases=["ulockchan"])
    async def unlockit(self, ctx):
        codei = f"""```xml\n<Syntax : {ctx.prefix}unlockit [channel] >\nAlias: {ctx.prefix}ulockchan```"""

        emi = discord.Embed(description=f"{codei}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emi.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emi.set_footer(text="Developed by GhOsT#4615")
        emi.add_field(
            name="**Unlock selected text/voice channel.**",
            value=
            "Enables the ability of users to send messages\nin a  text channel or join a voice channel again.",
            inline=False)
        emi.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Channels`**\n**User: `Manage Messages`**",
            inline=False)
        emi.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emi)

    @help.command(aliases=["rename"])
    async def nick(self, ctx):
        codej = f"""```xml\n<Syntax : {ctx.prefix}nick <user> [nickname] >\nAlias: {ctx.prefix}rename```"""

        emj = discord.Embed(description=f"{codej}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emj.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emj.set_footer(text="Developed by GhOsT#4615")
        emj.add_field(
            name="**Change a user's nickname.**",
            value=
            "Changes the specified user's nickname. Does what\nit's supposed to do. What more could you want?\n\nThis command requires a modlog channel to be setup",
            inline=False)
        emj.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Nicknames`**\n**User: `Manage Nicknames`**",
            inline=False)
        emj.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 3 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emj)

    @help.command(aliases=["mls"])
    async def modlogset(self, ctx):
        codek = f"""```xml\n<Syntax : {ctx.prefix}modlogset [channel] >\nAlias: {ctx.prefix}mls```"""

        emk = discord.Embed(description=f"{codek}",
                            color=0x33fcff,
                            timestamp=datetime.utcnow())
        emk.set_author(name=f"{self.bot.user.name} Help Menu",
                       icon_url=f'{self.bot.user.avatar_url}')
        emk.set_footer(text="Developed by GhOsT#4615")
        emk.add_field(
            name="**Set a Modlog channel.**",
            value=
            "Sets a channel for modlog events to be posted to.",
            inline=False)
        emk.add_field(
            name="**Permissions**",
            value="**Bot: `Manage Server`**\n**User: `Manage Server`**",
            inline=False)
        emk.add_field(name="**Cooldown:**",
                      value="Can be used 1 time per 5 seconds, per user.",
                      inline=False)
        await ctx.send(embed=emk)


#The help subcommands are limited to the moderation commands for now. There are a lot of other commands in the bot, but I was too lazy to make a help command for them. Maybe I'll do it later...


# Adds the extention
def setup(bot):
    bot.add_cog(Help(bot))
