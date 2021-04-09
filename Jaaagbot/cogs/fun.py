# Imports
import discord
from discord.ext import commands
import random
import aiohttp
from Jaaagbot.utils.stuff import roast, jaaagroast
from PIL import Image
from io import BytesIO
from datetime import datetime


# Intializing the extension
class Fun(commands.Cog):
    """A cog containing fun commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Prints on the console when the extension is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # A fun 8ball command
    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidely so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Dont count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."
        ]
        await ctx.reply(f':8ball: {random.choice(responses)}',
                        mention_author=True)

    # A fun command that sends trending memes from a subreddit as an embed
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        embed = discord.Embed(title="Memes",
                              description="Here, take some memes")

        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/dankmemes/new.json?sort=hot'
            ) as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(
                    0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    # This command repeats the author's message
    @commands.command(aliases=["echo"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

    # A simple command that replies back to the user
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.reply(f'sup {ctx.author.mention}!')

    # This is my favourite command so far, It takes a template named 'wanted.jpg' and it taked the avatar of the user who ran the command or of a user who is mentioned and pastes it in the middle, creating a wanted poster.
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("wanted.jpg")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((251, 251))

        wanted.paste(pfp, (101, 204))

        wanted.save("profile.jpg")

        await ctx.send(file=discord.File("profile.jpg"))

    # A command throws an roast at the user that the author mentions, if the user is none, then the author gets roasted and if the author tries the bot to get to insult itself, the bot will really badly roast the author.
    @commands.command(aliases=["insult"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roast(self, ctx, *, member: discord.Member = None):

        if member == self.bot.user:
            await ctx.send(f"{ctx.author.mention} {random.choice(jaaagroast)}")

        elif member is None:
            await ctx.send(f"{ctx.author.mention} {random.choice(roast)}")

        else:
            await ctx.send(f'{member.mention} {random.choice(roast)}')

    # A modified version of a slot machine command that can be found here: https://github.com/AlexFlipnote/discord_bot.py
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slots(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"```xml\n>{a} {b} {c}<```"

        if (a == b == c):
            ema = discord.Embed(
                title=f"{ctx.author.name}'s slot machine",
                description=f"{slotmachine}\nAll matching, you won!",
                color=discord.Color.green(),
                timestamp=datetime.utcnow())
            ema.set_footer(text="Good job!")
            await ctx.send(embed=ema)

        elif (a == b) or (a == c) or (b == c):
            emb = discord.Embed(
                title=f"{ctx.author.name}'s slot machine",
                description=f"{slotmachine}\n2 in a row, you won!",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow())
            emb.set_footer(text="Close")
            await ctx.send(embed=emb)

        else:
            emc = discord.Embed(
                title=f"{ctx.author.name}'s slot machine",
                description=f"{slotmachine}\nNo match, you lost.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow())
            emc.set_footer(text="Sucks to suck")
            await ctx.send(embed=emc)

    # A modified version of a hotrate command that can be found here: https://github.com/AlexFlipnote/discord_bot.py
    @commands.command(aliases=["hotrate"])
    async def howhot(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author

        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"

        elif hot > 50:
            emoji = "💖"

        elif hot > 75:
            emoji = "💞"

        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")


# Adds the extention
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
