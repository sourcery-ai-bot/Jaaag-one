import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from os import getenv
from Keeping_alive import keep_alive
import json
from utils.util import get_prefix

load_dotenv()

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=get_prefix,
                   intents=discord.Intents.all(),
                   help_command=None)

cogs = ["cogs.mod", "cogs.fun", "cogs.utility", "cogs.help", "cogs.errors"]

for cog in cogs:
    bot.load_extension(cog)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('..help'))


@bot.event
async def on_guild_join(guild):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ".."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

@bot.group()
@commands.is_owner()
async def sudo(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(
            "Use `..sudo <command>` to perform your bot admin actions.")


@sudo.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Sucessfully loaded the `{extension}` Cog.")


@sudo.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(
        f"Successfully unloaded the `{extension}` Cog.\nLol why are u making me more useless?"
    )


@sudo.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Done. Reloaded The `{extension}` Cog.")


@sudo.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("logging out... bye!")
    await ctx.bot.logout()


keep_alive()
bot.run(getenv("TOKEN"))
