import discord
from discord.ext import commands
import random
import aiohttp
from PIL import Image
from io import BytesIO


class Fun(commands.Cog):
    """A cog containing fun commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        """ Ask the 8ball a question and it shall reply"""
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

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rickroll(self, ctx):
        await ctx.send('Here, get ricked... https://youtu.be/dQw4w9WgXcQ')

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

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.send(f'sup {ctx.author.mention}')

    @commands.command()
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
    
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kekw(self, ctx):
        await ctx.send('https://tenor.com/view/kekgiggle-kekw-gif-20353601')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def omgwow(self, ctx):
        await ctx.send('https://tenor.com/view/omg-oh-my-god-wow-gif-11411674')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def oof(self, ctx):
        await ctx.send(
            'https://tenor.com/view/whoo-wtf-supa-hot-fire-rap-battle-im-not-arapper-gif-16789777'
        )

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bonk(self, ctx):
        await ctx.send(
            'https://tenor.com/view/walter-bonk-walter-bonk-nelson-dog-gif-15721111def'
        )

def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))